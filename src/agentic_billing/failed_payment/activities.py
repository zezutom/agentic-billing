"""Temporal activities for the failed payment recovery workflow.

Each activity is a discrete unit of work that runs outside the workflow sandbox
and can perform I/O (LLM calls, validation, simulated execution).
"""

from temporalio import activity

from agentic_billing.config import get_model
from agentic_billing.llm import get_llm_client
from agentic_billing.models import FailedPaymentEvent, PaymentRecoveryDecision
from agentic_billing.validation import validate_payment_recovery

SYSTEM_PROMPT = """\
You are a payment recovery specialist analyzing failed payment events.

Given a failed payment event, decide the best recovery strategy based on:
- Number of retry attempts already made
- Invoice amount
- Customer's plan type
- The failure reason

Guidelines:
- First failure with a transient reason (network error, timeout): RETRY_PAYMENT
- After 1-2 retries or a soft decline (insufficient funds): SEND_REMINDER
- Valued customer (enterprise/business plan) with repeated failures: APPLY_GRACE_PERIOD
- After 3+ retries or a hard decline (card stolen, account closed): ESCALATE_TO_SUPPORT

Return your decision with a clear reason and your confidence level (0.0 to 1.0).\
"""


@activity.defn
async def decide_recovery(event_data: dict) -> dict:
    """Call the LLM to decide the recovery action for a failed payment."""
    event = FailedPaymentEvent(**event_data)
    client = get_llm_client()

    decision = client.chat.completions.create(
        model=get_model(),
        response_model=PaymentRecoveryDecision,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Failed payment event:\n{event.model_dump_json(indent=2)}"},
        ],
    )

    print("\n  --- LLM Decision ---")
    print(f"    Action:     {decision.action}")
    print(f"    Reason:     {decision.reason}")
    print(f"    Confidence: {decision.confidence:.2f}")
    return decision.model_dump()


@activity.defn
async def validate_recovery(decision_data: dict) -> dict:
    """Apply deterministic validation to the LLM's recovery decision."""
    original = PaymentRecoveryDecision(**decision_data)
    validated = validate_payment_recovery(original)

    print("\n  --- Validation ---")
    if validated.action != original.action:
        print(f"    ESCALATED: {original.action} -> {validated.action}")
        print(f"    Reason:    {validated.reason}")
    else:
        print(f"    Passed:    {validated.action} (confidence {validated.confidence:.2f})")
    return validated.model_dump()


@activity.defn
async def execute_recovery(decision_data: dict) -> str:
    """Simulate executing the recovery action."""
    decision = PaymentRecoveryDecision(**decision_data)

    print("\n  --- Execute Action ---")
    match decision.action:
        case "RETRY_PAYMENT":
            print("    [Payment Gateway] Retrying charge...")
            print("    # stripe.PaymentIntent.confirm(payment_intent_id)")
        case "SEND_REMINDER":
            print("    [Email Service] Sending payment reminder...")
            print("    # email_service.send_payment_reminder(customer_id, invoice_id)")
        case "APPLY_GRACE_PERIOD":
            print("    [Billing API] Extending payment deadline by 7 days...")
            print("    # billing_api.extend_due_date(invoice_id, days=7)")
        case "ESCALATE_TO_SUPPORT":
            print("    [Ticketing] Creating support escalation ticket...")
            print("    # ticketing.create_ticket(customer_id, priority='high')")

    return f"Executed: {decision.action}"
