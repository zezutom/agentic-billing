# Commercial consistency audit — ScreenshotOne

**We found 3 commercial promises worth checking.**

Source: https://screenshotone.com/ · 15 public pages read · 17 commercial promises extracted · 27 quotes verified against their source page · 2026-09-02 07:57:31 UTC

## What you appear to sell

- **Free** — $0 — 100 screenshots per month
- **Basic** — $17 per month
- **Growth** — $79 per month
- **Scale** — $259 per month

## 1. Three of your pages give three different answers to what happens when a customer exceeds their plan

`high impact` · `Ambiguity` · `high confidence`

This is the question every API customer asks before they build on you, and your site answers it three ways. The pricing page presents it as a simple per-unit price — go over, pay $0.009 each. The credits documentation adds a condition the pricing page never mentions: overage is billed automatically only if extra charging is enabled, leaving the reader to guess what happens when it is not. The terms of service describe a third outcome, where exceeding plan limits may bring throttling or temporary suspension of access. A developer whose product depends on your API cannot tell whether hitting the limit costs them money, degrades their service, or stops it.

**What one page says:** Going over the plan is simply billed at a per-screenshot rate
> $0.009 per extra
> — [https://screenshotone.com/pricing](https://screenshotone.com/pricing)

**What another page says:** Exceeding plan limits may instead result in throttling or temporary suspension of access
> throttling, or temporary suspension of access
> — [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)

*Why this is not just wording: Paying a few tenths of a cent more, having requests slowed, and losing access are three different outcomes for the same event, not three descriptions of one.*

*What would make this a non-issue: The likely reality is that overage billing is the normal path and throttling is a reserve power for abuse. The docs page's "if extra charging is enabled" is the sentence that most needs finishing: it is the only hint that a customer might have the option switched off, and it never says what happens then.*

## 2. Your terms let you change the usage limits and quotas themselves at any time, not just the price

`medium impact` · `Missing information` · `high confidence`

Most terms of service reserve the right to change prices. Yours goes further and reserves the right to modify usage limits, quotas and plan structures too. The screenshot allowances are the product — 2,000, 10,000 and 50,000 a month are the reason a customer picks one plan over another — so this clause says the thing being bought can be redefined mid-subscription. Nothing on the pricing page hints at it, and no notice period is given anywhere we could read.

**What one page says:** Each plan is sold on a specific monthly screenshot allowance
> 50,000 screenshots
> — [https://screenshotone.com/pricing](https://screenshotone.com/pricing)

**What another page says:** Pricing, features, usage limits, quotas and plan structures may all be changed at any time
> We reserve the right to modify pricing, features, usage limits, quotas, or plan structures at any time.
> — [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)

*Why this is not just wording: A right to change quotas is materially different from a right to change prices, because it can reduce what a customer receives without changing what they pay.*

*What would make this a non-issue: This is a clause you probably have no intention of using against existing customers, and a notice commitment on the pricing page would neutralise it entirely.*

## 3. Your pricing page offers a full refund within 30 days, no questions asked; your credits documentation says unused credits are never refunded

`medium impact` · `Likely contradiction` · `medium confidence`

"Email us within 30 days and we will refund you in full, no questions asked" is an unconditional promise, and it is one of the reasons someone signs up. Your credits page carries a heading that says the opposite for the most common case: no refunds for unused credits. A customer who buys a Scale plan, uses a fraction of the 50,000 screenshots and asks for their money back inside the first month has been told both that they get everything back and that unused credits simply expire.

**What one page says:** A full refund is available for any reason within 30 days
> email us at support@screenshotone.com within 30 days, and we will refund you in full, no questions asked
> — [https://screenshotone.com/pricing](https://screenshotone.com/pricing)

**What another page says:** Unused credits are not refunded; they expire at the end of the cycle
> No refunds for unused credits
> — [https://screenshotone.com/docs/credits](https://screenshotone.com/docs/credits)

*Why this is not just wording: One page promises money back for any reason inside 30 days and the other rules out a refund in the situation where a customer would most often ask for one.*

*What would make this a non-issue: These probably address different things — the 30-day guarantee refunds the subscription fee, while the credits page is explaining that credit balances have no cash value on cancellation. Read in that order they still conflict, and the credits page is the one a cancelling customer lands on.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [ScreenshotOne Pricing — Website Screenshot API Plans](https://screenshotone.com/pricing) | Pricing page | 617 | read |
| [How credits work in ScreenshotOne - ScreenshotOne Docs](https://screenshotone.com/docs/credits) | Usage limits / quotas | 317 | read |
| [ScreenshotOne Integrations](https://screenshotone.com/integrations) | Add-ons & integrations | 483 | read |
| [Get Usage - ScreenshotOne Docs](https://screenshotone.com/docs/get-usage) | Usage limits / quotas | 198 | read |
| [Getting Started - ScreenshotOne Docs](https://screenshotone.com/docs) | Product documentation | 393 | read |
| [Getting Started - ScreenshotOne Docs](https://screenshotone.com/docs/getting-started) | Product documentation | 393 | read |
| [The Screenshot API for Zapier](https://screenshotone.com/integrations/zapier) | Add-ons & integrations | 178 | read |
| [Terms of Service](https://screenshotone.com/terms-of-service) | Terms / legal | 953 | read |
| [Guides - ScreenshotOne Docs](https://screenshotone.com/docs/guides) | Help centre | 153 | read |
| [HTML and URL to PDF Generation API — ScreenshotOne](https://screenshotone.com/pdf-generation-api) | Product documentation | 1305 | read |
| [Fail rendering if the content contains a string - Screensh](https://screenshotone.com/docs/guides/fail-if-content-contains) | Help centre | 282 | read |
| [Upload to S3 - ScreenshotOne Docs](https://screenshotone.com/docs/guides/upload-to-s3) | Help centre | 873 | read |
| [The Screenshot API for Airtable](https://screenshotone.com/integrations/airtable) | Add-ons & integrations | 169 | read |
| [The Screenshot API for Make](https://screenshotone.com/integrations/make) | Add-ons & integrations | 183 | read |
| [The Screenshot API for Bubble](https://screenshotone.com/integrations/bubble) | Add-ons & integrations | 167 | read |
| https://dash.screenshotone.com/sign-up | — | — | blocked by robots.txt |
| https://screenshotone.com/faq | — | — | HTTP 404 |
| https://screenshotone.com/terms | — | — | HTTP 404 |

## What we could not check

This is the most complete set of pages of the ten companies: fifteen pages all readable, with a pricing page that publishes per-plan quotas, rate limits and overage rates inline, and a credits page that explains reset and rollover behaviour properly. What we could not check is what actually happens when extra charging is disabled and the quota runs out — no page we read says. We also could not confirm whether the free tier survives cancellation: the credits page says a cancelled customer is downgraded to the free plan "or if the free plan is not available, you will lose access", without saying when the free plan would not be available.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.