"""Turn a company's public pages into a readable dossier for the analyst.

The model reads prose, not HTML. This stage renders each page as compact
Markdown-ish text, keeping headings, bullets and table rows and dropping
navigation and boilerplate, and spends its size budget on the parts of a page
that actually talk about money.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, Tag

from .discover import CATEGORIES, discover
from .fetcher import Fetcher, canonical_url, registered_domain

DROP_TAGS = {"script", "style", "noscript", "svg", "iframe", "template", "head",
             "form", "input", "button", "select", "canvas"}
DROP_ROLES = {"navigation", "banner", "contentinfo", "search", "complementary"}
DROP_CLASS_RE = re.compile(
    r"\b(nav|navbar|menu|header|footer|cookie|consent|banner|breadcrumb|social|"
    r"newsletter|subscribe-form|sidebar|toc|table-of-contents|skip-link|announce)\b", re.I)

# Text that earns its place in the dossier.
COMMERCIAL_RE = re.compile(
    r"\$|€|£|\bUSD\b|\bEUR\b|\bGBP\b|/mo\b|/month|per month|per year|annually|monthly|billed|"
    r"\bprice|\bpricing|\bplan\b|\bplans\b|\btier|plan\b|plans\b|\bfree\b|\btrial\b|\bupgrade|"
    r"\bdowngrade|\bsubscription|\bbilling|\binvoice|\brefund|\brenew|\bcancel|"
    r"\bunlimited\b|\blimit|\bquota|\ballowance|\bcredit|\bseat|\buser[s]?\b|\bteam member|"
    r"\bincluded\b|\bincludes\b|\bper seat|\bper user|\bfair use|\bfair usage|\bacceptable use|"
    r"\bovera?ge|\bexceed|\brate limit|\bthrottl|\badd[- ]?on|\bextra\b|\benterprise\b|"
    r"\bcontact sales|\bcustom pricing|\bquote\b|\brequests? per|\bGB\b|\bTB\b|\bMB\b|"
    r"\bstorage\b|\bretention\b|\bavailable on\b|\brequires\b|\bonly\b.{0,20}\bplan",
    re.I)

MAX_CHARS_PER_PAGE = 6000
MAX_CHARS_PER_DOSSIER = 46_000
MIN_USABLE_WORDS = 120


@dataclass
class HarvestedPage:
    url: str
    final_url: str
    title: str
    category: str
    why_selected: str
    discovered_via: str
    ok: bool
    error: str
    rendered: bool
    word_count: int
    text: str = ""          # the rendered dossier text for this page
    truncated: bool = False
    usable: bool = True

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Dossier:
    company: str
    root_url: str
    domain: str
    harvested_at: str
    pages: list[HarvestedPage] = field(default_factory=list)
    failures: list[dict] = field(default_factory=list)
    discovery_notes: list[str] = field(default_factory=list)
    pricing_urls: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))
        return path

    @classmethod
    def load(cls, path: str | Path) -> "Dossier":
        d = json.loads(Path(path).read_text())
        pages = [HarvestedPage(**p) for p in d.pop("pages", [])]
        return cls(pages=pages, **d)

    # --- what the analyst actually reads ---------------------------------

    def as_briefing(self) -> str:
        """The dossier as one readable document, with a source URL per page."""
        parts = [
            f"# Public pages of {self.company} ({self.domain})",
            "",
            f"Harvested {self.harvested_at}. "
            f"{sum(1 for p in self.pages if p.ok and p.usable)} usable pages.",
            "",
        ]
        for i, p in enumerate([p for p in self.pages if p.ok and p.usable], 1):
            parts.append(f"--- PAGE {i} ---")
            parts.append(f"URL: {p.url}")
            parts.append(f"TITLE: {p.title}")
            parts.append(f"PAGE TYPE: {CATEGORIES.get(p.category, {}).get('label', p.category)}")
            if p.truncated:
                parts.append("(text truncated to the commercially relevant sections)")
            parts.append("")
            parts.append(p.text)
            parts.append("")
        unusable = [p for p in self.pages if p.ok and not p.usable]
        if unusable:
            parts.append("--- PAGES THAT RETURNED ALMOST NO READABLE TEXT ---")
            for p in unusable:
                parts.append(f"- {p.url} ({p.word_count} words; likely rendered in the browser)")
            parts.append("")
        if self.failures:
            parts.append("--- PAGES THAT COULD NOT BE FETCHED ---")
            for f in self.failures:
                parts.append(f"- {f['url']} ({f['reason']})")
            parts.append("")
        return "\n".join(parts)


# ------------------------------------------------------------------ rendering

def _clean(s: str) -> str:
    return " ".join((s or "").replace("\xa0", " ").split())


def _alive(tag: Tag) -> bool:
    """find_all() snapshots the tree, so a tag may already have been removed as
    part of an ancestor. Touching a decomposed tag raises."""
    return not getattr(tag, "decomposed", False) and tag.parent is not None


def _strip_chrome(soup: BeautifulSoup) -> None:
    for t in soup.find_all(list(DROP_TAGS)):
        if _alive(t):
            t.decompose()
    for t in soup.find_all(["nav", "header", "footer", "aside"]):
        if _alive(t):
            t.decompose()
    for t in soup.find_all(attrs={"role": True}):
        if _alive(t) and (t.get("role") or "").lower() in DROP_ROLES:
            t.decompose()
    for t in soup.find_all(attrs={"class": True}):
        if _alive(t) and DROP_CLASS_RE.search(" ".join(t.get("class") or [])):
            t.decompose()
    for t in soup.find_all(attrs={"aria-hidden": "true"}):
        if _alive(t):
            t.decompose()


def _render_table(table: Tag) -> list[str]:
    rows = []
    for tr in table.find_all("tr"):
        cells = [_clean(c.get_text(" ", strip=True)) or "-"
                 for c in tr.find_all(["th", "td"])]
        if any(c != "-" for c in cells):
            rows.append("| " + " | ".join(cells) + " |")
    return rows if len(rows) >= 2 else []


def html_to_text(html: str) -> tuple[str, str]:
    """Render a page as compact Markdown-ish text. Returns (title, text)."""
    soup = BeautifulSoup(html, "lxml")
    title = ""
    if soup.title and soup.title.string:
        title = _clean(soup.title.string)[:150]
    _strip_chrome(soup)
    if not title:
        h1 = soup.find("h1")
        title = _clean(h1.get_text(" ", strip=True))[:150] if h1 else ""

    lines: list[str] = []
    seen: set[str] = set()

    def emit(line: str) -> None:
        key = line.strip().lower()
        if not key:
            return
        # De-duplicate repeated prose (nav echoes, repeated CTAs) but never
        # short values: a comparison grid built from divs legitimately repeats
        # "1", "2", "Unlimited" down its columns, and dropping the repeats
        # silently destroys the table.
        if len(key) > 24 and not key.startswith("|"):
            if key in seen:
                return
            seen.add(key)
        lines.append(line)

    handled: set[int] = set()
    for table in soup.find_all("table"):
        for row in _render_table(table):
            emit(row)
        for d in table.descendants:
            if isinstance(d, Tag):
                handled.add(id(d))
        handled.add(id(table))

    block_tags = ["h1", "h2", "h3", "h4", "h5", "h6", "li", "p", "dt", "dd",
                  "blockquote", "figcaption", "div", "section", "article", "td", "th"]
    for el in soup.find_all(block_tags):
        if id(el) in handled:
            continue
        if any(isinstance(c, Tag) and c.name in block_tags and c.get_text(strip=True)
               for c in el.descendants if isinstance(c, Tag)):
            continue  # not a leaf; its children will be emitted
        txt = _clean(el.get_text(" ", strip=True))
        if not txt or len(txt) > 900:
            continue
        if el.name.startswith("h") and len(el.name) == 2:
            emit("")
            emit("## " + txt)
        elif el.name == "li":
            emit("- " + txt)
        else:
            emit(txt)
    return title, "\n".join(lines).strip()


def _trim_to_commercial(text: str, budget: int) -> tuple[str, bool]:
    """Keep the sections that talk about money, plans and limits."""
    if len(text) <= budget:
        return text, False
    lines = text.split("\n")
    keep = [False] * len(lines)
    for i, ln in enumerate(lines):
        if COMMERCIAL_RE.search(ln):
            # keep a little context either side so the section still reads
            for j in range(max(0, i - 2), min(len(lines), i + 3)):
                keep[j] = True
        if ln.startswith("## "):
            keep[i] = True
    out: list[str] = []
    total = 0
    gap = False
    for ln, k in zip(lines, keep):
        if not k:
            gap = True
            continue
        if gap and out:
            out.append("[...]")
            total += 6
        gap = False
        out.append(ln)
        total += len(ln) + 1
        if total >= budget:
            out.append("[... truncated ...]")
            break
    return "\n".join(out), True


# -------------------------------------------------------------------- harvest

def harvest(
    root_url: str,
    company: str | None = None,
    max_pages: int = 16,
    extra_urls: list[str] | None = None,
    fetcher: Fetcher | None = None,
    page_budget: int = MAX_CHARS_PER_PAGE,
    dossier_budget: int = MAX_CHARS_PER_DOSSIER,
    verbose: bool = True,
) -> Dossier:
    started = time.time()
    own = fetcher is None
    fetcher = fetcher or Fetcher()
    root = canonical_url(root_url if "://" in root_url else "https://" + root_url)
    domain = registered_domain(root)
    dossier = Dossier(
        company=company or domain, root_url=root, domain=domain,
        harvested_at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(started)),
    )
    try:
        disc = discover(fetcher, root, max_pages=max_pages, extra_urls=extra_urls)
        dossier.discovery_notes = disc.notes
        dossier.pricing_urls = disc.pricing_urls

        queue = list(disc.selected)
        reserve = list(disc.backup)
        seen: set[str] = set()
        spent = 0
        while queue:
            cand = queue.pop(0)
            if cand.url in seen:
                continue
            seen.add(cand.url)
            res = fetcher.get(cand.url)
            if not res.ok:
                dossier.failures.append({"url": cand.url, "category": cand.category,
                                         "reason": res.error or f"HTTP {res.status}"})
                while reserve:
                    nxt = reserve.pop(0)
                    if nxt.url not in seen:
                        queue.append(nxt)
                        break
                continue
            title, text = html_to_text(res.html)
            words = len(text.split())
            # Pricing pages get the biggest share of the budget.
            budget = page_budget * 2 if cand.category in ("pricing", "compare") else page_budget
            budget = min(budget, max(1200, dossier_budget - spent))
            text, truncated = _trim_to_commercial(text, budget)
            spent += len(text)
            page = HarvestedPage(
                url=cand.url, final_url=res.final_url, title=title or cand.url,
                category=cand.category, why_selected=cand.reason,
                discovered_via=cand.source, ok=True, error="", rendered=res.rendered,
                word_count=words, text=text, truncated=truncated,
                usable=words >= MIN_USABLE_WORDS,
            )
            dossier.pages.append(page)
            if verbose:
                flag = "" if page.usable else "  (too little text, client-rendered?)"
                print(f"  [{cand.category:12}] {words:5} words  {cand.url}{flag}")
            if spent >= dossier_budget:
                dossier.discovery_notes.append(
                    f"dossier size budget reached after {len(dossier.pages)} pages")
                break

        usable = [p for p in dossier.pages if p.usable]
        dossier.stats = {
            "pages_selected": len(disc.selected),
            "pages_fetched_ok": len(dossier.pages),
            "pages_usable": len(usable),
            "pages_failed": len(dossier.failures),
            "pages_js_rendered": sum(1 for p in dossier.pages if p.rendered),
            "urls_considered": disc.considered,
            "dossier_chars": sum(len(p.text) for p in usable),
            "harvest_seconds": round(time.time() - started, 1),
            "fetcher": dict(fetcher.stats),
        }
    finally:
        if own:
            fetcher.close()
    return dossier
