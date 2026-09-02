"""The analysis contract: what the model is asked to return, and what counts as valid.

This module is the single source of truth. `prompts.py` describes this shape to
the model in prose, `verify.py` enforces it, and `render.py` consumes it.
"""

from __future__ import annotations

FINDING_TYPES = (
    "likely_contradiction",   # two public statements that cannot both be true
    "ambiguity",              # both can be true; a customer cannot tell what they get
    "potentially_outdated",   # looks left over from earlier packaging
    "missing_information",    # changes the deal, published where the buyer will not look
)
SEVERITIES = ("high", "medium", "low")
CONFIDENCES = ("high", "medium", "low")

FINDING_TYPE_LABEL = {
    "likely_contradiction": "Likely contradiction",
    "ambiguity": "Ambiguity",
    "potentially_outdated": "Possibly out of date",
    "missing_information": "Missing information",
}
FINDING_TYPE_BLURB = {
    "likely_contradiction": "Two public statements that cannot both be true.",
    "ambiguity": "Both statements can be true, but a customer cannot tell what they get.",
    "potentially_outdated": "Content that looks left over from an earlier version of your packaging.",
    "missing_information": "Something that changes the deal, published somewhere the buyer will not look.",
}

# One JSON object per company. Quotes must be verbatim from the dossier.
ANALYSIS_SCHEMA = {
    "company": "str",
    "plans": [{
        "name": "str",
        "headline_price": "str | null",     # exactly as printed, e.g. '$29/mo billed annually'
        "billing_periods": ["str"],
        "evidence": {"quote": "str", "url": "str"},
    }],
    "promises": [{
        "kind": "str",   # plan_price | trial | limit | unlimited | entitlement | addon | condition
        "statement": "str",
        "plan": "str | null",
        "evidence": {"quote": "str", "url": "str"},
    }],
    "findings": [{
        "type": f"one of {FINDING_TYPES}",
        "severity": f"one of {SEVERITIES}",
        "confidence": f"one of {CONFIDENCES}",
        "headline": "str",
        "explanation": "str",
        "claim_a": {"statement": "str", "quote": "str", "url": "str"},
        "claim_b": {"statement": "str", "quote": "str", "url": "str"},
        "why_not_just_wording": "str",
        "caveat": "str",
    }],
    "coverage_notes": {
        "unusable_pages": ["str"],
        "what_was_not_checkable": "str",
    },
}

REQUIRED_FINDING_KEYS = (
    "type", "severity", "confidence", "headline", "explanation",
    "claim_a", "claim_b", "why_not_just_wording", "caveat",
)
REQUIRED_CLAIM_KEYS = ("statement", "quote", "url")


def blank_analysis(company: str) -> dict:
    return {"company": company, "plans": [], "promises": [], "findings": [],
            "coverage_notes": {"unusable_pages": [], "what_was_not_checkable": ""}}
