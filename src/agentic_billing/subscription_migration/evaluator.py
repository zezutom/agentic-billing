"""Subscription migration evaluator with Langfuse tracing.

This module focuses on evaluation and observability rather than orchestration.
It calls the LLM, validates the recommendation, and records the full decision
trace in Langfuse for later review.
"""

from langfuse import Langfuse

from agentic_billing.config import get_langfuse_config, get_model
from agentic_billing.llm import get_llm_client
from agentic_billing.models import MigrationDecision, MigrationEvent
from agentic_billing.validation import validate_migration

SYSTEM_PROMPT = """\
You are a subscription migration advisor evaluating plan change requests.

Given a migration request, recommend the best approach based on:
- Whether the customer has a grandfathered (legacy) price
- Whether the request is mid-billing-cycle
- The price difference between plans
- How long the customer has been on their current plan

Guidelines:
- Standard upgrade, not mid-cycle: IMMEDIATE_PRORATED_MIGRATION
- Standard upgrade, mid-cycle with small price difference: SCHEDULE_MIGRATION_AT_RENEWAL
- Grandfathered customer with significant price increase and long tenure: PRESERVE_GRANDFATHERED_PRICE
- Upgrade with large price jump for a loyal customer: MIGRATE_WITH_COMPENSATION_DISCOUNT
- Complex or ambiguous scenarios: ESCALATE_TO_HUMAN

Return your decision with a clear reason and your confidence level (0.0 to 1.0).\
"""


def _looks_like_placeholder(value: str) -> bool:
    """Return True if the value is empty or an obvious placeholder from .env.example."""
    if not value:
        return True
    placeholders = {"sk-lf-your-secret-key", "pk-lf-your-public-key", "your-secret-key", "your-public-key"}
    return value.strip() in placeholders


def create_langfuse_client() -> Langfuse | None:
    """Create a Langfuse client if real credentials are configured."""
    config = get_langfuse_config()
    if _looks_like_placeholder(config["secret_key"]) or _looks_like_placeholder(config["public_key"]):
        print("  [Langfuse] No credentials configured — tracing disabled.")
        print("  Set LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY in .env to enable.\n")
        return None
    try:
        return Langfuse(**config)
    except Exception as e:
        print(f"  [Langfuse] Failed to initialize: {e} — tracing disabled.\n")
        return None


def evaluate_migration(
    event: MigrationEvent,
    langfuse: Langfuse | None = None,
    trace_name: str = "migration_evaluation",
) -> MigrationDecision:
    """Evaluate a migration request: prompt the LLM, validate, and trace."""
    client = get_llm_client()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Migration request:\n{event.model_dump_json(indent=2)}"},
    ]

    # Call the LLM
    decision = client.chat.completions.create(
        model=get_model(),
        response_model=MigrationDecision,
        messages=messages,
    )

    # Validate (may escalate)
    validated = validate_migration(decision)
    was_escalated = validated.action != decision.action

    print(f"    Action:     {validated.action}")
    print(f"    Reason:     {validated.reason}")
    print(f"    Confidence: {validated.confidence:.2f}")
    if was_escalated:
        print(f"    (escalated from {decision.action})")

    # Record trace in Langfuse (v4 API: start_observation / score)
    if langfuse:
        span = langfuse.start_observation(
            name=trace_name,
            as_type="span",
            input=event.model_dump(),
            metadata={
                "customer_id": event.customer_id,
                "was_escalated": was_escalated,
            },
        )
        generation = span.start_observation(
            name="migration_decision",
            as_type="generation",
            model=get_model(),
            input=messages,
            output=validated.model_dump(),
        )
        generation.end()
        span.score(name="confidence", value=validated.confidence)
        span.end(output=validated.model_dump())

    return validated
