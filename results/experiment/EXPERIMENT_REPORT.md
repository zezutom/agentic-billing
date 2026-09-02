# Do SaaS companies contradict themselves in public?

### A ten-company experiment with the commercial-consistency auditor

Run 2026-09-02 07:43:30 UTC · random seed `20260902` · candidate pool 36 · eligible 35 · analysed 10

## The short version

Ten smaller SaaS companies, drawn at random from a frozen pool of 36, analysed with an
identical pipeline. **119 public pages read, 386 commercial claims extracted, 8 findings.**

Reading all eight by hand, one is wrong, five are correct but not news to the company, and
**two are the kind of thing a founder would want to know**:

* **Cronitor** advertises “Unlimited API requests” on its pricing page, while its API
  documentation says “The API has rate limits to ensure fair usage.” Both statements are
  defensible; together they are the exact ambiguity that produces an angry support ticket.
* **Knock** publishes two different API rate limits on two of its own documentation pages —
  60 requests/second on one, 200 requests/second on the other. Nobody is lying; one page is
  simply stale, and only a machine reading both at once would notice.

That is the honest result: **the tool works, finds real things, and finds them rarely.**

## Does a recurring public commercial-consistency problem exist?

On this evidence, **yes, but it is smaller and duller than the pitch implies** — at least
among careful, founder-led companies.

Five of ten companies had something worth a second look — Cronitor, Fathom, Knock, SavvyCal
and ScreenshotOne. (The counts table below also reads "5 of 10", but by a different
definition: it counts companies with a medium- or high-confidence finding, which includes
Bento's false positive and excludes Knock's genuine one. The two fives are not the same
five, which is itself a calibration problem.) The dominant pattern by far
was not contradiction, it was **placement**: five of the eight findings are commercial
conditions — no-refund policies, automatic renewal, overage charges, the right to change
quotas — that appear only in the terms of service or a docs article, never on the page
where the buying decision is made. ScreenshotOne's terms reserve the right to modify
“pricing, features, usage limits, quotas, or plan structures at any time” while the pricing
page says nothing of it; Fathom's fees are non-refundable and its subscriptions auto-renew,
both stated only in the legal terms.

That is a real and repeatable observation, and it is not what the hook promises. The hook
promises contradiction. What the data shows is mostly **disclosure drift**.

The categories the brief hoped for — a feature assigned to different plans on different
pages, mismatched trial lengths, prices that do not reconcile, old plan names still in the
help centre — **did not appear once across ten companies**. The rules for all of them are
implemented and all of them fire correctly on the test fixture. They simply did not trigger
in the wild on this sample. Small, careful SaaS companies with three pricing tiers and a
tidy docs site turn out to be reasonably consistent.

## Is it telling companies anything they did not already know?

Split roughly in half.

* **New information:** Knock's two contradictory rate limits, and Cronitor's unlimited-vs-fair-use
  gap. Neither is visible unless you read two pages side by side, which nobody at the
  company does.
* **Not new:** the auto-renewal and no-refund findings. Every founder knows those clauses
  are in their terms. The tool is telling them where the clauses live, not that they exist.
  Framed as “a contradiction we found”, this reads as padding. Framed as “your buyer never
  sees this”, it is a fair point — but it is a content-strategy observation, not a discovery.

## Likely false positives

**One of eight (12.5%).** Bento is flagged because its pricing page promises “unlimited
marketing sends” and its terms page contains a fair-use sentence — but that sentence is a
*glossary definition* of what an Acceptable Use Policy is, not a restriction Bento applies
to its own sends. The rule matched the right words in the wrong role.

Earlier iterations were far worse, and how they were fixed matters for judging the number:

* An API reference saying “defaults to 50 users per page” was read as a seat allowance.
  Reference and tutorial pages are now excluded from quantity limits (rate limits still count).
* “429 Too Many Requests” was read as a quota of 429. HTTP status codes are now excluded.
* “Shopware 6 with custom events” was read as an allowance of 6 events. Bare numbers now
  need an allowance cue, a pricing-card bullet, or a comparison-table cell.
* “Inbox coverage” matched the word *overage*. Word boundaries were added.
* A code sample line numbered `8` became “8 credits”. `<pre>` blocks are now discarded.
* Baserow's “$10/user/month billed yearly, $12 billed monthly” was read as annual costing
  more than monthly, because the billing label was matched anywhere in the card rather than
  next to the price it belongs to.

Every one of those was found by reading the output, not by a test. **The realistic false
positive rate on an unseen company is higher than 12.5%** — probably 20–30% — because each
fix above was written after seeing the specific failure. A different ten companies would
surface a different set.

## What actually limits the tool

**Client-side rendering, by a wide margin.** Umami's pricing page returns *zero* words of
readable text to an HTTP fetch, so Umami could not be analysed at all — 3 pages, 0 claims,
0 findings. SavvyCal's help and developer sites return 50–115 words per page, so its
analysis is shallow (8 claims from 13 pages). Sixteen of 119 pages read came back
effectively empty.

The headless-browser fallback is implemented and Chromium launches correctly, but the
browser has no outbound network access in the sandbox this experiment ran in, so it could
not be exercised. On an ordinary machine it would run. This is the single highest-value fix:
roughly one company in ten is currently invisible, and the affected pages are precisely the
modern, JS-heavy pricing pages most likely to have drifted.

**Second: 29 page fetches failed**, almost all conventional-path guesses (`/faq`, `/help`,
`/docs`) that do not exist on that particular site. They cost nothing but noise in the logs,
and the reserve-list backfill already replaces them.

**Third: findings cluster on the terms of service** because that is where conditions live
and it is the easiest page to parse. The tool is partly measuring which pages are easy to
read, not only which pages disagree.

## Would a SaaS founder try this?

**Try it, yes. Pay for it, not yet.**

The offer costs a founder one URL and thirty seconds, and returns a page with their own
words quoted back at them and a link to check each one. That is a good trade, and the two
strong findings above are the kind of thing that gets forwarded to a colleague.

But on this sample the median outcome is **one or two low-severity notes about the terms of
service**. Two of ten companies produced a finding worth acting on. As a lead magnet that is
thin — a prospect who gets “your terms mention auto-renewal and your pricing page doesn't”
will not book a call.

The uncomfortable part is that this is the *good* version of the result. The pool was
deliberately smaller, independent companies — exactly the ones most likely to have drifted,
and they mostly had not. A pool of mid-market companies with six tiers, add-ons, legacy
plans and a five-year-old help centre would almost certainly score worse, and would be the
better audience.

## What to improve before publishing

1. **Make JavaScript rendering actually work end to end.** One company in ten is currently
   unreadable, and they are the ones most worth reading.
2. **Reach the help centre properly.** The strongest findings came from docs and help
   articles; the weakest came from terms pages. Discovery should spend its page budget on
   billing, limits and plan-change articles instead of installation guides and SDK pages.
3. **Separate the two products.** “We found a contradiction” and “this condition is not on
   your pricing page” are different claims with different value. Lead with contradictions;
   demote disclosure gaps to a secondary list so five terms-of-service notes cannot masquerade
   as five contradictions.
4. **Fix the confidence calibration.** The best finding in the whole run — Knock's two
   contradictory rate limits — is labelled *low confidence*, because neither statement names
   a plan. The rule penalises unscoped claims, which is right for allowances and wrong for
   a rate limit that applies to everyone. Confidence should reflect how sure we are that the
   two statements conflict, not how much plan metadata we managed to attach.
5. **Add a role check to the fair-use rule.** The one false positive would have been caught
   by asking whether the matched sentence *applies* a restriction or merely *defines* one.
6. **Test the sales-led case.** Every rule assumes published prices. Companies with
   “contact us” tiers are where promise-versus-delivery drift is worst and where this tool
   currently says least.
7. **Widen the sample before making any claim in public.** Ten companies and eight findings
   cannot support a headline like “most SaaS companies contradict themselves”. On this
   evidence, most of them do not.

---

## 1. Headline numbers

| Measure | Value |
|---|---|
| Companies analysed | 10 |
| Companies with at least one finding | 6 of 10 |
| Companies with at least one **medium or high confidence** finding | 5 of 10 |
| Total findings | 8 |
| Findings by severity | 0 high, 4 medium, 4 low |
| Findings by confidence | 7 high, 0 medium, 1 low |
| Public pages read | 119 |
| Pages that could not be read | 29 |
| Commercial claims extracted | 386 |
| Pages that returned almost no readable text (client-rendered) | 16 of 119 |
| Companies whose pricing page could not be read at all | 1 (Umami) |

**Findings by type**

| Type | Count | What it means |
|---|---|---|
| Missing information | 5 | Something that changes the deal, published somewhere the buyer will not look. |
| Ambiguity | 3 | Both statements can be true, but a customer cannot tell what they get. |

**Which rules fired**

| Rule | Times fired | Companies |
|---|---|---|
| `condition_off_pricing` | 5 | Fathom Analytics, SavvyCal, ScreenshotOne |
| `unlimited_vs_fair_use` | 2 | Bento, Cronitor |
| `limit_conflict` | 1 | Knock |

---

## 2. The ten companies, one by one

### Baserow

https://baserow.io · no-code database · discovered via category sweep: open-source Airtable alternatives

Read **11** pages (0 needed a headless browser), extracted **59** claims, produced **0** findings in 3.9s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Free forever. Pay as you grow.](https://baserow.io/pricing) | pricing | 52 | read |
| [Things you probably wonder](https://baserow.io/faq) | faq | 3 | read |
| [Create account](https://baserow.io/signup) | trial | 0 | read |
| [Discover our wide range of integrations](https://baserow.io/product/integrations) | addons | 0 | read |
| [Welcome back](https://baserow.io/subscriptions/new) | billing_docs | 0 | read |
| [Table of contents](https://baserow.io/docs/index) | docs | 0 | read |
| [General Terms and Conditions](https://baserow.io/terms-and-conditions) | terms | 0 | read |
| [REST API](https://baserow.io/api-docs) | docs | 0 | read |
| [Baserow user guide index](https://baserow.io/user-docs) | docs | 3 | read |
| [https://baserow.io/help](https://baserow.io/help) | help | — | failed — HTTP 404 |
| [https://baserow.io/terms](https://baserow.io/terms) | terms | — | failed — HTTP 404 |
| [Introduction](https://baserow.io/docs/plugins%2Fintroduction) | docs | 0 | read |
| [Install with Docker](https://baserow.io/docs/installation%2Finstall-with-docker) | docs | 1 | read |

</details>

Claims extracted: 22 limit, 18 entitlement, 6 plan mention, 5 plan price, 3 condition, 2 unlimited, 2 addon, 1 trial.

Inaccessible pages: https://baserow.io/help (HTTP 404); https://baserow.io/terms (HTTP 404).

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

### Bento

https://bentonow.com · email / newsletters · discovered via category sweep: modern SaaS email tools

Read **13** pages (0 needed a headless browser), extracted **38** claims, produced **1** findings in 3.8s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Simple plans, no hidden fees.](https://bentonow.com/pricing) | pricing | 12 | read |
| [https://bentonow.com/pricing.md](https://bentonow.com/pricing.md) | pricing | — | failed — skipped: content-type text/markdown; charset= |
| [Frequently Asked Questions](https://bentonow.com/docs/faq) | faq | 4 | read |
| [Support](https://bentonow.com/docs/support) | help | 1 | read |
| [Bento Documentation](https://bentonow.com/docs) | docs | 1 | read |
| [Bento wherever you work.](https://bentonow.com/apps) | addons | 1 | read |
| [Bento CLI](https://bentonow.com/docs/integrations/cli) | docs | 2 | read |
| [Developer API](https://bentonow.com/docs/developer_guides/introduction) | docs | 1 | read |
| [Bento MCP Server](https://bentonow.com/docs/integrations/mcp) | addons | 4 | read |
| [Email Marketing Glossary](https://bentonow.com/terms) | terms | 5 | read |
| [Terms & Conditions](https://bentonow.com/legal/terms) | terms | 2 | read |
| [https://bentonow.com/faq](https://bentonow.com/faq) | faq | — | failed — HTTP 404 |
| [Documentation](https://bentonow.com/help) | help | 2 | read |
| [https://app.bentonow.com/pricing?source=pricing&plan=start](https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000) | pricing | — | failed — blocked by robots.txt |
| [https://app.bentonow.com/pricing?source=pricing&package=tr](https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0) | pricing | — | failed — blocked by robots.txt |
| [Bento Skills for AI Agents](https://bentonow.com/docs/integrations/skills) | addons | 1 | read |
| [https://bentonow.com/docs/integrations/cli.md](https://bentonow.com/docs/integrations/cli.md) | addons | — | failed — skipped: content-type text/markdown; charset= |
| [Acceptable Use Policy](https://bentonow.com/legal/acceptable-use-policy) | terms | 2 | read |

</details>

Claims extracted: 13 trial, 9 addon, 7 limit, 6 condition, 2 plan mention, 1 unlimited.

Inaccessible pages: https://bentonow.com/pricing.md (skipped: content-type text/markdown; charset=utf-8); https://bentonow.com/faq (HTTP 404); https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000 (blocked by robots.txt); https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0 (blocked by robots.txt); https://bentonow.com/docs/integrations/cli.md (skipped: content-type text/markdown; charset=utf-8).

**1. “Unlimited” is advertised, but a fair-use restriction is buried on another page**  
`medium impact` · `Ambiguity` · `high confidence` · `unlimited_vs_fair_use`

Your commercial pages advertise unlimited marketing sends, while a separate page qualifies usage with a fair-use or acceptable-use restriction. A customer deciding on price never sees the qualifier; a customer who hits it experiences it as a broken promise.

- **Claim A:** Unlimited marketing sends (no specific plan)
  - Evidence: “Pick Marketing Platform for $29/mo for up to 5,000 Active Users * , get unlimited marketing sends on paid plans. Add Bento Chat for $30/mo, or use Transactional Email on its own.”
  - Source: [Simple plans, no hidden fees.](https://bentonow.com/pricing)
- **Claim B:** Usage is subject to a fair-use / acceptable-use restriction
  - Evidence: “An Acceptable Use Policy (AUP) is a set of rules defined by an ESP or ISP that governs what type of content and behavior is allowed on their network.”
  - Source: [Email Marketing Glossary](https://bentonow.com/terms)
- *Caveat: Fair-use clauses are standard practice. The issue is placement and wording, not the existence of the clause.*


### Checkly

https://www.checklyhq.com · monitoring · discovered via category sweep: synthetic monitoring

Read **12** pages (0 needed a headless browser), extracted **22** claims, produced **0** findings in 4.6s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Reliability starts with a plan](https://www.checklyhq.com/pricing) | pricing | 14 | read |
| [https://app.checklyhq.com/signup](https://app.checklyhq.com/signup) | trial | — | failed — blocked by robots.txt |
| [Send Alerts to Discord](https://www.checklyhq.com/docs/integrations/alerts/discord) | addons | 0 | read |
| [How to get help with Checkly](https://www.checklyhq.com/support) | help | 1 | read |
| [Checkly Documentation](https://www.checklyhq.com/docs) | docs | 0 | read |
| [Monitoring that works like your code does](https://www.checklyhq.com/solutions/developers) | docs | 3 | read |
| [Checkly CLI](https://www.checklyhq.com/docs/cli) | docs | 0 | read |
| [Terms of use](https://www.checklyhq.com/terms) | terms | 1 | read |
| [Slack](https://www.checklyhq.com/docs/integrations/alerts/slack) | addons | 3 | read |
| [Guides to Using Checkly](https://www.checklyhq.com/docs/guides/overview) | help | 0 | read |
| [https://www.checklyhq.com/faq](https://www.checklyhq.com/faq) | faq | — | failed — HTTP 404 |
| [https://www.checklyhq.com/help](https://www.checklyhq.com/help) | help | — | failed — HTTP 404 |
| [https://www.checklyhq.com/docs/llms.txt](https://www.checklyhq.com/docs/llms.txt) | docs | — | failed — skipped: content-type text/plain; charset=utf |
| [What is Checkly?](https://www.checklyhq.com/docs/what-is-checkly) | docs | 0 | read |
| [Using the Checkly API](https://www.checklyhq.com/docs/api-reference/overview) | docs | 0 | read |
| [Checkly Documentation](https://developers.checklyhq.com/) | docs | 0 | read |

</details>

Claims extracted: 5 limit, 5 addon, 5 condition, 4 plan mention, 3 entitlement.

Inaccessible pages: https://app.checklyhq.com/signup (blocked by robots.txt); https://www.checklyhq.com/faq (HTTP 404); https://www.checklyhq.com/help (HTTP 404); https://www.checklyhq.com/docs/llms.txt (skipped: content-type text/plain; charset=utf-8).

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

### Cronitor

https://cronitor.io · monitoring · discovered via category sweep: independent uptime and cron monitoring

Read **12** pages (0 needed a headless browser), extracted **28** claims, produced **1** findings in 1.9s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Simple Pricing](https://cronitor.io/pricing) | pricing | 22 | read |
| [Monitoring made for developers.](https://cronitor.io/sign-up) | trial | 1 | read |
| [Start your free trial](https://cronitor.io/sign-up?flow=trial&plan=metered&billing_frequency=month) | trial | 2 | read |
| [Integrations](https://cronitor.io/docs/integrations) | addons | 0 | read |
| [We're here to help.](https://cronitor.io/help) | help | 0 | read |
| [Cronitor Developer Docs](https://cronitor.io/docs) | docs | 0 | read |
| [Cronitor API Docs](https://cronitor.io/docs/api) | docs | 1 | read |
| [https://cronitor.io/terms](https://cronitor.io/terms) | terms | — | failed — blocked by robots.txt |
| [Cronitor Developer Guides](https://cronitor.io/guides) | help | 1 | read |
| [How to find and read crontab logs](https://cronitor.io/guides/where-are-cron-logs-stored) | help | 0 | read |
| [SDKs & Agents](https://cronitor.io/docs/sdks) | docs | 0 | read |
| [https://cronitor.io/faq](https://cronitor.io/faq) | faq | — | failed — HTTP 404 |
| [Configuring SAML SSO](https://cronitor.io/docs/saml-sso) | docs | 1 | read |
| [[Cron] Job Monitoring](https://cronitor.io/docs/cron-job-monitoring) | docs | 0 | read |

</details>

Claims extracted: 11 entitlement, 5 trial, 4 limit, 4 plan mention, 3 unlimited, 1 condition.

Inaccessible pages: https://cronitor.io/terms (blocked by robots.txt); https://cronitor.io/faq (HTTP 404).

**1. “Unlimited” is advertised, but a fair-use restriction is buried on another page**  
`medium impact` · `Ambiguity` · `high confidence` · `unlimited_vs_fair_use`

Your commercial pages advertise unlimited API requests, while a separate page qualifies usage with a fair-use or acceptable-use restriction. A customer deciding on price never sees the qualifier; a customer who hits it experiences it as a broken promise.

- **Claim A:** Unlimited API requests (no specific plan)
  - Evidence: “Unlimited API requests”
  - Source: [Simple Pricing](https://cronitor.io/pricing)
- **Claim B:** Usage is subject to a fair-use / acceptable-use restriction
  - Evidence: “The API has rate limits to ensure fair usage.”
  - Source: [Cronitor API Docs](https://cronitor.io/docs/api)
- *Caveat: Fair-use clauses are standard practice. The issue is placement and wording, not the existence of the clause.*


### Fathom Analytics

https://usefathom.com · web analytics · discovered via category sweep: privacy-focused web analytics

Read **13** pages (0 needed a headless browser), extracted **28** claims, produced **2** findings in 4.2s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Simple and sustainable pricing](https://usefathom.com/pricing) | pricing | 8 | read |
| [https://app.usefathom.com/register](https://app.usefathom.com/register) | trial | 0 | read |
| [https://app.usefathom.com/register?plan=price_1OMiuQJpbH9s](https://app.usefathom.com/register?plan=price_1OMiuQJpbH9soFseaah1xMDb) | trial | 0 | read |
| [Rate limits and concurrency](https://usefathom.com/api/v1/rate-limits) | limits | 0 | read |
| [Integrations](https://usefathom.com/docs/integrations) | addons | 2 | read |
| [Help Centre](https://usefathom.com/docs) | docs | 1 | read |
| [Fathom Analytics API](https://usefathom.com/api/v1) | docs | 0 | read |
| [https://usefathom.com/api/llms.txt](https://usefathom.com/api/llms.txt) | docs | — | failed — skipped: content-type text/plain; charset=utf |
| [WordPress](https://usefathom.com/docs/integrations/wordpress) | addons | 3 | read |
| [Privacy law compliance](https://usefathom.com/legal/compliance) | terms | 2 | read |
| [Fathom Analytics Terms and Conditions](https://usefathom.com/legal/terms) | terms | 6 | read |
| [https://usefathom.com/faq](https://usefathom.com/faq) | faq | — | failed — HTTP 404 |
| [https://usefathom.com/help](https://usefathom.com/help) | help | — | failed — HTTP 404 |
| [Discourse](https://usefathom.com/docs/integrations/discourse) | addons | 2 | read |
| [Kit](https://usefathom.com/docs/integrations/convertkit) | addons | 2 | read |
| [Webflow](https://usefathom.com/docs/integrations/webflow) | addons | 2 | read |

</details>

Claims extracted: 9 trial, 8 limit, 4 addon, 4 condition, 3 unlimited.

Inaccessible pages: https://usefathom.com/api/llms.txt (skipped: content-type text/plain; charset=utf-8); https://usefathom.com/faq (HTTP 404); https://usefathom.com/help (HTTP 404).

**1. A commercial condition — a no-refund policy — appears only away from your pricing page**  
`low impact` · `Missing information` · `high confidence` · `condition_off_pricing`

Fathom Analytics Terms and Conditions sets out a no-refund policy, but nothing equivalent appears on your pricing page. Conditions that change what a customer actually pays or receives belong where the buying decision is made; discovering them later is where churn and chargebacks start.

- **Claim A:** Pricing page: condition not stated
  - Evidence: “(no equivalent statement found on the pricing page)”
  - Source: [Pricing page](https://usefathom.com/pricing)
- **Claim B:** Fathom Analytics Terms and Conditions: a no-refund policy
  - Evidence: “All Fees paid by you to us are non-refundable, except if required by law.”
  - Source: [Fathom Analytics Terms and Conditions](https://usefathom.com/legal/terms)
- *Caveat: This is standard legal wording in the right place; the question is only whether the pricing page sets the same expectation. Detected by absence, so a condition stated in an image, a tooltip or a collapsed accordion on the pricing page would be missed.*

**2. A commercial condition — automatic renewal — appears only away from your pricing page**  
`low impact` · `Missing information` · `high confidence` · `condition_off_pricing`

Fathom Analytics Terms and Conditions sets out automatic renewal, but nothing equivalent appears on your pricing page. Conditions that change what a customer actually pays or receives belong where the buying decision is made; discovering them later is where churn and chargebacks start.

- **Claim A:** Pricing page: condition not stated
  - Evidence: “(no equivalent statement found on the pricing page)”
  - Source: [Pricing page](https://usefathom.com/pricing)
- **Claim B:** Fathom Analytics Terms and Conditions: automatic renewal
  - Evidence: “At the end of each Billing Cycle, your Subscription will automatically renew unless you or we cancel it pursuant to these Terms.”
  - Source: [Fathom Analytics Terms and Conditions](https://usefathom.com/legal/terms)
- *Caveat: This is standard legal wording in the right place; the question is only whether the pricing page sets the same expectation. Detected by absence, so a condition stated in an image, a tooltip or a collapsed accordion on the pricing page would be missed.*


### Knock

https://knock.app · notifications API · discovered via category sweep: notification infrastructure

Read **16** pages (0 needed a headless browser), extracted **80** claims, produced **1** findings in 3.2s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Pricing that scales with you](https://knock.app/pricing) | pricing | 56 | read |
| [Subscriptions](https://docs.knock.app/concepts/subscriptions) | billing_docs | 0 | read |
| [Workflows API reference](https://docs.knock.app/api-reference/workflows/cancel) | billing_docs | 0 | read |
| [Users API reference](https://docs.knock.app/api-reference/users/list_subscriptions) | billing_docs | 3 | read |
| [API reference](https://docs.knock.app/reference) | docs | 4 | read |
| [https://dashboard.knock.app/signup](https://dashboard.knock.app/signup) | trial | — | failed — blocked by robots.txt |
| [API reference](https://docs.knock.app/api-reference/overview) | docs | 4 | read |
| [API reference](https://docs.knock.app/api-reference/overview/rate-limits) | limits | 4 | read |
| [API reference](https://docs.knock.app/api-reference/overview/batch-rate-limits) | limits | 4 | read |
| [Integrations overview](https://docs.knock.app/integrations/overview) | addons | 0 | read |
| [Powering cross-channel configurable alerts with Knock](https://docs.knock.app/guides/alerting) | help | 0 | read |
| [Implementing Knock guides in Vue.js](https://docs.knock.app/tutorials/guides-in-vue) | help | 1 | read |
| [Knock MCP server](https://docs.knock.app/developer-tools/mcp-server) | docs | 1 | read |
| [Users API reference](https://docs.knock.app/api-reference/users/guides/get_channel) | help | 3 | read |
| [Integrations](https://knock.app/integrations) | addons | 0 | read |
| [See how Knock compares](https://knock.app/compare) | compare | 0 | read |
| [Objects API reference](https://docs.knock.app/api-reference/objects/list_subscriptions) | billing_docs | 0 | read |

</details>

Claims extracted: 28 unlimited, 20 limit, 13 entitlement, 8 plan price, 6 plan mention, 5 condition.

Inaccessible pages: https://dashboard.knock.app/signup (blocked by robots.txt).

**1. Two different allowances are published for API requests**  
`medium impact` · `Ambiguity` · `low confidence` · `limit_conflict`

API reference states 60 per second and API reference states 200 per second for API requests. Neither figure is tied to a named plan, so a customer cannot work out which applies to them.

- **Claim A:** 60 API requests per second (no specific plan)
  - Evidence: “60 requests / second”
  - Source: [API reference](https://docs.knock.app/reference)
- **Claim B:** 200 API requests per second (no specific plan)
  - Evidence: “200 requests / second”
  - Source: [API reference](https://docs.knock.app/api-reference/overview)
- *Caveat: The two numbers may be scoped to different plans or to different objects (per workspace vs per account). Treat this as a prompt to check, not proof.*


### SavvyCal

https://savvycal.com · scheduling · discovered via category sweep: independent scheduling tools

Read **13** pages (0 needed a headless browser), extracted **8** claims, produced **1** findings in 3.5s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Join thousands of happy customers](https://savvycal.com/pricing) | pricing | 6 | read |
| [SavvyCal Meetings](https://savvycal.com/signup) | trial | 0 | read |
| [Integrations](https://savvycal.com/integrations-directory) | addons | 0 | read |
| [How can we help?](https://docs.savvycal.com/) | help | 0 | read |
| [SavvyCal Meetings Developer Docs](https://developers.savvycal.com/) | docs | 0 | read |
| [SavvyCal Terms of Use](https://savvycal.com/terms) | terms | 2 | read |
| [Free Time Zone API by SavvyCal](https://savvycal.com/time-zone-api) | docs | 0 | read |
| [https://savvycal.com/faq](https://savvycal.com/faq) | faq | — | failed — HTTP 404 |
| [REST API](https://developers.savvycal.com/category/rest-api) | docs | 0 | read |
| [SavvyCal End User License Agreement for Downloadable Tools](https://savvycal.com/eula) | terms | 0 | read |
| [Authentication](https://developers.savvycal.com/authentication) | help | 0 | read |
| [Webhooks](https://developers.savvycal.com/webhooks) | help | 0 | read |
| [Integrations](https://docs.savvycal.com/category/5-integrations) | addons | 0 | read |
| [Use Cases](https://docs.savvycal.com/category/7-usage) | limits | 0 | read |
| [https://savvycal.com/help](https://savvycal.com/help) | help | — | failed — HTTP 404 |
| [https://savvycal.com/docs](https://savvycal.com/docs) | docs | — | failed — HTTP 404 |

</details>

Claims extracted: 3 plan mention, 2 unlimited, 2 condition, 1 trial.

Inaccessible pages: https://savvycal.com/faq (HTTP 404); https://savvycal.com/help (HTTP 404); https://savvycal.com/docs (HTTP 404).

**1. A commercial condition — automatic renewal — appears only away from your pricing page**  
`low impact` · `Missing information` · `high confidence` · `condition_off_pricing`

SavvyCal Terms of Use sets out automatic renewal, but nothing equivalent appears on your pricing page. Conditions that change what a customer actually pays or receives belong where the buying decision is made; discovering them later is where churn and chargebacks start.

- **Claim A:** Pricing page: condition not stated
  - Evidence: “(no equivalent statement found on the pricing page)”
  - Source: [Pricing page](https://savvycal.com/pricing)
- **Claim B:** SavvyCal Terms of Use: automatic renewal
  - Evidence: “Subscriptions will automatically renew for the same subscription period unless you cancel the account by the end of the then-current subscription period.”
  - Source: [SavvyCal Terms of Use](https://savvycal.com/terms)
- *Caveat: This is standard legal wording in the right place; the question is only whether the pricing page sets the same expectation. Detected by absence, so a condition stated in an image, a tooltip or a collapsed accordion on the pricing page would be missed.*


### ScreenshotOne

https://screenshotone.com · media API · discovered via category sweep: screenshot APIs

Read **15** pages (0 needed a headless browser), extracted **86** claims, produced **2** findings in 2.7s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Start rendering for free](https://screenshotone.com/pricing) | pricing | 66 | read |
| [How credits work in ScreenshotOne](https://screenshotone.com/docs/credits) | limits | 3 | read |
| [https://dash.screenshotone.com/sign-up](https://dash.screenshotone.com/sign-up) | trial | — | failed — blocked by robots.txt |
| [Automate website screenshots in your workflows](https://screenshotone.com/integrations) | addons | 2 | read |
| [Get Usage](https://screenshotone.com/docs/get-usage) | limits | 2 | read |
| [Getting Started](https://screenshotone.com/docs) | docs | 1 | read |
| [Getting Started](https://screenshotone.com/docs/getting-started) | docs | 1 | read |
| [Zapier](https://screenshotone.com/integrations/zapier) | addons | 1 | read |
| [Terms of Service](https://screenshotone.com/terms-of-service) | terms | 3 | read |
| [Guides](https://screenshotone.com/docs/guides) | help | 1 | read |
| [Generate PDFs from URLs, HTML, or Markdown via API](https://screenshotone.com/pdf-generation-api) | docs | 1 | read |
| [Fail rendering if the content contains a string](https://screenshotone.com/docs/guides/fail-if-content-contains) | help | 1 | read |
| [Upload to S3](https://screenshotone.com/docs/guides/upload-to-s3) | help | 1 | read |
| [https://screenshotone.com/faq](https://screenshotone.com/faq) | faq | — | failed — HTTP 404 |
| [https://screenshotone.com/terms](https://screenshotone.com/terms) | terms | — | failed — HTTP 404 |
| [Airtable](https://screenshotone.com/integrations/airtable) | addons | 1 | read |
| [Make](https://screenshotone.com/integrations/make) | addons | 1 | read |
| [Bubble](https://screenshotone.com/integrations/bubble) | addons | 1 | read |

</details>

Claims extracted: 50 entitlement, 12 addon, 10 condition, 6 plan price, 5 limit, 3 plan mention.

Inaccessible pages: https://dash.screenshotone.com/sign-up (blocked by robots.txt); https://screenshotone.com/faq (HTTP 404); https://screenshotone.com/terms (HTTP 404).

**1. A commercial condition — charges that apply once an allowance is exceeded — appears only away from your pricing page**  
`medium impact` · `Missing information` · `high confidence` · `condition_off_pricing`

Terms of Service sets out charges that apply once an allowance is exceeded, but nothing equivalent appears on your pricing page. Conditions that change what a customer actually pays or receives belong where the buying decision is made; discovering them later is where churn and chargebacks start.

- **Claim A:** Pricing page: condition not stated
  - Evidence: “(no equivalent statement found on the pricing page)”
  - Source: [Pricing page](https://screenshotone.com/pricing)
- **Claim B:** Terms of Service: charges that apply once an allowance is exceeded
  - Evidence: “Use of the Service may be subject to pricing plans, quotas, rate limits, and overage charges described on our website or documentation.”
  - Source: [Terms of Service](https://screenshotone.com/terms-of-service)
- *Caveat: Detected by absence, so a condition stated in an image, a tooltip or a collapsed accordion on the pricing page would be missed.*

**2. A commercial condition — the right to change prices — appears only away from your pricing page**  
`low impact` · `Missing information` · `high confidence` · `condition_off_pricing`

Terms of Service sets out the right to change prices, but nothing equivalent appears on your pricing page. Conditions that change what a customer actually pays or receives belong where the buying decision is made; discovering them later is where churn and chargebacks start.

- **Claim A:** Pricing page: condition not stated
  - Evidence: “(no equivalent statement found on the pricing page)”
  - Source: [Pricing page](https://screenshotone.com/pricing)
- **Claim B:** Terms of Service: the right to change prices
  - Evidence: “We reserve the right to modify pricing, features, usage limits, quotas, or plan structures at any time.”
  - Source: [Terms of Service](https://screenshotone.com/terms-of-service)
- *Caveat: This is standard legal wording in the right place; the question is only whether the pricing page sets the same expectation. Detected by absence, so a condition stated in an image, a tooltip or a collapsed accordion on the pricing page would be missed.*


### Umami

https://umami.is · web analytics · discovered via category sweep: open-source analytics with a hosted tier

Read **3** pages (0 needed a headless browser), extracted **0** claims, produced **0** findings in 2.5s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [https://umami.is/pricing](https://umami.is/pricing) | pricing | 0 | read |
| [Introduction](https://umami.is/docs) | docs | 0 | read |
| [https://umami.is/terms](https://umami.is/terms) | terms | 0 | read |

</details>

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

### Unkey

https://www.unkey.com · API management · discovered via category sweep: API key management

Read **11** pages (0 needed a headless browser), extracted **37** claims, produced **0** findings in 5.5s.

<details><summary>Pages read</summary>

| Page | Category | Claims | Status |
|---|---|---|---|
| [Start for free, scale as you go with predictable usage-bas](https://www.unkey.com/pricing) | pricing | 36 | read |
| [What is Unkey?](https://www.unkey.com/docs) | docs | 0 | read |
| [Billing](https://unkey.com/docs/platform/workspaces/billing) | billing_docs | 1 | read |
| [What is Unkey?](https://unkey.com/docs/introduction) | docs | 0 | read |
| [https://www.unkey.com/docs/llms.txt](https://www.unkey.com/docs/llms.txt) | docs | — | failed — skipped: content-type text/plain; charset=utf |
| [Website Terms of Use](https://www.unkey.com/policies/terms) | terms | 0 | read |
| [https://www.unkey.com/faq](https://www.unkey.com/faq) | faq | — | failed — HTTP 404 |
| [https://app.unkey.com/auth/sign-up](https://app.unkey.com/auth/sign-up) | trial | — | failed — HTTP 429 |
| [https://app.unkey.com/](https://app.unkey.com/) | trial | — | failed — HTTP 429 |
| [https://www.unkey.com/help](https://www.unkey.com/help) | help | — | failed — HTTP 404 |
| [https://www.unkey.com/terms](https://www.unkey.com/terms) | terms | — | failed — HTTP 404 |
| [What is Unkey?](https://www.unkey.com/docs/introduction) | docs | 0 | read |
| [Regions](https://unkey.com/docs/build-and-deploy/regions) | docs | 0 | read |
| [Observability](https://unkey.com/docs/observability/overview) | docs | 0 | read |
| [Overview](https://www.unkey.com/docs/api-reference/overview) | docs | 0 | read |
| [Deploy your first app](https://www.unkey.com/docs/quickstart/deploy) | docs | 0 | read |
| [Quickstart](https://www.unkey.com/docs/quickstart/quickstart) | docs | 0 | read |

</details>

Claims extracted: 15 entitlement, 13 plan price, 7 plan mention, 1 unlimited, 1 limit.

Inaccessible pages: https://www.unkey.com/docs/llms.txt (skipped: content-type text/plain; charset=utf-8); https://www.unkey.com/faq (HTTP 404); https://app.unkey.com/auth/sign-up (HTTP 429); https://app.unkey.com/ (HTTP 429); https://www.unkey.com/help (HTTP 404).

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

---

## 3. Selection method

1. A candidate pool of **36** smaller SaaS companies was frozen in `src/promise_audit/experiment/pool.py` before any company was analysed.
2. Every candidate was put through the same automated eligibility pre-check:
   - not on the excluded large-platform list
   - homepage reachable over HTTPS and allowed by robots.txt
   - a public pricing page can be discovered automatically
   - public documentation, help, FAQ, comparison or terms content can be discovered
3. **35** candidates passed.
4. Ten were drawn with `random.Random(20260902).sample(...)` over the eligible candidates sorted by URL, so the draw is reproducible and independent of the order the pre-check finished in.
5. All ten were analysed with identical settings (`{"max_pages": 16, "max_findings": 12}`). No rule, threshold or prompt was changed for any individual company.

**Selected:** Baserow, Bento, Checkly, Cronitor, Fathom Analytics, Knock, SavvyCal, ScreenshotOne, Umami, Unkey.

### Complete candidate pool

| # | Company | Category | Where it was found | Why it qualifies | Eligible? |
|---|---|---|---|---|---|
| 1 | [Fathom Analytics](https://usefathom.com) | web analytics | category sweep: privacy-focused web analytics | Independent, founder-led analytics vendor with a public per-plan pricing page and a public documentation site. | **yes — selected** |
| 2 | [Simple Analytics](https://www.simpleanalytics.com) | web analytics | category sweep: privacy-focused web analytics | Small European analytics vendor publishing usage-based plans and public docs. | yes |
| 3 | [Pirsch Analytics](https://pirsch.io) | web analytics | category sweep: privacy-focused web analytics | Small independent analytics product with published pageview allowances and docs. | yes |
| 4 | [Umami](https://umami.is) | web analytics | category sweep: open-source analytics with a hosted tier | Open-source analytics with a commercial hosted plan and public documentation. | **yes — selected** |
| 5 | [Buttondown](https://buttondown.com) | email / newsletters | category sweep: independent newsletter platforms | Solo-founder newsletter tool with subscriber-tiered public pricing and docs. | yes |
| 6 | [EmailOctopus](https://emailoctopus.com) | email / newsletters | category sweep: independent email marketing | Small email marketing vendor with public contact-tiered pricing and a help centre. | yes |
| 7 | [Loops](https://loops.so) | email / newsletters | category sweep: modern SaaS email tools | Early-stage email platform with public per-contact pricing and public docs. | yes |
| 8 | [Bento](https://bentonow.com) | email / newsletters | category sweep: modern SaaS email tools | Small marketing-automation vendor with published plans and a help centre. | **yes — selected** |
| 9 | [Tally](https://tally.so) | forms | category sweep: independent form builders | Bootstrapped form builder with a public two-tier pricing page and a help centre. | yes |
| 10 | [Fillout](https://www.fillout.com) | forms | category sweep: independent form builders | Small form product with public plan tiers, response limits and documentation. | yes |
| 11 | [Formspree](https://formspree.io) | forms | category sweep: form back-end APIs | Long-running independent form back end with submission-limited plans and docs. | yes |
| 12 | [SavvyCal](https://savvycal.com) | scheduling | category sweep: independent scheduling tools | Bootstrapped scheduling product with public pricing and a help centre. | **yes — selected** |
| 13 | [Cal.com](https://cal.com) | scheduling | category sweep: open-source scheduling | Open-source scheduling vendor with a public seat-based pricing page and docs. | yes |
| 14 | [ScrapingBee](https://www.scrapingbee.com) | web data API | category sweep: web-scraping APIs | Small API vendor with credit-based public pricing and full API documentation. | yes |
| 15 | [Scrapfly](https://scrapfly.io) | web data API | category sweep: web-scraping APIs | Independent scraping API with published credit allowances and detailed docs. | yes |
| 16 | [ScreenshotOne](https://screenshotone.com) | media API | category sweep: screenshot APIs | Solo-founder screenshot API with request-quota pricing and public documentation. | **yes — selected** |
| 17 | [Bannerbear](https://www.bannerbear.com) | media API | category sweep: image generation APIs | Bootstrapped image-generation API with quota-based plans and public docs. | yes |
| 18 | [Placid](https://placid.app) | media API | category sweep: image generation APIs | Small creative-automation API with public usage tiers and documentation. | yes |
| 19 | [Baserow](https://baserow.io) | no-code database | category sweep: open-source Airtable alternatives | Open-core database vendor with public per-seat pricing and extensive docs. | **yes — selected** |
| 20 | [NocoDB](https://nocodb.com) | no-code database | category sweep: open-source Airtable alternatives | Open-source database platform with a public cloud pricing page and docs. | yes |
| 21 | [Chartbrew](https://chartbrew.com) | BI / dashboards | category sweep: small open-source BI tools | Small open-source dashboard product with a hosted paid tier and public docs. | yes |
| 22 | [Outseta](https://www.outseta.com) | subscription / CRM | category sweep: all-in-one SaaS back-office tools | Small vendor bundling billing, CRM and help desk, with public pricing and a KB. | yes |
| 23 | [Userlist](https://userlist.com) | lifecycle marketing | category sweep: SaaS lifecycle messaging | Bootstrapped lifecycle email tool with user-count pricing and a help centre. | yes |
| 24 | [Encharge](https://encharge.io) | lifecycle marketing | category sweep: SaaS lifecycle messaging | Small marketing-automation vendor with public tiered pricing and documentation. | no — no public pricing page could be discovered |
| 25 | [Resend](https://resend.com) | email API | category sweep: developer email APIs | Early-stage transactional email API with public volume pricing and docs. | yes |
| 26 | [Knock](https://knock.app) | notifications API | category sweep: notification infrastructure | Small notifications-infrastructure vendor with public MAU pricing and docs. | **yes — selected** |
| 27 | [Svix](https://www.svix.com) | webhooks API | category sweep: webhook infrastructure | Small webhooks-as-a-service vendor with public message-volume pricing and docs. | yes |
| 28 | [Hookdeck](https://hookdeck.com) | webhooks API | category sweep: webhook infrastructure | Independent event-gateway vendor with public request-volume pricing and docs. | yes |
| 29 | [Cronitor](https://cronitor.io) | monitoring | category sweep: independent uptime and cron monitoring | Small monitoring vendor with public per-monitor pricing and documentation. | **yes — selected** |
| 30 | [Checkly](https://www.checklyhq.com) | monitoring | category sweep: synthetic monitoring | Mid-size independent monitoring vendor with usage-based pricing and full docs. | **yes — selected** |
| 31 | [Instatus](https://instatus.com) | status pages | category sweep: status page vendors | Small status-page vendor with public tiered pricing and a help centre. | yes |
| 32 | [Tinybird](https://www.tinybird.co) | data infrastructure | category sweep: real-time analytics back ends | Independent real-time data platform with public usage pricing and docs. | yes |
| 33 | [Turso](https://turso.tech) | data infrastructure | category sweep: hosted database startups | Early-stage hosted database with public row/storage allowances and docs. | yes |
| 34 | [Doppler](https://www.doppler.com) | secrets management | category sweep: developer secrets management | Small secrets-management vendor with public per-seat pricing and documentation. | yes |
| 35 | [Infisical](https://infisical.com) | secrets management | category sweep: open-source secrets management | Open-source secrets platform with a public cloud pricing page and docs. | yes |
| 36 | [Unkey](https://www.unkey.com) | API management | category sweep: API key management | Early-stage API management vendor with public request-volume pricing and docs. | **yes — selected** |
