# Fathom Analytics: commercial consistency audit

**We found 4 commercial promises worth checking.**

https://usefathom.com/ | 10 pages read | 15 promises extracted | 25 quotes verified | 2026-09-02 07:57:21 UTC

## What you appear to sell

- **Up to 500,000 pageviews**: $45 /month
- **Larger pageview tiers (2M, 10M, 25M+)**: priced by pageview band; largest tiers contact us

## 1. Pricing page says you never switch analytics off. Terms allow suspension.

`high` `Likely contradiction` `high confidence`

The terms also add a first-month trigger the FAQ never mentions, and an account left suspended two months can be deleted with no refund.

**What one page says:** Never switched off for overage
> We'll never turn your analytics off for occasional traffic spikes or if a payment fails the first time
> [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Suspension after seven days
> In the event you fail to upgrade your account within seven days of our request, we reserve the right to suspend your account and restrict your use of our Services anytime after the seventh day following our notice to you.
> [https://usefathom.com/legal/terms](https://usefathom.com/legal/terms)

*Why this is not just wording: Never turn your analytics off and reserve the right to suspend your account describe opposite outcomes for the same customer.*

*What would make this a non-issue: The terms describe a right you may never use and the FAQ describes what you actually do. Dropping the word never would close it.*

## 2. Pricing page sells full API access. The $19 to $399 ladder is elsewhere.

`high` `Missing information` `high confidence`

600 an hour is Tier 1 of six. The top tier costs nearly nine times the $45 plan it sits on.

**What one page says:** Full API access, 600 per hour
> Full API access with 600 requests per hour included.
> [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Up to $399 a month for more
> Tier 6 | $399/mo | 16,000 | 25
> [https://usefathom.com/api/v1/rate-limits](https://usefathom.com/api/v1/rate-limits)

*Why this is not just wording: The pricing page names no price for API capacity while another page prices it in six steps.*

*What would make this a non-issue: 600 requests an hour is generous and most customers stay on Tier 1. The word Full is doing the work in a list that otherwise advertises no extra fees.*

## 3. Event tracking has no extra fees, but events count as pageviews.

`medium` `Ambiguity` `medium confidence`

Your price is set entirely by monthly pageviews, so heavy event tracking moves a customer into a higher band.

**What one page says:** Events included, no extra fees
> Track conversions, revenue, and custom events on every plan. No extra fees.
> [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Events counted as pageviews
> those requests will be counted as if they were pageviews
> [https://usefathom.com/pricing](https://usefathom.com/pricing)

*Why this is not just wording: No extra fees and counted as pageviews have different consequences for the invoice.*

*What would make this a non-issue: No extra fees is fair if it means no separate line item, which is true. The two statements are about 2,000 words apart on the page.*

## 4. You say you never discount. Your help centre lists an article on discount codes.

`low` `Ambiguity` `medium confidence`

If codes exist for partners or non-profits, everyone pays the exact same price needs a qualifier.

**What one page says:** Never any discounts, ever
> We've never done discounts, nor will we ever.
> [https://usefathom.com/pricing](https://usefathom.com/pricing)

**What another page says:** Help centre: Discount codes
> Discount codes
> [https://usefathom.com/docs/integrations](https://usefathom.com/docs/integrations)

*Why this is not just wording: An article about discount codes implies a way to pay less than list price, which the FAQ says does not exist.*

*What would make this a non-issue: This is the weakest item here. We saw the article title in a sidebar, not its contents, and it may say you do not issue codes.*

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
| https://usefathom.com/api/llms.txt | | | skipped: content-type text/plain; charset=utf |
| https://usefathom.com/faq | | | HTTP 404 |
| https://usefathom.com/help | | | HTTP 404 |

## What we could not check

Discovery did not reach the help articles behind the sidebar titles: Exceeding your plan limits, Billing FAQ, How do free trials work, Discount codes, and Upgrading or downgrading. Those are the pages most likely either to resolve or to worsen the findings above. Nothing we read says whether a credit card is required to begin the 7-day trial. The pricing page's slider shows one pageview band at a time, so we could only read the $45 band for 500,000 pageviews.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.