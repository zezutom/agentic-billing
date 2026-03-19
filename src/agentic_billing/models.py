"""Shared data models for billing events and LLM decisions."""

from typing import Literal

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Events
# ---------------------------------------------------------------------------

class MeteredUsageEvent(BaseModel):
    customer_id: str
    plan: str
    included_units: int
    used_units: int
    unit_type: str = "API calls"


class FailedPaymentEvent(BaseModel):
    customer_id: str
    invoice_id: str
    amount: float
    currency: str = "USD"
    retry_count: int
    plan_type: str
    failure_reason: str


class MigrationEvent(BaseModel):
    customer_id: str
    current_plan: str
    requested_plan: str
    is_grandfathered: bool
    is_mid_cycle: bool
    current_price: float
    new_price: float
    months_on_current_plan: int


# ---------------------------------------------------------------------------
# Decisions — Literal types constrain the LLM to the allowed action set
# ---------------------------------------------------------------------------

class MeteredUsageDecision(BaseModel):
    action: Literal[
        "NO_ACTION",
        "NOTIFY_THRESHOLD",
        "RECOMMEND_PLAN_UPGRADE",
        "ESCALATE_TO_HUMAN",
    ]
    reason: str = Field(description="Explanation for the chosen action")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level from 0.0 to 1.0"
    )


class PaymentRecoveryDecision(BaseModel):
    action: Literal[
        "RETRY_PAYMENT",
        "SEND_REMINDER",
        "APPLY_GRACE_PERIOD",
        "ESCALATE_TO_SUPPORT",
    ]
    reason: str = Field(description="Explanation for the chosen action")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level from 0.0 to 1.0"
    )


class MigrationDecision(BaseModel):
    action: Literal[
        "IMMEDIATE_PRORATED_MIGRATION",
        "SCHEDULE_MIGRATION_AT_RENEWAL",
        "PRESERVE_GRANDFATHERED_PRICE",
        "MIGRATE_WITH_COMPENSATION_DISCOUNT",
        "ESCALATE_TO_HUMAN",
    ]
    reason: str = Field(description="Explanation for the chosen action")
    confidence: float = Field(
        ge=0.0, le=1.0, description="Confidence level from 0.0 to 1.0"
    )
