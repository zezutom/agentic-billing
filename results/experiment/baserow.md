# Baserow: commercial consistency audit

**We found 2 commercial promises worth checking.**

https://baserow.io/ | 7 pages read | 20 promises extracted | 28 quotes verified | 2026-09-02 07:57:07 UTC

## What you appear to sell

- **Free**: $0
- **Premium**: $10 per user/month billed yearly, $12 billed monthly
- **Advanced**: $18 per user/month billed yearly, $22 billed monthly
- **Enterprise**: On request

## 1. Pricing page offers invoicing. FAQ says card only.

`medium` `Likely contradiction` `high confidence`

An enterprise buyer doing diligence reads the FAQ and concludes you cannot invoice them.

**What one page says:** Enterprise pays by invoice
> Payment by invoice
> [https://baserow.io/pricing](https://baserow.io/pricing)

**What another page says:** Credit card only
> Currently, you can pay only with a credit card. We plan to add more payment methods in the future.
> [https://baserow.io/faq](https://baserow.io/faq)

*Why this is not just wording: One page sells invoicing as an Enterprise benefit, the other says no other payment method exists.*

*What would make this a non-issue: The FAQ answer is probably about self-serve checkout, with invoicing arranged through sales. Neither page says so.*

## 2. API concurrency is 10 on every paid plan. The comparison never says so.

`medium` `Missing information` `medium confidence`

Rows scale from 3,000 to 1,000,000 across the tiers. API throughput does not move at all.

**What one page says:** Advanced buys 250,000 rows
> 250,000 rows per workspace
> [https://baserow.io/pricing](https://baserow.io/pricing)

**What another page says:** 10 concurrent requests, any plan
> In Baserow Cloud, there's a limit of 10 concurrent API requests. This limit is subject to a fair use policy, and we reserve the right to lower it if it affects overall performance.
> [https://baserow.io/faq](https://baserow.io/faq)

*Why this is not just wording: Every other usage dimension is listed by tier and this one is absent, so a reader cannot infer either the cap or that it never improves.*

*What would make this a non-issue: Your pricing page carries a collapsed FAQ titled "What are the limitations in records, rows, and API requests?". We could read the heading, not the panel.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing](https://baserow.io/pricing) | Pricing page | 623 | read |
| [FAQ](https://baserow.io/faq) | FAQ | 1163 | read |
| [Create account - Baserow](https://baserow.io/signup) | Trial / signup | 16 | too little text to read |
| [Baserow](https://baserow.io/product/integrations) | Add-ons & integrations | 82 | too little text to read |
| [Welcome back - Baserow](https://baserow.io/subscriptions/new) | Billing & subscription help | 16 | too little text to read |
| [Table of contents](https://baserow.io/docs/index) | Product documentation | 1297 | read |
| [General Terms and Conditions](https://baserow.io/terms-and-conditions) | Terms / legal | 3106 | read |
| [REST API documentation - Baserow](https://baserow.io/api-docs) | Product documentation | 32 | too little text to read |
| [Baserow table of contents](https://baserow.io/user-docs) | Product documentation | 1949 | read |
| [Introduction](https://baserow.io/docs/plugins%2Fintroduction) | Product documentation | 524 | read |
| [Install with Docker](https://baserow.io/docs/installation%2Finstall-with-docker) | Product documentation | 2836 | read |
| https://baserow.io/help | | | HTTP 404 |
| https://baserow.io/terms | | | HTTP 404 |

## What we could not check

The plan comparison on your pricing page is built from styled divs rather than a real table, so per-plan values lose their column alignment when flattened to text. Several rows publish three values for four plans, including row change history and application users. That may be a real gap or an artefact of the flattening, so we did not report it. The Premium plan advertises a free trial with no length stated on any page we read, and nothing says whether a card is required to start it.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.