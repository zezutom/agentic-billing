# Unkey: commercial consistency audit

**We found 2 commercial promises worth checking.**

https://www.unkey.com/ | 10 pages read | 14 promises extracted | 23 quotes verified | 2026-09-02 08:08:53 UTC

## What you appear to sell

- **Starter**: $5 / mo
- **Pro**: $25 / mo
- **Business**: $50 / mo
- **Enterprise**: Contact the team; annual contracts available
- **Free plan (documented only in the docs)**: not published on the pricing page

## 1. Free plan keeps logs longer than the $5 plan.

`high` `Likely contradiction` `high confidence`

Pro at $25 still has less audit retention than free. Only Business at $50 matches it.

**What one page says:** Free: 7 days logs, 30 audit
> | Audit log retention | 30 days | Varies by plan |
> [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)

**What another page says:** Starter: 3 days logs, 7 audit
> $5
1
3 days
7 days
Email
> [https://www.unkey.com/pricing](https://www.unkey.com/pricing)

*Why this is not just wording: The same two named metrics, in the same unit, are larger on the free tier than the paid one.*

*What would make this a non-issue: Paid figures come from a grid built from divs, so we checked the column against the plan cards. It also gives Starter 1 vCPU, 2 GB, 1 domain and $5 credits, all matching.*

## 2. Pricing page says start for free. No free plan is shown.

`medium` `Missing information` `high confidence`

The free plan exists with real numbers: 150,000 API requests a month, 7 days of log retention, no team members.

**What one page says:** Start for free, twice on page
> Start for free, scale as you go with predictable usage-based pricing.
> [https://www.unkey.com/pricing](https://www.unkey.com/pricing)

**What another page says:** Free plan is in the docs only
> | API requests per month | 150,000 | Varies by plan |
> [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)

*Why this is not just wording: A whole plan with published quotas is missing from the page whose job is to list the plans.*

*What would make this a non-issue: The free tier may be being retired, or offered only at signup. The pricing page still promises it twice.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing - Unkey](https://www.unkey.com/pricing) | Pricing page | 325 | read |
| [What is Unkey? - Unkey Docs](https://www.unkey.com/docs) | Product documentation | 515 | read |
| [Billing - Unkey Docs](https://unkey.com/docs/platform/workspaces/billing) | Billing & subscription help | 327 | read |
| [What is Unkey? - Unkey Docs](https://unkey.com/docs/introduction) | Product documentation | 515 | read |
| [Website Terms of Use - Unkey Inc. - Unkey](https://www.unkey.com/policies/terms) | Terms / legal | 2898 | read |
| [What is Unkey? - Unkey Docs](https://www.unkey.com/docs/introduction) | Product documentation | 515 | read |
| [Regions - Unkey Docs](https://unkey.com/docs/build-and-deploy/regions) | Product documentation | 149 | read |
| [Observability - Unkey Docs](https://unkey.com/docs/observability/overview) | Product documentation | 81 | too little text to read |
| [Overview - Unkey Docs](https://www.unkey.com/docs/api-reference/overview) | Product documentation | 253 | read |
| [Deploy your first app - Unkey Docs](https://www.unkey.com/docs/quickstart/deploy) | Product documentation | 153 | read |
| [Quickstart - Unkey Docs](https://www.unkey.com/docs/quickstart/quickstart) | Product documentation | 903 | read |
| https://www.unkey.com/docs/llms.txt | | | skipped: content-type text/plain; charset=utf |
| https://www.unkey.com/faq | | | HTTP 404 |
| https://app.unkey.com/auth/sign-up | | | HTTP 429 |
| https://app.unkey.com/ | | | HTTP 429 |
| https://www.unkey.com/help | | | HTTP 404 |
| https://www.unkey.com/terms | | | HTTP 404 |

## What we could not check

The pricing page FAQ rendered as a heading with no questions, so anything it says about the free plan, trials or overage was not visible to us. The pricing page states API request allowances nowhere at all. The docs give the free plan 150,000 a month and say paid plans vary, but no page we read says by how much, so request quotas could not be checked against each other. The cost calculator produced a single $188 estimate from its default inputs rather than a price list.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.