"""Comparison rules: turn extracted claims into evidence-backed findings.

Design principle: a rule only fires when two claims are genuinely about the
same thing. Where the evidence is thin the rule still fires but says so, and
degrades its own confidence. Different wording alone is never a finding.
"""

from __future__ import annotations

import itertools
from dataclasses import asdict, dataclass, field

from .claims import Claim, feature_similarity, metric_label, normalise_plan

# Where a tier sits in the ladder. Used to tell real tiering ("unlimited on
# Enterprise, 25 seats on Starter") apart from a genuine contradiction.
TIER_RANK = {
    "free": 0, "trial": 0, "hobby": 1, "personal": 1, "individual": 1, "solo": 1,
    "lite": 1, "light": 1, "creator": 1, "basic": 2, "starter": 2, "start": 2,
    "launch": 2, "essential": 2, "core": 2, "standard": 3, "plus": 4, "pro": 5,
    "premium": 5, "advanced": 6, "team": 6, "business": 7, "growth": 7,
    "studio": 7, "scale": 8, "agency": 8, "company": 8, "expert": 8,
    "enterprise": 9, "ultimate": 9, "custom": 9, "elite": 9, "max": 9, "ultra": 9,
}

FINDING_KINDS = ("likely_contradiction", "ambiguity", "potentially_outdated", "missing_information")
SEVERITY_WEIGHT = {"high": 3.0, "medium": 2.0, "low": 1.0}
CONFIDENCE_WEIGHT = {"high": 3.0, "medium": 2.0, "low": 1.0}
KIND_WEIGHT = {"likely_contradiction": 1.15, "ambiguity": 1.0,
               "potentially_outdated": 0.95, "missing_information": 0.85}


@dataclass
class Evidence:
    url: str
    page_title: str
    page_category: str
    quote: str

    @classmethod
    def of(cls, c: Claim) -> "Evidence":
        return cls(url=c.page_url, page_title=c.page_title,
                   page_category=c.page_category, quote=c.short_evidence)


@dataclass
class Finding:
    rule: str
    kind: str
    severity: str
    confidence: str
    headline: str
    explanation: str
    claim_a: str          # the two conflicting claims, in plain English
    claim_b: str
    evidence_a: Evidence
    evidence_b: Evidence | None = None
    caveat: str = ""      # why this might not be a real problem
    tags: list[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        return (SEVERITY_WEIGHT[self.severity] * CONFIDENCE_WEIGHT[self.confidence]
                * KIND_WEIGHT.get(self.kind, 1.0))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["score"] = round(self.score, 2)
        return d


def _rank(plan: str | None) -> int | None:
    if not plan:
        return None
    if plan in TIER_RANK:
        return TIER_RANK[plan]
    for w in plan.split():
        if w in TIER_RANK:
            return TIER_RANK[w]
    return None


def _short(s: str, words: int = 5, chars: int = 46) -> str:
    """Comparison-table rows carry their tooltip text; headlines must not."""
    s = " ".join((s or "").split()[:words])
    return s if len(s) <= chars else s[:chars].rstrip(" ,.;:-") + "…"


def _fmt_num(v: float) -> str:
    if v == int(v):
        return f"{int(v):,}"
    return f"{v:,.2f}"


def _plan_str(plan_raw: str | None, plan: str | None) -> str:
    name = plan_raw or plan
    return f"the {name} plan" if name else "no specific plan"


def _pricing_pages(claims: list[Claim]) -> set[str]:
    return {c.page_url for c in claims if c.page_category in ("pricing", "compare")}


# --------------------------------------------------------------------- rules

def _commercial_limits(claims: list[Claim]) -> list[Claim]:
    """Numeric limits that describe what a customer is entitled to.

    A count taken from an API reference or a tutorial ("up to 10 actors",
    "defaults to 50 per page", "a Vue.js 3 project") is a description of how the
    software behaves, not of what the plan includes. Rate limits are the
    exception: a published requests-per-second ceiling is a commercial promise
    wherever it appears.
    """
    return [c for c in claims
            if c.kind == "limit" and c.data.get("metric")
            and (not c.data.get("page_is_reference")
                 or c.data.get("limit_kind") == "rate")]


def rule_unlimited_vs_limit(claims: list[Claim]) -> list[Finding]:
    out = []
    unlimited = [c for c in claims if c.kind == "unlimited" and c.data.get("metric")]
    limits = _commercial_limits(claims)
    seen: set[tuple] = set()
    for u in unlimited:
        for l in limits:
            if u.data["metric"] != l.data["metric"]:
                continue
            if u.page_url == l.page_url:
                continue
            ru, rl = _rank(u.plan), _rank(l.plan)
            if u.plan and l.plan and u.plan != l.plan:
                if ru is not None and rl is not None and ru > rl:
                    continue  # higher tier is unlimited: normal tiering, not a conflict
                if ru is None or rl is None:
                    continue
            metric = u.data["metric"]
            key = (metric, u.plan or "", l.plan or "", l.data.get("value"))
            if key in seen:
                continue
            seen.add(key)

            is_rate = l.data.get("limit_kind") == "rate"
            same_plan = bool(u.plan and l.plan and u.plan == l.plan)
            unit = l.data.get("unit")
            amount = _fmt_num(l.data["value"]) + (f" {unit}" if unit and unit != "count" else "")
            window = f" per {l.data['window']}" if l.data.get("window") else ""

            if is_rate:
                kind, severity = "ambiguity", "medium"
                headline = (f"“Unlimited {_short(u.data['subject'])}” is advertised, "
                            f"but a rate limit is documented")
                explanation = (
                    f"Your pricing pages promise unlimited {metric_label(metric)}"
                    f"{' on ' + (u.plan_raw or u.plan) if u.plan else ''}, while your documentation "
                    f"caps usage at {amount} {metric_label(metric)}{window}. Both can be true at "
                    f"once, but a customer "
                    f"reading only the pricing page will not expect a throttle — and a customer "
                    f"reading only the docs cannot tell whether the cap is a hard ceiling.")
                caveat = ("A rate limit and a volume allowance are technically different things. "
                          "This is a clarity problem rather than a broken promise.")
            else:
                kind = "likely_contradiction"
                severity = "high" if (same_plan or u.plan or l.plan) else "medium"
                headline = (f"“Unlimited {_short(u.data['subject'])}” is advertised, "
                            f"but a hard limit of {amount} is documented")
                explanation = (
                    f"One page promises unlimited {metric_label(metric)}"
                    f"{' on ' + (u.plan_raw or u.plan) if u.plan else ''}. Another states a specific "
                    f"ceiling of {amount}{' on ' + (l.plan_raw or l.plan) if l.plan else ''}. "
                    f"These cannot both describe what the customer receives.")
                caveat = ""
            if same_plan:
                confidence = "high"
            elif u.plan or l.plan:
                confidence = "medium"
                caveat = (caveat + " " if caveat else "") + (
                    "Only one of the two statements names a plan, so it is possible they describe "
                    "different tiers.")
            else:
                confidence, severity = "low", "medium"
                caveat = (caveat + " " if caveat else "") + (
                    "Neither statement names a plan, so this may be a documentation-scoping issue "
                    "rather than a conflict.")

            out.append(Finding(
                rule="unlimited_vs_limit", kind=kind, severity=severity, confidence=confidence,
                headline=headline, explanation=explanation,
                claim_a=f"Unlimited {_short(u.data['subject'])} ({_plan_str(u.plan_raw, u.plan)})",
                claim_b=(f"A limit of {amount} {metric_label(metric)}{window} "
                         f"({_plan_str(l.plan_raw, l.plan)})"),
                evidence_a=Evidence.of(u), evidence_b=Evidence.of(l), caveat=caveat.strip(),
                tags=["unlimited", metric]))
    return out


def rule_unlimited_vs_fair_use(claims: list[Claim]) -> list[Finding]:
    out = []
    unlimited = [c for c in claims if c.kind == "unlimited"]
    fair = [c for c in claims if c.kind == "condition" and c.data.get("condition") == "fair_use"]
    if not unlimited or not fair:
        return out
    u = sorted(unlimited, key=lambda c: 0 if c.page_category in ("pricing", "compare") else 1)[0]
    for f in fair:
        if f.page_url == u.page_url:
            continue
        out.append(Finding(
            rule="unlimited_vs_fair_use", kind="ambiguity", severity="medium", confidence="high",
            headline="“Unlimited” is advertised, but a fair-use restriction is buried on another page",
            explanation=(
                f"Your commercial pages advertise unlimited {_short(u.data.get('subject','usage'))}, while "
                f"a separate page qualifies usage with a fair-use or acceptable-use restriction. "
                f"A customer deciding on price never sees the qualifier; a customer who hits it "
                f"experiences it as a broken promise."),
            claim_a=f"Unlimited {_short(u.data.get('subject', 'usage'))} ({_plan_str(u.plan_raw, u.plan)})",
            claim_b="Usage is subject to a fair-use / acceptable-use restriction",
            evidence_a=Evidence.of(u), evidence_b=Evidence.of(f),
            caveat=("Fair-use clauses are standard practice. The issue is placement and wording, "
                    "not the existence of the clause."),
            tags=["unlimited", "fair_use"]))
        break
    return out


def rule_trial_conflict(claims: list[Claim]) -> list[Finding]:
    out = []
    trials = [c for c in claims if c.kind == "trial" and c.data.get("days")]
    by_days: dict[int, list[Claim]] = {}
    for t in trials:
        by_days.setdefault(int(t.data["days"]), []).append(t)
    if len(by_days) >= 2:
        pairs = sorted(by_days.items())
        (d1, c1s), (d2, c2s) = pairs[0], pairs[-1]
        a, b = c1s[0], c2s[0]
        if a.page_url != b.page_url:
            same_plan_scope = (a.plan or None) == (b.plan or None)
            out.append(Finding(
                rule="trial_length_conflict",
                kind="likely_contradiction" if same_plan_scope else "ambiguity",
                severity="high", confidence="high" if same_plan_scope else "medium",
                headline=f"Your free trial is described as {d1} days on one page and {d2} days on another",
                explanation=(
                    f"Trial length is one of the first commitments a prospect reads and one of the "
                    f"first things support gets asked about. Right now {a.page_title or a.page_url} "
                    f"says {d1} days and {b.page_title or b.page_url} says {d2} days. Whichever is "
                    f"correct, one page is setting the wrong expectation."),
                claim_a=f"{d1}-day trial", claim_b=f"{d2}-day trial",
                evidence_a=Evidence.of(a), evidence_b=Evidence.of(b),
                caveat=("" if same_plan_scope else
                        "The two statements may be scoped to different plans or to a legacy offer."),
                tags=["trial"]))
        if len(by_days) > 2:
            others = ", ".join(f"{d} days" for d in sorted(by_days)[1:-1])
            out[-1].explanation += f" A further variant is also published on your site ({others})."

    card_req = [c for c in claims if c.kind == "trial" and c.data.get("card_required")]
    no_card = [c for c in claims if c.kind == "trial" and c.data.get("no_card")]
    if card_req and no_card:
        a, b = no_card[0], card_req[0]
        if a.page_url != b.page_url:
            out.append(Finding(
                rule="trial_card_conflict", kind="likely_contradiction", severity="high",
                confidence="medium",
                headline="One page says the trial needs no credit card; another says payment details are required",
                explanation=(
                    "This is the single most common cause of abandoned signups. One of your pages "
                    "removes the friction and another reinstates it, so prospects who read both "
                    "stop trusting either."),
                claim_a="No credit card required to start the trial",
                claim_b="Payment details are required to start the trial",
                evidence_a=Evidence.of(a), evidence_b=Evidence.of(b),
                caveat="Check whether the two statements refer to different signup routes or plans.",
                tags=["trial", "signup"]))
    return out


def rule_price_conflict(claims: list[Claim]) -> list[Finding]:
    out = []
    prices = [c for c in claims if c.kind == "plan_price" and c.plan
              and c.data.get("amount") and c.data.get("period") in ("month", "year")]
    groups: dict[tuple, list[Claim]] = {}
    for p in prices:
        key = (p.plan, p.data["currency"], p.data["period"], bool(p.data.get("per_seat")),
               bool(p.data.get("billed_annually")))
        groups.setdefault(key, []).append(p)
    for key, items in groups.items():
        amounts = {c.data["amount"]: c for c in items}
        if len(amounts) < 2:
            continue
        pages = {c.page_url for c in items}
        if len(pages) < 2:
            continue  # a monthly/annual toggle on one page is not a conflict
        lo, hi = min(amounts), max(amounts)
        a, b = amounts[lo], amounts[hi]
        if a.page_url == b.page_url:
            continue
        plan, cur, period, per_seat, annual = key
        unit = f"/{period}" + (" per seat" if per_seat else "")
        suffix = " (billed annually)" if annual else ""
        out.append(Finding(
            rule="price_conflict", kind="likely_contradiction", severity="high",
            confidence="high" if hi / lo < 10 else "medium",
            headline=f"The {a.plan_raw or plan} plan is priced at two different amounts on your own site",
            explanation=(
                f"{a.page_title or a.page_url} lists {cur} {_fmt_num(lo)}{unit}{suffix} while "
                f"{b.page_title or b.page_url} lists {cur} {_fmt_num(hi)}{unit}{suffix} for the same "
                f"plan and the same billing period. Prospects who compare the two pages, and "
                f"customers who quote the cheaper one back to you, will both cost you time."),
            claim_a=f"{a.plan_raw or plan}: {cur} {_fmt_num(lo)}{unit}{suffix}",
            claim_b=f"{b.plan_raw or plan}: {cur} {_fmt_num(hi)}{unit}{suffix}",
            evidence_a=Evidence.of(a), evidence_b=Evidence.of(b),
            caveat=("One of the pages may be an out-of-date snapshot, a regional price, or a "
                    "promotional rate. Worth confirming which is authoritative."),
            tags=["price", plan]))
    return out


def rule_annual_monthly(claims: list[Claim]) -> list[Finding]:
    """Check that annual and monthly prices for the same plan reconcile."""
    out = []
    prices = [c for c in claims if c.kind == "plan_price" and c.plan and c.data.get("amount")]
    by_plan: dict[str, list[Claim]] = {}
    for p in prices:
        by_plan.setdefault(p.plan, []).append(p)
    for plan, items in by_plan.items():
        monthly = [c for c in items if c.data["period"] == "month" and not c.data.get("billed_annually")]
        annual_mo = [c for c in items if c.data["period"] == "month" and c.data.get("billed_annually")]
        yearly = [c for c in items if c.data["period"] == "year"]
        if monthly and annual_mo:
            m = min(c.data["amount"] for c in monthly)
            a = max(c.data["amount"] for c in annual_mo)
            if a > m * 1.001:
                ca = next(c for c in annual_mo if c.data["amount"] == a)
                cm = next(c for c in monthly if c.data["amount"] == m)
                out.append(Finding(
                    rule="annual_costs_more", kind="likely_contradiction", severity="high",
                    confidence="medium",
                    headline=f"On the {ca.plan_raw or plan} plan, committing annually appears to cost more per month",
                    explanation=(
                        f"The annual price works out at {_fmt_num(a)} per month while the monthly "
                        f"price is {_fmt_num(m)}. Annual commitment normally buys a discount, so "
                        f"either the figures are stale or the labels are the wrong way round. "
                        f"Either way the pricing page is arguing against your own upsell."),
                    claim_a=f"{_fmt_num(m)} per month, billed monthly",
                    claim_b=f"{_fmt_num(a)} per month, billed annually",
                    evidence_a=Evidence.of(cm), evidence_b=Evidence.of(ca),
                    caveat=("Automated price reading can mis-pair a headline price with the wrong "
                            "billing toggle. Confirm against the live toggle before acting."),
                    tags=["price", "annual", plan]))
        if monthly and yearly:
            m = min(c.data["amount"] for c in monthly)
            y = min(c.data["amount"] for c in yearly)
            if m > 0 and y > m * 12 * 1.02:
                cy = next(c for c in yearly if c.data["amount"] == y)
                cm = next(c for c in monthly if c.data["amount"] == m)
                out.append(Finding(
                    rule="annual_total_exceeds_monthly", kind="likely_contradiction",
                    severity="high", confidence="medium",
                    headline=f"The annual price of the {cy.plan_raw or plan} plan is higher than paying monthly for a year",
                    explanation=(
                        f"Twelve months at {_fmt_num(m)} comes to {_fmt_num(m * 12)}, but the "
                        f"published annual price is {_fmt_num(y)}. A customer who does the "
                        f"arithmetic is being asked to pay more for committing longer."),
                    claim_a=f"{_fmt_num(m)} per month ({_fmt_num(m * 12)} over a year)",
                    claim_b=f"{_fmt_num(y)} per year",
                    evidence_a=Evidence.of(cm), evidence_b=Evidence.of(cy),
                    caveat="Verify that both figures refer to the same seat count and currency.",
                    tags=["price", "annual", plan]))
    return out


def rule_limit_conflict(claims: list[Claim]) -> list[Finding]:
    out = []
    limits = _commercial_limits(claims)
    by_metric: dict[str, list[Claim]] = {}
    for l in limits:
        by_metric.setdefault(l.data["metric"], []).append(l)
    seen: set[tuple] = set()
    for metric, items in by_metric.items():
        for a, b in itertools.combinations(items, 2):
            if a.page_url == b.page_url:
                continue
            if a.data.get("limit_kind") != b.data.get("limit_kind"):
                continue
            if a.data.get("unit") != b.data.get("unit"):
                continue
            if a.data.get("window") != b.data.get("window"):
                continue
            va, vb = a.data["value"], b.data["value"]
            if va == vb:
                continue
            if a.plan and b.plan and a.plan != b.plan:
                continue  # different tiers legitimately have different allowances
            explicit = bool(a.plan and b.plan and a.plan == b.plan)
            if not explicit:
                # An unscoped docs limit is only interesting if it matches no
                # published plan allowance at all.
                unscoped = a if not a.plan else b
                scoped_vals = {c.data["value"] for c in items if c.plan}
                if scoped_vals and unscoped.data["value"] in scoped_vals:
                    continue
                if max(va, vb) / max(min(va, vb), 0.0001) < 1.5:
                    continue
            key = (metric, min(va, vb), max(va, vb), a.plan or b.plan or "")
            if key in seen:
                continue
            seen.add(key)
            unit = a.data.get("unit")
            fmt = lambda v: _fmt_num(v) + (f" {unit}" if unit and unit != "count" else "")
            window = f" per {a.data['window']}" if a.data.get("window") else ""
            label = metric_label(metric)
            out.append(Finding(
                rule="limit_conflict",
                kind="likely_contradiction" if explicit else "ambiguity",
                severity="high" if explicit else "medium",
                confidence="high" if explicit else "low",
                headline=(f"Two different allowances are published for {label}"
                          + (f" on the {a.plan_raw or a.plan} plan" if explicit else "")),
                explanation=(
                    f"{a.page_title or a.page_url} states {fmt(va)}{window} and "
                    f"{b.page_title or b.page_url} states {fmt(vb)}{window} for {label}"
                    + (f" on {a.plan_raw or a.plan}." if explicit else
                       ". Neither figure is tied to a named plan, so a customer cannot work out "
                       "which applies to them.")),
                claim_a=f"{fmt(va)} {label}{window} ({_plan_str(a.plan_raw, a.plan)})",
                claim_b=f"{fmt(vb)} {label}{window} ({_plan_str(b.plan_raw, b.plan)})",
                evidence_a=Evidence.of(a), evidence_b=Evidence.of(b),
                caveat=("" if explicit else
                        "The two numbers may be scoped to different plans or to different objects "
                        "(per workspace vs per account). Treat this as a prompt to check, not proof."),
                tags=["limit", metric]))
    return out


def rule_feature_plan_conflict(claims: list[Claim]) -> list[Finding]:
    out = []
    ents = [c for c in claims if c.kind == "entitlement" and c.plan]
    pricing_ents = [c for c in ents if c.page_category in ("pricing", "compare")]
    other_ents = [c for c in ents if c.page_category not in ("pricing", "compare")]
    if not pricing_ents or not other_ents:
        return out
    seen: set[str] = set()
    for d in other_ents:
        feat_d = d.data.get("feature", "")
        matches = [(feature_similarity(feat_d, p.data.get("feature", "")), p) for p in pricing_ents]
        matches = [(s, p) for s, p in matches if s >= 0.5]
        if not matches:
            continue
        plans_with_feature = {p.plan for _, p in matches}
        if d.plan in plans_with_feature:
            continue
        best_sim, best = max(matches, key=lambda t: t[0])
        # Pricing cards are cumulative, so the lowest tier that lists it wins.
        ranked = [(_rank(p.plan), p) for _, p in matches]
        ranked = [(r, p) for r, p in ranked if r is not None]
        lowest = min(ranked, key=lambda t: t[0])[1] if ranked else best
        rd, rp = _rank(d.plan), _rank(lowest.plan)
        if rd is not None and rp is not None and rd <= rp:
            continue  # docs gate it no higher than pricing does
        key = feat_d.lower()[:60]
        if key in seen:
            continue
        seen.add(key)
        out.append(Finding(
            rule="feature_plan_conflict", kind="likely_contradiction", severity="high",
            confidence="high" if best_sim >= 0.7 else "medium",
            headline=(f"“{lowest.data.get('feature', '')[:60]}” is sold with "
                      f"{lowest.plan_raw or lowest.plan} but documented as "
                      f"{d.plan_raw or d.plan}-only"),
            explanation=(
                f"Your pricing page lists this feature under the {lowest.plan_raw or lowest.plan} "
                f"plan, while {d.page_title or d.page_url} tells customers it requires "
                f"{d.plan_raw or d.plan}. A customer who buys the cheaper plan for that feature "
                f"will open a support ticket, and probably a refund request."),
            claim_a=f"Included in {lowest.plan_raw or lowest.plan}: {lowest.data.get('feature','')[:80]}",
            claim_b=f"Requires {d.plan_raw or d.plan}",
            evidence_a=Evidence.of(lowest), evidence_b=Evidence.of(d),
            caveat=("" if best_sim >= 0.7 else
                    "The two pages describe the feature in different words, so confirm they mean "
                    "the same capability."),
            tags=["entitlement", d.plan or ""]))
    return out


def rule_plan_name_drift(claims: list[Claim]) -> list[Finding]:
    out = []
    pricing_plans = {c.plan for c in claims
                     if c.kind in ("plan_mention", "plan_price")
                     and c.page_category in ("pricing", "compare") and c.plan}
    if len(pricing_plans) < 2:
        return out
    ignore = {"custom", "trial", "free", "unlimited", "current", "paid", "annual", "monthly", "legacy"}
    stray: dict[str, list[Claim]] = {}
    for c in claims:
        if c.kind != "plan_mention" or c.page_category in ("pricing", "compare"):
            continue
        if not c.plan or c.plan in pricing_plans or c.plan in ignore:
            continue
        if _rank(c.plan) is None:
            continue
        stray.setdefault(c.plan, []).append(c)
    for plan, items in sorted(stray.items(), key=lambda kv: -len(kv[1]))[:3]:
        a = items[0]
        pages = ", ".join(sorted({i.page_title or i.page_url for i in items})[:3])
        out.append(Finding(
            rule="plan_name_drift", kind="potentially_outdated", severity="medium",
            confidence="medium" if len(items) > 1 else "low",
            headline=f"Your help content still refers to a “{a.plan_raw or plan}” plan that is not on the pricing page",
            explanation=(
                f"The plans you currently sell are {', '.join(sorted(pricing_plans))}. "
                f"{pages} still describes a {a.plan_raw or plan} plan. Either it is a legacy tier "
                f"that existing customers are on — in which case say so — or the content was "
                f"never updated after a repackaging, and new customers are reading instructions "
                f"for a plan they cannot buy."),
            claim_a=f"Pricing page sells: {', '.join(sorted(pricing_plans))}",
            claim_b=f"Help content references a {a.plan_raw or plan} plan",
            evidence_a=Evidence.of(a), evidence_b=None,
            caveat=("Legacy plans are often referenced deliberately for grandfathered customers. "
                    "The question is whether a new customer can tell."),
            tags=["plan_naming", plan]))
    return out


CONDITION_SEVERITY = {
    "overage": ("high", "charges that apply once an allowance is exceeded"),
    "seat_minimum": ("high", "a minimum seat count"),
    "fair_use": ("medium", "a fair-use restriction on usage"),
    "no_refund": ("medium", "a no-refund policy"),
    "auto_renew": ("low", "automatic renewal"),
    "price_change": ("low", "the right to change prices"),
}


def rule_condition_off_pricing(claims: list[Claim]) -> list[Finding]:
    out = []
    pricing_urls = _pricing_pages(claims)
    if not pricing_urls:
        return out
    on_pricing = {c.data.get("condition") for c in claims
                  if c.kind == "condition" and c.page_url in pricing_urls}
    elsewhere: dict[str, Claim] = {}
    for c in claims:
        if c.kind != "condition" or c.page_url in pricing_urls:
            continue
        cond = c.data.get("condition")
        if cond in CONDITION_SEVERITY and cond not in on_pricing and cond not in elsewhere:
            elsewhere[cond] = c
    unlimited_urls = {c.page_url for c in claims if c.kind == "unlimited"}
    BOILERPLATE_ON_TERMS = {"auto_renew", "no_refund", "price_change"}
    emitted = 0
    for cond, c in sorted(elsewhere.items(),
                          key=lambda kv: SEVERITY_WEIGHT[CONDITION_SEVERITY[kv[0]][0]] * -1):
        if cond == "fair_use" and unlimited_urls:
            continue  # already reported as an "unlimited but fair use" finding
        if emitted >= 2:
            break  # two of these is a point; five is a listicle
        severity, desc = CONDITION_SEVERITY[cond]
        on_terms = c.page_category == "terms"
        if on_terms and cond in BOILERPLATE_ON_TERMS:
            # Where else would a renewal clause live? Note it, do not headline it.
            severity = "low"
        elif on_terms and severity == "high":
            # A generic reference to overages in the contract is weaker evidence
            # than an actual overage table in the help centre.
            severity = "medium"
        emitted += 1
        out.append(Finding(
            rule="condition_off_pricing", kind="missing_information", severity=severity,
            confidence="high",
            headline=f"A commercial condition — {desc} — appears only away from your pricing page",
            explanation=(
                f"{c.page_title or c.page_url} sets out {desc}, but nothing equivalent appears on "
                f"your pricing page. Conditions that change what a customer actually pays or "
                f"receives belong where the buying decision is made; discovering them later is "
                f"where churn and chargebacks start."),
            claim_a="Pricing page: condition not stated",
            claim_b=f"{c.page_title or c.page_url}: {desc}",
            evidence_a=Evidence(url=sorted(pricing_urls)[0], page_title="Pricing page",
                                page_category="pricing",
                                quote="(no equivalent statement found on the pricing page)"),
            evidence_b=Evidence.of(c),
            caveat=(("This is standard legal wording in the right place; the question is only "
                     "whether the pricing page sets the same expectation. " if on_terms and
                     cond in BOILERPLATE_ON_TERMS else "")
                    + "Detected by absence, so a condition stated in an image, a tooltip or a "
                      "collapsed accordion on the pricing page would be missed."),
            tags=["condition", cond]))
    return out


def rule_vague_entitlement(claims: list[Claim]) -> list[Finding]:
    out = []
    vague = [c for c in claims if c.kind == "entitlement" and c.data.get("vague_gate")]
    named_plans = {c.plan for c in claims if c.kind == "plan_mention" and c.plan}
    if not vague or len(named_plans) < 2:
        return out
    c = vague[0]
    others = len(vague) - 1
    out.append(Finding(
        rule="vague_entitlement", kind="missing_information", severity="medium",
        confidence="medium" if others else "low",
        headline="Documented features are gated to “paid plans” without naming which plan",
        explanation=(
            f"You sell {len(named_plans)} distinct plans, but "
            f"{c.page_title or c.page_url} gates a feature to a “{c.data['vague_gate']}” plan "
            f"without saying which one"
            + (f", and {others} other statement(s) on your site do the same. " if others else ". ")
            + "A prospect cannot work out which plan to buy, and support has to answer it "
              "one ticket at a time."),
        claim_a=f"Feature described: {c.data.get('feature', '')[:100]}",
        claim_b=f"Entitlement given only as “{c.data['vague_gate']} plans”",
        evidence_a=Evidence.of(c), evidence_b=None,
        caveat="Low-stakes on its own; it matters most where the feature drives the upgrade.",
        tags=["entitlement", "vague"]))
    return out


def rule_price_only_on_request(claims: list[Claim]) -> list[Finding]:
    """A plan documented in help content but with no published price at all."""
    out = []
    priced = {c.plan for c in claims if c.kind == "plan_price" and c.data.get("amount") and c.plan}
    pricing_urls = _pricing_pages(claims)
    if not priced or not pricing_urls:
        return out
    docs_plans: dict[str, Claim] = {}
    for c in claims:
        if c.kind == "plan_mention" and c.plan and c.plan not in priced \
                and c.page_url not in pricing_urls and _rank(c.plan) is not None:
            docs_plans.setdefault(c.plan, c)
    for plan, c in list(docs_plans.items())[:1]:
        # Enterprise is sales-led by design and a free plan has no price to publish.
        if plan in ("enterprise", "custom", "free", "trial"):
            continue
        out.append(Finding(
            rule="unpriced_plan", kind="missing_information", severity="low", confidence="low",
            headline=f"A “{c.plan_raw or plan}” plan is documented but carries no published price",
            explanation=(
                f"Your documentation refers to a {c.plan_raw or plan} plan, but no price for it "
                f"appears anywhere on your public pages. Prospects who find the documentation "
                f"first have no way to qualify themselves."),
            claim_a=f"Published prices exist for: {', '.join(sorted(priced))}",
            claim_b=f"Documentation refers to a {c.plan_raw or plan} plan",
            evidence_a=Evidence.of(c), evidence_b=None,
            caveat="May be an intentionally sales-led tier, or a legacy name.",
            tags=["plan_naming", plan]))
    return out


ALL_RULES = (
    rule_unlimited_vs_limit,
    rule_unlimited_vs_fair_use,
    rule_trial_conflict,
    rule_price_conflict,
    rule_annual_monthly,
    rule_limit_conflict,
    rule_feature_plan_conflict,
    rule_plan_name_drift,
    rule_condition_off_pricing,
    rule_vague_entitlement,
    rule_price_only_on_request,
)


def dedupe(findings: list[Finding]) -> list[Finding]:
    """Keep the strongest version of each substantially identical finding."""
    exact: set[tuple] = set()
    soft_seen: set[tuple] = set()
    out: list[Finding] = []
    for f in sorted(findings, key=lambda f: -f.score):
        key = (f.rule, f.evidence_a.url, f.evidence_b.url if f.evidence_b else "",
               f.claim_a[:50], f.claim_b[:50])
        if key in exact:
            continue
        soft = (f.rule, tuple(sorted(f.tags)))
        # These two rules can fire many times over the same metric; one is enough.
        if f.rule in ("unlimited_vs_limit", "limit_conflict") and soft in soft_seen:
            continue
        exact.add(key)
        soft_seen.add(soft)
        out.append(f)
    return out


def run_rules(claims: list[Claim], max_findings: int = 12) -> list[Finding]:
    findings: list[Finding] = []
    for rule in ALL_RULES:
        try:
            findings.extend(rule(claims))
        except Exception as exc:
            findings.append(Finding(
                rule=rule.__name__, kind="ambiguity", severity="low", confidence="low",
                headline="Internal rule error", explanation=str(exc)[:200],
                claim_a="", claim_b="",
                evidence_a=Evidence(url="", page_title="", page_category="", quote="")))
    findings = [f for f in findings if f.headline != "Internal rule error"]
    return dedupe(findings)[:max_findings]
