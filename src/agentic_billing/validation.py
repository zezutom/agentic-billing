"""Deterministic validation for LLM-generated billing decisions.

Every decision is checked against the allowed action set and a confidence
threshold before execution.  If either check fails, the decision is replaced
with an escalation action so a human reviews it.

The action-set check is defense-in-depth: Pydantic's Literal type already
constrains the LLM output, but we verify explicitly as a safety boundary.
"""

from .models import (
    MeteredUsageDecision,
    MigrationDecision,
    PaymentRecoveryDecision,
)

CONFIDENCE_THRESHOLD = 0.7

METERED_USAGE_ACTIONS = frozenset({
    "NO_ACTION", "NOTIFY_THRESHOLD",
    "RECOMMEND_PLAN_UPGRADE", "ESCALATE_TO_HUMAN",
})

PAYMENT_RECOVERY_ACTIONS = frozenset({
    "RETRY_PAYMENT", "SEND_REMINDER",
    "APPLY_GRACE_PERIOD", "ESCALATE_TO_SUPPORT",
})

MIGRATION_ACTIONS = frozenset({
    "IMMEDIATE_PRORATED_MIGRATION", "SCHEDULE_MIGRATION_AT_RENEWAL",
    "PRESERVE_GRANDFATHERED_PRICE", "MIGRATE_WITH_COMPENSATION_DISCOUNT",
    "ESCALATE_TO_HUMAN",
})


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

def validate_metered_usage(decision: MeteredUsageDecision) -> MeteredUsageDecision:
    if decision.action not in METERED_USAGE_ACTIONS:
        return _escalate_usage(f"Unrecognized action: {decision.action}")
    if decision.confidence < CONFIDENCE_THRESHOLD:
        return _escalate_usage(
            f"Low confidence ({decision.confidence:.2f}): {decision.reason}"
        )
    return decision


def validate_payment_recovery(
    decision: PaymentRecoveryDecision,
) -> PaymentRecoveryDecision:
    if decision.action not in PAYMENT_RECOVERY_ACTIONS:
        return _escalate_payment(f"Unrecognized action: {decision.action}")
    if decision.confidence < CONFIDENCE_THRESHOLD:
        return _escalate_payment(
            f"Low confidence ({decision.confidence:.2f}): {decision.reason}"
        )
    return decision


def validate_migration(decision: MigrationDecision) -> MigrationDecision:
    if decision.action not in MIGRATION_ACTIONS:
        return _escalate_migration(f"Unrecognized action: {decision.action}")
    if decision.confidence < CONFIDENCE_THRESHOLD:
        return _escalate_migration(
            f"Low confidence ({decision.confidence:.2f}): {decision.reason}"
        )
    return decision


# ---------------------------------------------------------------------------
# Escalation helpers
# ---------------------------------------------------------------------------

def _escalate_usage(reason: str) -> MeteredUsageDecision:
    return MeteredUsageDecision(
        action="ESCALATE_TO_HUMAN", reason=reason, confidence=1.0,
    )


def _escalate_payment(reason: str) -> PaymentRecoveryDecision:
    return PaymentRecoveryDecision(
        action="ESCALATE_TO_SUPPORT", reason=reason, confidence=1.0,
    )


def _escalate_migration(reason: str) -> MigrationDecision:
    return MigrationDecision(
        action="ESCALATE_TO_HUMAN", reason=reason, confidence=1.0,
    )
