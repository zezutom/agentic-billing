"""Extract structured commercial claims from a fetched page.

Everything produced here is anchored to a literal quote from the page, so a
finding can always be shown to the reader with its own words as evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from bs4 import BeautifulSoup, NavigableString, Tag

from .claims import (
    KNOWN_PLAN_WORDS, Claim, normalise_metric, normalise_plan,
)

BLOCK_TAGS = {
    "p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "div", "section",
    "article", "figcaption", "dd", "dt", "blockquote", "summary", "label", "caption",
}
DROP_TAGS = {"script", "style", "noscript", "svg", "iframe", "template", "head"}

CURRENCY = {"$": "USD", "€": "EUR", "£": "GBP", "usd": "USD", "eur": "EUR", "gbp": "GBP",
            "us$": "USD", "a$": "AUD", "c$": "CAD", "₹": "INR", "¥": "JPY"}

PRICE_RE = re.compile(
    r"(?P<sym>[$€£₹¥]|\bUSD\b|\bEUR\b|\bGBP\b|\bAUD\b|\bCAD\b)\s?"
    r"(?P<amt>\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?|\d+(?:\.\d{1,2})?)",
    re.I,
)
PERIOD_PATTERNS = [
    (re.compile(r"/\s*mo\b|/\s*month|per\s+month|a\s+month|monthly|/\s*m\b", re.I), "month"),
    (re.compile(r"/\s*yr\b|/\s*year|per\s+year|a\s+year|annually|/\s*annum|yearly|/\s*y\b", re.I), "year"),
    (re.compile(r"one[- ]time|once|lifetime|forever(?!\s+free)", re.I), "one_time"),
]
PER_SEAT_RE = re.compile(
    r"per\s+(?:user|seat|member|editor|agent|person|host|contributor)|/\s*(?:user|seat|member)\b",
    re.I,
)
BILLED_ANNUALLY_RE = re.compile(r"billed\s+(?:annually|yearly|per\s+year)|paid\s+(?:annually|yearly)"
                                r"|annual(?:ly)?\s+billing|when\s+billed\s+annually", re.I)
BILLED_MONTHLY_RE = re.compile(r"billed\s+monthly|paid\s+monthly|monthly\s+billing", re.I)
SAVE_PCT_RE = re.compile(r"sav(?:e|ing[s]?)\s+(?:up\s+to\s+)?(\d{1,2})\s*%|(\d{1,2})\s*%\s+(?:off|discount|cheaper)", re.I)

TRIAL_RES = [
    re.compile(r"(\d{1,3})[\s-]*(?:calendar\s+)?day[s]?[\s-]*(?:free[\s-]*)?trial", re.I),
    re.compile(r"free\s+trial\s+(?:of|for|lasts?|runs?\s+for)?\s*(\d{1,3})\s*days?", re.I),
    re.compile(r"trial\s+(?:period\s+)?(?:is|lasts?|of)\s+(\d{1,3})\s*days?", re.I),
    re.compile(r"try\s+(?:it\s+)?(?:free\s+)?for\s+(\d{1,3})\s*days?", re.I),
    re.compile(r"(\d{1,3})\s*days?\s+(?:for\s+)?free\b", re.I),
    re.compile(r"free\s+for\s+(\d{1,3})\s*days?", re.I),
]
TRIAL_EXCLUDE_RE = re.compile(
    r"money[\s-]?back|refund|guarantee|retention|retain|history|log[s]?\b|backup|archive|"
    r"notice\s+period|cancel(?:lation)?\s+(?:within|policy)|delet|grace\s+period|expire[sd]?\s+after",
    re.I,
)
TRIAL_NO_LENGTH_RE = re.compile(r"free\s+trial|start\s+(?:your|a)\s+free|try\s+(?:it\s+)?free", re.I)
TRIAL_NO_CARD_RE = re.compile(r"no\s+credit\s+card(?:\s+required)?|without\s+a\s+credit\s+card", re.I)
CARD_REQUIRED_RE = re.compile(
    r"(?<!no\s)(?<!without\s)(?<!not\s)\b(?:a\s+)?credit\s+card\s+(?:is\s+)?required"
    r"|requires?\s+a\s+(?:valid\s+)?credit\s+card"
    r"|payment\s+(?:details|method|information)\s+(?:is|are)?\s*required", re.I)

UNLIMITED_RE = re.compile(
    r"\bunlimited\s+(?P<what>[a-z][a-z0-9\- ]{2,40}?)(?=[,.;:!)]|\s+(?:on|for|in|with|and|per|to|are|is|that|which|when|but)\b|$)",
    re.I,
)
NUMBER = r"(?P<num>\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)"
# A bare "<number> <noun>" is only an allowance if the sentence is shaped like
# one. Without this, "Shopware 6 with custom events" becomes "6 events".
ALLOWANCE_CUE_RE = re.compile(
    r"\bup\s+to\b|\bincluded?\b|\bincludes\b|\blimit(?:ed|s)?\b|\bmaximum\b|\bmax\.?\b"
    r"|\ballowance\b|\bquota\b|\bper\s+month\b|/\s*month\b|/\s*mo\b|\ba\s+month\b"
    r"|\bmonthly\b|\bcapped\b|\bstarting\s+at\b|\beach\s+month\b|\bat\s+most\b", re.I)
LEADING_STOPWORD_RE = re.compile(
    r"^(?:with|and|or|for|of|to|in|on|at|by|from|that|which|the|a|an|is|are|was|were|"
    r"times|more|less|other|such)\b", re.I)

QUANTITY_RES = [
    re.compile(rf"\bup\s+to\s+{NUMBER}\s*(?P<unit>[a-zA-Z]{{0,3}})\s*(?P<what>[a-z][a-z\- ]{{2,32}})", re.I),
    re.compile(rf"\b(?:maximum|max\.?|limit|limited|capped)\s+(?:of\s+|to\s+|is\s+)?{NUMBER}\s*(?P<unit>[a-zA-Z]{{0,3}})\s*(?P<what>[a-z][a-z\- ]{{2,32}})", re.I),
    re.compile(rf"\b{NUMBER}\s*(?P<unit>GB|TB|MB|K|k|M)?\s+(?P<what>[a-z][a-z\- ]{{2,32}})\b", re.I),
]
RATE_LIMIT_RE = re.compile(
    rf"{NUMBER}\s*(?P<what>[a-z][a-z\- ]{{2,30}}?)\s*(?:per|/|a)\s*(?P<window>second|sec|minute|min|hour|day)\b",
    re.I,
)
RETENTION_RE = re.compile(
    r"(?P<num>\d{1,4})[\s-]*(?P<unit>day|days|month|months|year|years)\s+(?:of\s+)?"
    r"(?P<what>data\s+retention|retention|history|log\s+retention|version\s+history|activity\s+(?:log|history)|backup)",
    re.I,
)

ENTITLEMENT_RES = [
    re.compile(r"(?:is\s+)?(?:only\s+)?available\s+(?:on|to|for|with|in)\s+(?:the\s+)?(?P<plan>[A-Z][A-Za-z+ ]{1,20}?)\s+(?:plan|tier|edition|and\s+above|customers|subscribers)", re.I),
    re.compile(r"requires?\s+(?:a\s+|the\s+|an\s+)?(?P<plan>[A-Z][A-Za-z+ ]{1,20}?)\s+(?:plan|tier|edition|subscription)", re.I),
    re.compile(r"included\s+(?:in|with)\s+(?:the\s+|all\s+)?(?P<plan>[A-Z][A-Za-z+ ]{1,20}?)\s+(?:plan|tier|edition)", re.I),
    re.compile(r"\b(?P<plan>[A-Z][A-Za-z+]{2,18})\s+plan\s+(?:and\s+above|or\s+higher|and\s+higher|only)", re.I),
    re.compile(r"\bonly\s+(?:on|in|for)\s+(?:the\s+)?(?P<plan>[A-Z][A-Za-z+ ]{1,20}?)\s+(?:plan|tier|edition)", re.I),
    re.compile(r"\b(?P<plan>Enterprise|Business|Pro|Professional|Premium|Team|Growth|Scale|Plus|Advanced)[- ]only\b", re.I),
    re.compile(r"upgrade\s+to\s+(?:the\s+|a\s+)?(?P<plan>[A-Z][A-Za-z+ ]{1,20}?)\s+(?:plan|tier|edition)", re.I),
]
PLAN_MENTION_RE = re.compile(r"\b(?P<plan>[A-Z][A-Za-z+]{2,18})\s+(?:plan|tier|edition)\b")
# Gating language that never names an actual tier.
VAGUE_GATE_RE = re.compile(
    r"(?:available\s+(?:on|to|for|with)|requires?|included\s+(?:in|with)|only\s+(?:on|for|in)|"
    r"upgrade\s+to|reserved\s+for)\s+(?:a\s+|an\s+|our\s+|the\s+|any\s+)?"
    r"(?P<gate>paid|premium|higher|upgraded|advanced|certain|selected|eligible|some)\s+"
    r"(?:plans?|tiers?|subscriptions?|accounts?)", re.I)

CONTACT_SALES_RE = re.compile(r"contact\s+(?:us|sales|our\s+sales)|talk\s+to\s+(?:us|sales)|"
                              r"get\s+(?:a\s+)?(?:custom\s+)?quote|request\s+(?:a\s+)?(?:demo|quote|pricing)|"
                              r"let'?s\s+talk|custom\s+pricing|book\s+a\s+(?:call|demo)", re.I)
FAIR_USE_RE = re.compile(r"fair\s+use|fair\s+usage|acceptable\s+use|reasonable\s+use|"
                         r"subject\s+to\s+(?:a\s+)?(?:fair|reasonable|acceptable)", re.I)
OVERAGE_RE = re.compile(r"overage|over[\s-]?limit|additional\s+(?:usage\s+)?(?:is\s+)?(?:billed|charged)|"
                        r"exceed[s]?\s+(?:your|the)\s+(?:limit|quota|allowance)|"
                        r"charged?\s+(?:\$|€|£)?[\d.]+\s*(?:per|for\s+each)|extra\s+charge", re.I)
SEAT_MINIMUM_RE = re.compile(r"minimum\s+of\s+(\d{1,3})\s*(?:seats?|users?|licen[cs]es?)|"
                             r"(\d{1,3})[\s-]*(?:seat|user|licen[cs]e)\s+minimum|"
                             r"starts?\s+at\s+(\d{1,3})\s+(?:seats?|users?)", re.I)
AUTO_RENEW_RE = re.compile(r"automatically\s+renew|auto[\s-]?renew|renews?\s+automatically", re.I)
NO_REFUND_RE = re.compile(r"no\s+refunds?|non[\s-]?refundable|not\s+refundable|"
                          r"do\s+not\s+(?:offer|provide|issue)\s+refunds?", re.I)
PRICE_CHANGE_RE = re.compile(r"(?:may|can|reserve[s]?\s+the\s+right\s+to)\s+(?:change|modify|adjust|increase)\s+"
                             r"(?:the\s+|our\s+)?(?:pricing|prices|fees|rates)", re.I)

CHECK_MARK_RE = re.compile(r"^\s*(?:✓|✔|✅|●|•|yes|included|included\.|available|✔️|check|true)\s*$", re.I)
CROSS_MARK_RE = re.compile(r"^\s*(?:—|-|–|✗|✕|❌|×|no|not\s+included|n/?a|unavailable|false)\s*$", re.I)


@dataclass
class PageDoc:
    url: str
    title: str
    category: str
    segments: list[str] = field(default_factory=list)
    text: str = ""
    plan_cards: list[dict] = field(default_factory=list)
    tables: list[dict] = field(default_factory=list)
    word_count: int = 0
    rendered: bool = False


# ---------------------------------------------------------------- page parse

def _clean_text(s: str) -> str:
    return " ".join((s or "").replace("\xa0", " ").split())


_PHRASE_CUT_RE = re.compile(r"\s+(?:per|for|on|in|with|and|of|to|at|are|is|that|which)\b.*$", re.I)


def _trim_phrase(s: str, max_words: int = 4) -> str:
    """Noun-phrase captures run on; keep the head of the phrase only."""
    s = _PHRASE_CUT_RE.sub("", _clean_text(s)).strip(" ,.;:-")
    return " ".join(s.split()[:max_words])


def _leaf_blocks(soup: BeautifulSoup) -> list[str]:
    """Text of block elements that contain no nested block element with text.

    This keeps naturally-adjacent things together ('$29 /month') without
    duplicating the same sentence at every level of the DOM.
    """
    out: list[str] = []
    for el in soup.find_all(BLOCK_TAGS):
        has_block_child = any(
            isinstance(c, Tag) and c.name in BLOCK_TAGS and c.get_text(strip=True)
            for c in el.descendants if isinstance(c, Tag)
        )
        if has_block_child:
            continue
        txt = _clean_text(el.get_text(" ", strip=True))
        if txt and 1 < len(txt) < 700:
            out.append(txt)
    # De-duplicate while preserving order.
    seen: set[str] = set()
    uniq = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _plan_name_in(el: Tag) -> str | None:
    """Find the tier name inside a pricing card."""
    candidates: list[str] = []
    for h in el.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        candidates.append(_clean_text(h.get_text(" ", strip=True)))
    for c in el.find_all(attrs={"class": True}):
        cls = " ".join(c.get("class") or []).lower()
        if any(k in cls for k in ("plan-name", "plan_title", "tier-name", "tier__name",
                                  "pricing-title", "card-title", "plan-title", "package-name")):
            candidates.append(_clean_text(c.get_text(" ", strip=True)))
    scored: list[tuple[int, str]] = []
    for c in candidates:
        if not c or len(c) > 32 or PRICE_RE.search(c):
            continue
        words = c.split()
        if len(words) > 4:
            continue
        low = c.lower().replace("plan", "").strip()
        if any(w.strip(".,:") in KNOWN_PLAN_WORDS for w in low.split()):
            scored.append((0, c))
        elif c[:1].isupper():
            scored.append((1, c))
    if not scored:
        return None
    scored.sort(key=lambda t: (t[0], len(t[1])))
    return scored[0][1]


def _extract_plan_cards(soup: BeautifulSoup) -> list[dict]:
    """Locate pricing cards by climbing from each price to its smallest
    ancestor that also names a plan."""
    cards: list[dict] = []
    seen_ids: set[int] = set()
    price_nodes = []
    for node in soup.find_all(string=PRICE_RE):
        if isinstance(node, NavigableString) and node.parent is not None:
            price_nodes.append(node.parent)
    for start in price_nodes:
        el: Tag | None = start
        card: Tag | None = None
        for _ in range(9):
            if el is None or not isinstance(el, Tag):
                break
            txt = _clean_text(el.get_text(" ", strip=True))
            if len(txt) > 2600:
                break
            if len(txt) >= 25 and _plan_name_in(el):
                card = el
                break
            el = el.parent
        if card is None or id(card) in seen_ids:
            continue
        seen_ids.add(id(card))
        text = _clean_text(card.get_text(" ", strip=True))
        name = _plan_name_in(card)
        prices = []
        for m in PRICE_RE.finditer(text):
            window = text[max(0, m.start() - 60): m.end() + 90]
            prices.append({
                "raw": m.group(0),
                "currency": CURRENCY.get(m.group("sym").lower(), m.group("sym").upper()),
                "amount": float(m.group("amt").replace(",", "")),
                "context": window,
            })
        bullets = [_clean_text(li.get_text(" ", strip=True)) for li in card.find_all("li")]
        bullets = [b for b in bullets if 2 < len(b) < 160]
        cards.append({"plan_raw": name, "text": text, "prices": prices, "bullets": bullets})
    # Drop cards nested inside a bigger card we already captured.
    cards = [c for c in cards if c["plan_raw"]]
    deduped: list[dict] = []
    for c in sorted(cards, key=lambda c: len(c["text"])):
        if any(c["text"] in d["text"] for d in deduped):
            continue
        deduped.append(c)
    return deduped


def _extract_tables(soup: BeautifulSoup) -> list[dict]:
    """Plan-comparison tables: header row of plan names, one feature per row."""
    out = []
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if len(rows) < 2:
            continue
        header_cells = [_clean_text(c.get_text(" ", strip=True)) for c in rows[0].find_all(["th", "td"])]
        if len(header_cells) < 2:
            continue
        plan_cols: dict[int, str] = {}
        for i, h in enumerate(header_cells):
            if i == 0:
                continue
            n = normalise_plan(h)
            if n and (n in KNOWN_PLAN_WORDS or any(w in KNOWN_PLAN_WORDS for w in n.split())):
                plan_cols[i] = h
        if len(plan_cols) < 2:
            continue
        body = []
        for r in rows[1:]:
            cells = [_clean_text(c.get_text(" ", strip=True)) for c in r.find_all(["th", "td"])]
            if len(cells) < 2 or not cells[0]:
                continue
            body.append(cells)
        if body:
            out.append({"plan_cols": plan_cols, "rows": body, "header": header_cells})
    return out


def _accept_cards(cards: list[dict], category: str) -> list[dict]:
    """A heading next to a price is only a plan card if it names a tier.

    Without this, a docs page titled 'Usage limits' that quotes '$0.01 per call'
    becomes a 'Usage limits plan' and mis-scopes every claim on the page.
    """
    def names_a_tier(name: str | None) -> bool:
        n = normalise_plan(name)
        return bool(n) and any(w in KNOWN_PLAN_WORDS for w in n.split())

    known = [c for c in cards if names_a_tier(c["plan_raw"])]
    if category in ("pricing", "compare"):
        priced = [c for c in cards if c["prices"]]
        # A real pricing grid has several priced cards; trust it even with
        # unconventional tier names ("Hobby Rocket", "Ninja").
        if len(priced) >= 3 and len(known) < len(priced):
            return priced
        return known or priced[:0]
    return known


def parse_page(html: str, url: str, category: str, rendered: bool = False) -> PageDoc:
    soup = BeautifulSoup(html, "lxml")
    for t in soup.find_all(list(DROP_TAGS)):
        t.decompose()
    title = ""
    if soup.title and soup.title.string:
        title = _clean_text(soup.title.string)[:140]
    if not title:
        h1 = soup.find("h1")
        title = _clean_text(h1.get_text(" ", strip=True))[:140] if h1 else url
    segments = _leaf_blocks(soup)
    doc = PageDoc(
        url=url, title=title, category=category, segments=segments,
        text=" \n".join(segments),
        plan_cards=_accept_cards(_extract_plan_cards(soup), category),
        tables=_extract_tables(soup), rendered=rendered,
    )
    doc.word_count = len(doc.text.split())
    return doc


# ------------------------------------------------------------ claim builders

def _period_of(context: str) -> tuple[str, bool]:
    for rx, name in PERIOD_PATTERNS:
        if rx.search(context):
            return name, bool(PER_SEAT_RE.search(context))
    return "unknown", bool(PER_SEAT_RE.search(context))


def _claim(doc: PageDoc, kind: str, evidence: str, extractor: str,
           plan_raw: str | None = None, **data) -> Claim:
    return Claim(
        kind=kind, page_url=doc.url, page_title=doc.title, page_category=doc.category,
        evidence=_clean_text(evidence)[:400], plan=normalise_plan(plan_raw),
        plan_raw=_clean_text(plan_raw) if plan_raw else None, data=data, extractor=extractor,
    )


def extract_prices(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    for card in doc.plan_cards:
        for price in card["prices"]:
            ctx = price["context"]
            period, per_seat = _period_of(ctx)
            if period == "unknown":
                period, per_seat2 = _period_of(card["text"][:400])
                per_seat = per_seat or per_seat2
            annual_commit = bool(BILLED_ANNUALLY_RE.search(ctx) or BILLED_ANNUALLY_RE.search(card["text"]))
            monthly_commit = bool(BILLED_MONTHLY_RE.search(ctx))
            # A "save 20%" badge or a struck-through price is not the plan price.
            if re.search(r"sav(?:e|ings)|discount|%\s*off", ctx, re.I) and price["amount"] < 100:
                if re.search(r"\d\s*%", ctx):
                    continue
            claims.append(_claim(
                doc, "plan_price", ctx, "pricing_card", plan_raw=card["plan_raw"],
                amount=price["amount"], currency=price["currency"], period=period,
                per_seat=per_seat, billed_annually=annual_commit, billed_monthly=monthly_commit,
                raw=price["raw"],
            ))
        if not card["prices"] and CONTACT_SALES_RE.search(card["text"]):
            claims.append(_claim(doc, "plan_price", card["text"][:300], "pricing_card_contact_sales",
                                 plan_raw=card["plan_raw"], amount=None, currency=None,
                                 period="unknown", contact_sales=True))
    return claims


def extract_trials(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[tuple[int, str]] = set()
    for seg in doc.segments:
        if TRIAL_EXCLUDE_RE.search(seg):
            continue
        if "trial" not in seg.lower() and "free for" not in seg.lower() and "days free" not in seg.lower():
            continue
        for rx in TRIAL_RES:
            m = rx.search(seg)
            if not m:
                continue
            days = int(m.group(1))
            if not (1 <= days <= 365):
                continue
            lower = seg.lower()
            near = lower[max(0, m.start() - 60): m.end() + 60]
            if "trial" not in near and "free" not in near:
                continue
            plan = None
            pm = PLAN_MENTION_RE.search(seg)
            if pm:
                plan = pm.group("plan")
            key = (days, plan or "")
            if key in seen:
                break
            seen.add(key)
            no_card = bool(TRIAL_NO_CARD_RE.search(seg))
            claims.append(_claim(doc, "trial", seg, "trial_length", plan_raw=plan, days=days,
                                 card_required=bool(CARD_REQUIRED_RE.search(seg)) and not no_card,
                                 no_card=no_card))
            break
    if not claims:
        for seg in doc.segments:
            if TRIAL_NO_LENGTH_RE.search(seg) and not TRIAL_EXCLUDE_RE.search(seg):
                claims.append(_claim(doc, "trial", seg, "trial_unspecified", days=None))
                break
    for seg in doc.segments:
        low = seg.lower()
        if "trial" not in low and "sign up" not in low and "get started" not in low:
            continue
        no_card = bool(TRIAL_NO_CARD_RE.search(seg))
        card_req = bool(CARD_REQUIRED_RE.search(seg)) and not no_card
        if no_card:
            claims.append(_claim(doc, "trial", seg, "trial_no_card", days=None, no_card=True))
            break
        if card_req:
            claims.append(_claim(doc, "trial", seg, "trial_card_required", days=None,
                                 card_required=True))
            break
    return claims


def _plan_for_segment(doc: PageDoc, seg: str) -> str | None:
    for card in doc.plan_cards:
        if seg in card["text"] and card["plan_raw"]:
            return card["plan_raw"]
    m = PLAN_MENTION_RE.search(seg)
    if m:
        return m.group("plan")
    return None


def extract_unlimited(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[tuple[str, str]] = set()
    for seg in doc.segments:
        if "unlimited" not in seg.lower():
            continue
        for m in UNLIMITED_RE.finditer(seg):
            what = _trim_phrase(m.group("what"))
            if not what:
                continue
            metric = normalise_metric(what)
            plan = _plan_for_segment(doc, seg)
            key = (metric or what.lower(), normalise_plan(plan) or "")
            if key in seen:
                continue
            seen.add(key)
            claims.append(_claim(doc, "unlimited", seg, "unlimited_phrase", plan_raw=plan,
                                 subject=what, metric=metric))
    # Comparison tables often say "Unlimited" in a cell for a named plan.
    for table in doc.tables:
        for row in table["rows"]:
            feature = row[0]
            metric = normalise_metric(feature)
            for idx, plan_raw in table["plan_cols"].items():
                if idx < len(row) and re.fullmatch(r"\s*unlimited\s*", row[idx], re.I):
                    key = (metric or feature.lower(), normalise_plan(plan_raw) or "")
                    if key in seen:
                        continue
                    seen.add(key)
                    claims.append(_claim(
                        doc, "unlimited", f"{feature}: Unlimited ({plan_raw} plan)",
                        "unlimited_table", plan_raw=plan_raw, subject=feature, metric=metric))
    return claims


def _is_price_context(seg: str, pos: int) -> bool:
    return bool(PRICE_RE.search(seg[max(0, pos - 12):pos + 4]))


def extract_limits(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[tuple] = set()

    def add(seg, plan_raw, metric, value, unit, limit_kind, subject, extractor, window=None):
        key = (metric, value, unit, normalise_plan(plan_raw) or "", limit_kind)
        if key in seen:
            return
        seen.add(key)
        claims.append(_claim(doc, "limit", seg, extractor, plan_raw=plan_raw, metric=metric,
                             value=value, unit=unit, limit_kind=limit_kind, subject=subject,
                             window=window))

    for seg in doc.segments:
        plan = _plan_for_segment(doc, seg)
        consumed: list[tuple[int, int]] = []

        for m in RATE_LIMIT_RE.finditer(seg):
            what = _trim_phrase(m.group("what"))
            metric = normalise_metric(what)
            if _is_price_context(seg, m.start()):
                continue
            consumed.append((m.start(), m.end()))
            if not metric:
                continue
            add(seg, plan, metric, float(m.group("num").replace(",", "")), "count",
                "rate", what, "rate_limit", window=m.group("window").lower())

        for m in RETENTION_RE.finditer(seg):
            consumed.append((m.start(), m.end()))
            add(seg, plan, "retention", float(m.group("num")), m.group("unit").lower().rstrip("s"),
                "quantity", _clean_text(m.group("what")), "retention_limit")

        has_cue = bool(ALLOWANCE_CUE_RE.search(seg))
        for rx_idx, rx in enumerate(QUANTITY_RES):
            for m in rx.finditer(seg):
                raw_what = m.group("what")
                if LEADING_STOPWORD_RE.match(raw_what.strip()):
                    continue
                what = _trim_phrase(raw_what)
                metric = normalise_metric(what)
                if not metric:
                    continue
                if rx_idx == 2:
                    # The bare "<n> <noun>" pattern needs the sentence to look
                    # like an allowance: a cue word, a short bullet, or the
                    # number leading the line ("3 sites", "10 GB storage").
                    bullet_like = len(seg) <= 90
                    leads = m.start("num") <= 2
                    if not (has_cue or bullet_like or leads):
                        continue
                    if len(seg) > 320 and not leads:
                        continue
                if _is_price_context(seg, m.start()):
                    continue
                if any(a <= m.start("num") < b for a, b in consumed):
                    continue  # already captured as a rate limit
                unit = (m.groupdict().get("unit") or "").strip()
                value = float(m.group("num").replace(",", ""))
                if unit.upper() in ("GB", "TB", "MB"):
                    metric, unit = "storage", unit.upper()
                elif unit.lower() == "k":
                    value, unit = value * 1000, "count"
                elif unit.upper() == "M" and metric != "minutes":
                    value, unit = value * 1_000_000, "count"
                else:
                    unit = "count"
                if value <= 0 or value > 5_000_000_000:
                    continue
                add(seg, plan, metric, value, unit, "quantity", what, rx.pattern[:24])
                break

    for table in doc.tables:
        for row in table["rows"]:
            feature = row[0]
            metric = normalise_metric(feature)
            if not metric:
                continue
            for idx, plan_raw in table["plan_cols"].items():
                if idx >= len(row):
                    continue
                cell = row[idx]
                m = re.fullmatch(r"\s*(\d{1,3}(?:,\d{3})*|\d+)\s*(GB|TB|MB|k|K|M)?\s*[a-z ]{0,14}\s*", cell, re.I)
                if not m:
                    continue
                value = float(m.group(1).replace(",", ""))
                unit = (m.group(2) or "count").upper()
                if unit in ("GB", "TB", "MB"):
                    metric = "storage"
                elif unit == "K":
                    value, unit = value * 1000, "count"
                elif unit == "M":
                    value, unit = value * 1_000_000, "count"
                else:
                    unit = "count"
                add(f"{feature}: {cell} ({plan_raw} plan)", plan_raw, metric, value, unit,
                    "quantity", feature, "comparison_table")
    return claims


def extract_entitlements(doc: PageDoc) -> list[Claim]:
    """Which plan a feature belongs to, from pricing cards, tables and prose."""
    claims: list[Claim] = []
    seen: set[tuple[str, str]] = set()

    def add(feature, plan_raw, evidence, extractor):
        feature = _clean_text(feature)
        if not feature or len(feature) < 4 or len(feature) > 120:
            return
        key = (feature.lower(), (normalise_plan(plan_raw) or ""))
        if key in seen:
            return
        seen.add(key)
        claims.append(_claim(doc, "entitlement", evidence, extractor, plan_raw=plan_raw,
                             feature=feature))

    for card in doc.plan_cards:
        if not card["plan_raw"]:
            continue
        for bullet in card["bullets"]:
            if PRICE_RE.search(bullet) and len(bullet) < 24:
                continue
            add(bullet, card["plan_raw"], f"{card['plan_raw']} plan includes: {bullet}", "pricing_card_bullet")

    for table in doc.tables:
        for row in table["rows"]:
            feature = row[0]
            for idx, plan_raw in table["plan_cols"].items():
                if idx < len(row) and CHECK_MARK_RE.match(row[idx]):
                    add(feature, plan_raw, f"{feature}: included in {plan_raw}", "comparison_table")

    for seg in doc.segments:
        vg = VAGUE_GATE_RE.search(seg)
        if vg:
            feature = re.sub(r"\s+(?:is|are|was|were|can|will|may)\s*$", "",
                             _clean_text(seg[:vg.start()])).rstrip(" ,.:;-")
            if 4 <= len(feature) <= 160:
                claims.append(_claim(doc, "entitlement", seg, "vague_gate", plan_raw=None,
                                     feature=feature[-140:], vague_gate=vg.group("gate").lower()))
        for rx in ENTITLEMENT_RES:
            m = rx.search(seg)
            if not m:
                continue
            plan_raw = _clean_text(m.group("plan"))
            if not normalise_plan(plan_raw):
                continue
            if normalise_plan(plan_raw) not in KNOWN_PLAN_WORDS and \
               not any(w in KNOWN_PLAN_WORDS for w in (normalise_plan(plan_raw) or "").split()):
                continue
            feature = re.sub(r"\s+(?:is|are|was|were|can|will|may)\s*$", "",
                             _clean_text(seg[:m.start()])).rstrip(" ,.:;-")
            if len(feature) < 4:
                feature = _clean_text(seg)[:120]
            add(feature[-120:], plan_raw, seg, "prose_entitlement")
            break
    return claims


def extract_plan_mentions(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[str] = set()
    for card in doc.plan_cards:
        n = normalise_plan(card["plan_raw"])
        if n and n not in seen:
            seen.add(n)
            claims.append(_claim(doc, "plan_mention", card["text"][:200], "pricing_card",
                                 plan_raw=card["plan_raw"], source="card"))
    for table in doc.tables:
        for plan_raw in table["plan_cols"].values():
            n = normalise_plan(plan_raw)
            if n and n not in seen:
                seen.add(n)
                claims.append(_claim(doc, "plan_mention", f"comparison table column '{plan_raw}'",
                                     "comparison_table", plan_raw=plan_raw, source="table"))
    for seg in doc.segments:
        for m in PLAN_MENTION_RE.finditer(seg):
            plan_raw = m.group("plan")
            n = normalise_plan(plan_raw)
            if not n or n in seen:
                continue
            if n not in KNOWN_PLAN_WORDS:
                continue
            seen.add(n)
            claims.append(_claim(doc, "plan_mention", seg, "prose_mention",
                                 plan_raw=plan_raw, source="prose"))
    return claims


def extract_addons(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[str] = set()
    ADDON_RE = re.compile(r"\badd[\s-]?on[s]?\b|\bextra\b|\bboost\b|\btop[\s-]?up\b", re.I)
    for seg in doc.segments:
        if not ADDON_RE.search(seg):
            continue
        m = PRICE_RE.search(seg)
        name = _clean_text(seg)[:100]
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        claims.append(_claim(doc, "addon", seg, "addon_mention", name=name,
                             amount=float(m.group("amt").replace(",", "")) if m else None,
                             currency=CURRENCY.get(m.group("sym").lower(), None) if m else None))
        if len(claims) >= 12:
            break
    return claims


CONDITION_RULES = [
    ("fair_use", FAIR_USE_RE, "a fair-use or acceptable-use restriction"),
    ("overage", OVERAGE_RE, "charges or cut-offs once an allowance is exceeded"),
    ("seat_minimum", SEAT_MINIMUM_RE, "a minimum number of seats"),
    ("auto_renew", AUTO_RENEW_RE, "automatic renewal"),
    ("no_refund", NO_REFUND_RE, "a no-refund policy"),
    ("price_change", PRICE_CHANGE_RE, "the right to change prices"),
    ("contact_sales", CONTACT_SALES_RE, "pricing only available by contacting sales"),
]


def extract_conditions(doc: PageDoc) -> list[Claim]:
    claims: list[Claim] = []
    seen: set[str] = set()
    for seg in doc.segments:
        for name, rx, desc in CONDITION_RULES:
            if name in seen:
                continue
            if rx.search(seg):
                seen.add(name)
                plan = _plan_for_segment(doc, seg)
                claims.append(_claim(doc, "condition", seg, f"condition_{name}", plan_raw=plan,
                                     condition=name, description=desc))
    return claims


EXTRACTORS = (
    extract_prices, extract_trials, extract_unlimited, extract_limits,
    extract_entitlements, extract_plan_mentions, extract_addons, extract_conditions,
)


def extract_claims(doc: PageDoc) -> list[Claim]:
    out: list[Claim] = []
    for fn in EXTRACTORS:
        try:
            out.extend(fn(doc))
        except Exception as exc:  # one bad page must not kill the audit
            out.append(_claim(doc, "extraction_error", f"{fn.__name__}: {exc}"[:200], "error"))
    return out
