# Agentic Billing

A runnable prototype demonstrating **AI-native billing orchestration** — the idea that billing-related events can be received by an application, interpreted by an LLM-based decision layer, and routed to appropriate actions, while actual financial operations remain firmly under human and system control.

This repository contains three independent examples, each using a different orchestration or observability framework, all sharing a common set of models, configuration, and validation logic.

## Also in this repository: the public commercial-consistency auditor

`src/promise_audit/` is a separate, self-contained prototype that asks the public half of
the same question this repository asks internally: **does what a company promises its
customers actually hold together?**

Point it at a SaaS company's homepage and it finds the pricing page, discovers the docs,
help articles, FAQs and terms that make commercial promises, extracts those promises as
structured claims, and reports where the company's own pages disagree. Each finding is backed
by two verbatim quotes and two links. No LLM, no database, no authentication; public pages
only.

```bash
pip install requests beautifulsoup4 lxml
PYTHONPATH=src python -m promise_audit.cli https://example.com --name "Example"
```

See [PROMISE_AUDIT.md](PROMISE_AUDIT.md) for full instructions, the ten-company batch
experiment in `results/experiment/EXPERIMENT_REPORT.md`, and
[RECOMMENDATION.md](RECOMMENDATION.md) for whether it is worth publishing.

## Architecture

The core pattern in every example is the same:

1. **Event handler** receives a billing event (usage report, failed payment, migration request).
2. **Decision context** is built from the event data — plan type, amounts, retry counts, tenure, etc.
3. **LLM decision** is requested using structured outputs. The model must choose from a constrained set of actions and return its reasoning and confidence level.
4. **Deterministic validation** checks the action against the allowed set and a confidence threshold. Low-confidence or unexpected decisions are escalated to human review.
5. **Simulated execution** prints what would happen in a real system (API calls, emails, tickets). No real financial operations are performed.

The LLM is a decision advisor, not an executor. Every decision passes through validation before any action — simulated or otherwise — is taken.

## Repository Structure

```
.
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
└── src/
    └── agentic_billing/
        ├── __init__.py
        ├── config.py                        # Environment variable access
        ├── llm.py                           # Shared LLM client (instructor + OpenAI)
        ├── models.py                        # Pydantic models for events and decisions
        ├── validation.py                    # Deterministic validation logic
        │
        ├── metered_usage/                   # Example 1: LangGraph
        │   ├── graph.py                     # State graph: record → decide → validate → execute
        │   └── run.py                       # Entry point with sample events
        │
        ├── failed_payment/                  # Example 2: Temporal
        │   ├── activities.py                # Temporal activities (LLM, validation, execution)
        │   ├── workflows.py                 # Durable workflow definition
        │   └── run.py                       # Entry point with sample events
        │
        └── subscription_migration/          # Example 3: Langfuse
            ├── evaluator.py                 # Migration evaluation with Langfuse tracing
            ├── dataset.py                   # Representative test scenarios
            └── run.py                       # Entry point with evaluation summary
```

## Prerequisites

- Python 3.11+
- An OpenAI API key (or compatible API)
- [Temporal CLI](https://docs.temporal.io/cli) (for the failed payment example only)
- [Langfuse account](https://langfuse.com) (for the subscription migration example, optional)

## Setup

```bash
# Clone the repository
git clone <repo-url> && cd agentic-billing

# Create a virtual environment and install
python -m venv .venv
source .venv/bin/activate
pip install -e .

# Configure environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `OPENAI_API_KEY` | Yes | — | OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | Model to use for decisions |
| `TEMPORAL_ADDRESS` | No | `localhost:7233` | Temporal server address |
| `LANGFUSE_SECRET_KEY` | No | — | Langfuse secret key |
| `LANGFUSE_PUBLIC_KEY` | No | — | Langfuse public key |
| `LANGFUSE_HOST` | No | `https://cloud.langfuse.com` | Langfuse host URL |

## Running the Examples

### 1. Metered Usage (LangGraph)

```bash
python -m agentic_billing.metered_usage.run
```

Processes three sample usage events through a LangGraph state graph:
- Low usage (450/1000) → expects `NO_ACTION`
- Near limit (8500/10000) → expects `NOTIFY_THRESHOLD`
- Over limit (1847/1000) → expects `RECOMMEND_PLAN_UPGRADE`

Each event flows through: **record usage → LLM decision → validation → simulated execution**.

### 2. Failed Payment Recovery (Temporal)

First, start a local Temporal dev server:

```bash
temporal server start-dev
```

Then, in another terminal:

```bash
python -m agentic_billing.failed_payment.run
```

Runs four sample failed payment events as Temporal workflows:
- First failure, transient error → expects `RETRY_PAYMENT`
- Multiple retries, insufficient funds → expects `SEND_REMINDER`
- Enterprise customer, repeated failures → expects `APPLY_GRACE_PERIOD`
- Hard decline after many retries → expects `ESCALATE_TO_SUPPORT`

Each workflow demonstrates Temporal's durable execution: **decide → validate → execute**, with each step as a separate activity.

### 3. Subscription Migration Evaluation (Langfuse)

```bash
python -m agentic_billing.subscription_migration.run
```

Evaluates five migration scenarios against expected outcomes:
- Standard upgrade at renewal
- Mid-cycle upgrade with small price change
- Grandfathered enterprise customer
- Loyal customer with large price jump
- Ambiguous mid-cycle grandfathered scenario

This example focuses on **evaluation and observability**. It does not execute actions — it recommends them and records decision traces. If Langfuse credentials are configured, all traces appear in your Langfuse dashboard. The example runs without Langfuse too, just without tracing.

## What Each Example Proves

| Example | Framework | Proves |
|---|---|---|
| Metered usage | LangGraph | An LLM can inspect event data and make different decisions based on usage patterns, integrated into a stateful graph pipeline |
| Failed payment | Temporal | LLM-based decisions can be embedded in durable workflows with retry guarantees and activity-level isolation |
| Subscription migration | Langfuse | LLM decisions can be traced, scored, and evaluated against a dataset of expected outcomes for quality assurance |

## Safety Boundaries

This prototype is designed with explicit safety constraints:

- **AI does not move money.** All financial operations (charges, refunds, plan changes) are simulated with print statements. The LLM recommends actions; it never executes them.
- **Actions are constrained.** Each decision model uses `Literal` types to restrict the LLM to a fixed set of allowed actions. The model cannot invent new actions.
- **Decisions are validated.** Every LLM output passes through deterministic validation that checks the action is in the allowed set and the confidence meets a minimum threshold.
- **Uncertain cases escalate.** If the LLM's confidence is below 0.7 or the action is unrecognized, the system automatically routes to human review (`ESCALATE_TO_HUMAN` or `ESCALATE_TO_SUPPORT`).

## Out of Scope

The following are intentionally excluded from this prototype:

- **Real payment processing** — no Stripe, no payment gateways, no real money movement
- **Production databases** — no persistent storage; events are defined inline as sample data
- **Authentication / authorization** — no API keys, user sessions, or access control
- **Production deployment** — no Docker, Kubernetes, or CI/CD configuration
- **Multi-tenant isolation** — all examples run as single-tenant local scripts
- **Real email / notification delivery** — all side effects are print statements

This is a proof of concept. It demonstrates the decision architecture, not a production billing system.
