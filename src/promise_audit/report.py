"""Render an audit as a founder-readable HTML page, a Markdown file, or terminal text."""

from __future__ import annotations

import html
import json
from pathlib import Path

from .audit import AuditResult

KIND_LABEL = {
    "likely_contradiction": "Likely contradiction",
    "ambiguity": "Ambiguity",
    "potentially_outdated": "Possibly out of date",
    "missing_information": "Missing information",
}
KIND_BLURB = {
    "likely_contradiction": "Two public statements that cannot both be true.",
    "ambiguity": "Both statements can be true, but a customer cannot tell what they get.",
    "potentially_outdated": "Content that looks left over from an earlier version of your packaging.",
    "missing_information": "Something that changes the deal, published somewhere the buyer will not look.",
}
CATEGORY_LABEL = {
    "pricing": "Pricing", "compare": "Plan comparison", "limits": "Usage limits",
    "billing_docs": "Billing help", "trial": "Trial / signup", "addons": "Add-ons",
    "faq": "FAQ", "help": "Help centre", "docs": "Documentation", "terms": "Terms",
    "manual": "Supplied manually",
}

HEADLINE_NOUN = {1: "commercial promise", }


def _headline(n: int) -> str:
    if n == 0:
        return "We found no clear contradictions in your public commercial promises."
    noun = "commercial promise" if n == 1 else "commercial promises"
    return f"We found {n} {noun} worth checking."


CLOSING = ("These are the promises your customers can see. "
           "Do your billing system and product deliver the same thing?")

CLOSING_BODY = (
    "This audit only reads what is published on your website. It cannot see what your "
    "billing system actually meters, what your product actually enforces, or what your "
    "customer records actually entitle people to. In most companies those three answers "
    "have drifted apart quietly, and the public pages are the only place the drift is "
    "visible from outside. If the contradictions above are news to you, the more expensive "
    "question is what else is out of step behind them."
)

CSS = """
:root{--ink:#12151c;--muted:#5d6675;--line:#e3e6ec;--bg:#fbfbfc;--card:#fff;
--high:#c0392b;--high-bg:#fdf0ee;--med:#b06f13;--med-bg:#fdf6ea;--low:#4a6b8a;--low-bg:#eff4f8;
--accent:#1a4fa0;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Helvetica,Arial,sans-serif;}
.wrap{max-width:840px;margin:0 auto;padding:56px 24px 96px;}
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
.f h3{font-size:18px;margin:0 0 10px;line-height:1.35;letter-spacing:-.01em}
.f p{margin:0 0 14px;color:#2b3140}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:16px 0 0}
@media(max-width:640px){.pair{grid-template-columns:1fr}}
.side{background:#f7f8fa;border:1px solid var(--line);border-radius:9px;padding:14px 15px;}
.side .lab{font-size:11.5px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);
font-weight:700;margin-bottom:6px}
.side .claim{font-weight:600;font-size:15px;margin-bottom:9px;line-height:1.4}
.side blockquote{margin:0 0 9px;padding-left:11px;border-left:2px solid #cdd3dd;color:#4a5262;
font-size:13.5px;line-height:1.5;font-style:italic;}
.side a{font-size:13px;color:var(--accent);text-decoration:none;word-break:break-all}
.side a:hover{text-decoration:underline}
.caveat{margin-top:15px;padding-top:13px;border-top:1px dashed var(--line);color:var(--muted);
font-size:13.5px;}
.caveat b{color:#4a5262;font-weight:600}
table{width:100%;border-collapse:collapse;font-size:14px;margin-top:10px}
th,td{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
td a{color:var(--accent);text-decoration:none;word-break:break-all}
.tag{display:inline-block;background:#f1f2f5;color:var(--muted);font-size:11.5px;
padding:2px 7px;border-radius:4px}
.close{margin-top:56px;padding:28px 30px;background:#12151c;color:#f2f4f7;border-radius:12px}
.close h2{color:#fff;margin:0 0 12px;font-size:22px;line-height:1.35}
.close p{color:#c2c8d2;margin:0;font-size:15.5px}
.legend{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 20px;
font-size:14px;color:var(--muted)}
.legend div{margin:5px 0}
.legend b{color:var(--ink)}
.none{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:24px}
footer{margin-top:40px;color:var(--muted);font-size:13px;border-top:1px solid var(--line);padding-top:18px}
"""


def _esc(s) -> str:
    return html.escape("" if s is None else str(s))


def _side(label: str, claim: str, ev: dict | None) -> str:
    if not ev:
        return ""
    quote = ev.get("quote") or ""
    link = ev.get("url") or ""
    title = ev.get("page_title") or link
    return f"""<div class="side"><div class="lab">{_esc(label)}</div>
<div class="claim">{_esc(claim)}</div>
{'<blockquote>&ldquo;' + _esc(quote) + '&rdquo;</blockquote>' if quote else ''}
<a href="{_esc(link)}" target="_blank" rel="noopener">{_esc(title)}</a></div>"""


def render_html(result: AuditResult) -> str:
    findings = result.findings
    n = len(findings)
    kinds_present = []
    for k in ("likely_contradiction", "ambiguity", "potentially_outdated", "missing_information"):
        if any(f["kind"] == k for f in findings):
            kinds_present.append(k)

    cards = []
    for f in findings:
        sides = _side("What your pricing says", f["claim_a"], f["evidence_a"])
        if f.get("evidence_b"):
            sides += _side("What another page says", f["claim_b"], f["evidence_b"])
        else:
            sides += (f"""<div class="side"><div class="lab">The other side of it</div>
<div class="claim">{_esc(f['claim_b'])}</div></div>""")
        caveat = ""
        if f.get("caveat"):
            caveat = f'<div class="caveat"><b>Worth knowing:</b> {_esc(f["caveat"])}</div>'
        cards.append(f"""<article class="f {_esc(f['severity'])}">
<div class="chips">
  <span class="chip {_esc(f['severity'])}">{_esc(f['severity'])} impact</span>
  <span class="chip kind">{_esc(KIND_LABEL.get(f['kind'], f['kind']))}</span>
  <span class="chip conf">{_esc(f['confidence'])} confidence</span>
</div>
<h3>{_esc(f['headline'])}</h3>
<p>{_esc(f['explanation'])}</p>
<div class="pair">{sides}</div>
{caveat}
</article>""")

    if not findings:
        cards = [f"""<div class="none"><p>We read {result.stats.get('pages_fetched_ok', 0)}
of your public pages and could not find two statements that clearly disagree with each other.
That is a genuinely good result — most sites we look at have at least one.</p>
<p>It does not mean everything reconciles. This tool only reads what is published, and it only
flags conflicts it can evidence with two quotes.</p></div>"""]

    legend = "".join(
        f"<div><b>{_esc(KIND_LABEL[k])}</b> — {_esc(KIND_BLURB[k])}</div>" for k in kinds_present)

    rows = []
    for p in result.pages:
        status = "read" if p.ok else f"failed &mdash; {_esc(p.error)[:60]}"
        rows.append(f"""<tr><td><a href="{_esc(p.url)}" target="_blank" rel="noopener">
{_esc(p.title or p.url)}</a><br><span class="tag">{_esc(CATEGORY_LABEL.get(p.category, p.category))}</span>
{' <span class="tag">JS-rendered</span>' if p.rendered else ''}</td>
<td>{_esc(p.claim_count) if p.ok else '&mdash;'}</td><td>{status}</td></tr>""")

    sev = result.stats.get("findings_by_severity", {})
    sev_line = ", ".join(f"{v} {k}" for k, v in sev.items()) or "none"

    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Commercial consistency audit — {_esc(result.company)}</title><style>{CSS}</style></head><body>
<div class="wrap">
<p class="eyebrow">Commercial consistency audit</p>
<h1>{_esc(_headline(n))}</h1>
<p class="sub">Everything below is taken word-for-word from
<a href="{_esc(result.root_url)}" style="color:inherit">{_esc(result.domain)}</a>.
Nothing here is inferred from anything private.</p>
<p class="meta"><b>{result.stats.get('pages_fetched_ok', 0)}</b> public pages read &middot;
<b>{result.stats.get('claims', 0)}</b> commercial claims extracted &middot;
<b>{sev_line}</b> &middot; run {_esc(result.started_at)}</p>

{'<h2>What we found</h2>' if findings else ''}
{''.join(cards)}

{'<h2>How to read these</h2><div class="legend">' + legend + '</div>' if legend else ''}

<h2>Pages we read</h2>
<table><thead><tr><th>Page</th><th>Claims</th><th>Status</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>

<div class="close"><h2>{_esc(CLOSING)}</h2><p>{_esc(CLOSING_BODY)}</p></div>
<footer>Automated read of public pages only. Every finding is shown with the quote it came from
so you can check it yourself in a minute. No login, no billing data, no customer records were
involved.</footer>
</div></body></html>"""


def render_markdown(result: AuditResult) -> str:
    n = len(result.findings)
    lines = [f"# Commercial consistency audit — {result.company}", "",
             f"**{_headline(n)}**", "",
             f"Source: {result.root_url} · {result.stats.get('pages_fetched_ok', 0)} public pages read · "
             f"{result.stats.get('claims', 0)} commercial claims extracted · {result.started_at}", ""]
    for i, f in enumerate(result.findings, 1):
        lines += [f"## {i}. {f['headline']}", "",
                  f"`{f['severity']} impact` · `{KIND_LABEL.get(f['kind'], f['kind'])}` "
                  f"· `{f['confidence']} confidence`", "", f["explanation"], ""]
        for lab, claim, ev in (("What your pricing says", f["claim_a"], f["evidence_a"]),
                               ("What another page says", f["claim_b"], f.get("evidence_b"))):
            lines.append(f"**{lab}:** {claim}")
            if ev:
                lines.append(f"> {ev['quote']}")
                lines.append(f"> — [{ev['page_title'] or ev['url']}]({ev['url']})")
            lines.append("")
        if f.get("caveat"):
            lines += [f"*Worth knowing: {f['caveat']}*", ""]
    lines += ["## Pages we read", "", "| Page | Category | Claims | Status |", "|---|---|---|---|"]
    for p in result.pages:
        st = "read" if p.ok else f"failed — {p.error[:50]}"
        lines.append(f"| [{(p.title or p.url)[:60]}]({p.url}) | "
                     f"{CATEGORY_LABEL.get(p.category, p.category)} | "
                     f"{p.claim_count if p.ok else '—'} | {st} |")
    lines += ["", "---", "", f"**{CLOSING}**", "", CLOSING_BODY]
    return "\n".join(lines)


def render_terminal(result: AuditResult) -> str:
    out = ["", "=" * 76, _headline(len(result.findings)).upper(), "=" * 76,
           f"{result.company}  ·  {result.stats.get('pages_fetched_ok', 0)} pages read  ·  "
           f"{result.stats.get('claims', 0)} claims extracted  ·  {result.duration_seconds}s", ""]
    for i, f in enumerate(result.findings, 1):
        out.append(f"{i}. [{f['severity'].upper()} · {f['confidence']} confidence · "
                   f"{KIND_LABEL.get(f['kind'], f['kind'])}]")
        out.append(f"   {f['headline']}")
        out.append(f"   A: {f['claim_a']}")
        out.append(f"      {f['evidence_a']['url']}")
        if f.get("evidence_b"):
            out.append(f"   B: {f['claim_b']}")
            out.append(f"      {f['evidence_b']['url']}")
        else:
            out.append(f"   B: {f['claim_b']}")
        out.append("")
    if not result.findings:
        out.append("No clearly evidenced contradictions found.\n")
    out += ["-" * 76, CLOSING, "-" * 76, ""]
    return "\n".join(out)


def write_all(result: AuditResult, outdir: str | Path, slug: str) -> dict[str, Path]:
    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    paths = {
        "json": outdir / f"{slug}.json",
        "html": outdir / f"{slug}.html",
        "markdown": outdir / f"{slug}.md",
    }
    paths["json"].write_text(json.dumps(result.to_dict(), indent=2))
    paths["html"].write_text(render_html(result))
    paths["markdown"].write_text(render_markdown(result))
    return paths
