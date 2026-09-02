# Knock: commercial consistency audit

**We found 2 commercial promises worth checking.**

https://knock.app/ | 8 pages read | 17 promises extracted | 24 quotes verified | 2026-09-02 07:57:24 UTC

## What you appear to sell

- **Developer**: $0 / month
- **Starter**: $250 / month
- **Enterprise**: Contact us

## 1. Pricing page says triggers are unlimited. Every endpoint is rate limited.

`medium` `Ambiguity` `high confidence`

Triggering a workflow is an API call, and the tiers are never mapped to plans or endpoints.

**What one page says:** Unlimited workflow triggers
> Workflow triggers | Unlimited | Unlimited | Unlimited
> [https://knock.app/pricing](https://knock.app/pricing)

**What another page says:** 1 to 1,000 requests per second
> Each endpoint in the Knock API is rate limited. Knock uses a tier system to determine the rate limit scale for each endpoint.
> [https://docs.knock.app/api-reference/overview/rate-limits](https://docs.knock.app/api-reference/overview/rate-limits)

*Why this is not just wording: Unlimited triggers and a per-second ceiling answer the same buyer question with different numbers.*

*What would make this a non-issue: Rate limits and volume allowances are different, and your docs invite customers to ask for more. Naming the tier for the trigger endpoint would fix it.*

## 2. Enterprise guides default to the Starter allowance. Only the FAQ says so.

`medium` `Missing information` `high confidence`

A customer paying well above Starter, who assumed guides scaled with their contract, finds out when you ask them to get in touch.

**What one page says:** Contact us, volume discounts
> Contact us Volume-based discounts and monthly notified user pricing available.
> [https://knock.app/pricing](https://knock.app/pricing)

**What another page says:** 2,500 users, same as Starter
> you'll have the same guides limit as our Starter plan: 2,500 active users a month
> [https://knock.app/pricing](https://knock.app/pricing)

*Why this is not just wording: Contact us invites the reader to assume a negotiated number while the FAQ states a specific default equal to the tier below.*

*What would make this a non-issue: The FAQ is on the same page, forty rows down, under a question aimed at existing customers rather than buyers.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing - Knock](https://knock.app/pricing) | Pricing page | 1856 | read |
| [Subscriptions - Knock Docs](https://docs.knock.app/concepts/subscriptions) | Billing & subscription help | 1150 | read |
| [Workflows API reference - Knock Docs](https://docs.knock.app/api-reference/workflows/cancel) | Billing & subscription help | 509 | read |
| [Users API reference - Knock Docs](https://docs.knock.app/api-reference/users/list_subscriptions) | Billing & subscription help | 3661 | read |
| [API reference - Knock Docs](https://docs.knock.app/reference) | Product documentation | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview) | Product documentation | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview/rate-limits) | Usage limits / quotas | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview/batch-rate-limits) | Usage limits / quotas | 2033 | read |
| https://dashboard.knock.app/signup | | | blocked by robots.txt |

## What we could not check

We did not report the rate-limit tier table that appears on two documentation pages with different numbers in view. It is one table of endpoint scales reproduced on both pages, not two conflicting limits, and an automated reader could easily mistake it for a contradiction. We could not check which tier any given endpoint belongs to, since that mapping is not on the pages we read. Your pricing table promises unlimited feed retention while the API reference refers to data subject to deletion under the retention policy on your account. The retention policy page was not reachable from our crawl, so we could not tell whether these describe the same data and did not report it. The signup page is blocked by robots.txt, so trial and card-requirement terms were not checked.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.