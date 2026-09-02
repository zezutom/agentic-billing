"""Render a verified analysis as a report a founder will actually read."""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

from .discover import CATEGORIES
from .harvest import Dossier
from .schema import FINDING_TYPE_BLURB, FINDING_TYPE_LABEL

CLOSING = ("These are the promises your customers can see. "
           "Do your billing system and product deliver the same thing?")

CLOSING_BODY = (
    "This audit reads your public pages only. It cannot see what your billing system "
    "meters, what your product enforces, or what your customer records entitle people to. "
    "If the findings above are news to you, the question worth asking is what else is out "
    "of step behind them."
)


def headline(n: int) -> str:
    if n == 0:
        return "We found no clear contradictions in your public commercial promises."
    noun = "commercial promise" if n == 1 else "commercial promises"
    return f"We found {n} {noun} worth checking."


CSS = """
:root{--ink:#12151c;--muted:#5d6675;--line:#e3e6ec;--bg:#fbfbfc;--card:#fff;
--high:#c0392b;--high-bg:#fdf0ee;--med:#b06f13;--med-bg:#fdf6ea;--low:#4a6b8a;--low-bg:#eff4f8;
--accent:#1a4fa0;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;}
.wrap{max-width:860px;margin:0 auto;padding:56px 24px 96px;}
.eyebrow{font-size:13px;letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
font-weight:600;margin:0 0 12px;}
h1{font-size:34px;line-height:1.22;margin:0 0 14px;letter-spacing:-.02em;font-weight:700;}
.sub{color:var(--muted);font-size:17px;margin:0 0 8px;}
.meta{color:var(--muted);font-size:14px;margin:22px 0 0;padding-top:18px;border-top:1px solid var(--line);}
.meta b{color:var(--ink);font-weight:600}
h2{font-size:20px;margin:52px 0 14px;letter-spacing:-.01em;}
.f{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:22px 24px;
margin:0 0 18px;box-shadow:0 1px 2px rgba(16,24,40,.04);}
.f.high{border-left:4px solid var(--high)} .f.medium{border-left:4px solid var(--med)}
.f.low{border-left:4px solid var(--low)}
.chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:12px;align-items:center}
.chip{font-size:11.5px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;
padding:4px 9px;border-radius:5px;}
.chip.high{background:var(--high-bg);color:var(--high)}
.chip.medium{background:var(--med-bg);color:var(--med)}
.chip.low{background:var(--low-bg);color:var(--low)}
.chip.kind{background:#f1f2f5;color:var(--muted)}
.chip.conf{background:transparent;color:var(--muted);border:1px solid var(--line);font-weight:600}
.chip.ok{background:#eef7f0;color:#2f6b40}
.f h3{font-size:18px;margin:0 0 10px;line-height:1.35;letter-spacing:-.01em}
.f p{margin:0 0 14px;color:#2b3140}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 0}
@media(max-width:660px){.pair{grid-template-columns:1fr}}
.side{background:#f7f8fa;border:1px solid var(--line);border-radius:9px;padding:14px 15px;}
.side .lab{font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
font-weight:700;margin-bottom:6px}
.side .claim{font-weight:600;font-size:15px;margin-bottom:9px;line-height:1.4}
.side blockquote{margin:0 0 9px;padding-left:11px;border-left:2px solid #cdd3dd;color:#4a5262;
font-size:13.5px;line-height:1.5;font-style:italic;}
.side a{font-size:13px;color:var(--accent);text-decoration:none;word-break:break-all}
.side a:hover{text-decoration:underline}
.note{margin-top:15px;padding-top:13px;border-top:1px dashed var(--line);color:var(--muted);
font-size:13.5px;}
.note b{color:#4a5262;font-weight:600}
.note div{margin:4px 0}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
td a{color:var(--accent);text-decoration:none;word-break:break-all}
.tag{display:inline-block;background:#f1f2f5;color:var(--muted);font-size:11.5px;
padding:2px 7px;border-radius:4px;margin-right:4px}
.close{margin-top:56px;padding:28px 30px;background:#12151c;color:#f2f4f7;border-radius:12px}
.close h2{color:#fff;margin:0 0 12px;font-size:22px;line-height:1.35}
.close p{color:#c2c8d2;margin:0;font-size:15.5px}
.legend{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 20px;
font-size:14px;color:var(--muted)}
.legend div{margin:5px 0}
.legend b{color:var(--ink)}
.none{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px}
details{margin-top:10px}summary{cursor:pointer;color:var(--muted);font-size:14px}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:18px}
"""


def _e(s) -> str:
    return html.escape("" if s is None else str(s))


def _side(label: str, claim: dict) -> str:
    q = claim.get("quote") or ""
    url = claim.get("url") or ""
    return f"""<div class="side"><div class="lab">{_e(label)}</div>
<div class="claim">{_e(claim.get('statement'))}</div>
{'<blockquote>&ldquo;' + _e(q) + '&rdquo;</blockquote>' if q else ''}
<a href="{_e(url)}" target="_blank" rel="noopener">{_e(url)}</a></div>"""


def render_html(analysis: dict, dossier: Dossier) -> str:
    findings = analysis.get("findings", [])
    n = len(findings)
    kinds = [k for k in FINDING_TYPE_LABEL if any(f["type"] == k for f in findings)]

    cards = []
    for f in findings:
        notes = [f'<div><b>Why this is not just wording:</b> {_e(f.get("why_not_just_wording"))}</div>']
        if (f.get("caveat") or "").strip():
            notes.append(f'<div><b>What would make this a non-issue:</b> {_e(f["caveat"])}</div>')
        cards.append(f"""<article class="f {_e(f['severity'])}">
<div class="chips">
  <span class="chip {_e(f['severity'])}">{_e(f['severity'])} impact</span>
  <span class="chip kind">{_e(FINDING_TYPE_LABEL.get(f['type'], f['type']))}</span>
  <span class="chip conf">{_e(f['confidence'])} confidence</span>
  <span class="chip ok">evidence verified</span>
</div>
<h3>{_e(f['headline'])}</h3>
<p>{_e(f['explanation'])}</p>
<div class="pair">{_side('What one page says', f['claim_a'])}{_side('What another page says', f['claim_b'])}</div>
<div class="note">{''.join(notes)}</div>
</article>""")

    if not findings:
        usable = dossier.stats.get("pages_usable", 0)
        cards = [f"""<div class="none"><p>We read {usable} of your public pages and could not
find two statements that clearly disagree with each other. Most sites we look at have at
least one.</p>
<p>It does not mean everything reconciles. We only report a conflict when we can show you
both halves of it, quoted from two different pages of your own site.</p></div>"""]

    legend = "".join(f"<div><b>{_e(FINDING_TYPE_LABEL[k])}:</b> {_e(FINDING_TYPE_BLURB[k])}</div>"
                     for k in kinds)

    rows = []
    for p in dossier.pages:
        tags = f'<span class="tag">{_e(CATEGORIES.get(p.category, {}).get("label", p.category))}</span>'
        if p.rendered:
            tags += '<span class="tag">JS-rendered</span>'
        if p.ok and not p.usable:
            tags += '<span class="tag">too little text to read</span>'
        rows.append(f"""<tr><td><a href="{_e(p.url)}" target="_blank" rel="noopener">
{_e(p.title or p.url)}</a><br>{tags}</td><td>{_e(p.word_count)}</td>
<td>{'read' if p.ok else 'failed'}</td></tr>""")
    for f in dossier.failures:
        rows.append(f"""<tr><td>{_e(f['url'])}<br><span class="tag">not reached</span></td>
<td>&mdash;</td><td>{_e(f['reason'])[:60]}</td></tr>""")

    v = analysis.get("verification", {})
    promises = analysis.get("promises", [])
    plans = analysis.get("plans", [])
    plan_line = ", ".join(
        f"{p.get('name')}{', ' + p['headline_price'] if p.get('headline_price') else ''}"
        for p in plans) or "no plans could be read from these pages"

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_e(analysis.get('company'))} Promise Audit</title>
<style>{CSS}</style></head><body><div class="wrap">
<p class="eyebrow">Commercial consistency audit</p>
<h1>{_e(headline(n))}</h1>
<p class="sub">Everything below is quoted word-for-word from
<a href="{_e(dossier.root_url)}" style="color:inherit">{_e(dossier.domain)}</a>.
Nothing here is inferred from anything private.</p>
<p class="meta"><b>{dossier.stats.get('pages_usable', 0)}</b> public pages read &middot;
<b>{len(promises)}</b> commercial promises extracted &middot;
<b>{v.get('quotes_checked', 0)}</b> quotes checked against their source page &middot;
run {_e(dossier.harvested_at)}</p>

<h2>What you appear to sell</h2>
<div class="legend">{_e(plan_line)}</div>

{'<h2>What we found</h2>' if findings else '<h2>What we found</h2>'}
{''.join(cards)}

{'<h2>How to read these</h2><div class="legend">' + legend + '</div>' if legend else ''}

<h2>Pages we read</h2>
<table><thead><tr><th>Page</th><th>Words</th><th>Status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>

<div class="close"><h2>{_e(CLOSING)}</h2><p>{_e(CLOSING_BODY)}</p></div>
<footer>Automated read of public pages only, then checked: every quote above was located in
the page it is attributed to, and
{v.get('findings_rejected', 0)} candidate finding(s) were discarded because their evidence
could not be verified. No login, no billing data and no customer records were involved.</footer>
</div></body></html>"""


def render_markdown(analysis: dict, dossier: Dossier) -> str:
    findings = analysis.get("findings", [])
    v = analysis.get("verification", {})
    L = [f"# {analysis.get('company')}: commercial consistency audit", "",
         f"**{headline(len(findings))}**", "",
         f"{dossier.root_url} | {dossier.stats.get('pages_usable',0)} pages read | "
         f"{len(analysis.get('promises', []))} promises extracted | "
         f"{v.get('quotes_checked',0)} quotes verified | {dossier.harvested_at}", ""]
    plans = analysis.get("plans", [])
    if plans:
        L += ["## What you appear to sell", ""]
        for p in plans:
            L.append(f"- **{p.get('name')}**: {p.get('headline_price') or 'no published price'}")
        L.append("")
    for i, f in enumerate(findings, 1):
        L += [f"## {i}. {f['headline']}", "",
              f"`{f['severity']}` `{FINDING_TYPE_LABEL.get(f['type'], f['type'])}` "
              f"`{f['confidence']} confidence`", "", f["explanation"], ""]
        for lab, c in (("What one page says", f["claim_a"]),
                       ("What another page says", f["claim_b"])):
            L += [f"**{lab}:** {c.get('statement')}", f"> {c.get('quote')}",
                  f"> [{c.get('url')}]({c.get('url')})", ""]
        L += [f"*Why this is not just wording: {f.get('why_not_just_wording')}*", ""]
        if (f.get("caveat") or "").strip():
            L += [f"*What would make this a non-issue: {f['caveat']}*", ""]
    if not findings:
        L += ["No conflict could be evidenced from the pages read.", ""]
    L += ["## Pages we read", "", "| Page | Type | Words | Status |", "|---|---|---|---|"]
    for p in dossier.pages:
        label = CATEGORIES.get(p.category, {}).get("label", p.category)
        st = "read" if p.ok else "failed"
        if p.ok and not p.usable:
            st = "too little text to read"
        L.append(f"| [{(p.title or p.url)[:58].replace('|','-')}]({p.url}) | {label} | "
                 f"{p.word_count} | {st} |")
    for f in dossier.failures:
        L.append(f"| {f['url']} | | | {f['reason'][:45]} |")
    notes = analysis.get("coverage_notes") or {}
    if notes.get("what_was_not_checkable"):
        L += ["", "## What we could not check", "", notes["what_was_not_checkable"]]
    L += ["", "---", "", f"**{CLOSING}**", "", CLOSING_BODY]
    return "\n".join(L)


def render_terminal(analysis: dict, dossier: Dossier) -> str:
    findings = analysis.get("findings", [])
    v = analysis.get("verification", {})
    out = ["", "=" * 78, headline(len(findings)).upper(), "=" * 78,
           f"{analysis.get('company')}   {dossier.stats.get('pages_usable',0)} pages read   "
           f"{len(analysis.get('promises', []))} promises   "
           f"{v.get('quotes_checked',0)} quotes verified   "
           f"{v.get('findings_rejected',0)} discarded", ""]
    for i, f in enumerate(findings, 1):
        out += [f"{i}. [{f['severity'].upper()}] {FINDING_TYPE_LABEL.get(f['type'], f['type'])}"
                f", {f['confidence']} confidence",
                f"   {f['headline']}",
                f"   A: {f['claim_a'].get('statement')}",
                f"      {f['claim_a'].get('url')}",
                f"   B: {f['claim_b'].get('statement')}",
                f"      {f['claim_b'].get('url')}", ""]
    if not findings:
        out.append("No conflict could be evidenced from the pages read.\n")
    out += ["-" * 78, CLOSING, "-" * 78, ""]
    return "\n".join(out)


def write_all(analysis: dict, dossier: Dossier, outdir: str | Path, slug: str) -> dict[str, Path]:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    paths = {"json": outdir / f"{slug}.json", "html": outdir / f"{slug}.html",
             "markdown": outdir / f"{slug}.md", "artifact": outdir / f"{slug}.artifact.html",
             "dossier": outdir / f"{slug}.dossier.json"}
    payload = dict(analysis)
    payload["source"] = {"root_url": dossier.root_url, "domain": dossier.domain,
                         "harvested_at": dossier.harvested_at, "stats": dossier.stats,
                         "pages": [p.to_dict() | {"text": ""} for p in dossier.pages],
                         "failures": dossier.failures}
    paths["json"].write_text(json.dumps(payload, indent=2))
    paths["html"].write_text(render_html(analysis, dossier))
    paths["markdown"].write_text(render_markdown(analysis, dossier))
    paths["artifact"].write_text(render_artifact(analysis, dossier))
    dossier.save(paths["dossier"])
    return paths


# --------------------------------------------------------------- artifact view
# A shareable, theme-aware version of the report, written as artifact body
# content (no doctype/html/head/body wrapper) so it can be published directly.
#
# The layout leads with the two conflicting values, because that contrast is
# what the reader needs and everything else is support.

ARTIFACT_CSS = """
:root{
  --ground:#f6f7f9; --surface:#ffffff; --ink:#14181f; --ink-soft:#3b4350;
  --muted:#5a6371; --rule:#dfe3ea; --rule-soft:#ebeef2;
  --accent:#26547c; --high:#9e2b25; --medium:#8a5a16; --low:#4a5a6b;
  --verified:#2c6b4f; --quote:#454f5d; --quote-rule:#c8d0da; --panel:#f0f2f5;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#12151a; --surface:#191d24; --ink:#e6e9ee; --ink-soft:#c3cad3;
    --muted:#98a2b0; --rule:#2a3038; --rule-soft:#21262d;
    --accent:#7fb0dc; --high:#e08b84; --medium:#d7a455; --low:#9badc0;
    --verified:#7fc4a0; --quote:#b3bcc7; --quote-rule:#3a424c; --panel:#1e232a;
  }
}
:root[data-theme="dark"]{
  --ground:#12151a; --surface:#191d24; --ink:#e6e9ee; --ink-soft:#c3cad3;
  --muted:#98a2b0; --rule:#2a3038; --rule-soft:#21262d;
  --accent:#7fb0dc; --high:#e08b84; --medium:#d7a455; --low:#9badc0;
  --verified:#7fc4a0; --quote:#b3bcc7; --quote-rule:#3a424c; --panel:#1e232a;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans",-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
.sheet{max-width:76ch;margin:0 auto;padding:clamp(30px,6vw,60px) clamp(18px,5vw,32px) 80px;}
.mono{font-family:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted); margin:0 0 16px;
}
h1{
  font-family:Newsreader,Georgia,"Times New Roman",serif;
  font-size:clamp(29px,5vw,40px); line-height:1.12; font-weight:500;
  letter-spacing:-.015em; margin:0 0 12px; text-wrap:balance;
}
.standfirst{font-size:15.5px;color:var(--muted);margin:0;max-width:60ch;}
.standfirst a{color:var(--accent);text-decoration:none;}
.standfirst a:hover{text-decoration:underline}
.ledger{
  display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
  gap:1px; background:var(--rule); border:1px solid var(--rule); margin:30px 0 0;
}
.ledger div{background:var(--surface);padding:12px 14px;}
.ledger dt{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted); margin:0 0 4px;
}
.ledger dd{margin:0;font-size:20px;font-weight:600;font-variant-numeric:tabular-nums;}
h2{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px; font-weight:500;
  letter-spacing:.14em; text-transform:uppercase; color:var(--muted);
  margin:56px 0 0; padding-bottom:8px; border-bottom:1px solid var(--rule);
}
.sells{margin:16px 0 0;font-size:15px;color:var(--ink-soft);}
.sells span{display:block;padding:3px 0;}
.sells b{font-weight:600;color:var(--ink);}
.finding{padding:28px 0 6px;border-bottom:1px solid var(--rule-soft);}
.finding:last-of-type{border-bottom:0}
.tags{
  display:flex; flex-wrap:wrap; align-items:center; gap:6px 16px;
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10.5px;
  letter-spacing:.1em; text-transform:uppercase; margin-bottom:10px;
}
.num{color:var(--muted);font-variant-numeric:tabular-nums;}
.sev{display:inline-flex;align-items:center;gap:6px;font-weight:500}
.sev::before{content:"";width:8px;height:8px;flex:0 0 auto}
.sev.high{color:var(--high)} .sev.high::before{background:var(--high)}
.sev.medium{color:var(--medium)} .sev.medium::before{background:var(--medium)}
.sev.low{color:var(--low)} .sev.low::before{background:var(--low)}
.tags .kind,.tags .conf{color:var(--muted)}
.finding h3{
  font-family:Newsreader,Georgia,serif; font-weight:500; font-size:23px;
  line-height:1.22; letter-spacing:-.012em; margin:0 0 16px; text-wrap:balance;
}
.versus{
  display:grid; grid-template-columns:1fr 1fr; gap:1px;
  background:var(--rule); border:1px solid var(--rule);
}
.versus > div{background:var(--surface);padding:14px 16px;}
@media (max-width:600px){.versus{grid-template-columns:1fr}}
.where{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted); margin:0 0 7px;
}
.value{font-size:17px;font-weight:600;line-height:1.3;margin:0 0 10px;}
.versus blockquote{
  margin:0 0 10px; padding-left:11px; border-left:2px solid var(--quote-rule);
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:12px;
  line-height:1.55; color:var(--quote); white-space:pre-wrap; overflow-wrap:anywhere;
}
.src{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px;
  color:var(--accent); text-decoration:none; overflow-wrap:anywhere; display:block;
}
.src:hover{text-decoration:underline}
.meta{
  display:grid; grid-template-columns:auto 1fr; gap:5px 14px;
  margin:14px 0 4px; font-size:14px; color:var(--ink-soft); align-items:baseline;
}
.meta dt{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted);
}
.meta dd{margin:0}
.legend{margin:16px 0 0;font-size:14.5px;}
.legend p{margin:0 0 7px;color:var(--muted);}
.legend b{color:var(--ink);font-weight:600;}
.scroller{overflow-x:auto;margin-top:14px;}
table{width:100%;border-collapse:collapse;font-size:13.5px;min-width:430px;}
th{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10px;
  letter-spacing:.1em; text-transform:uppercase; color:var(--muted);
  text-align:left; font-weight:500; padding:0 12px 7px 0;
  border-bottom:1px solid var(--rule);
}
td{padding:8px 12px 8px 0;border-bottom:1px solid var(--rule-soft);vertical-align:top;}
td:last-child,th:last-child{padding-right:0}
td a{color:var(--accent);text-decoration:none;}
td a:hover{text-decoration:underline}
.words{font-variant-numeric:tabular-nums;color:var(--muted);}
.state{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;
  color:var(--muted);white-space:nowrap;}
.state.dim{opacity:.7}
.kicker{margin:58px 0 0;padding:26px 0 0;border-top:2px solid var(--ink);}
.kicker h2{
  font-family:Newsreader,Georgia,serif; font-size:clamp(20px,3.3vw,25px);
  font-weight:500; line-height:1.25; letter-spacing:-.01em; color:var(--ink);
  text-transform:none; letter-spacing:-.01em; margin:0 0 12px; padding:0; border:0;
  text-wrap:balance;
}
.kicker p{margin:0;color:var(--ink-soft);font-size:15px;}
footer{margin-top:40px;padding-top:16px;border-top:1px solid var(--rule);
  font-size:12px;color:var(--muted);}
.none{margin-top:18px;padding:20px 22px;background:var(--surface);border:1px solid var(--rule);}
.none p{margin:0 0 10px;color:var(--ink-soft);}
.none p:last-child{margin-bottom:0}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}}
"""

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
    "family=Newsreader:opsz,wght@6..72,400;6..72,500&"
    "family=IBM+Plex+Sans:wght@400;500;600&"
    "family=IBM+Plex+Mono:wght@400;500&display=swap\">"
)


def _page_label(dossier: Dossier, url: str) -> str:
    """Name the page a claim came from, using the page type we crawled it as."""
    key = (url or "").rstrip("/")
    for p in dossier.pages:
        if key in (p.url.rstrip("/"), (p.final_url or "").rstrip("/")):
            return CATEGORIES.get(p.category, {}).get("label", p.category)
    return "Another page"


def _versus(where: str, claim: dict) -> str:
    quote = (claim.get("quote") or "").strip()
    url = claim.get("url") or ""
    short = re.sub(r"^https?://(www\.)?", "", url)
    return (
        f'<div><p class="where">{_e(where)}</p>'
        f'<p class="value">{_e(claim.get("statement"))}</p>'
        + (f"<blockquote>{_e(quote)}</blockquote>" if quote else "")
        + f'<a class="src" href="{_e(url)}" target="_blank" rel="noopener">{_e(short)}</a></div>'
    )


def render_artifact(analysis: dict, dossier: Dossier) -> str:
    """The report as artifact body content: theme-aware, shareable, no wrapper."""
    findings = analysis.get("findings", [])
    n = len(findings)
    company = analysis.get("company") or dossier.company
    v = analysis.get("verification", {})
    st = dossier.stats

    records = []
    for i, f in enumerate(findings, 1):
        where_a = _page_label(dossier, f["claim_a"].get("url"))
        where_b = ("Same page, further down" if f.get("same_page")
                   else _page_label(dossier, f["claim_b"].get("url")))
        meta = []
        if (f.get("explanation") or "").strip():
            meta.append(f'<dt>Impact</dt><dd>{_e(f["explanation"])}</dd>')
        if (f.get("caveat") or "").strip():
            meta.append(f'<dt>Check</dt><dd>{_e(f["caveat"])}</dd>')
        records.append(
            f'<article class="finding"><p class="tags">'
            f'<span class="num">{i:02d}</span>'
            f'<span class="sev {_e(f["severity"])}">{_e(f["severity"])}</span>'
            f'<span class="kind">{_e(FINDING_TYPE_LABEL.get(f["type"], f["type"]))}</span>'
            f'<span class="conf">{_e(f["confidence"])} confidence</span></p>'
            f'<h3>{_e(f["headline"])}</h3>'
            f'<div class="versus">{_versus(where_a, f["claim_a"])}'
            f'{_versus(where_b, f["claim_b"])}</div>'
            + (f'<dl class="meta">{"".join(meta)}</dl>' if meta else "")
            + "</article>"
        )
    if not findings:
        records.append(
            f'<div class="none"><p>We read {st.get("pages_usable", 0)} of your public pages '
            "and found no two statements that clearly disagree. Most sites we look at have "
            "at least one.</p><p>This does not mean everything reconciles. We only report a "
            "conflict when we can show you both halves of it, quoted from your own site.</p></div>"
        )

    kinds = [k for k in FINDING_TYPE_LABEL if any(f["type"] == k for f in findings)]
    legend = "".join(
        f"<p><b>{_e(FINDING_TYPE_LABEL[k])}:</b> {_e(FINDING_TYPE_BLURB[k])}</p>" for k in kinds)

    rows = []
    for p in dossier.pages:
        label = CATEGORIES.get(p.category, {}).get("label", p.category)
        state = "read" if p.usable else "no readable text"
        dim = "" if p.usable else " dim"
        rows.append(
            f'<tr><td><a href="{_e(p.url)}" target="_blank" rel="noopener">'
            f'{_e((p.title or p.url)[:64])}</a></td><td class="state">{_e(label)}</td>'
            f'<td class="words">{p.word_count:,}</td>'
            f'<td class="state{dim}">{_e(state)}</td></tr>')
    for f in dossier.failures:
        rows.append(f'<tr><td>{_e(f["url"])}</td><td class="state"></td>'
                    f'<td class="words"></td>'
                    f'<td class="state dim">{_e(f["reason"])[:44]}</td></tr>')

    plans = "".join(
        f"<span><b>{_e(p.get('name'))}</b> {_e(p.get('headline_price') or 'no published price')}</span>"
        for p in analysis.get("plans", [])
    ) or "<span>No plans could be read from these pages.</span>"

    ledger = [("Pages read", st.get("pages_usable", 0)),
              ("Promises", len(analysis.get("promises", []))),
              ("Quotes verified", v.get("quotes_checked", 0)),
              ("Discarded", v.get("findings_rejected", 0))]
    ledger_html = "".join(f"<div><dt>{_e(k)}</dt><dd>{_e(val)}</dd></div>" for k, val in ledger)

    domain = _e(dossier.domain)
    return f"""<title>{_e(company)} Promise Audit</title>
{FONT_LINK}
<style>{ARTIFACT_CSS}</style>
<main class="sheet">
  <p class="eyebrow">Commercial consistency audit</p>
  <h1>{_e(headline(n))}</h1>
  <p class="standfirst">Every quote below was checked against the page it came from.
    Public pages of <a href="{_e(dossier.root_url)}" target="_blank" rel="noopener">{domain}</a>
    only. Nothing private was used.</p>
  <dl class="ledger">{ledger_html}</dl>

  <h2>Plans found</h2>
  <p class="sells">{plans}</p>

  <h2>Findings</h2>
  {''.join(records)}

  {'<h2>Definitions</h2><div class="legend">' + legend + '</div>' if legend else ''}

  <h2>Pages read</h2>
  <div class="scroller"><table><thead><tr><th>Page</th><th>Type</th><th>Words</th>
    <th>Status</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>

  <section class="kicker"><h2>{_e(CLOSING)}</h2><p>{_e(CLOSING_BODY)}</p></section>
  <footer>Public pages only. Every quote above was located in the page it is attributed to.
    {v.get('findings_rejected', 0)} candidate finding(s) were discarded because their evidence
    could not be verified. No login, no billing data, no customer records.</footer>
</main>"""
