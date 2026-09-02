"""Discovery: find a company's pricing page and the other pages that make
commercial promises, using sitemaps, navigation links and one hop of crawling."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from .fetcher import Fetcher, canonical_url, registered_domain

# Each category carries URL-path signals and anchor-text signals.
CATEGORIES: dict[str, dict] = {
    "pricing": {
        "label": "Pricing page",
        "weight": 100,
        "path": ["pricing", "prices", "plans", "plans-and-pricing", "pricing-plans", "buy", "subscribe"],
        "anchor": ["pricing", "plans", "price", "see pricing", "view plans"],
    },
    "compare": {
        "label": "Plan comparison",
        "weight": 70,
        "path": ["compare", "plan-comparison", "compare-plans", "editions", "which-plan", "feature-comparison"],
        "anchor": ["compare plans", "plan comparison", "compare editions", "which plan"],
    },
    "limits": {
        "label": "Usage limits / quotas",
        "weight": 85,
        "path": ["limits", "quota", "quotas", "rate-limit", "rate-limits", "usage", "usage-limits",
                 "fair-use", "fair-usage", "allowance", "credits", "seats", "overage"],
        "anchor": ["limits", "usage limits", "rate limits", "quotas", "fair use", "credits", "overage"],
    },
    "billing_docs": {
        "label": "Billing & subscription help",
        "weight": 90,
        "path": ["billing", "subscription", "subscriptions", "invoice", "invoices", "payment",
                 "manage-plan", "change-plan", "upgrade", "downgrade", "cancel", "refund"],
        "anchor": ["billing", "subscription", "manage your plan", "upgrade", "cancel", "refund"],
    },
    "trial": {
        "label": "Trial / signup",
        "weight": 80,
        "path": ["trial", "free-trial", "start-free", "signup", "sign-up", "get-started",
                 "register"],
        "anchor": ["free trial", "start free", "sign up", "get started", "try free"],
    },
    "addons": {
        "label": "Add-ons & integrations",
        "weight": 75,
        "path": ["add-on", "add-ons", "addon", "addons", "extras", "marketplace", "apps", "integrations"],
        "anchor": ["add-ons", "add ons", "extras", "integrations"],
    },
    "faq": {
        "label": "FAQ",
        "weight": 80,
        "path": ["faq", "faqs", "frequently-asked", "questions"],
        "anchor": ["faq", "faqs", "frequently asked questions"],
    },
    "help": {
        "label": "Help centre",
        "weight": 60,
        "path": ["help", "support", "knowledge-base", "kb", "hc", "articles", "guides"],
        "anchor": ["help", "help centre", "help center", "support", "knowledge base"],
    },
    "docs": {
        "label": "Product documentation",
        "weight": 55,
        "path": ["docs", "documentation", "developers", "developer", "api", "reference", "manual"],
        "anchor": ["docs", "documentation", "developers", "api reference"],
    },
    "terms": {
        "label": "Terms / legal",
        "weight": 45,
        "path": ["terms", "tos", "terms-of-service", "terms-and-conditions", "legal",
                 "service-agreement", "msa", "eula", "aup", "acceptable-use"],
        "anchor": ["terms", "terms of service", "legal", "acceptable use"],
    },
}

# Paths that never contain commercial promises but score highly by accident.
NEGATIVE_PATH = [
    "blog", "post", "posts", "article", "articles", "opinion", "essay", "news", "press", "careers", "jobs", "about", "team", "contact", "customers",
    "case-study", "case-studies", "story", "stories", "events", "webinar", "podcast",
    "changelog", "release-notes", "status", "security", "privacy", "cookie", "gdpr", "dpa",
    "login", "signin", "log-in", "sign-in", "auth", "account", "dashboard", "app",
    "author", "tag", "tags", "category", "categories", "search", "sitemap", "rss",
    "partners", "affiliate", "resources", "ebook", "template", "templates", "glossary",
    "alternatives", "vs", "comparison-to", "download", "roadmap", "community", "forum",
]

DOC_SUBDOMAINS = ("docs.", "help.", "support.", "developer.", "developers.", "api.",
                  "kb.", "learn.", "guide.", "guides.", "manual.", "knowledge.")

MAX_PAGES_DEFAULT = 16


@dataclass
class Candidate:
    url: str
    category: str
    score: float
    reason: str
    anchor: str = ""
    source: str = ""      # how we found it
    verified: bool = True  # False for conventional-path guesses that may 404


@dataclass
class DiscoveryResult:
    root: str
    domain: str
    pricing_urls: list[str] = field(default_factory=list)
    selected: list[Candidate] = field(default_factory=list)
    backup: list[Candidate] = field(default_factory=list)
    considered: int = 0
    notes: list[str] = field(default_factory=list)


def _path_tokens(url: str) -> list[str]:
    p = urlparse(url)
    raw = (p.path or "/").lower()
    return [t for t in re.split(r"[/\-_.]+", raw) if t]


def score_url(url: str, anchor: str, domain: str) -> tuple[str, float, str] | None:
    """Return (category, score, reason) for a URL, or None if it is not relevant."""
    p = urlparse(url)
    host = p.netloc.lower()
    if registered_domain(url) != domain:
        return None
    if p.scheme not in ("http", "https"):
        return None

    tokens = _path_tokens(url)
    path = (p.path or "/").lower()
    anchor_l = (anchor or "").strip().lower()[:120]
    depth = len([t for t in path.split("/") if t])

    best: tuple[str, float, str] | None = None
    for cat, spec in CATEGORIES.items():
        score = 0.0
        reasons = []
        for kw in spec["path"]:
            kw_tokens = kw.split("-")
            if all(t in tokens for t in kw_tokens):
                score += spec["weight"]
                reasons.append(f"url path contains '{kw}'")
                break
        for kw in spec["anchor"]:
            if anchor_l and kw in anchor_l:
                score += spec["weight"] * 0.45
                reasons.append(f"link text '{anchor_l[:40]}'")
                break
        if cat in ("docs", "help") and any(host.startswith(s) for s in DOC_SUBDOMAINS):
            score += 40
            reasons.append(f"documentation subdomain '{host}'")
        if score <= 0:
            continue
        # Shallow pages are the canonical ones; deep ones are usually long-tail articles.
        score -= min(depth, 6) * 4
        if best is None or score > best[1]:
            best = (cat, score, "; ".join(reasons))

    if best is None:
        return None

    cat, score, reason = best
    for neg in NEGATIVE_PATH:
        if neg in tokens:
            # A billing help article under /help/ is fine; a blog post is not.
            if neg in ("help", "support", "resources") and cat in ("billing_docs", "limits", "faq", "trial"):
                continue
            score -= 70
            reason += f"; penalised for '{neg}'"
            break
    if score <= 0:
        return None
    return cat, score, reason


def _links_from_html(html: str, base_url: str) -> list[tuple[str, str]]:
    soup = BeautifulSoup(html, "lxml")
    out = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        try:
            full = canonical_url(urljoin(base_url, href))
        except Exception:
            continue
        text = " ".join(a.get_text(" ", strip=True).split())[:120]
        out.append((full, text))
    return out


def _sitemap_urls(fetcher: Fetcher, root: str, limit: int = 4000) -> list[str]:
    urls: list[str] = []
    seen_maps: set[str] = set()
    queue = list(fetcher.sitemaps(root))[:5]
    while queue and len(urls) < limit:
        sm = queue.pop(0)
        if sm in seen_maps:
            continue
        seen_maps.add(sm)
        res = fetcher.get(sm, render_if_thin=False)
        if not res.ok or not res.html:
            continue
        locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", res.html, flags=re.I)
        if "<sitemapindex" in res.html[:2000].lower():
            # Prefer child sitemaps that look like they hold marketing/doc pages.
            ranked = sorted(locs, key=lambda u: (0 if re.search(
                r"page|pricing|docs|help|support|main|post", u, re.I) else 1, len(u)))
            queue.extend(ranked[:6])
        else:
            urls.extend(locs)
    return [canonical_url(u) for u in urls[:limit]]


def discover(
    fetcher: Fetcher,
    root_url: str,
    max_pages: int = MAX_PAGES_DEFAULT,
    extra_urls: list[str] | None = None,
) -> DiscoveryResult:
    """Find the pricing page plus the most relevant supporting pages."""
    root = canonical_url(root_url if "://" in root_url else "https://" + root_url)
    domain = registered_domain(root)
    result = DiscoveryResult(root=root, domain=domain)

    pool: dict[str, Candidate] = {}

    def offer(url: str, anchor: str, source: str, verified: bool = True) -> None:
        url = canonical_url(url)
        scored = score_url(url, anchor, domain)
        if scored is None:
            return
        cat, score, reason = scored
        if not verified:
            # An invented URL is worth less than one the site actually links to.
            score -= 30
            reason += " (guessed conventional path, not linked)"
        prev = pool.get(url)
        if prev is None or score > prev.score:
            pool[url] = Candidate(url=url, category=cat, score=score, reason=reason,
                                  anchor=anchor, source=source, verified=verified)

    # 1. Homepage navigation.
    home = fetcher.get(root)
    if home.ok:
        for url, text in _links_from_html(home.html, home.final_url):
            offer(url, text, "homepage navigation")
    else:
        result.notes.append(f"homepage fetch failed: {home.error}")

    # 2. Sitemap.
    sm_urls = _sitemap_urls(fetcher, root)
    if sm_urls:
        result.notes.append(f"sitemap supplied {len(sm_urls)} URLs")
    for url in sm_urls:
        offer(url, "", "sitemap")

    # 2b. Some companies put the pricing table on the homepage and link to an
    # anchor on it. The fragment is stripped during canonicalisation, so detect
    # it from the link text instead.
    if home.ok:
        for url, text in _links_from_html(home.html, home.final_url):
            if canonical_url(url) == root and re.search(r"\bpricing\b|\bplans\b", text, re.I):
                pool[root] = Candidate(
                    url=root, category="pricing", score=95,
                    reason=f"homepage carries the pricing section (nav link '{text[:30]}')",
                    anchor=text, source="homepage navigation")
                break

    # 3. Common conventional paths, in case navigation is JS-only.
    for guess in ("/pricing", "/plans", "/help", "/docs", "/faq", "/terms"):
        offer(urljoin(root + "/", guess.lstrip("/")), "", "conventional path guess",
              verified=False)

    result.considered = len(pool)

    # 4. The pricing page anchors the whole audit, so keep trying candidates
    # until one actually resolves rather than trusting the first guess.
    pricing = sorted([c for c in pool.values() if c.category == "pricing"],
                     key=lambda c: -c.score)
    attempts = 0
    for cand in pricing:
        if len(result.pricing_urls) >= 2 or attempts >= 5:
            break
        attempts += 1
        res = fetcher.get(cand.url)
        if not res.ok:
            pool.pop(cand.url, None)  # do not spend a slot on a dead guess
            continue
        result.pricing_urls.append(cand.url)
        for url, text in _links_from_html(res.html, res.final_url):
            offer(url, text, f"linked from pricing page {cand.url}")

    if not result.pricing_urls:
        result.notes.append("no pricing page identified from navigation, sitemap or conventional paths")

    # 4b. Documentation and help hubs are where limits and entitlements live,
    # so take one hop from the best hub as well.
    hubs = sorted([c for c in pool.values() if c.category in ("docs", "help", "faq")],
                  key=lambda c: -c.score)[:2]
    for cand in hubs:
        res = fetcher.get(cand.url)
        if not res.ok:
            pool.pop(cand.url, None)
            continue
        for url, text in _links_from_html(res.html, res.final_url):
            offer(url, text, f"linked from {cand.category} hub {cand.url}")

    # 5. Manually supplied URLs always win.
    forced: list[Candidate] = []
    for url in extra_urls or []:
        url = canonical_url(url)
        scored = score_url(url, "", domain)
        cat = scored[0] if scored else "manual"
        forced.append(Candidate(url=url, category=cat, score=999, reason="supplied manually",
                                source="user-supplied"))
        pool.pop(url, None)

    # 6. Select a spread across categories rather than 16 pages of docs.
    per_category_cap = {
        "pricing": 2, "compare": 2, "limits": 3, "billing_docs": 3, "trial": 2,
        "addons": 2, "faq": 2, "help": 3, "docs": 3, "terms": 2,
    }
    ranked = sorted(pool.values(), key=lambda c: -c.score)
    chosen: list[Candidate] = list(forced)
    counts: dict[str, int] = {}
    for cand in ranked:
        if len(chosen) >= max_pages:
            break
        if any(c.url == cand.url for c in chosen):
            continue
        if counts.get(cand.category, 0) >= per_category_cap.get(cand.category, 2):
            continue
        counts[cand.category] = counts.get(cand.category, 0) + 1
        chosen.append(cand)

    # Pricing pages always lead the list.
    chosen.sort(key=lambda c: (0 if c.category == "pricing" else 1, -c.score))
    result.selected = chosen
    chosen_urls = {c.url for c in chosen}
    result.backup = [c for c in ranked if c.url not in chosen_urls][:12]
    return result
