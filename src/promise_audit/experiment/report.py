"""Assemble the experiment report from the batch manifest.

Everything in here is derived from the saved results. The qualitative
assessment lives in `narrative.md` next to the manifest and is inserted
verbatim, so the judgement calls are visibly separate from the measurements.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from ..report import KIND_LABEL

SEV_ORDER = ["high", "medium", "low"]


def _load(outdir: Path) -> dict:
    return json.loads((outdir / "manifest.json").read_text())


def _company_results(outdir: Path, manifest: dict) -> list[tuple[dict, dict]]:
    out = []
    for run in manifest["runs"]:
        if "result_file" not in run:
            out.append((run, {}))
            continue
        out.append((run, json.loads(Path(run["result_file"]).read_text())))
    return out


def build(outdir: str | Path = "results/experiment") -> Path:
    outdir = Path(outdir)
    m = _load(outdir)
    rows = _company_results(outdir, m)

    total_findings = sum(len(r.get("findings", [])) for _, r in rows)
    sev = Counter()
    conf = Counter()
    kind = Counter()
    rule = Counter()
    with_finding = 0
    credible = 0  # at least one finding that is not low-confidence
    for _, r in rows:
        fs = r.get("findings", [])
        if fs:
            with_finding += 1
        if any(f["confidence"] in ("high", "medium") for f in fs):
            credible += 1
        for f in fs:
            sev[f["severity"]] += 1
            conf[f["confidence"]] += 1
            kind[f["kind"]] += 1
            rule[f["rule"]] += 1

    L: list[str] = []
    A = L.append

    A("# Do SaaS companies contradict themselves in public?")
    A("")
    A("### A ten-company experiment with the commercial-consistency auditor")
    A("")
    A(f"Run {m['run_at']} · random seed `{m['random_seed']}` · "
      f"candidate pool {len(m['pool'])} · eligible {m['eligibility']['eligible']} · "
      f"analysed {len(rows)}")
    A("")

    narrative = outdir / "narrative.md"
    if narrative.exists():
        A(narrative.read_text().strip())
        A("")

    # ---------------------------------------------------------------- results
    A("---")
    A("")
    A("## 1. Headline numbers")
    A("")
    A("| Measure | Value |")
    A("|---|---|")
    A(f"| Companies analysed | {len(rows)} |")
    A(f"| Companies with at least one finding | {with_finding} of {len(rows)} |")
    A(f"| Companies with at least one **medium or high confidence** finding | {credible} of {len(rows)} |")
    A(f"| Total findings | {total_findings} |")
    A(f"| Findings by severity | " +
      ", ".join(f"{sev.get(s,0)} {s}" for s in SEV_ORDER) + " |")
    A(f"| Findings by confidence | " +
      ", ".join(f"{conf.get(s,0)} {s}" for s in SEV_ORDER) + " |")
    A(f"| Public pages read | {sum(r.get('stats',{}).get('pages_fetched_ok',0) for _,r in rows)} |")
    A(f"| Pages that could not be read | {sum(r.get('stats',{}).get('pages_failed',0) for _,r in rows)} |")
    A(f"| Commercial claims extracted | {sum(r.get('stats',{}).get('claims',0) for _,r in rows)} |")
    A("")
    A("**Findings by type**")
    A("")
    A("| Type | Count | What it means |")
    A("|---|---|---|")
    from ..report import KIND_BLURB
    for k, c in kind.most_common():
        A(f"| {KIND_LABEL.get(k,k)} | {c} | {KIND_BLURB.get(k,'')} |")
    A("")
    A("**Which rules fired**")
    A("")
    A("| Rule | Times fired | Companies |")
    A("|---|---|---|")
    for rl, c in rule.most_common():
        companies = sorted({run["candidate"]["name"] for run, r in rows
                            if any(f["rule"] == rl for f in r.get("findings", []))})
        A(f"| `{rl}` | {c} | {', '.join(companies)} |")
    A("")

    # ------------------------------------------------------------- per company
    A("---")
    A("")
    A("## 2. The ten companies, one by one")
    A("")
    for run, r in rows:
        cand = run["candidate"]
        A(f"### {cand['name']}")
        A("")
        A(f"{cand['url']} · {cand['category']} · discovered via {cand['discovered_via']}")
        A("")
        if not r:
            A(f"**Run failed:** {run.get('error','unknown error')}")
            A("")
            continue
        st = r.get("stats", {})
        A(f"Read **{st.get('pages_fetched_ok',0)}** pages "
          f"({st.get('pages_js_rendered',0)} needed a headless browser), extracted "
          f"**{st.get('claims',0)}** claims, produced **{len(r.get('findings',[]))}** findings "
          f"in {r.get('duration_seconds',0)}s.")
        A("")
        A("<details><summary>Pages read</summary>")
        A("")
        A("| Page | Category | Claims | Status |")
        A("|---|---|---|---|")
        for p in r.get("pages", []):
            status = "read" if p["ok"] else f"failed — {p['error'][:45]}"
            title = (p["title"] or p["url"]).replace("|", "-")[:58]
            A(f"| [{title}]({p['url']}) | {p['category']} | "
              f"{p['claim_count'] if p['ok'] else '—'} | {status} |")
        A("")
        A("</details>")
        A("")
        by_kind = r.get("stats", {}).get("claims_by_kind", {})
        if by_kind:
            A("Claims extracted: " +
              ", ".join(f"{v} {k.replace('_',' ')}" for k, v in by_kind.items()) + ".")
            A("")
        fails = r.get("failures", [])
        if fails:
            A("Inaccessible pages: " +
              "; ".join(f"{f['url']} ({f['reason'][:50]})" for f in fails[:5]) + ".")
            A("")
        if not r.get("findings"):
            A("**No findings.** Nothing on the pages read contradicted anything else "
              "with enough evidence to report.")
            A("")
            continue
        for i, f in enumerate(r["findings"], 1):
            A(f"**{i}. {f['headline']}**  ")
            A(f"`{f['severity']} impact` · `{KIND_LABEL.get(f['kind'],f['kind'])}` "
              f"· `{f['confidence']} confidence` · `{f['rule']}`")
            A("")
            A(f"{f['explanation']}")
            A("")
            for lab, claim, ev in (("Claim A", f["claim_a"], f["evidence_a"]),
                                   ("Claim B", f["claim_b"], f.get("evidence_b"))):
                A(f"- **{lab}:** {claim}")
                if ev:
                    q = ev["quote"].replace("\n", " ")[:230]
                    A(f"  - Evidence: “{q}”")
                    A(f"  - Source: [{ev['page_title'] or ev['url']}]({ev['url']})")
            if f.get("caveat"):
                A(f"- *Caveat: {f['caveat']}*")
            A("")
        A("")

    # ------------------------------------------------------------------- pool
    A("---")
    A("")
    A("## 3. Selection method")
    A("")
    A(f"1. A candidate pool of **{len(m['pool'])}** smaller SaaS companies was frozen in "
      f"`src/promise_audit/experiment/pool.py` before any company was analysed.")
    A("2. Every candidate was put through the same automated eligibility pre-check:")
    for c in m["eligibility"]["criteria"]:
        A(f"   - {c}")
    A(f"3. **{m['eligibility']['eligible']}** candidates passed.")
    A(f"4. Ten were drawn with `random.Random({m['random_seed']}).sample(...)` over the "
      f"eligible candidates sorted by URL, so the draw is reproducible and independent of "
      f"the order the pre-check finished in.")
    A("5. All ten were analysed with identical settings "
      f"(`{json.dumps(m['audit_settings'])}`). No rule, threshold or prompt was changed "
      "for any individual company.")
    A("")
    A("**Selected:** " + ", ".join(c["name"] for c in m["selected"]) + ".")
    A("")
    A("### Complete candidate pool")
    A("")
    A("| # | Company | Category | Where it was found | Why it qualifies | Eligible? |")
    A("|---|---|---|---|---|---|")
    elig_by_url = {c["url"]: c for c in m["eligibility"]["candidates"]}
    selected_names = {c["name"] for c in m["selected"]}
    for i, c in enumerate(m["pool"], 1):
        e = elig_by_url.get(c["url"], {})
        mark = "**yes — selected**" if c["name"] in selected_names else (
            "yes" if e.get("eligible") else f"no — {e.get('reason','not checked')[:70]}")
        A(f"| {i} | [{c['name']}]({c['url']}) | {c['category']} | {c['discovered_via']} | "
          f"{c['why_qualifies']} | {mark} |")
    A("")

    text = "\n".join(L)
    path = outdir / "EXPERIMENT_REPORT.md"
    path.write_text(text)
    return path


def main(argv: list[str] | None = None) -> int:
    outdir = Path(argv[0]) if argv else Path("results/experiment")
    p = build(outdir)
    print(f"Wrote {p} ({p.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
