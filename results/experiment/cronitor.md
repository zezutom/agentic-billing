# Commercial consistency audit — Cronitor

**We found 2 commercial promises worth checking.**

Source: https://cronitor.io/ · 9 public pages read · 18 commercial promises extracted · 25 quotes verified against their source page · 2026-09-02 07:57:19 UTC

## What you appear to sell

- **Hacker** — $0 free forever
- **Business** — $2 /mo per monitor plus $5 /mo per user
- **Enterprise** — from $6,000 /yr annual invoice billing

## 1. Your pricing page sells "unlimited API requests" while your API documentation says the API is rate limited

`medium impact` · `Ambiguity` · `high confidence`

The Business plan is advertised as including unlimited API requests, which a buyer will read as "I will never be cut off". Your API documentation tells a different story: there are rate limits, and exceeding them returns a 429. Both statements can be true at once — a rate limit throttles the speed of requests rather than capping the total — but nothing on either page says so, and the documentation never publishes the actual numbers. The customer who finds out is a developer whose integration has just started failing in production.

**What one page says:** The Business plan includes unlimited API requests
> Unlimited API requests
> — [https://cronitor.io/pricing](https://cronitor.io/pricing)

**What another page says:** The API is rate limited and rejects requests above the limit
> The API has rate limits to ensure fair usage. If you exceed these limits, you'll receive a 429 Too Many Requests response.
> — [https://cronitor.io/docs/api](https://cronitor.io/docs/api)

*Why this is not just wording: "Unlimited" and "you will be refused with a 429 past a limit we do not publish" are different commercial promises, not two phrasings of one.*

*What would make this a non-issue: A throughput limit and a volume allowance really are different things, so this is a clarity problem rather than a broken promise. One sentence on the pricing page, and the actual numbers in the docs, would close it.*

## 2. Your SSO documentation tells customers they need the Business plan, without mentioning that SSO costs an extra $5 per user on top

`medium impact` · `Missing information` · `medium confidence`

Your pricing page is clear that SAML single sign-on is a paid add-on for Business customers at $5 per user per month. Your SSO setup guide tells an administrator who finds the button greyed out simply to make sure the team is on the Business plan. An admin following the documentation reasonably concludes that upgrading to Business is all that is required, and only discovers the per-user surcharge when the bill changes. On a twenty-person team that is an unbudgeted $100 a month.

**What one page says:** SAML SSO is an add-on costing $5 per user per month on Business
> SAML SSO (+$5/mo per user)
> — [https://cronitor.io/pricing](https://cronitor.io/pricing)

**What another page says:** The SSO setup guide gives a Business subscription as the requirement, and says nothing about an additional charge
> Note: If the button is disabled, ensure your team is subscribed to the Business plan.
> — [https://cronitor.io/docs/saml-sso](https://cronitor.io/docs/saml-sso)

*Why this is not just wording: One page states a per-user charge that the other page omits entirely while answering the exact question of what a customer needs in order to use the feature.*

*What would make this a non-issue: The documentation is not wrong — a Business subscription genuinely is required. It is incomplete rather than contradictory, and adding six words to that note would fix it.*

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
| https://cronitor.io/terms | — | — | blocked by robots.txt |
| https://cronitor.io/faq | — | — | HTTP 404 |

## What we could not check

Both signup pages and the help centre returned almost no readable text, so we could not check whether the 14-day trial requires a credit card, or whether the help centre repeats the pricing page's figures. The API documentation states that rate limits exist but never publishes the numbers, so we could not check them against the 'unlimited' claim or against each other. We also saw no terms of service page, so renewal, refund and price-change terms were not reviewed.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.