# Commercial consistency audit — Baserow

**We found 2 commercial promises worth checking.**

Source: https://baserow.io/ · 7 public pages read · 20 commercial promises extracted · 28 quotes verified against their source page · 2026-09-02 07:57:07 UTC

## What you appear to sell

- **Free** — $0
- **Premium** — $10 per user/month billed yearly, $12 billed monthly
- **Advanced** — $18 per user/month billed yearly, $22 billed monthly
- **Enterprise** — On request

## 1. Your pricing page offers Enterprise customers payment by invoice; your FAQ says you only accept credit cards

`medium impact` · `Likely contradiction` · `high confidence`

"Payment by invoice" is listed as a reason to choose Enterprise, and it appears again in the plan comparison table. Your FAQ answers the question of what payment methods are accepted with a flat statement that credit card is currently the only option. An enterprise buyer doing diligence — exactly the buyer who cannot put a five-figure annual contract on a corporate card — will read the FAQ and conclude that you cannot invoice them.

**What one page says:** Enterprise customers can pay by invoice
> Payment by invoice
> — [https://baserow.io/pricing](https://baserow.io/pricing)

**What another page says:** Credit card is the only payment method accepted
> Currently, you can pay only with a credit card. We plan to add more payment methods in the future.
> — [https://baserow.io/faq](https://baserow.io/faq)

*Why this is not just wording: One page names invoicing as a purchasable Enterprise benefit and the other states that no payment method other than credit card exists; those are different facts, not different phrasings.*

*What would make this a non-issue: The FAQ answer is almost certainly about self-serve checkout, where credit card genuinely is the only route, and invoicing is arranged through sales. As written, though, neither page says so, and the FAQ is the page a buyer searches.*

## 2. Every paid plan is capped at the same 10 concurrent API requests, and your plan comparison never mentions it

`medium impact` · `Missing information` · `medium confidence`

Your pricing page sells usage that scales with price: rows go from 3,000 to 1,000,000 and automation credits from 2,000 to 2,000,000 across the tiers. API throughput does not scale at all. The FAQ discloses a flat ceiling of 10 concurrent requests for every Baserow Cloud plan, adds that it is subject to fair use, and reserves the right to lower it. For a product that markets itself as API-first, a customer sizing an integration against the Advanced tier has no way of learning from the pricing page that paying nine times more buys no additional API concurrency.

**What one page says:** Usage allowances scale by plan on the pricing page — Advanced buys 250,000 rows per workspace
> 250,000 rows per workspace
> — [https://baserow.io/pricing](https://baserow.io/pricing)

**What another page says:** API concurrency is fixed at 10 for every Cloud plan and may be reduced at Baserow's discretion
> In Baserow Cloud, there's a limit of 10 concurrent API requests. This limit is subject to a fair use policy, and we reserve the right to lower it if it affects overall performance.
> — [https://baserow.io/faq](https://baserow.io/faq)

*Why this is not just wording: The plan comparison lists every other usage dimension by tier and omits this one entirely, so a reader cannot infer either the cap or the fact that it does not improve with price.*

*What would make this a non-issue: Your pricing page does carry a collapsed FAQ item titled "What are the limitations in records, rows, and API requests?", so the answer may be one click away rather than on another page. We could not read the collapsed panel, only its heading.*

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
| https://baserow.io/help | — | — | HTTP 404 |
| https://baserow.io/terms | — | — | HTTP 404 |

## What we could not check

The plan comparison table on the pricing page is built from styled divs rather than a real table, so when it is flattened to text the values lose their column alignment. Several rows publish three values for four plans (row change history, application users), which may be a genuine gap or may just be how the grid collapses — we could not tell, and did not report it. The Premium plan advertises a "Free trial" with no length stated on any page we read, and nothing anywhere states whether a credit card is required to start it.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.