"""Assemble the experiment report from the batch manifest.

Everything here is derived from saved results. The qualitative judgement lives
in `narrative.md` beside the manifest and is inserted verbatim, so what was
measured stays visibly separate from what was concluded.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from ..discover import CATEGORIES
from ..schema import FINDING_TYPE_BLURB, FINDING_TYPE_LABEL

ORDER = ["high", "medium", "low"]


def build(outdir: str | Path = "results/experiment") -> Path:
    outdir = Path(outdir)
    m = json.loads((outdir / "manifest.json").read_text())
    rows = []
    for run in m["runs"]:
        result = {}
        if run.get("result_file") and Path(run["result_file"]).exists():
            result = json.loads(Path(run["result_file"]).read_text())
        rows.append((run, result))

    sev, conf, kind = Counter(), Counter(), Counter()
    total_findings = with_finding = credible = 0
    pages = usable = thin = failed = promises = 0
    quotes_checked = quotes_failed = rejected = corrections = 0
    blind = []

    for run, r in rows:
        src = r.get("source", {})
        st = src.get("stats", {})
        pages += st.get("pages_fetched_ok", 0)
        usable += st.get("pages_usable", 0)
        thin += st.get("pages_fetched_ok", 0) - st.get("pages_usable", 0)
        failed += st.get("pages_failed", 0)
        promises += len(r.get("promises", []))
        v = r.get("verification", {})
        quotes_checked += v.get("quotes_checked", 0)
        quotes_failed += v.get("quotes_failed", 0)
        rejected += v.get("findings_rejected", 0)
        corrections += v.get("url_corrections", 0)
        pricing = [p for p in src.get("pages", []) if p.get("category") == "pricing"]
        if pricing and all(not p.get("usable") for p in pricing):
            blind.append(run["candidate"]["name"])
        fs = r.get("findings", [])
        total_findings += len(fs)
        if fs:
            with_finding += 1
        if any(f["confidence"] in ("high", "medium") for f in fs):
            credible += 1
        for f in fs:
            sev[f["severity"]] += 1
            conf[f["confidence"]] += 1
            kind[f["type"]] += 1

    L: list[str] = []
    A = L.append
    A("# Do SaaS companies contradict themselves in public?")
    A("")
    A("### A ten-company experiment with the commercial-consistency auditor")
    A("")
    A(f"Harvested {m['harvested_at']} · analysed {m.get('finished_at','')} · "
      f"analyst backend `{m.get('backend','agent')}` · random seed `{m['random_seed']}` · "
      f"candidate pool {len(m['pool'])} · eligible {m['eligibility']['eligible']} · "
      f"analysed {len(rows)}")
    A("")

    narrative = outdir / "narrative.md"
    if narrative.exists():
        A(narrative.read_text().strip())
        A("")

    A("---")
    A("")
    A("## 1. Headline numbers")
    A("")
    A("| Measure | Value |")
    A("|---|---|")
    A(f"| Companies analysed | {len(rows)} |")
    A(f"| Companies with at least one finding | {with_finding} of {len(rows)} |")
    A(f"| Companies with a medium- or high-confidence finding | {credible} of {len(rows)} |")
    A(f"| Total findings (after verification) | {total_findings} |")
    A("| Findings by severity | " + ", ".join(f"{sev.get(s,0)} {s}" for s in ORDER) + " |")
    A("| Findings by confidence | " + ", ".join(f"{conf.get(s,0)} {s}" for s in ORDER) + " |")
    A(f"| Commercial promises extracted | {promises} |")
    A(f"| Public pages fetched | {pages} |")
    A(f"| Pages with enough readable text to analyse | {usable} |")
    A(f"| Pages that returned almost no text (client-rendered) | {thin} |")
    A(f"| Pages that could not be fetched at all | {failed} |")
    A(f"| Companies whose pricing page could not be read | {len(blind)}"
      + (f" ({', '.join(blind)})" if blind else "") + " |")
    A("")
    A("**Verification** — every quote the analyst produced was checked against the page it "
      "was attributed to:")
    A("")
    A("| Check | Count |")
    A("|---|---|")
    A(f"| Quotes checked against their source page | {quotes_checked} |")
    A(f"| Quotes that could not be found anywhere in the harvest | {quotes_failed} |")
    A(f"| Quotes real but attributed to the wrong page (corrected) | {corrections} |")
    A(f"| Candidate findings discarded as unverifiable | {rejected} |")
    A("")
    A("**Findings by type**")
    A("")
    A("| Type | Count | What it means |")
    A("|---|---|---|")
    for k, c in kind.most_common():
        A(f"| {FINDING_TYPE_LABEL.get(k,k)} | {c} | {FINDING_TYPE_BLURB.get(k,'')} |")
    A("")

    A("---")
    A("")
    A("## 2. The ten companies, one by one")
    A("")
    for run, r in rows:
        cand = run["candidate"]
        A(f"### {cand['name']}")
        A("")
        A(f"{cand['url']} · {cand['category']} · found via {cand['discovered_via']}")
        A("")
        if run.get("status") != "ok" or not r:
            A(f"**No result:** {run.get('status', 'unknown')} "
              f"{run.get('error', '')}".strip())
            A("")
            continue
        src, st = r["source"], r["source"]["stats"]
        v = r["verification"]
        A(f"Read **{st.get('pages_usable',0)}** usable pages of "
          f"{st.get('pages_fetched_ok',0)} fetched, extracted **{len(r.get('promises',[]))}** "
          f"commercial promises, produced **{len(r['findings'])}** findings. "
          f"{v['quotes_checked']} quotes verified, {v['findings_rejected']} candidate "
          f"finding(s) discarded.")
        A("")
        plans = r.get("plans", [])
        if plans:
            A("**Plans found:** " + "; ".join(
                f"{p.get('name')} ({p.get('headline_price') or 'no published price'})"
                for p in plans))
            A("")
        A("<details><summary>Pages read</summary>")
        A("")
        A("| Page | Type | Words | Status |")
        A("|---|---|---|---|")
        for p in src.get("pages", []):
            label = CATEGORIES.get(p["category"], {}).get("label", p["category"])
            status = "read" if p.get("usable") else "too little text to read"
            title = (p.get("title") or p["url"]).replace("|", "-")[:56]
            A(f"| [{title}]({p['url']}) | {label} | {p.get('word_count',0)} | {status} |")
        for f in src.get("failures", []):
            A(f"| {f['url']} | — | — | {f['reason'][:45]} |")
        A("")
        A("</details>")
        A("")
        if not r["findings"]:
            A("**No findings.** Nothing on the pages read contradicted anything else with "
              "enough evidence to report.")
            A("")
        for i, f in enumerate(r["findings"], 1):
            A(f"**{i}. {f['headline']}**  ")
            A(f"`{f['severity']} impact` · `{FINDING_TYPE_LABEL.get(f['type'], f['type'])}` "
              f"· `{f['confidence']} confidence`")
            A("")
            A(f["explanation"])
            A("")
            for lab, c in (("Claim A", f["claim_a"]), ("Claim B", f["claim_b"])):
                A(f"- **{lab}:** {c['statement']}")
                A(f"  - Evidence: “{c['quote'][:230]}”")
                A(f"  - Source: [{c['url']}]({c['url']})")
            A(f"- *Why this is not just wording: {f.get('why_not_just_wording','')}*")
            if (f.get("caveat") or "").strip():
                A(f"- *What would make this a non-issue: {f['caveat']}*")
            A("")
        notes = r.get("coverage_notes") or {}
        if notes.get("what_was_not_checkable"):
            A(f"*Not checkable from these pages: {notes['what_was_not_checkable']}*")
            A("")

    A("---")
    A("")
    A("## 3. Selection method")
    A("")
    A(f"1. A candidate pool of **{len(m['pool'])}** smaller SaaS companies was frozen in "
      "`src/promise_audit/experiment/pool.py` before any company was analysed.")
    A("2. Every candidate was put through the same automated eligibility pre-check:")
    for c in m["eligibility"]["criteria"]:
        A(f"   - {c}")
    A(f"3. **{m['eligibility']['eligible']}** candidates passed.")
    A(f"4. Ten were drawn with `random.Random({m['random_seed']}).sample(...)` over the "
      "eligible candidates sorted by URL, so the draw is reproducible and independent of "
      "the order the pre-check finished in.")
    A("5. All ten were harvested with identical settings "
      f"(`{json.dumps(m['harvest_settings'])}`) and analysed with the identical prompt from "
      "`prompts.py`. Nothing was changed for any individual company.")
    A("")
    A("**Selected:** " + ", ".join(c["name"] for c in m["selected"]) + ".")
    A("")
    A("### Complete candidate pool")
    A("")
    A("| # | Company | Category | Where it was found | Why it qualifies | Eligible? |")
    A("|---|---|---|---|---|---|")
    elig = {c["url"]: c for c in m["eligibility"]["candidates"]}
    chosen = {c["name"] for c in m["selected"]}
    for i, c in enumerate(m["pool"], 1):
        e = elig.get(c["url"], {})
        mark = ("**yes — selected**" if c["name"] in chosen else
                ("yes" if e.get("eligible") else f"no — {e.get('reason','not checked')[:70]}"))
        A(f"| {i} | [{c['name']}]({c['url']}) | {c['category']} | {c['discovered_via']} | "
          f"{c['why_qualifies']} | {mark} |")
    A("")

    path = outdir / "EXPERIMENT_REPORT.md"
    path.write_text("\n".join(L))
    return path


def main(argv: list[str] | None = None) -> int:
    outdir = Path(argv[0]) if argv else Path("results/experiment")
    p = build(outdir)
    print(f"Wrote {p} ({p.stat().st_size:,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
