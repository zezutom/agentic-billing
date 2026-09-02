"""Batch experiment: pre-check the candidate pool, draw a seeded random sample,
harvest all ten, then verify and render whatever the analyst returns.

The analysis itself is a separate step because the analyst is a Claude session,
not a subprocess. `harvest` writes ten dossiers and ten request files; the
session answers each one; `finish` verifies every quote and renders the reports.
Running with `--backend api` collapses the two into one command.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

from ..analyze import AnalysisPending, analyse, analysis_path
from ..discover import discover
from ..fetcher import Fetcher
from ..harvest import Dossier, harvest
from ..render import write_all
from .pool import (
    CANDIDATE_POOL, EXCLUDED_LARGE_PLATFORMS, RANDOM_SEED, SAMPLE_SIZE, pool_as_dicts,
)

DOC_CATEGORIES = {"docs", "help", "faq", "limits", "billing_docs", "compare", "terms"}
HARVEST_SETTINGS = {"max_pages": 16}


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


# ------------------------------------------------------------------- eligibility

def precheck(outdir: Path, delay: float = 1.0, allow_render: bool = True) -> dict:
    """Apply the inclusion criteria to every candidate, before any selection."""
    fetcher = Fetcher(cache_dir=".promise_audit_cache", delay=delay, allow_render=allow_render)
    records = []
    try:
        for i, cand in enumerate(CANDIDATE_POOL, 1):
            print(f"[{i:2}/{len(CANDIDATE_POOL)}] pre-checking {cand.name} ...", flush=True)
            rec = cand.to_dict()
            excluded = next((n for n in EXCLUDED_LARGE_PLATFORMS if n in cand.url.lower()), None)
            if excluded:
                rec.update(eligible=False, reason=f"excluded as a large platform ('{excluded}')")
                records.append(rec)
                continue
            try:
                d = discover(fetcher, cand.url, max_pages=16)
                cats = {c.category for c in d.selected}
                has_pricing, has_docs = bool(d.pricing_urls), bool(cats & DOC_CATEGORIES)
                rec.update(pricing_urls=d.pricing_urls, categories_found=sorted(cats),
                           pages_discovered=len(d.selected),
                           eligible=bool(has_pricing and has_docs))
                if not has_pricing:
                    rec["reason"] = "no public pricing page could be discovered"
                elif not has_docs:
                    rec["reason"] = "no public documentation, help or FAQ content could be discovered"
                else:
                    rec["reason"] = (f"pricing page found ({d.pricing_urls[0]}) and "
                                     f"{len(cats & DOC_CATEGORIES)} supporting content types discovered")
            except Exception as exc:
                rec.update(eligible=False, reason=f"pre-check failed: {type(exc).__name__}: {exc}"[:180])
            records.append(rec)
    finally:
        fetcher.close()

    out = {
        "checked_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "pool_size": len(CANDIDATE_POOL),
        "eligible": sum(1 for r in records if r.get("eligible")),
        "criteria": [
            "not on the excluded large-platform list",
            "homepage reachable over HTTPS and allowed by robots.txt",
            "a public pricing page can be discovered automatically",
            "public documentation, help, FAQ, comparison or terms content can be discovered",
        ],
        "candidates": records,
    }
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "eligibility.json").write_text(json.dumps(out, indent=2))
    return out


def select(eligibility: dict, seed: int = RANDOM_SEED, n: int = SAMPLE_SIZE) -> list[dict]:
    """Seeded random draw over the eligible candidates, sorted by URL first so
    the result does not depend on the order the pre-check finished in."""
    eligible = sorted([c for c in eligibility["candidates"] if c.get("eligible")],
                      key=lambda c: c["url"])
    rng = random.Random(seed)
    chosen = eligible if len(eligible) <= n else rng.sample(eligible, n)
    return sorted(chosen, key=lambda c: c["name"].lower())


# ---------------------------------------------------------------------- phases

def cmd_harvest(args) -> int:
    outdir, workdir = Path(args.out), Path(args.work)
    elig_path = outdir / "eligibility.json"
    if args.skip_precheck and elig_path.exists():
        eligibility = json.loads(elig_path.read_text())
        print(f"Reusing pre-check: {eligibility['eligible']}/{eligibility['pool_size']} eligible")
    else:
        print(f"Pre-checking {len(CANDIDATE_POOL)} candidates ...")
        eligibility = precheck(outdir, delay=args.delay, allow_render=not args.no_render)
        print(f"  {eligibility['eligible']}/{eligibility['pool_size']} eligible")

    selected = select(eligibility)
    print(f"\nSeeded random sample (seed={RANDOM_SEED}): "
          f"{', '.join(c['name'] for c in selected)}\n")

    workdir.mkdir(parents=True, exist_ok=True)
    entries = []
    for i, cand in enumerate(selected, 1):
        slug = slugify(cand["name"])
        print(f"[{i}/{len(selected)}] harvesting {cand['name']} ({cand['url']})", flush=True)
        fetcher = Fetcher(cache_dir=".promise_audit_cache", delay=args.delay,
                          allow_render=not args.no_render)
        try:
            dossier = harvest(cand["url"], company=cand["name"], fetcher=fetcher,
                              verbose=False, **HARVEST_SETTINGS)
        except Exception as exc:
            print(f"    harvest failed: {exc}")
            entries.append({"candidate": cand, "slug": slug,
                            "error": f"{type(exc).__name__}: {exc}"[:200]})
            continue
        finally:
            fetcher.close()
        dossier.save(workdir / f"{slug}.dossier.json")
        from ..analyze import write_request
        write_request(dossier, workdir, slug)
        print(f"    {dossier.stats['pages_usable']}/{dossier.stats['pages_fetched_ok']} usable "
              f"pages, {dossier.stats['dossier_chars']:,} chars", flush=True)
        entries.append({"candidate": cand, "slug": slug,
                        "dossier_file": str(workdir / f"{slug}.dossier.json"),
                        "request_file": str(workdir / f"{slug}.request.md"),
                        "harvest_stats": dossier.stats})

    state = {
        "harvested_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "random_seed": RANDOM_SEED, "sample_size": SAMPLE_SIZE,
        "harvest_settings": HARVEST_SETTINGS,
        "pool": pool_as_dicts(), "eligibility": eligibility,
        "selected": selected, "entries": entries,
    }
    (outdir / "harvest_state.json").write_text(json.dumps(state, indent=2))
    print(f"\nWrote {outdir / 'harvest_state.json'}")
    print(f"\nNext: answer each request in {workdir}/<slug>.request.md by writing")
    print(f"      {workdir}/<slug>.analysis.json, then run:")
    print(f"      python -m promise_audit.experiment.run_batch finish --out {outdir} --work {workdir}")
    return 0


def cmd_finish(args) -> int:
    outdir, workdir = Path(args.out), Path(args.work)
    state = json.loads((outdir / "harvest_state.json").read_text())
    runs = []
    for entry in state["entries"]:
        slug, cand = entry["slug"], entry["candidate"]
        if "dossier_file" not in entry:
            runs.append({**entry, "status": "harvest_failed"})
            continue
        dossier = Dossier.load(entry["dossier_file"])
        try:
            analysis, report = analyse(dossier, backend=args.backend, workdir=workdir,
                                       slug=slug, model=args.model)
        except AnalysisPending:
            print(f"  {cand['name']:20} no analysis yet ({analysis_path(workdir, slug)})")
            runs.append({**entry, "status": "awaiting_analysis"})
            continue
        except Exception as exc:
            print(f"  {cand['name']:20} analysis failed: {exc}")
            runs.append({**entry, "status": "analysis_failed",
                         "error": f"{type(exc).__name__}: {exc}"[:200]})
            continue
        paths = write_all(analysis, dossier, outdir, slug)
        sev = {}
        for f in analysis["findings"]:
            sev[f["severity"]] = sev.get(f["severity"], 0) + 1
        v = analysis["verification"]
        print(f"  {cand['name']:20} {len(analysis['findings'])} findings {sev or ''} "
              f"({v['findings_rejected']} rejected, {v['quotes_checked']} quotes checked)")
        runs.append({**entry, "status": "ok", "result_file": str(paths["json"]),
                     "report_file": str(paths["html"]),
                     "summary": {"findings": len(analysis["findings"]),
                                 "by_severity": sev,
                                 "by_confidence": _count(analysis["findings"], "confidence"),
                                 "by_type": _count(analysis["findings"], "type"),
                                 "promises": len(analysis.get("promises", [])),
                                 "plans": len(analysis.get("plans", [])),
                                 "verification": v}})
    manifest = {**state, "finished_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                "backend": args.backend, "runs": runs}
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {outdir / 'manifest.json'}")
    return 0


def _count(items: list[dict], key: str) -> dict:
    out: dict[str, int] = {}
    for i in items:
        out[i.get(key, "?")] = out.get(i.get(key, "?"), 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="promise-audit-batch")
    sub = ap.add_subparsers(dest="cmd", required=True)

    h = sub.add_parser("harvest", help="pre-check, select and harvest the ten companies")
    h.add_argument("--out", default="results/experiment")
    h.add_argument("--work", default="work")
    h.add_argument("--delay", type=float, default=1.0)
    h.add_argument("--no-render", action="store_true")
    h.add_argument("--skip-precheck", action="store_true")
    h.set_defaults(func=cmd_harvest)

    f = sub.add_parser("finish", help="verify and render the analyses")
    f.add_argument("--out", default="results/experiment")
    f.add_argument("--work", default="work")
    f.add_argument("--backend", choices=("agent", "api"), default="agent")
    f.add_argument("--model", default="claude-opus-5")
    f.set_defaults(func=cmd_finish)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
