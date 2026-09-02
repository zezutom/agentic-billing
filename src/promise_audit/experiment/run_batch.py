"""Batch experiment: pre-check the candidate pool, draw a seeded random sample
of ten companies, and run the identical analysis pipeline against all of them.

The prompts, rules and thresholds are the same for every company. Nothing in
this script branches on which company is being analysed.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

from ..audit import audit_site
from ..discover import discover
from ..fetcher import Fetcher
from ..report import write_all
from .pool import CANDIDATE_POOL, EXCLUDED_LARGE_PLATFORMS, RANDOM_SEED, SAMPLE_SIZE, pool_as_dicts

DOC_CATEGORIES = {"docs", "help", "faq", "limits", "billing_docs", "compare", "terms"}
AUDIT_SETTINGS = {"max_pages": 16, "max_findings": 12}


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def precheck(outdir: Path, delay: float = 1.0) -> dict:
    """Apply the inclusion criteria to every candidate, before any selection."""
    fetcher = Fetcher(cache_dir=".promise_audit_cache", delay=delay)
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
                has_pricing = bool(d.pricing_urls)
                has_docs = bool(cats & DOC_CATEGORIES)
                rec.update(
                    pricing_urls=d.pricing_urls,
                    categories_found=sorted(cats),
                    pages_discovered=len(d.selected),
                    eligible=bool(has_pricing and has_docs),
                )
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
    """Seeded random draw. Sorting by URL first makes the draw reproducible
    regardless of the order the pre-check happened to finish in."""
    eligible = sorted([c for c in eligibility["candidates"] if c.get("eligible")],
                      key=lambda c: c["url"])
    rng = random.Random(seed)
    if len(eligible) <= n:
        return eligible
    return sorted(rng.sample(eligible, n), key=lambda c: c["name"].lower())


def run_batch(outdir: str | Path = "results/experiment", delay: float = 1.0,
              skip_precheck: bool = False) -> dict:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    elig_path = outdir / "eligibility.json"
    if skip_precheck and elig_path.exists():
        eligibility = json.loads(elig_path.read_text())
        print(f"Reusing pre-check: {eligibility['eligible']}/{eligibility['pool_size']} eligible")
    else:
        print(f"Pre-checking {len(CANDIDATE_POOL)} candidates against the inclusion criteria...")
        eligibility = precheck(outdir, delay=delay)
        print(f"  {eligibility['eligible']}/{eligibility['pool_size']} candidates eligible")

    selected = select(eligibility)
    print(f"\nSeeded random sample (seed={RANDOM_SEED}): "
          f"{', '.join(c['name'] for c in selected)}\n")

    runs = []
    for i, cand in enumerate(selected, 1):
        print(f"[{i}/{len(selected)}] auditing {cand['name']} ({cand['url']})", flush=True)
        fetcher = Fetcher(cache_dir=".promise_audit_cache", delay=delay)
        try:
            result = audit_site(cand["url"], company=cand["name"], fetcher=fetcher,
                                verbose=False, **AUDIT_SETTINGS)
        except Exception as exc:
            print(f"    run failed: {exc}")
            runs.append({"candidate": cand, "error": f"{type(exc).__name__}: {exc}"[:200]})
            continue
        finally:
            fetcher.close()
        slug = slugify(cand["name"])
        paths = write_all(result, outdir, slug)
        sev = result.stats.get("findings_by_severity", {})
        print(f"    {result.stats.get('pages_fetched_ok',0)} pages, "
              f"{result.stats.get('claims',0)} claims, "
              f"{len(result.findings)} findings ({sev or 'none'})", flush=True)
        runs.append({
            "candidate": cand,
            "result_file": str(paths["json"]),
            "report_file": str(paths["html"]),
            "summary": {
                "pages_fetched_ok": result.stats.get("pages_fetched_ok", 0),
                "pages_failed": result.stats.get("pages_failed", 0),
                "claims": result.stats.get("claims", 0),
                "findings": len(result.findings),
                "by_severity": sev,
                "by_confidence": result.stats.get("findings_by_confidence", {}),
                "by_kind": result.stats.get("findings_by_kind", {}),
                "duration_seconds": result.duration_seconds,
            },
        })

    manifest = {
        "run_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "random_seed": RANDOM_SEED,
        "sample_size": SAMPLE_SIZE,
        "audit_settings": AUDIT_SETTINGS,
        "pool": pool_as_dicts(),
        "eligibility": eligibility,
        "selected": selected,
        "runs": runs,
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print(f"\nWrote {outdir / 'manifest.json'}")
    return manifest


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="promise-audit-batch",
                                 description="Run the consistency audit across a seeded random "
                                             "sample of smaller SaaS companies.")
    ap.add_argument("--out", default="results/experiment")
    ap.add_argument("--delay", type=float, default=1.0)
    ap.add_argument("--precheck-only", action="store_true")
    ap.add_argument("--skip-precheck", action="store_true",
                    help="reuse an existing eligibility.json instead of re-checking")
    args = ap.parse_args(argv)
    outdir = Path(args.out)
    if args.precheck_only:
        e = precheck(outdir, delay=args.delay)
        print(f"{e['eligible']}/{e['pool_size']} eligible; wrote {outdir/'eligibility.json'}")
        return 0
    run_batch(outdir, delay=args.delay, skip_precheck=args.skip_precheck)
    return 0


if __name__ == "__main__":
    sys.exit(main())
