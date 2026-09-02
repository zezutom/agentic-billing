# Trigger.dev: commercial consistency audit

**We found 4 commercial promises worth checking.**

https://trigger.dev/ | 12 pages read | 21 promises extracted | 33 quotes verified | 2026-09-02 17:35:07 UTC

## What you appear to sell

- **Free**: $0 a month
- **Hobby**: $10 a month
- **Pro**: $50 a month
- **Enterprise**: Custom

## 1. Pricing page says Pro concurrency is 200. Docs say 100.

`high` `Likely contradiction` `high confidence`

Concurrency is the number that decides whether this product fits a workload. Your two pages differ on it by a factor of two.

**What one page says:** Pro limit is 200
> If your tasks require more than the Pro plan limit
> [https://trigger.dev/pricing](https://trigger.dev/pricing)

**What another page says:** Pro limit is 100+
> | Pro | 100+ concurrent runs |
> [https://trigger.dev/docs/limits](https://trigger.dev/docs/limits)

*Why this is not just wording: Both pages state a specific concurrent run ceiling for the same named plan and the numbers differ.*

*What would make this a non-issue: Your plan cards appear to show 20, 50 and 200 against the docs table's 10, 25 and 100, so all three tiers look doubled on one side. The cards lost their row labels when we flattened them, so treat the tier pattern as a prompt to check rather than as proof.*

## 2. Pricing page promises scaling without limits. Docs list limits per tier.

`medium` `Ambiguity` `high confidence`

The limits page sets per-tier ceilings on concurrency, queue size, schedules, preview branches, realtime connections, batches and alert destinations.

**What one page says:** Scale without limits
> Begin for free, invite your team, and scale without limits.
> [https://trigger.dev/pricing](https://trigger.dev/pricing)

**What another page says:** Per-tier limits on eight dimensions
> The limits below apply to Trigger.dev Cloud
> [https://trigger.dev/docs/limits](https://trigger.dev/docs/limits)

*Why this is not just wording: Without limits and a documented ceiling on eight dimensions answer the same question differently.*

*What would make this a non-issue: Read as scale without managing infrastructure, which is your actual pitch, the headline is fair. It sits directly above a grid of tiered numbers, which is what makes it read the other way.*

## 3. Pricing page says you can cap spend. Docs say the cap is soft.

`medium` `Missing information` `high confidence`

Spend can exceed the limit before enforcement applies, and the pricing page does not say so. Anyone setting a cap to protect a budget is relying on the stronger reading.

**What one page says:** Yes, set spend limits and alerts
> Yes. Configure billing alerts in your dashboard's organization settings.
> [https://trigger.dev/pricing](https://trigger.dev/pricing)

**What another page says:** Soft limits, spend can exceed
> not instantaneous hard caps. Usage is evaluated on a short delay, so spend can briefly exceed your limit before enforcement applies.
> [https://trigger.dev/docs/billing-limits](https://trigger.dev/docs/billing-limits)

*Why this is not just wording: A cap that can be exceeded and a cap that cannot are different products for a customer sizing their downside.*

*What would make this a non-issue: The docs are unusually straight about this and most usage-based platforms never say it at all. The gap is that the pricing page answer stops at yes.*

## 4. The Free plan stops at $5 of credits. The limits page omits it.

`medium` `Missing information` `medium confidence`

That $5 is the ceiling a free user actually hits. The page titled Limits says a spend cap is your setting rather than a platform limit, which is not true on Free.

**What one page says:** Free stops at $5 of credits
> On the Free plan, you'll need to upgrade to keep running tasks once the included $5 of credits is used.
> [https://trigger.dev/pricing](https://trigger.dev/pricing)

**What another page says:** Spend caps are not a platform limit
> Looking to cap your monthly spend? That's a setting you control, not a platform limit
> [https://trigger.dev/docs/limits](https://trigger.dev/docs/limits)

*Why this is not just wording: One page describes a platform-imposed spend ceiling and the other says spend ceilings are not platform limits.*

*What would make this a non-issue: The limits page sentence is about the billing limits feature rather than about free credits, so the conflict is one of placement more than of fact.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Cloud Pricing - Trigger.dev](https://trigger.dev/pricing) | Pricing page | 1221 | read |
| [Billing limits and alerts - Trigger.dev](https://trigger.dev/docs/billing-limits) | Billing & subscription help | 211 | read |
| [Limits - Trigger.dev](https://trigger.dev/docs/limits) | Usage limits / quotas | 658 | read |
| [Slack support - Trigger.dev](https://trigger.dev/docs/help-slack) | Help centre | 33 | too little text to read |
| [Usage - Trigger.dev](https://trigger.dev/docs/run-usage) | Usage limits / quotas | 199 | read |
| [Welcome to the Trigger.dev docs - Trigger.dev](https://trigger.dev/docs/introduction) | Product documentation | 544 | read |
| [Errors & Retrying - Trigger.dev](https://trigger.dev/docs/errors-retrying) | Product documentation | 565 | read |
| [Self-hosting overview - Trigger.dev](https://trigger.dev/docs/open-source-self-hosting) | Product documentation | 410 | read |
| [Terms & privacy - Trigger.dev](https://trigger.dev/legal) | Terms / legal | 6164 | read |
| [Frameworks, guides and examples - Trigger.dev](https://trigger.dev/docs/guides/introduction) | Help centre | 1329 | read |
| [AI agents overview - Trigger.dev](https://trigger.dev/docs/guides/ai-agents/overview) | Help centre | 257 | read |
| [Login to Trigger.dev](https://cloud.trigger.dev/) | Trial / signup | 36 | too little text to read |
| [Terms & privacy - Trigger.dev](https://trigger.dev/terms) | Terms / legal | 6164 | read |
| [Tasks: Overview - Trigger.dev](https://trigger.dev/docs/tasks-overview) | Product documentation | 1962 | read |
| https://trigger.dev/faq | | | HTTP 404 |

## What we could not check

Your plan comparison grid is built from styled divs, so the row labels did not survive flattening to text. We could read the values in each column but not always what they measure, and we did not report anything that depended on guessing. The Pro concurrency finding above rests on your own FAQ sentence rather than on the grid. Your terms of service run to about 6,200 words and were truncated to fit the dossier, so we could not check the refund policy that the billing limits page points at. Your legal page and terms page returned the same 6,200 word document at two URLs. Nothing on the pricing page states what the second value in each plan card means, so the word Unlimited appearing in all three cards could not be attributed to a metric.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.