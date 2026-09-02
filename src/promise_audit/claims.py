"""Structured representation of a public commercial promise."""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Any

# --- plan vocabulary -------------------------------------------------------

KNOWN_PLAN_WORDS = {
    "free", "freemium", "trial", "starter", "start", "basic", "essential", "essentials",
    "standard", "lite", "light", "personal", "individual", "solo", "hobby", "core",
    "plus", "pro", "professional", "premium", "advanced", "team", "teams", "business",
    "growth", "scale", "company", "agency", "studio", "enterprise", "ultimate", "unlimited",
    "custom", "startup", "founder", "expert", "master", "elite", "max", "ultra", "launch",
    "creator", "developer", "cloud", "server", "gold", "silver", "bronze", "platinum",
}

# Names that are the same product tier written two ways.
PLAN_ALIASES = {
    "professional": "pro",
    "essentials": "essential",
    "teams": "team",
    "individuals": "individual",
    "businesses": "business",
    "startups": "startup",
    "premium plus": "premium",
    "free forever": "free",
    "freemium": "free",
}

PLAN_STOPWORDS = {"plan", "plans", "tier", "tiers", "edition", "package", "pricing", "the", "a"}


def normalise_plan(name: str | None) -> str | None:
    if not name:
        return None
    s = re.sub(r"[^a-z0-9+ ]+", " ", name.lower())
    s = " ".join(w for w in s.split() if w not in PLAN_STOPWORDS).strip()
    if not s or len(s) > 28:
        return None
    s = PLAN_ALIASES.get(s, s)
    if s.endswith("s") and s[:-1] in KNOWN_PLAN_WORDS:
        s = s[:-1]
    return s or None


# --- metric vocabulary -----------------------------------------------------

METRIC_SYNONYMS: dict[str, list[str]] = {
    "seats": ["seat", "user", "users", "team member", "team members", "member", "editor",
              "collaborator", "admin", "agent", "contributor", "author", "licence", "license"],
    "projects": ["project", "workspace", "site", "board", "app", "application", "repository",
                 "repo", "space", "brand", "store", "shop", "property", "environment", "pipeline"],
    "api_requests": ["api call", "api request", "api requests", "api calls", "request", "call",
                     "api credit", "api token", "endpoint call"],
    "storage": ["storage", "file storage", "disk", "disk space", "space"],
    "credits": ["credit", "ai credit", "token", "word", "generation", "run", "task", "action",
                "execution", "operation"],
    "contacts": ["contact", "subscriber", "lead", "customer record", "record", "row", "profile"],
    "emails": ["email", "email send", "send", "message", "sms", "notification", "newsletter"],
    "integrations": ["integration", "connection", "connector", "automation", "zap", "workflow",
                     "scenario", "sync"],
    "documents": ["document", "file", "form", "submission", "signature", "envelope", "invoice",
                  "report", "template", "contract", "pdf"],
    "events": ["event", "pageview", "page view", "visit", "session", "tracked event",
               "monthly active user", "mau", "active user", "visitor", "impression"],
    "minutes": ["minute", "hour", "video minute", "transcription minute", "recording minute",
                "compute hour", "build minute"],
    "retention": ["history", "retention", "data retention", "log retention", "version history",
                  "activity history", "backup"],
    "domains": ["domain", "custom domain", "subdomain", "website", "url"],
    "webhooks": ["webhook", "hook", "callback"],
    "dashboards": ["dashboard", "chart", "widget", "view", "report page"],
}

_METRIC_LOOKUP: dict[str, str] = {}
for _canon, _syns in METRIC_SYNONYMS.items():
    for _s in _syns:
        _METRIC_LOOKUP[_s] = _canon
        _METRIC_LOOKUP[_s + "s"] = _canon

METRIC_LABELS = {
    "seats": "seats / users", "projects": "projects or workspaces",
    "api_requests": "API requests", "storage": "storage", "credits": "credits",
    "contacts": "contacts or records", "emails": "emails or messages",
    "integrations": "integrations or automations", "documents": "documents or files",
    "events": "tracked events or visitors", "minutes": "minutes of usage",
    "retention": "data retention", "domains": "domains", "webhooks": "webhooks",
    "dashboards": "dashboards",
}


def normalise_metric(phrase: str | None) -> str | None:
    if not phrase:
        return None
    s = re.sub(r"[^a-z ]+", " ", phrase.lower()).strip()
    s = re.sub(r"\b(monthly|per month|each|included|of|the|your|additional|extra|more|active|total)\b", " ", s)
    s = " ".join(s.split())
    if not s:
        return None
    if s in _METRIC_LOOKUP:
        return _METRIC_LOOKUP[s]
    words = s.split()
    for n in (3, 2, 1):
        for i in range(len(words) - n + 1):
            frag = " ".join(words[i:i + n])
            if frag in _METRIC_LOOKUP:
                return _METRIC_LOOKUP[frag]
    return None


def metric_label(metric: str) -> str:
    return METRIC_LABELS.get(metric, metric.replace("_", " "))


# --- feature matching ------------------------------------------------------

FEATURE_STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "with", "to", "of", "in", "on", "your", "you",
    "all", "any", "per", "up", "plan", "plans", "included", "include", "includes", "unlimited",
    "access", "support", "custom", "advanced", "basic", "free", "new", "more", "full", "is",
    "are", "can", "get", "use", "using", "our", "their", "its", "from", "by", "as", "at",
    "this", "that", "these", "those", "available", "feature", "features", "everything",
    "plus", "also", "we", "us", "it", "be", "have", "has", "will", "each", "one", "two",
}


def _singular(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("s") and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def feature_tokens(text: str) -> set[str]:
    s = re.sub(r"[^a-z0-9 ]+", " ", (text or "").lower())
    return {_singular(w) for w in s.split()
            if w not in FEATURE_STOPWORDS and len(w) > 2}


def feature_similarity(a: str, b: str) -> float:
    ta, tb = feature_tokens(a), feature_tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# --- the claim record ------------------------------------------------------

@dataclass
class Claim:
    """One extracted public commercial promise, always tied to a literal quote."""

    kind: str                     # plan_price | trial | unlimited | limit | entitlement
                                  # | addon | condition | plan_mention | feature_doc
    page_url: str
    page_title: str
    page_category: str
    evidence: str                 # verbatim text from the page
    plan: str | None = None       # normalised plan name, when the claim is plan-scoped
    plan_raw: str | None = None
    data: dict[str, Any] = field(default_factory=dict)
    extractor: str = ""           # which rule produced it (for debugging / trust)

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def short_evidence(self) -> str:
        e = " ".join(self.evidence.split())
        return e if len(e) <= 240 else e[:237] + "..."
