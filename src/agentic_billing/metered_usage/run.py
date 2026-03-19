"""Run the metered usage example with sample events.

Usage:
    python -m agentic_billing.metered_usage.run
"""

from agentic_billing.models import MeteredUsageEvent
from agentic_billing.metered_usage.graph import handle_usage_event

SAMPLE_EVENTS = [
    # Low usage — should trigger NO_ACTION
    MeteredUsageEvent(
        customer_id="cust_001",
        plan="starter",
        included_units=1000,
        used_units=450,
        unit_type="API calls",
    ),
    # Approaching limit — should trigger NOTIFY_THRESHOLD
    MeteredUsageEvent(
        customer_id="cust_002",
        plan="professional",
        included_units=10_000,
        used_units=8_500,
        unit_type="API calls",
    ),
    # Well over limit — should trigger RECOMMEND_PLAN_UPGRADE
    MeteredUsageEvent(
        customer_id="cust_003",
        plan="starter",
        included_units=1_000,
        used_units=1_847,
        unit_type="API calls",
    ),
]


def main():
    print("=" * 60)
    print("  LangGraph Example: Metered Usage Follow-Up")
    print("=" * 60)

    for event in SAMPLE_EVENTS:
        print(f"\n{'─' * 60}")
        print(f"  Event: {event.customer_id} | {event.plan} | "
              f"{event.used_units:,}/{event.included_units:,} {event.unit_type}")
        print(f"{'─' * 60}")

        result = handle_usage_event(event)
        print(f"\n  >>> {result}")


if __name__ == "__main__":
    main()
