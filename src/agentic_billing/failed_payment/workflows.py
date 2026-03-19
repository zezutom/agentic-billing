"""Temporal workflow for failed payment recovery.

The workflow orchestrates the decision pipeline with durable execution
guarantees: if the process crashes mid-way, Temporal will resume from the
last completed activity.
"""

from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from agentic_billing.failed_payment.activities import (
        decide_recovery,
        execute_recovery,
        validate_recovery,
    )


@workflow.defn
class PaymentRecoveryWorkflow:
    """Durable workflow: decide -> validate -> execute recovery action."""

    @workflow.run
    async def run(self, event_data: dict) -> str:
        # Step 1: LLM decides the recovery strategy
        decision = await workflow.execute_activity(
            decide_recovery,
            event_data,
            start_to_close_timeout=timedelta(seconds=60),
        )

        # Step 2: Deterministic validation (escalate if confidence is too low)
        validated = await workflow.execute_activity(
            validate_recovery,
            decision,
            start_to_close_timeout=timedelta(seconds=10),
        )

        # Step 3: Simulate executing the chosen action
        result = await workflow.execute_activity(
            execute_recovery,
            validated,
            start_to_close_timeout=timedelta(seconds=10),
        )

        return result
