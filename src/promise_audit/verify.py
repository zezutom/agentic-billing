"""Check the analyst's evidence against the pages it came from.

This is what makes it reasonable to put an LLM in the middle of the pipeline.
Every quote is located, character by character, in the harvested text of the
page the model attributed it to. A finding whose evidence cannot be found is
discarded before anyone reads it, and the discard is counted and reported.

The comparison is deliberately a little forgiving. Whitespace, curly quotes,
dashes and case are normalised, and an ellipsis inside a quote is treated as
"these fragments, in this order", because those are rendering artefacts rather
than fabrication. It is not forgiving about anything else.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

from .harvest import Dossier
from .schema import (
    CONFIDENCES, FINDING_TYPES, REQUIRED_CLAIM_KEYS, REQUIRED_FINDING_KEYS, SEVERITIES,
)

_PUNCT_MAP = {
    "‘": "'", "’": "'", "‚": "'", "‛": "'",
    "“": '"', "”": '"', "„": '"',
    "–": "-", "—": "-", "−": "-", "‐": "-", "‑": "-",
    " ": " ", " ": " ", " ": " ", "​": "",
}
_ELLIPSIS_RE = re.compile(r"\s*(?:…|\.\.\.|\[\.\.\.\])\s*")
# A finding's evidence must be a substantial passage: a three-character quote
# would match half the page and prove nothing. Plan and promise evidence is
# context rather than an accusation, so a bare price like "$5 / mo" is fine.
MIN_FINDING_QUOTE_CHARS = 8
MIN_CONTEXT_QUOTE_CHARS = 4


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    for a, b in _PUNCT_MAP.items():
        text = text.replace(a, b)
    return re.sub(r"\s+", " ", text).strip().lower()


@dataclass
class Rejection:
    where: str          # "finding[2].claim_b" etc.
    reason: str
    detail: str = ""


@dataclass
class VerificationReport:
    findings_in: int = 0
    findings_out: int = 0
    quotes_checked: int = 0
    quotes_failed: int = 0
    url_corrections: int = 0
    rejections: list[Rejection] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "findings_in": self.findings_in, "findings_out": self.findings_out,
            "findings_rejected": self.findings_in - self.findings_out,
            "quotes_checked": self.quotes_checked, "quotes_failed": self.quotes_failed,
            "url_corrections": self.url_corrections,
            "rejections": [{"where": r.where, "reason": r.reason, "detail": r.detail}
                           for r in self.rejections],
        }


class QuoteIndex:
    """Normalised text of every harvested page, searchable by URL or globally."""

    def __init__(self, dossier: Dossier) -> None:
        self.by_url: dict[str, str] = {}
        for p in dossier.pages:
            if not p.ok:
                continue
            body = normalise(f"{p.title}\n{p.text}")
            for key in {p.url, p.final_url}:
                if key:
                    self.by_url[key.rstrip("/")] = body

    def contains(self, url: str, quote: str, min_chars: int = MIN_FINDING_QUOTE_CHARS) -> bool:
        body = self.by_url.get((url or "").rstrip("/"))
        return body is not None and self._in(body, quote, min_chars)

    def find_url(self, quote: str, min_chars: int = MIN_FINDING_QUOTE_CHARS) -> str | None:
        for url, body in self.by_url.items():
            if self._in(body, quote, min_chars):
                return url
        return None

    @staticmethod
    def _in(body: str, quote: str, min_chars: int = MIN_FINDING_QUOTE_CHARS) -> bool:
        q = normalise(quote)
        if len(q) < min_chars:
            return False
        if q in body:
            return True
        # An ellipsis means the model elided the middle of a passage.
        parts = [normalise(p) for p in _ELLIPSIS_RE.split(quote) if normalise(p)]
        if len(parts) < 2:
            return False
        pos = 0
        for part in parts:
            if len(part) < 4:
                continue
            idx = body.find(part, pos)
            if idx == -1:
                return False
            pos = idx + len(part)
        return True


def _check_claim(index: QuoteIndex, claim: dict, where: str,
                 report: VerificationReport) -> bool:
    missing = [k for k in REQUIRED_CLAIM_KEYS if not claim.get(k)]
    if missing:
        report.rejections.append(Rejection(where, "claim is missing fields",
                                           ", ".join(missing)))
        return False
    report.quotes_checked += 1
    quote, url = claim["quote"], claim["url"]
    if index.contains(url, quote):
        return True
    # The quote may be real but attributed to the wrong page; that is a
    # citation error, not a fabrication, so correct it and note it.
    actual = index.find_url(quote)
    if actual:
        claim["url"] = actual
        claim["url_corrected_from"] = url
        report.url_corrections += 1
        return True
    report.quotes_failed += 1
    report.rejections.append(Rejection(
        where, "quote not found on any harvested page", quote[:120]))
    return False


def verify(analysis: dict, dossier: Dossier) -> tuple[dict, VerificationReport]:
    """Return the analysis with unverifiable findings removed, plus a report."""
    index = QuoteIndex(dossier)
    report = VerificationReport()

    kept_findings = []
    for i, f in enumerate(analysis.get("findings", []) or []):
        report.findings_in += 1
        where = f"findings[{i}]"
        missing = [k for k in REQUIRED_FINDING_KEYS if k not in f]
        if missing:
            report.rejections.append(Rejection(where, "finding is missing fields",
                                               ", ".join(missing)))
            continue
        if f.get("type") not in FINDING_TYPES:
            report.rejections.append(Rejection(where, "unknown finding type",
                                               str(f.get("type"))))
            continue
        if f.get("severity") not in SEVERITIES or f.get("confidence") not in CONFIDENCES:
            report.rejections.append(Rejection(where, "invalid severity or confidence",
                                               f"{f.get('severity')}/{f.get('confidence')}"))
            continue
        if not (f.get("why_not_just_wording") or "").strip():
            report.rejections.append(
                Rejection(where, "no reason given why this is more than a wording difference"))
            continue
        ok_a = _check_claim(index, f.get("claim_a") or {}, where + ".claim_a", report)
        ok_b = _check_claim(index, f.get("claim_b") or {}, where + ".claim_b", report)
        if not (ok_a and ok_b):
            continue
        qa, qb = normalise(f["claim_a"]["quote"]), normalise(f["claim_b"]["quote"])
        # The two sides must be genuinely different passages. They may live on
        # the same page: a feature bullet at the top of a pricing page and an
        # FAQ answer two thousand words below it are not one statement, and a
        # pricing page that argues with itself is worth more to the reader than
        # one that argues with the terms of service.
        if qa == qb or qa in qb or qb in qa:
            report.rejections.append(
                Rejection(where, "both sides cite the same passage", qa[:100]))
            continue
        f["same_page"] = (f["claim_a"]["url"].rstrip("/")
                          == f["claim_b"]["url"].rstrip("/"))
        kept_findings.append(f)
        report.findings_out += 1

    # Plans and promises are context, not accusations: flag rather than drop.
    for bucket in ("plans", "promises"):
        for item in analysis.get(bucket, []) or []:
            ev = item.get("evidence") or {}
            if not ev.get("quote"):
                item["evidence_verified"] = False
                continue
            report.quotes_checked += 1
            if index.contains(ev.get("url", ""), ev["quote"], MIN_CONTEXT_QUOTE_CHARS):
                item["evidence_verified"] = True
            else:
                actual = index.find_url(ev["quote"], MIN_CONTEXT_QUOTE_CHARS)
                if actual:
                    ev["url_corrected_from"] = ev.get("url", "")
                    ev["url"] = actual
                    report.url_corrections += 1
                    item["evidence_verified"] = True
                else:
                    item["evidence_verified"] = False
                    report.quotes_failed += 1

    analysis = dict(analysis)
    analysis["findings"] = _rank(kept_findings)
    analysis["verification"] = report.to_dict()
    return analysis, report


_SEV_W = {"high": 3, "medium": 2, "low": 1}
_CONF_W = {"high": 3, "medium": 2, "low": 1}
_TYPE_W = {"likely_contradiction": 1.15, "ambiguity": 1.0,
           "potentially_outdated": 0.95, "missing_information": 0.85}


def score(f: dict) -> float:
    return (_SEV_W.get(f.get("severity"), 1) * _CONF_W.get(f.get("confidence"), 1)
            * _TYPE_W.get(f.get("type"), 1.0))


def _rank(findings: list[dict]) -> list[dict]:
    for f in findings:
        f["score"] = round(score(f), 2)
    return sorted(findings, key=lambda f: -f["score"])
