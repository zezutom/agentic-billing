# Cronitor: commercial consistency audit

**We found 2 commercial promises worth checking.**

https://cronitor.io/ | 9 pages read | 18 promises extracted | 25 quotes verified | 2026-09-02 07:57:19 UTC

## What you appear to sell

- **Hacker**: $0 free forever
- **Business**: $2 /mo per monitor plus $5 /mo per user
- **Enterprise**: from $6,000 /yr annual invoice billing

## 1. Pricing page sells unlimited API requests. Docs document rate limits.

`medium` `Ambiguity` `high confidence`

The docs never publish the numbers, so a developer cannot size an integration before building it.

**What one page says:** Unlimited API requests
> Unlimited API requests
> [https://cronitor.io/pricing](https://cronitor.io/pricing)

**What another page says:** Rate limited, 429 on excess
> The API has rate limits to ensure fair usage. If you exceed these limits, you'll receive a 429 Too Many Requests response.
> [https://cronitor.io/docs/api](https://cronitor.io/docs/api)

*Why this is not just wording: Unlimited and refused with a 429 past an unpublished ceiling are different answers to how much you can send.*

*What would make this a non-issue: A rate limit caps speed, not volume, so both can be true. One line on the pricing page would close it.*

## 2. SSO guide names the plan requirement. It omits the $5 per user charge.

`medium` `Missing information` `medium confidence`

An admin who follows the guide upgrades to Business and meets the surcharge on the next invoice. On twenty seats that is $100 a month.

**What one page says:** SSO costs $5 per user extra
> SAML SSO (+$5/mo per user)
> [https://cronitor.io/pricing](https://cronitor.io/pricing)

**What another page says:** Just subscribe to Business
> Note: If the button is disabled, ensure your team is subscribed to the Business plan.
> [https://cronitor.io/docs/saml-sso](https://cronitor.io/docs/saml-sso)

*Why this is not just wording: One page states a per-user charge the other omits while answering what a customer needs to use the feature.*

*What would make this a non-issue: The guide is not wrong, a Business subscription genuinely is required. Six more words would make it complete.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Simple Pricing - Cronitor](https://cronitor.io/pricing) | Pricing page | 495 | read |
| [Sign Up - Cronitor](https://cronitor.io/sign-up) | Trial / signup | 33 | too little text to read |
| [Sign Up - Cronitor](https://cronitor.io/sign-up?flow=trial&plan=metered&billing_frequency=month) | Trial / signup | 89 | too little text to read |
| [Integrations](https://cronitor.io/docs/integrations) | Add-ons & integrations | 288 | read |
| [Help Center - Cronitor](https://cronitor.io/help) | Help centre | 105 | too little text to read |
| [Cronitor Developer Docs](https://cronitor.io/docs) | Product documentation | 214 | read |
| [Cronitor API Docs](https://cronitor.io/docs/api) | Product documentation | 738 | read |
| [Developer Guides - Learn best practices for monitoring mod](https://cronitor.io/guides) | Help centre | 799 | read |
| [How to find and read crontab logs](https://cronitor.io/guides/where-are-cron-logs-stored) | Help centre | 292 | read |
| [SDKs & Agents](https://cronitor.io/docs/sdks) | Product documentation | 214 | read |
| [Configuring SAML SSO](https://cronitor.io/docs/saml-sso) | Product documentation | 844 | read |
| [[Cron] Job Monitoring](https://cronitor.io/docs/cron-job-monitoring) | Product documentation | 881 | read |
| https://cronitor.io/terms | | | blocked by robots.txt |
| https://cronitor.io/faq | | | HTTP 404 |

## What we could not check

Both signup pages and the help centre returned almost no readable text, so we could not check whether the 14-day trial requires a credit card, or whether the help centre repeats the pricing page's figures. The API documentation states that rate limits exist but never publishes the numbers, so we could not check them against the unlimited claim. We saw no terms of service page, so renewal, refund and price-change terms were not reviewed.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.