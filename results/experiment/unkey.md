# Commercial consistency audit — Unkey

**We found 2 commercial promises worth checking.**

Source: https://www.unkey.com/ · 10 public pages read · 14 commercial promises extracted · 23 quotes verified against their source page · 2026-09-02 08:08:53 UTC

## What you appear to sell

- **Starter** — $5 / mo
- **Pro** — $25 / mo
- **Business** — $50 / mo
- **Enterprise** — Contact the team; annual contracts available
- **Free plan (documented only in the docs)** — not published on the pricing page

## 1. Your free plan keeps logs longer than the $5 plan and audit logs longer than the $25 plan

`high impact` · `Likely contradiction` · `high confidence`

Your documentation says the free plan retains logs for 7 days and audit logs for 30 days. Your pricing page's comparison table gives Starter, at $5 a month, 3 days of log retention and 7 days of audit log retention — less than free on both counts. Pro, at $25 a month, gets 7 days and 14 days, so it too has less audit log retention than the free plan, and only matches free on ordinary logs. Only Business at $50 finally reaches the free plan's 30 days of audit retention. A customer who upgrades from free to Starter to get a production-grade service will find their observability window has shrunk, which is the opposite of what upgrading is supposed to do.

**What one page says:** The free plan retains logs for 7 days and audit logs for 30 days
> | Audit log retention | 30 days | Varies by plan |
> — [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)

**What another page says:** The paid comparison table gives Starter 3 days of log retention and 7 days of audit log retention, rising to 14 and 30 only on Business
> $5
1
3 days
7 days
Email
> — [https://www.unkey.com/pricing](https://www.unkey.com/pricing)

*Why this is not just wording: These are the same two named metrics, measured in the same unit, and the free tier's numbers are larger than the paid tier's — one of the two pages must be wrong about what a paying customer receives.*

*What would make this a non-issue: We read the paid figures from a comparison grid that is built from styled divs rather than a real table, so column alignment had to be inferred. We checked it against the plan cards and it holds — the same column that gives Starter 3 days also gives it 1 vCPU, 2 GB, 1 custom domain and $5 of usage credits, all of which match the Starter card exactly. Still worth thirty seconds with the live page before acting.*

## 2. Your pricing page says "start for free" but never shows the free plan or what it includes

`medium impact` · `Missing information` · `high confidence`

"Start for free, scale as you go" is the first line of your pricing page and the closing call to action repeats it. The plans below begin at $5 a month, and no free tier appears anywhere on the page. The free plan does exist, and it is specified in your billing documentation with real numbers — 150,000 API requests a month, 7 days of log retention, no team members. A developer evaluating you is told twice that they can start for free and then shown nothing they can start with, which turns the most important question on the page into a support conversation.

**What one page says:** The pricing page invites developers to start for free
> Start for free, scale as you go with predictable usage-based pricing.
> — [https://www.unkey.com/pricing](https://www.unkey.com/pricing)

**What another page says:** The free plan and its allowances exist, but are documented only in the billing docs
> | API requests per month | 150,000 | Varies by plan |
> — [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)

*Why this is not just wording: A whole plan with published quotas is absent from the page whose job is to list the plans, so the pricing page cannot answer what "free" means.*

*What would make this a non-issue: The free tier may be in the process of being retired, or may be offered only at signup. Either way the pricing page still promises it twice.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing - Unkey](https://www.unkey.com/pricing) | Pricing page | 325 | read |
| [What is Unkey? - Unkey Docs](https://www.unkey.com/docs) | Product documentation | 515 | read |
| [Billing - Unkey Docs](https://unkey.com/docs/platform/workspaces/billing) | Billing & subscription help | 327 | read |
| [What is Unkey? - Unkey Docs](https://unkey.com/docs/introduction) | Product documentation | 515 | read |
| [Website Terms of Use - Unkey Inc. - Unkey](https://www.unkey.com/policies/terms) | Terms / legal | 2898 | read |
| [What is Unkey? - Unkey Docs](https://www.unkey.com/docs/introduction) | Product documentation | 515 | read |
| [Regions - Unkey Docs](https://unkey.com/docs/build-and-deploy/regions) | Product documentation | 149 | read |
| [Observability - Unkey Docs](https://unkey.com/docs/observability/overview) | Product documentation | 81 | too little text to read |
| [Overview - Unkey Docs](https://www.unkey.com/docs/api-reference/overview) | Product documentation | 253 | read |
| [Deploy your first app - Unkey Docs](https://www.unkey.com/docs/quickstart/deploy) | Product documentation | 153 | read |
| [Quickstart - Unkey Docs](https://www.unkey.com/docs/quickstart/quickstart) | Product documentation | 903 | read |
| https://www.unkey.com/docs/llms.txt | — | — | skipped: content-type text/plain; charset=utf |
| https://www.unkey.com/faq | — | — | HTTP 404 |
| https://app.unkey.com/auth/sign-up | — | — | HTTP 429 |
| https://app.unkey.com/ | — | — | HTTP 429 |
| https://www.unkey.com/help | — | — | HTTP 404 |
| https://www.unkey.com/terms | — | — | HTTP 404 |

## What we could not check

The pricing page's FAQ rendered as a heading with no questions, so anything it says about the free plan, trials or overage was not visible to us. The pricing page states API request allowances nowhere at all — the docs give the free plan 150,000 a month and say paid plans vary, but no page we read says by how much, so we could not check request quotas against each other. The interactive cost calculator produced a single $188 estimate from its default inputs rather than a price list.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.