"""Run the subscription migration evaluation example.

Usage:
    python -m agentic_billing.subscription_migration.run

This runs each scenario from the dataset through the LLM evaluator, records
traces in Langfuse (if configured), and prints a comparison of expected vs
actual outcomes.
"""

from agentic_billing.models import MigrationEvent
from agentic_billing.subscription_migration.dataset import MIGRATION_SCENARIOS
from agentic_billing.subscription_migration.evaluator import (
    create_langfuse_client,
    evaluate_migration,
)


def handle_migration_request(event: MigrationEvent, langfuse=None) -> str:
    """Event handler for subscription migration requests."""
    decision = evaluate_migration(event, langfuse=langfuse)
    # No autonomous execution — this example only recommends actions
    return decision.action


def main():
    print("=" * 60)
    print("  Langfuse Example: Subscription Migration Evaluation")
    print("=" * 60)

    langfuse = create_langfuse_client()

    results = []

    for scenario in MIGRATION_SCENARIOS:
        event = MigrationEvent(**scenario["input"])
        expected = scenario["expected_action"]

        print(f"\n{'─' * 60}")
        print(f"  Scenario: {scenario['name']}")
        print(f"  {event.current_plan} -> {event.requested_plan} "
              f"(${event.current_price:.0f} -> ${event.new_price:.0f})")
        if event.is_grandfathered:
            print(f"  Grandfathered: yes | Tenure: {event.months_on_current_plan} months")
        if event.is_mid_cycle:
            print(f"  Mid-cycle: yes")
        print()

        actual = handle_migration_request(event, langfuse=langfuse)
        match = actual == expected

        results.append({
            "scenario": scenario["name"],
            "expected": expected,
            "actual": actual,
            "match": match,
        })

        status = "MATCH" if match else "MISMATCH"
        print(f"    Expected:   {expected}")
        print(f"    Result:     {status}")

    # Summary
    matches = sum(1 for r in results if r["match"])
    total = len(results)

    print(f"\n{'=' * 60}")
    print(f"  Evaluation Summary: {matches}/{total} matched expected outcomes")
    print(f"{'=' * 60}")
    for r in results:
        icon = "+" if r["match"] else "-"
        print(f"  [{icon}] {r['scenario']}: {r['actual']}")

    if langfuse:
        langfuse.flush()
        print(f"\n  Traces recorded in Langfuse — check your dashboard for details.")


if __name__ == "__main__":
    main()
