# Commercial consistency audit — Knock

**We found 2 commercial promises worth checking.**

Source: https://knock.app/ · 8 public pages read · 17 commercial promises extracted · 24 quotes verified against their source page · 2026-09-02 07:57:24 UTC

## What you appear to sell

- **Developer** — $0 / month
- **Starter** — $250 / month
- **Enterprise** — Contact us

## 1. Your pricing page says workflow triggers are unlimited on every plan; your API reference rate limits every endpoint

`medium impact` · `Ambiguity` · `high confidence`

"Unlimited" appears against workflow triggers, notification workflows, channels and recipients for all three plans, including the free one. Triggering a workflow is an API call, and your API reference states plainly that every endpoint is rate limited, on a five-tier scale that starts at one request per second, and returns a 429 when exceeded. The two statements are compatible — a rate limit caps the rate, not the total — but the pricing page does not say so, and the rate-limit tiers are never mapped to plans or to specific endpoints, so a developer sizing a launch cannot work out what throughput they have actually bought.

**What one page says:** Workflow triggers are unlimited on every plan, including the free one
> Workflow triggers | Unlimited | Unlimited | Unlimited
> — [https://knock.app/pricing](https://knock.app/pricing)

**What another page says:** Every API endpoint is rate limited on a tier scale beginning at one request per second, returning 429 when exceeded
> Each endpoint in the Knock API is rate limited. Knock uses a tier system to determine the rate limit scale for each endpoint.
> — [https://docs.knock.app/api-reference/overview/rate-limits](https://docs.knock.app/api-reference/overview/rate-limits)

*Why this is not just wording: "Unlimited triggers" and "one to a thousand requests per second depending on an unpublished endpoint tier" answer the same buyer question — how much can I send — with different numbers.*

*What would make this a non-issue: This is a clarity problem, not a broken promise: rate limits and volume allowances genuinely are different, and your docs invite customers to ask for a higher rate. Naming which tier the trigger endpoint sits in would resolve it in one line.*

## 2. Enterprise customers get the same guides allowance as the $250 Starter plan, and only the FAQ says so

`medium impact` · `Missing information` · `high confidence`

In your comparison table the Enterprise column for guide active users says "Contact us", alongside a note about volume discounts. Every reasonable reading of that is "this number is negotiated, and it will be bigger than Starter's". An FAQ answer near the bottom of the same page says something different: unless guides were explicitly written into the enterprise agreement, an Enterprise customer gets 2,500 active users a month — exactly what Starter includes for $250. A customer paying well above Starter, who assumed guides scaled with their contract, finds out when you ask them to get in touch mid-quarter.

**What one page says:** The Enterprise guides allowance is presented as something to negotiate, with volume discounts available
> Contact us Volume-based discounts and monthly notified user pricing available.
> — [https://knock.app/pricing](https://knock.app/pricing)

**What another page says:** Enterprise defaults to the Starter allowance of 2,500 guide active users a month
> you'll have the same guides limit as our Starter plan: 2,500 active users a month
> — [https://knock.app/pricing](https://knock.app/pricing)

*Why this is not just wording: "Contact us" invites the reader to assume a negotiated, larger number, while the FAQ states a specific default equal to the tier below — that is a fact about the deal, not a phrasing choice.*

*What would make this a non-issue: The FAQ is on the same page as the table, so a thorough reader will find it. It is 40 rows below, under a question addressed to existing Enterprise customers rather than to buyers, and the table itself gives no hint that a default exists.*

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
| https://dashboard.knock.app/signup | — | — | blocked by robots.txt |

## What we could not check

We deliberately did not report the rate-limit tier table appearing on two documentation pages with different numbers in view — it is one table of endpoint scales reproduced on both pages, not two conflicting limits, and an automated reader could easily mistake it for a contradiction. We could not check which tier any given endpoint belongs to, since that mapping is not on the pages we read. Your pricing table promises unlimited feed retention while the API reference refers to data 'subject to deletion according to the data retention policy associated with your account'; the retention policy page was not reachable from our crawl, so we could not tell whether these describe the same data and did not report it. The signup page is blocked by robots.txt, so we could not check trial or card-requirement terms.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.