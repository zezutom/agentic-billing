"""LangGraph flow for metered usage follow-up decisions.

Pipeline: event_handler -> record_usage -> decide_action -> validate -> execute
"""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from agentic_billing.config import get_model
from agentic_billing.llm import get_llm_client
from agentic_billing.models import MeteredUsageDecision, MeteredUsageEvent
from agentic_billing.validation import validate_metered_usage

SYSTEM_PROMPT = """\
You are a billing operations assistant analyzing metered usage events.

Given a usage event, decide the appropriate follow-up action based on:
- The customer's current plan and included units
- How many units have been consumed
- The ratio of used to included units

Guidelines:
- Usage under 80% of included units: NO_ACTION
- Usage between 80-100% of included units: NOTIFY_THRESHOLD
- Usage exceeding included units: RECOMMEND_PLAN_UPGRADE
- Ambiguous or unusual patterns: ESCALATE_TO_HUMAN

Return your decision with a clear reason and your confidence level (0.0 to 1.0).\
"""


class UsageState(TypedDict):
    event: dict[str, Any]
    decision: dict[str, Any]
    result: str


# ---------------------------------------------------------------------------
# Graph nodes
# ---------------------------------------------------------------------------

def record_usage(state: UsageState) -> dict:
    """Simulate reporting usage to an external billing platform."""
    event = MeteredUsageEvent(**state["event"])
    usage_pct = (event.used_units / event.included_units) * 100

    print("\n--- Record Usage ---")
    print(f"  [Billing API] POST /v1/usage/report")
    print(f"  Customer:  {event.customer_id}")
    print(f"  Plan:      {event.plan}")
    print(f"  Usage:     {event.used_units:,} / {event.included_units:,} {event.unit_type} ({usage_pct:.0f}%)")
    # In production: billing_api.record_usage(customer_id, used_units)
    return {}


def decide_action(state: UsageState) -> dict:
    """Call the LLM to decide the follow-up action."""
    event = MeteredUsageEvent(**state["event"])
    client = get_llm_client()

    decision = client.chat.completions.create(
        model=get_model(),
        response_model=MeteredUsageDecision,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Usage event:\n{event.model_dump_json(indent=2)}"},
        ],
    )

    print("\n--- LLM Decision ---")
    print(f"  Action:     {decision.action}")
    print(f"  Reason:     {decision.reason}")
    print(f"  Confidence: {decision.confidence:.2f}")
    return {"decision": decision.model_dump()}


def validate_action(state: UsageState) -> dict:
    """Apply deterministic validation rules."""
    original = MeteredUsageDecision(**state["decision"])
    validated = validate_metered_usage(original)

    print("\n--- Validation ---")
    if validated.action != original.action:
        print(f"  ESCALATED: {original.action} -> {validated.action}")
        print(f"  Reason:    {validated.reason}")
    else:
        print(f"  Passed:    {validated.action} (confidence {validated.confidence:.2f})")
    return {"decision": validated.model_dump()}


def execute_action(state: UsageState) -> dict:
    """Simulate executing the decided action."""
    decision = MeteredUsageDecision(**state["decision"])
    event = MeteredUsageEvent(**state["event"])

    print("\n--- Execute Action ---")
    match decision.action:
        case "NO_ACTION":
            print("  [Skip] Usage within normal limits — no action needed.")
        case "NOTIFY_THRESHOLD":
            print(f"  [Email Service] Sending threshold alert to {event.customer_id}")
            print(f"  # email_service.send_threshold_alert('{event.customer_id}', usage_pct)")
        case "RECOMMEND_PLAN_UPGRADE":
            print(f"  [CRM] Creating upgrade recommendation for {event.customer_id}")
            print(f"  # crm.create_upgrade_opportunity('{event.customer_id}', suggested_plan='next_tier')")
        case "ESCALATE_TO_HUMAN":
            print(f"  [Ticketing] Creating human review ticket for {event.customer_id}")
            print(f"  # ticketing.create_ticket('{event.customer_id}', reason='{decision.reason}')")

    return {"result": f"Executed: {decision.action}"}


# ---------------------------------------------------------------------------
# Graph assembly
# ---------------------------------------------------------------------------

def build_graph():
    builder = StateGraph(UsageState)
    builder.add_node("record_usage", record_usage)
    builder.add_node("decide_action", decide_action)
    builder.add_node("validate_action", validate_action)
    builder.add_node("execute_action", execute_action)

    builder.add_edge(START, "record_usage")
    builder.add_edge("record_usage", "decide_action")
    builder.add_edge("decide_action", "validate_action")
    builder.add_edge("validate_action", "execute_action")
    builder.add_edge("execute_action", END)

    return builder.compile()


# ---------------------------------------------------------------------------
# Event handler — public entry point
# ---------------------------------------------------------------------------

def handle_usage_event(event: MeteredUsageEvent) -> str:
    """Receive a metered usage event and run the full decision pipeline."""
    graph = build_graph()
    result = graph.invoke({
        "event": event.model_dump(),
        "decision": {},
        "result": "",
    })
    return result["result"]
