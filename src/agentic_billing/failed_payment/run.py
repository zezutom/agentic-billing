"""Run the failed payment recovery example with sample events.

Prerequisites:
    1. Install and start a local Temporal dev server:
       temporal server start-dev

    2. Run this script:
       python -m agentic_billing.failed_payment.run

The script starts an in-process Temporal worker and submits sample workflows.
In production, the worker would run as a separate long-lived process.
"""

import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from agentic_billing.config import get_temporal_address
from agentic_billing.failed_payment.activities import (
    decide_recovery,
    execute_recovery,
    validate_recovery,
)
from agentic_billing.failed_payment.workflows import PaymentRecoveryWorkflow
from agentic_billing.models import FailedPaymentEvent

TASK_QUEUE = "billing-recovery"

SAMPLE_EVENTS = [
    # First failure, transient error — should RETRY_PAYMENT
    FailedPaymentEvent(
        customer_id="cust_101",
        invoice_id="inv_a1",
        amount=49.00,
        retry_count=0,
        plan_type="starter",
        failure_reason="network_timeout",
    ),
    # Multiple retries, soft decline — should SEND_REMINDER
    FailedPaymentEvent(
        customer_id="cust_102",
        invoice_id="inv_b2",
        amount=199.00,
        retry_count=2,
        plan_type="professional",
        failure_reason="insufficient_funds",
    ),
    # Enterprise customer, many retries — should APPLY_GRACE_PERIOD
    FailedPaymentEvent(
        customer_id="cust_103",
        invoice_id="inv_c3",
        amount=2_500.00,
        retry_count=2,
        plan_type="enterprise",
        failure_reason="card_declined",
    ),
    # Hard decline after many retries — should ESCALATE_TO_SUPPORT
    FailedPaymentEvent(
        customer_id="cust_104",
        invoice_id="inv_d4",
        amount=99.00,
        retry_count=4,
        plan_type="starter",
        failure_reason="card_stolen",
    ),
]


async def run_workflows():
    client = await Client.connect(get_temporal_address())

    # Start an in-process worker (in production this runs separately)
    worker = Worker(
        client,
        task_queue=TASK_QUEUE,
        workflows=[PaymentRecoveryWorkflow],
        activities=[decide_recovery, validate_recovery, execute_recovery],
    )

    worker_task = asyncio.create_task(worker.run())

    try:
        for event in SAMPLE_EVENTS:
            print(f"\n{'─' * 60}")
            print(f"  Event: {event.invoice_id} | {event.plan_type} | "
                  f"${event.amount:.2f} | retry #{event.retry_count} | {event.failure_reason}")
            print(f"{'─' * 60}")

            result = await client.execute_workflow(
                PaymentRecoveryWorkflow.run,
                event.model_dump(),
                id=f"recovery-{event.invoice_id}",
                task_queue=TASK_QUEUE,
            )
            print(f"\n  >>> Workflow result: {result}")
    finally:
        worker_task.cancel()
        try:
            await worker_task
        except asyncio.CancelledError:
            pass


def main():
    print("=" * 60)
    print("  Temporal Example: Failed Payment Recovery")
    print("=" * 60)
    asyncio.run(run_workflows())


if __name__ == "__main__":
    main()
