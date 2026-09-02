# Commercial consistency audit — Fathom Analytics

**We found 4 commercial promises worth checking.**

Source: https://usefathom.com/ · 10 public pages read · 15 commercial promises extracted · 25 quotes verified against their source page · 2026-09-02 07:57:21 UTC

## What you appear to sell

- **Up to 500,000 pageviews** — $45 /month
- **Larger pageview tiers (2M, 10M, 25M+)** — priced by pageview band; largest tiers contact us

## 1. Your pricing page promises you will never switch analytics off for going over; your terms reserve the right to suspend the account

`high impact` · `Likely contradiction` · `high confidence`

The FAQ on your pricing page is written to remove exactly this worry: you will never turn someone's analytics off over a traffic spike, and if they go over two months running you simply offer an upgrade, which they can take or leave with no hard feelings. Your terms and conditions describe a different process. There, a customer who does not upgrade within seven days of being asked can have their account suspended, and an account left suspended for two months can be deleted — with no refund. The terms also add a trigger the FAQ never mentions: significantly exceeding the limit inside the first month, judged at your sole discretion. For a company whose whole brand is candour about pricing, this is the one page where the reassurance does not hold.

**What one page says:** Analytics are never switched off for going over; the customer chooses whether to upgrade or leave
> We'll never turn your analytics off for occasional traffic spikes or if a payment fails the first time
> — [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Failing to upgrade within seven days can lead to suspension, and continued suspension to deletion, with no refund
> In the event you fail to upgrade your account within seven days of our request, we reserve the right to suspend your account and restrict your use of our Services anytime after the seventh day following our notice to you.
> — [https://usefathom.com/legal/terms](https://usefathom.com/legal/terms)

*Why this is not just wording: "We'll never turn your analytics off" and "we reserve the right to suspend your account and restrict your use of our Services" describe opposite outcomes for the same customer in the same situation.*

*What would make this a non-issue: The terms describe a right you may never exercise, and the FAQ describes what you actually do in practice. Most companies have this gap; it is more visible here because the FAQ makes such a specific promise. Softening "never" to "we won't" and mentioning the first-month trigger would close it.*

## 2. "Full API access" is on the pricing page; the $19–$399 a month you may need to pay for it is not

`high impact` · `Missing information` · `high confidence`

Your pricing page lists "Full API access with 600 requests per hour included" as a plan feature, in a list whose other entries end with reassurances like "No extra fees". A separate page reveals that 600 requests an hour is Tier 1 of a six-tier paid ladder, and that going beyond it costs $19, $39, $79, $199 or $399 a month. The top tier is nearly nine times the price of the $45 plan it sits on top of. Anyone sizing a real integration — the person most likely to care about the API at all — will build their business case from the pricing page and find the ladder only after they hit a 429.

**What one page says:** The plan includes full API access with 600 requests per hour
> Full API access with 600 requests per hour included.
> — [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** API throughput above the included allowance is a paid upgrade costing up to $399 a month
> Tier 6 | $399/mo | 16,000 | 25
> — [https://usefathom.com/api/v1/rate-limits](https://usefathom.com/api/v1/rate-limits)

*Why this is not just wording: The pricing page names no price for API capacity at all, while the other page prices it in six steps up to $399 a month, so a reader of the pricing page cannot arrive at the real cost of the product they are buying.*

*What would make this a non-issue: 600 requests an hour is generous for dashboard-style use, and most customers will never leave Tier 1. The issue is that the word "Full" is doing a lot of work in a list that otherwise advertises the absence of extra fees.*

## 3. Event tracking is advertised with "no extra fees", but events are counted as pageviews, which is what your price is based on

`medium impact` · `Ambiguity` · `medium confidence`

Your feature list says conversions, revenue and custom events are tracked on every plan with no extra fees. An FAQ answer much further down the same page confirms that custom events and API requests are counted as if they were pageviews. Since the plan price is set entirely by monthly pageviews, heavy event tracking does raise the bill — it moves the customer into a higher band, and by the terms it can eventually force an upgrade. Both statements are true; read in sequence they land as a contradiction.

**What one page says:** Event and ecommerce tracking is included on every plan with no extra fees
> Track conversions, revenue, and custom events on every plan. No extra fees.
> — [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Custom events and API requests consume the pageview allowance that sets the price
> those requests will be counted as if they were pageviews
> — [https://usefathom.com/pricing](https://usefathom.com/pricing)

*Why this is not just wording: "No extra fees" and "counted as if they were pageviews" have different consequences for the invoice, because pageviews are the only thing your price depends on.*

*What would make this a non-issue: "No extra fees" is fair if it means there is no separate line item for events, which is true. The two statements are roughly two thousand words apart on the page, so few readers will see both — which is also why it is worth a sentence next to the feature.*

## 4. You state you have never given a discount, while your help centre carries an article called "Discount codes"

`low impact` · `Ambiguity` · `medium confidence`

Your pricing FAQ is emphatic: never any sales or discounts, not even Black Friday, because everyone pays exactly the same price. That claim is part of your positioning. Every documentation page we read carries a help-centre link titled "Discount codes". If discount codes exist for partners, non-profits or migrations, then "everyone pays the exact same price" needs a qualifier; if they do not, the article title is misleading.

**What one page says:** There have never been and will never be discounts; everyone pays the same price
> We've never done discounts, nor will we ever.
> — [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** The help centre documents discount codes
> Discount codes
> — [https://usefathom.com/docs/integrations](https://usefathom.com/docs/integrations)

*Why this is not just wording: A help article dedicated to discount codes implies a mechanism for paying less than list price, which is what the pricing FAQ says does not exist.*

*What would make this a non-issue: This is the weakest item here and we want to be straight about why: we only saw the article's title in a navigation sidebar, not its contents. The article may explain that Fathom does not issue discount codes, or cover codes from a bundle or acquisition. Thirty seconds of checking settles it.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Simple and sustainable pricing - Fathom Analytics](https://usefathom.com/pricing) | Pricing page | 940 | read |
| [Fathom Analytics](https://app.usefathom.com/register) | Trial / signup | 0 | too little text to read |
| [Fathom Analytics](https://app.usefathom.com/register?plan=price_1OMiuQJpbH9soFseaah1xMDb) | Trial / signup | 0 | too little text to read |
| [Rate limits and concurrency · Fathom Analytics API](https://usefathom.com/api/v1/rate-limits) | Usage limits / quotas | 176 | read |
| [Integrations - Fathom Analytics](https://usefathom.com/docs/integrations) | Add-ons & integrations | 540 | read |
| [Get help with Fathom Analytics](https://usefathom.com/docs) | Product documentation | 298 | read |
| [Fathom Analytics API](https://usefathom.com/api/v1) | Product documentation | 108 | too little text to read |
| [WordPress - Fathom Analytics](https://usefathom.com/docs/integrations/wordpress) | Add-ons & integrations | 1399 | read |
| [Privacy law compliance - Fathom Analytics](https://usefathom.com/legal/compliance) | Terms / legal | 1292 | read |
| [Fathom Analytics Terms and Conditions](https://usefathom.com/legal/terms) | Terms / legal | 2199 | read |
| [Discourse - Fathom Analytics](https://usefathom.com/docs/integrations/discourse) | Add-ons & integrations | 838 | read |
| [Kit - Fathom Analytics](https://usefathom.com/docs/integrations/convertkit) | Add-ons & integrations | 562 | read |
| [Webflow - Fathom Analytics](https://usefathom.com/docs/integrations/webflow) | Add-ons & integrations | 553 | read |
| https://usefathom.com/api/llms.txt | — | — | skipped: content-type text/plain; charset=utf |
| https://usefathom.com/faq | — | — | HTTP 404 |
| https://usefathom.com/help | — | — | HTTP 404 |

## What we could not check

Discovery did not reach the help articles behind the sidebar titles — "Exceeding your plan limits", "Billing FAQ", "How do free trials work?", "Discount codes" and "Upgrading or downgrading" — which are the pages most likely either to resolve or to worsen the findings above. Nothing we read says whether a credit card is required to begin the 7-day trial. The pricing page's slider shows one pageview band at a time, so we could only read the $45 / 500,000 band and not the prices of the other tiers.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.