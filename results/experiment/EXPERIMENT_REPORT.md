# Do SaaS companies contradict themselves in public?

### A ten-company experiment with the commercial-consistency auditor

Harvested 2026-09-02 07:57:41 UTC · analysed 2026-09-02 17:12:08 UTC · analyst backend `agent` · random seed `20260902` · candidate pool 36 · eligible 35 · analysed 10

## Result

Ten smaller SaaS companies, drawn at random from a frozen pool of 36. Nine could be read.
**111 pages fetched, 90 readable, 140 commercial promises extracted, 19 findings, 208 quotes
verified against their source pages.**

Eight of the nine readable companies had at least one finding. The five strongest:

| Company | Finding |
|---|---|
| Unkey | Free plan keeps logs 7 days and audit logs 30 days. The $5 Starter plan gets 3 and 7. |
| Fathom | Pricing page says analytics are never switched off for going over. Terms allow suspension after seven days and deletion after two months, with no refund. |
| Fathom | "Full API access with 600 requests per hour included" sits next to "No extra fees". A separate page prices the next five rungs at $19 to $399 a month. |
| ScreenshotOne | Three pages give three answers to what happens when you exceed your plan: pay per extra, be billed only if extra charging is enabled, or be throttled and suspended. |
| Bento | Pricing page bills on active users, explicitly so dormant contacts do not inflate the bill. The docs FAQ says billing is on total subscribers, meaning every email address on file. |

Every one is two real sentences, quoted verbatim, with both links in the report.

## Is there a recurring problem?

Yes. It is drift, not dishonesty.

Eight of nine had something. In every case the pricing page and the documentation were
written at different times and never reconciled. Unkey's free-plan table predates a
repackaging. Bento's FAQ is copy from before the Active Users model. Fathom's terms were
last updated in 2021 and its FAQ is current marketing.

Three shapes recurred:

| Shape | Count | Companies |
|---|---|---|
| Pricing page and docs disagree about a number | 4 | Unkey, Bento, Baserow |
| "Unlimited" or "full" meets a documented limit | 4 | Cronitor, Knock, Fathom |
| A commercial condition lives only in the terms or a docs page | 6 | Fathom, ScreenshotOne, Baserow, Knock |

The third group needs care. ScreenshotOne reserving the right to change usage limits and
quotas, not just prices, is a real term about what a customer receives. Ordinary
auto-renewal boilerplate is not, and we rated it low.

## Is any of it new to the company?

About half.

New: Unkey's retention inversion, Knock's Enterprise guides default, ScreenshotOne's three
answers, Bento's billing metric. Seeing any of these requires reading two pages side by
side in one sitting, which nobody inside a company does.

Not new: auto-renewal clauses, price-change rights, refund wording. Every founder knows
those are in their terms. Presented as a contradiction, this is padding. Presented as
"your buyer never sees this", it is a fair point about placement, and we rated it low or
medium accordingly.

## False positives

No finding cites evidence that does not exist. All 208 quotes were located
character-by-character in the harvested page. No finding was discarded at verification.
That number needs the caveat below.

The risk in this design is not fabricated evidence. It is over-reading: two real sentences,
correctly quoted, that anyone at the company would reconcile in a second. Our own
assessment of the 19:

| Verdict | Count | Which |
|---|---|---|
| Would defend to a founder without hedging | 9 | Unkey x2, Fathom x2, ScreenshotOne overage, Bento billing metric, Knock guides, Cronitor x2 |
| Real but modest | 7 | Placement problems and boilerplate in the right place |
| An informed reader would push back | 3 | Fathom discount codes, SavvyCal price-change clause, Bento "no feature gating" |

Three soft findings in nineteen, about 16%. None fabricated. All three carry a caveat
saying what would make them wrong.

Two would-be false positives were caught and suppressed, which matters as much as the
findings:

1. Knock publishes an endpoint rate-limit tier table on two documentation pages. Read
   mechanically, "60 requests / second" on one and "200 requests / second" on the other
   looks like a contradiction. It is one table reproduced twice.
2. Checkly, Baserow and Unkey all build comparison tables from styled divs. Flattened to
   text, a monthly and annual toggle or a mis-aligned column produces convincing nonsense.
   The Unkey retention finding was reported only after cross-checking the column against
   the plan cards. The same column that gives Starter 3 days also gives it 1 vCPU, 2 GB,
   1 custom domain and $5 of credits, all matching the Starter card.

## What limits the tool

**Client-side rendering, by a wide margin.** Umami returned zero readable words from all
three pages we reached, including the pricing page, so it could not be analysed at all.
That is a miss, not a clean result, and we counted it as one. SavvyCal's comparison table
rendered as feature names with no values and its FAQ as an empty heading, so its report is
visibly thinner. Twenty-one of 111 pages came back effectively empty and 29 more could not
be fetched. The headless-browser fallback is implemented and Chromium launches, but the
browser had no outbound network access in the sandbox this ran in.

**Flattened tables.** Every comparison grid on these sites is divs, not a real table. An
early version of the harvester de-duplicated repeated text lines, which silently destroyed
those grids, because "1", "2" and "Unlimited" repeat down a column. Unkey's retention
finding, the best in the run, was invisible until that was fixed. There are almost
certainly equivalent findings still being missed elsewhere.

**Discovery spends its budget in the wrong place.** For Checkly the crawler returned twelve
pages, eleven of them product documentation and integration guides that make no commercial
claims. It never found a billing or usage-limits article. Checkly's zero is partly real,
their pricing page is the best of the ten, and partly an artefact of having little to
compare it to.

**Zero rejections is not evidence.** The analyst and the verifier were the same model in
the same session, checking quotes as it wrote them. The verifier was tested adversarially
instead: fabricated quotes, paraphrased quotes, one passage split into two claims, missing
schema fields and invalid severities are all rejected, and a real quote attributed to the
wrong page is corrected rather than dropped. An unattended API run would produce a non-zero
rejection rate. That is the number worth reporting next time.

**Two conflicts of interest.** The analyst had already seen these ten companies during an
earlier rule-based version of this tool, so this was not a blind read. The assessment above
is the analyst grading its own work. Both need an independent reviewer.

## Would a founder try it?

Yes, and would get something.

The offer costs one URL. Eight of nine readable companies got at least one finding, and
five got something worth forwarding to whoever owns the docs. The report quotes their own
words, links both pages, and states in one line what would make each finding wrong. The
whole thing is checkable in about two minutes.

Checkly got zero findings and a paragraph saying their pricing page publishes more than
most companies disclose anywhere. That is a good thing to receive and not an embarrassing
result for the tool.

One caution. This sample was small, independent, mostly developer-tool companies with three
or four tiers. That is the easy case, and it is not the case with the most money in it.

## What to fix before publishing

1. **Make JavaScript rendering work end to end.** One company in ten was invisible and
   another read at a quarter depth. Those are the modern pricing pages most likely to have
   drifted.
2. **Parse comparison grids instead of flattening them.** Every one of these sites builds
   its plan table from divs. Reconstructing the columns properly would turn the richest
   source of per-plan promises from a hazard into an asset.
3. **Spend the page budget on billing and limits content.** Discovery gave Checkly eleven
   documentation pages with no commercial claims. Prefer billing, quota, plan-change and
   FAQ articles over SDK references and installation guides.
4. **Fix the confidence calibration.** Knock's contradictory rate limits were labelled low
   confidence because neither statement names a plan. That penalty is right for allowances
   and wrong for a rate limit that applies to everyone.
5. **Run it unattended through the API backend and report the rejection rate.** The verifier
   is the reason to trust this design and it has not been tested where it matters.
6. **Get an independent reviewer before publishing any hit-rate claim.** The analyst wrote
   the findings and then graded them, having already seen these companies once.

---

## 1. Headline numbers

| Measure | Value |
|---|---|
| Companies analysed | 10 |
| Companies with at least one finding | 8 of 10 |
| Companies with a medium- or high-confidence finding | 8 of 10 |
| Total findings (after verification) | 19 |
| Findings by severity | 5 high, 12 medium, 2 low |
| Findings by confidence | 12 high, 7 medium, 0 low |
| Commercial promises extracted | 140 |
| Public pages fetched | 111 |
| Pages with enough readable text to analyse | 90 |
| Pages that returned almost no text (client-rendered) | 21 |
| Pages that could not be fetched at all | 29 |
| Companies whose pricing page could not be read | 1 (Umami) |

**Verification.** Every quote the analyst produced was checked against the page it was attributed to:

| Check | Count |
|---|---|
| Quotes checked against their source page | 208 |
| Quotes that could not be found anywhere in the harvest | 0 |
| Quotes real but attributed to the wrong page (corrected) | 0 |
| Candidate findings discarded as unverifiable | 0 |

**Findings by type**

| Type | Count | What it means |
|---|---|---|
| Missing information | 8 | Something that changes the deal, published somewhere the buyer will not look. |
| Ambiguity | 6 | Both statements can be true, but a customer cannot tell what they get. |
| Likely contradiction | 5 | Two public statements that cannot both be true. |

---

## 2. The ten companies, one by one

### Baserow

https://baserow.io · no-code database · found via category sweep: open-source Airtable alternatives

Read **7** usable pages of 11 fetched, extracted **20** commercial promises, produced **2** findings. 28 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Free ($0); Premium ($10 per user/month billed yearly, $12 billed monthly); Advanced ($18 per user/month billed yearly, $22 billed monthly); Enterprise (On request)

<details><summary>Pages read</summary>

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

</details>

**1. Pricing page offers invoicing. FAQ says card only.**  
`medium impact` · `Likely contradiction` · `high confidence`

An enterprise buyer doing diligence reads the FAQ and concludes you cannot invoice them.

- **Claim A:** Enterprise pays by invoice
  - Evidence: “Payment by invoice”
  - Source: [https://baserow.io/pricing](https://baserow.io/pricing)
- **Claim B:** Credit card only
  - Evidence: “Currently, you can pay only with a credit card. We plan to add more payment methods in the future.”
  - Source: [https://baserow.io/faq](https://baserow.io/faq)
- *Why this is not just wording: One page sells invoicing as an Enterprise benefit, the other says no other payment method exists.*
- *What would make this a non-issue: The FAQ answer is probably about self-serve checkout, with invoicing arranged through sales. Neither page says so.*

**2. API concurrency is 10 on every paid plan. The comparison never says so.**  
`medium impact` · `Missing information` · `medium confidence`

Rows scale from 3,000 to 1,000,000 across the tiers. API throughput does not move at all.

- **Claim A:** Advanced buys 250,000 rows
  - Evidence: “250,000 rows per workspace”
  - Source: [https://baserow.io/pricing](https://baserow.io/pricing)
- **Claim B:** 10 concurrent requests, any plan
  - Evidence: “In Baserow Cloud, there's a limit of 10 concurrent API requests. This limit is subject to a fair use policy, and we reserve the right to lower it if it affects overall performance.”
  - Source: [https://baserow.io/faq](https://baserow.io/faq)
- *Why this is not just wording: Every other usage dimension is listed by tier and this one is absent, so a reader cannot infer either the cap or that it never improves.*
- *What would make this a non-issue: Your pricing page carries a collapsed FAQ titled "What are the limitations in records, rows, and API requests?". We could read the heading, not the panel.*

*Not checkable from these pages: The plan comparison on your pricing page is built from styled divs rather than a real table, so per-plan values lose their column alignment when flattened to text. Several rows publish three values for four plans, including row change history and application users. That may be a real gap or an artefact of the flattening, so we did not report it. The Premium plan advertises a free trial with no length stated on any page we read, and nothing says whether a card is required to start it.*

### Bento

https://bentonow.com · email / newsletters · found via category sweep: modern SaaS email tools

Read **13** usable pages of 13 fetched, extracted **13** commercial promises, produced **2** findings. 20 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Marketing Platform ($29/mo up to 5,000 Active Users, then tiered from $0.01 per Active User); Transactional Email ($0/mo, first 100 emails free, then $5/mo to 12,500 and $0.09 per 1,000 after); Bento Chat (add-on) (+$30/mo, requires Marketing Platform)

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Bento Pricing - Email Marketing, Chat, and Transactional](https://bentonow.com/pricing) | Pricing page | 814 | read |
| [Frequently Asked Questions - Bento Documentation](https://bentonow.com/docs/faq) | FAQ | 1201 | read |
| [Support - Bento Documentation](https://bentonow.com/docs/support) | Help centre | 347 | read |
| [Bento Documentation](https://bentonow.com/docs) | Product documentation | 176 | read |
| [Download Bento Apps - Mac, Windows, iOS, Android - Bento](https://bentonow.com/apps) | Add-ons & integrations | 237 | read |
| [Bento CLI - CLI for Email Marketing - Bento Documentatio](https://bentonow.com/docs/integrations/cli) | Product documentation | 1677 | read |
| [Developer API Documentation - Bento Documentation](https://bentonow.com/docs/developer_guides/introduction) | Product documentation | 511 | read |
| [Bento MCP Server - AI-Powered Email Marketing - Bento Do](https://bentonow.com/docs/integrations/mcp) | Add-ons & integrations | 2260 | read |
| [Email Marketing Glossary: 186 Terms & Definitions - Bent](https://bentonow.com/terms) | Terms / legal | 7456 | read |
| [Terms & Conditions - Bento](https://bentonow.com/legal/terms) | Terms / legal | 5035 | read |
| [Documentation & Help Center - Bento Email Marketing - Be](https://bentonow.com/help) | Help centre | 2449 | read |
| [Bento Skills for AI Agents - Bento Documentation](https://bentonow.com/docs/integrations/skills) | Add-ons & integrations | 383 | read |
| [Acceptable Use Policy - Bento](https://bentonow.com/legal/acceptable-use-policy) | Terms / legal | 1281 | read |
| https://bentonow.com/pricing.md | | | skipped: content-type text/markdown; charset= |
| https://bentonow.com/faq | | | HTTP 404 |
| https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000 | | | blocked by robots.txt |
| https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0 | | | blocked by robots.txt |
| https://bentonow.com/docs/integrations/cli.md | | | skipped: content-type text/markdown; charset= |

</details>

**1. Pricing page bills on active users. FAQ says total subscribers.**  
`high impact` · `Likely contradiction` · `high confidence`

On a list with a long dormant tail those two rules produce different invoices. It is also the reason a prospect picks you over the competitors in your own table.

- **Claim A:** Active users, last 30 days
  - Evidence: “Subscribed users or people with an event in the last 30 days.”
  - Source: [https://bentonow.com/pricing](https://bentonow.com/pricing)
- **Claim B:** Every unique email address
  - Evidence: “Bento charges based on the number of subscribers you have.”
  - Source: [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)
- *Why this is not just wording: Active users in the last 30 days and every email address on file are different countable populations.*
- *What would make this a non-issue: The FAQ is probably older copy from before the Active Users model. It is still the page customers search when they want to know what drives their bill.*

**2. FAQ says nothing is gated. Pricing page sells chat at $30 a month.**  
`medium impact` · `Ambiguity` · `medium confidence`

Someone who reads the FAQ first budgets $29 and is surprised at $59.

- **Claim A:** No feature gating at any tier
  - Evidence: “All features are included at every tier”
  - Source: [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)
- **Claim B:** Chat costs $30 a month extra
  - Evidence: “+$30/mo adds shared inbox, live chat, SMS, routing, saved replies, and AI agents. Requires Marketing Platform.”
  - Source: [https://bentonow.com/pricing](https://bentonow.com/pricing)
- *Why this is not just wording: One page says nothing is behind a paywall, the other puts a named feature set behind a separate charge.*
- *What would make this a non-issue: Tier almost certainly means volume tier, and Chat is arguably a separate product. Four words in the FAQ would settle it.*

*Not checkable from these pages: The FAQ answer to "What's the API rate limit?" is collapsed and did not render, though a table of per-endpoint limits sits on the same page. Nothing we read says whether a card is required to start the 30-day trial, or what happens to a list that exceeds fair use on marketing sends. The term is used but never defined anywhere we could reach.*

### Checkly

https://www.checklyhq.com · monitoring · found via category sweep: synthetic monitoring

Read **10** usable pages of 12 fetched, extracted **16** commercial promises, produced **0** findings. 20 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Hobby ($0 per month); Starter ($24 per month, billed annually); Team ($64 per month, billed annually); Enterprise (Custom)

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Checkly Pricing Plans: Flexible Synthetic Monitoring Sol](https://www.checklyhq.com/pricing) | Pricing page | 1232 | read |
| [Send Alerts to Discord - Checkly Docs](https://www.checklyhq.com/docs/integrations/alerts/discord) | Add-ons & integrations | 269 | read |
| [Checkly Support - Get help with Checkly](https://www.checklyhq.com/support) | Help centre | 427 | read |
| [Checkly Documentation - Checkly Docs](https://www.checklyhq.com/docs) | Product documentation | 179 | read |
| [Synthetic Monitoring for Developers - Code-First - Check](https://www.checklyhq.com/solutions/developers) | Product documentation | 917 | read |
| [Checkly CLI - Checkly Docs](https://www.checklyhq.com/docs/cli) | Product documentation | 128 | read |
| [Checkly Terms of Use](https://www.checklyhq.com/terms) | Terms / legal | 4 | too little text to read |
| [Slack - Checkly Docs](https://www.checklyhq.com/docs/integrations/alerts/slack) | Add-ons & integrations | 268 | read |
| [Guides to Using Checkly - Checkly Docs](https://www.checklyhq.com/docs/guides/overview) | Help centre | 222 | read |
| [What is Checkly? - Checkly Docs](https://www.checklyhq.com/docs/what-is-checkly) | Product documentation | 224 | read |
| [Using the Checkly API - Checkly Docs](https://www.checklyhq.com/docs/api-reference/overview) | Product documentation | 85 | too little text to read |
| [Checkly Documentation - Checkly Docs](https://developers.checklyhq.com/) | Product documentation | 179 | read |
| https://app.checklyhq.com/signup | | | blocked by robots.txt |
| https://www.checklyhq.com/faq | | | HTTP 404 |
| https://www.checklyhq.com/help | | | HTTP 404 |
| https://www.checklyhq.com/docs/llms.txt | | | skipped: content-type text/plain; charset=utf |

</details>

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

*Not checkable from these pages: Nothing on the pages we read contradicts anything else, and this is a genuinely tidy set of pages. Your pricing page publishes included volumes, the pre-purchase rate and the higher automatic overage rate for both check types, retention periods, SMS credits and seat counts inline. That is more than most companies disclose anywhere. Two caveats on coverage. The plan comparison is built from styled divs rather than a real table, so per-plan values lose their column alignment when flattened to text. We could read the numbers but not always which plan they belong to, so most allowances above are recorded without a plan. Discovery also found no billing or usage-limit help article. The other pages we reached are product documentation and integration guides that make no commercial claims, so there was little opportunity for the documentation to disagree with the pricing page. We found nothing wrong, and we also had less to compare than at most companies. The Try for Free button on Starter is not explained anywhere we read: no trial length, and no statement about whether a card is required.*

### Cronitor

https://cronitor.io · monitoring · found via category sweep: independent uptime and cron monitoring

Read **9** usable pages of 12 fetched, extracted **18** commercial promises, produced **2** findings. 25 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Hacker ($0 free forever); Business ($2 /mo per monitor plus $5 /mo per user); Enterprise (from $6,000 /yr annual invoice billing)

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Simple Pricing - Cronitor](https://cronitor.io/pricing) | Pricing page | 495 | read |
| [Sign Up - Cronitor](https://cronitor.io/sign-up) | Trial / signup | 33 | too little text to read |
| [Sign Up - Cronitor](https://cronitor.io/sign-up?flow=trial&plan=metered&billing_frequency=month) | Trial / signup | 89 | too little text to read |
| [Integrations](https://cronitor.io/docs/integrations) | Add-ons & integrations | 288 | read |
| [Help Center - Cronitor](https://cronitor.io/help) | Help centre | 105 | too little text to read |
| [Cronitor Developer Docs](https://cronitor.io/docs) | Product documentation | 214 | read |
| [Cronitor API Docs](https://cronitor.io/docs/api) | Product documentation | 738 | read |
| [Developer Guides - Learn best practices for monitoring m](https://cronitor.io/guides) | Help centre | 799 | read |
| [How to find and read crontab logs](https://cronitor.io/guides/where-are-cron-logs-stored) | Help centre | 292 | read |
| [SDKs & Agents](https://cronitor.io/docs/sdks) | Product documentation | 214 | read |
| [Configuring SAML SSO](https://cronitor.io/docs/saml-sso) | Product documentation | 844 | read |
| [[Cron] Job Monitoring](https://cronitor.io/docs/cron-job-monitoring) | Product documentation | 881 | read |
| https://cronitor.io/terms | | | blocked by robots.txt |
| https://cronitor.io/faq | | | HTTP 404 |

</details>

**1. Pricing page sells unlimited API requests. Docs document rate limits.**  
`medium impact` · `Ambiguity` · `high confidence`

The docs never publish the numbers, so a developer cannot size an integration before building it.

- **Claim A:** Unlimited API requests
  - Evidence: “Unlimited API requests”
  - Source: [https://cronitor.io/pricing](https://cronitor.io/pricing)
- **Claim B:** Rate limited, 429 on excess
  - Evidence: “The API has rate limits to ensure fair usage. If you exceed these limits, you'll receive a 429 Too Many Requests response.”
  - Source: [https://cronitor.io/docs/api](https://cronitor.io/docs/api)
- *Why this is not just wording: Unlimited and refused with a 429 past an unpublished ceiling are different answers to how much you can send.*
- *What would make this a non-issue: A rate limit caps speed, not volume, so both can be true. One line on the pricing page would close it.*

**2. SSO guide names the plan requirement. It omits the $5 per user charge.**  
`medium impact` · `Missing information` · `medium confidence`

An admin who follows the guide upgrades to Business and meets the surcharge on the next invoice. On twenty seats that is $100 a month.

- **Claim A:** SSO costs $5 per user extra
  - Evidence: “SAML SSO (+$5/mo per user)”
  - Source: [https://cronitor.io/pricing](https://cronitor.io/pricing)
- **Claim B:** Just subscribe to Business
  - Evidence: “Note: If the button is disabled, ensure your team is subscribed to the Business plan.”
  - Source: [https://cronitor.io/docs/saml-sso](https://cronitor.io/docs/saml-sso)
- *Why this is not just wording: One page states a per-user charge the other omits while answering what a customer needs to use the feature.*
- *What would make this a non-issue: The guide is not wrong, a Business subscription genuinely is required. Six more words would make it complete.*

*Not checkable from these pages: Both signup pages and the help centre returned almost no readable text, so we could not check whether the 14-day trial requires a credit card, or whether the help centre repeats the pricing page's figures. The API documentation states that rate limits exist but never publishes the numbers, so we could not check them against the unlimited claim. We saw no terms of service page, so renewal, refund and price-change terms were not reviewed.*

### Fathom Analytics

https://usefathom.com · web analytics · found via category sweep: privacy-focused web analytics

Read **10** usable pages of 13 fetched, extracted **15** commercial promises, produced **4** findings. 25 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Up to 500,000 pageviews ($45 /month); Larger pageview tiers (2M, 10M, 25M+) (priced by pageview band; largest tiers contact us)

<details><summary>Pages read</summary>

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

</details>

**1. Pricing page says you never switch analytics off. Terms allow suspension.**  
`high impact` · `Likely contradiction` · `high confidence`

The terms also add a first-month trigger the FAQ never mentions, and an account left suspended two months can be deleted with no refund.

- **Claim A:** Never switched off for overage
  - Evidence: “We'll never turn your analytics off for occasional traffic spikes or if a payment fails the first time”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Suspension after seven days
  - Evidence: “In the event you fail to upgrade your account within seven days of our request, we reserve the right to suspend your account and restrict your use of our Services anytime after the seventh day following our notice to you.”
  - Source: [https://usefathom.com/legal/terms](https://usefathom.com/legal/terms)
- *Why this is not just wording: Never turn your analytics off and reserve the right to suspend your account describe opposite outcomes for the same customer.*
- *What would make this a non-issue: The terms describe a right you may never use and the FAQ describes what you actually do. Dropping the word never would close it.*

**2. Pricing page sells full API access. The $19 to $399 ladder is elsewhere.**  
`high impact` · `Missing information` · `high confidence`

600 an hour is Tier 1 of six. The top tier costs nearly nine times the $45 plan it sits on.

- **Claim A:** Full API access, 600 per hour
  - Evidence: “Full API access with 600 requests per hour included.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Up to $399 a month for more
  - Evidence: “Tier 6 | $399/mo | 16,000 | 25”
  - Source: [https://usefathom.com/api/v1/rate-limits](https://usefathom.com/api/v1/rate-limits)
- *Why this is not just wording: The pricing page names no price for API capacity while another page prices it in six steps.*
- *What would make this a non-issue: 600 requests an hour is generous and most customers stay on Tier 1. The word Full is doing the work in a list that otherwise advertises no extra fees.*

**3. Event tracking has no extra fees, but events count as pageviews.**  
`medium impact` · `Ambiguity` · `medium confidence`

Your price is set entirely by monthly pageviews, so heavy event tracking moves a customer into a higher band.

- **Claim A:** Events included, no extra fees
  - Evidence: “Track conversions, revenue, and custom events on every plan. No extra fees.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Events counted as pageviews
  - Evidence: “those requests will be counted as if they were pageviews”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- *Why this is not just wording: No extra fees and counted as pageviews have different consequences for the invoice.*
- *What would make this a non-issue: No extra fees is fair if it means no separate line item, which is true. The two statements are about 2,000 words apart on the page.*

**4. You say you never discount. Your help centre lists an article on discount codes.**  
`low impact` · `Ambiguity` · `medium confidence`

If codes exist for partners or non-profits, everyone pays the exact same price needs a qualifier.

- **Claim A:** Never any discounts, ever
  - Evidence: “We've never done discounts, nor will we ever.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Help centre: Discount codes
  - Evidence: “Discount codes”
  - Source: [https://usefathom.com/docs/integrations](https://usefathom.com/docs/integrations)
- *Why this is not just wording: An article about discount codes implies a way to pay less than list price, which the FAQ says does not exist.*
- *What would make this a non-issue: This is the weakest item here. We saw the article title in a sidebar, not its contents, and it may say you do not issue codes.*

*Not checkable from these pages: Discovery did not reach the help articles behind the sidebar titles: Exceeding your plan limits, Billing FAQ, How do free trials work, Discount codes, and Upgrading or downgrading. Those are the pages most likely either to resolve or to worsen the findings above. Nothing we read says whether a credit card is required to begin the 7-day trial. The pricing page's slider shows one pageview band at a time, so we could only read the $45 band for 500,000 pageviews.*

### Knock

https://knock.app · notifications API · found via category sweep: notification infrastructure

Read **8** usable pages of 8 fetched, extracted **17** commercial promises, produced **2** findings. 24 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Developer ($0 / month); Starter ($250 / month); Enterprise (Contact us)

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing - Knock](https://knock.app/pricing) | Pricing page | 1856 | read |
| [Subscriptions - Knock Docs](https://docs.knock.app/concepts/subscriptions) | Billing & subscription help | 1150 | read |
| [Workflows API reference - Knock Docs](https://docs.knock.app/api-reference/workflows/cancel) | Billing & subscription help | 509 | read |
| [Users API reference - Knock Docs](https://docs.knock.app/api-reference/users/list_subscriptions) | Billing & subscription help | 3661 | read |
| [API reference - Knock Docs](https://docs.knock.app/reference) | Product documentation | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview) | Product documentation | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview/rate-limits) | Usage limits / quotas | 2033 | read |
| [API reference - Knock Docs](https://docs.knock.app/api-reference/overview/batch-rate-limits) | Usage limits / quotas | 2033 | read |
| https://dashboard.knock.app/signup | | | blocked by robots.txt |

</details>

**1. Pricing page says triggers are unlimited. Every endpoint is rate limited.**  
`medium impact` · `Ambiguity` · `high confidence`

Triggering a workflow is an API call, and the tiers are never mapped to plans or endpoints.

- **Claim A:** Unlimited workflow triggers
  - Evidence: “Workflow triggers | Unlimited | Unlimited | Unlimited”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- **Claim B:** 1 to 1,000 requests per second
  - Evidence: “Each endpoint in the Knock API is rate limited. Knock uses a tier system to determine the rate limit scale for each endpoint.”
  - Source: [https://docs.knock.app/api-reference/overview/rate-limits](https://docs.knock.app/api-reference/overview/rate-limits)
- *Why this is not just wording: Unlimited triggers and a per-second ceiling answer the same buyer question with different numbers.*
- *What would make this a non-issue: Rate limits and volume allowances are different, and your docs invite customers to ask for more. Naming the tier for the trigger endpoint would fix it.*

**2. Enterprise guides default to the Starter allowance. Only the FAQ says so.**  
`medium impact` · `Missing information` · `high confidence`

A customer paying well above Starter, who assumed guides scaled with their contract, finds out when you ask them to get in touch.

- **Claim A:** Contact us, volume discounts
  - Evidence: “Contact us Volume-based discounts and monthly notified user pricing available.”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- **Claim B:** 2,500 users, same as Starter
  - Evidence: “you'll have the same guides limit as our Starter plan: 2,500 active users a month”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- *Why this is not just wording: Contact us invites the reader to assume a negotiated number while the FAQ states a specific default equal to the tier below.*
- *What would make this a non-issue: The FAQ is on the same page, forty rows down, under a question aimed at existing customers rather than buyers.*

*Not checkable from these pages: We did not report the rate-limit tier table that appears on two documentation pages with different numbers in view. It is one table of endpoint scales reproduced on both pages, not two conflicting limits, and an automated reader could easily mistake it for a contradiction. We could not check which tier any given endpoint belongs to, since that mapping is not on the pages we read. Your pricing table promises unlimited feed retention while the API reference refers to data subject to deletion under the retention policy on your account. The retention policy page was not reachable from our crawl, so we could not tell whether these describe the same data and did not report it. The signup page is blocked by robots.txt, so trial and card-requirement terms were not checked.*

### SavvyCal

https://savvycal.com · scheduling · found via category sweep: independent scheduling tools

Read **8** usable pages of 13 fetched, extracted **10** commercial promises, produced **2** findings. 16 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Basic ($10 /user/mo); Premium ($17 /user/mo)

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Plans & Pricing · SavvyCal](https://savvycal.com/pricing) | Pricing page | 179 | read |
| [Sign Up for SavvyCal](https://savvycal.com/signup) | Trial / signup | 54 | too little text to read |
| [Integrations · SavvyCal](https://savvycal.com/integrations-directory) | Add-ons & integrations | 303 | read |
| [Meetings Help](https://docs.savvycal.com/) | Help centre | 58 | too little text to read |
| [SavvyCal Meetings Platform - SavvyCal Meetings](https://developers.savvycal.com/) | Product documentation | 152 | read |
| [SavvyCal Terms of Use](https://savvycal.com/terms) | Terms / legal | 2725 | read |
| [Free Time Zone API Â· SavvyCal](https://savvycal.com/time-zone-api) | Product documentation | 208 | read |
| [REST API - SavvyCal Meetings](https://developers.savvycal.com/category/rest-api) | Product documentation | 33 | too little text to read |
| [SavvyCal End User License Agreement for Downloadable Too](https://savvycal.com/eula) | Terms / legal | 557 | read |
| [Authentication - SavvyCal Meetings](https://developers.savvycal.com/authentication) | Help centre | 601 | read |
| [Webhooks - SavvyCal Meetings](https://developers.savvycal.com/webhooks) | Help centre | 679 | read |
| [Integrations - Meetings Help](https://docs.savvycal.com/category/5-integrations) | Add-ons & integrations | 89 | too little text to read |
| [Use Cases - Meetings Help](https://docs.savvycal.com/category/7-usage) | Usage limits / quotas | 89 | too little text to read |
| https://savvycal.com/faq | | | HTTP 404 |
| https://savvycal.com/help | | | HTTP 404 |
| https://savvycal.com/docs | | | HTTP 404 |

</details>

**1. Pricing page offers a free start. It shows only paid plans.**  
`medium impact` · `Missing information` · `medium confidence`

No trial length, no card policy, and no explanation of what activation changes.

- **Claim A:** Kick the tires for free
  - Evidence: “Kick the tires for free and only upgrade when you're ready to activate.”
  - Source: [https://savvycal.com/pricing](https://savvycal.com/pricing)
- **Claim B:** Cheapest plan is $10 a user
  - Evidence: “$ 10 /user/mo”
  - Source: [https://savvycal.com/pricing](https://savvycal.com/pricing)
- *Why this is not just wording: One sentence offers a free route in and the rest of the page documents only paid ones.*
- *What would make this a non-issue: The answer is likely in the FAQ, which is collapsed and did not render for us. The comparison table rendered without values for the same reason.*

**2. Terms allow price changes at any time, with no notice period.**  
`low impact` · `Missing information` · `high confidence`

Together these let a renewing price move without warning. Nothing on the pricing page sets an expectation either way.

- **Claim A:** Prices change at any time
  - Evidence: “We may change prices at any time.”
  - Source: [https://savvycal.com/terms](https://savvycal.com/terms)
- **Claim B:** Subscriptions renew automatically
  - Evidence: “Subscriptions will automatically renew for the same subscription period unless you cancel the account by the end of the then-current subscription period.”
  - Source: [https://savvycal.com/terms](https://savvycal.com/terms)
- *Why this is not just wording: The two clauses combine into a commercial term that appears nowhere the buyer decides.*
- *What would make this a non-issue: Ordinary boilerplate in the right place, and your 30-day money back guarantee already gives customers a way out.*

*Not checkable from these pages: This is the weakest coverage of the ten companies and we would rather say so than pad the report. The plan comparison on your pricing page rendered as a list of feature names with no per-plan values, so we could not check a single feature entitlement against your documentation. The FAQ rendered as a heading with no questions or answers. Your help site returned almost no readable text. We could not check the two things most worth checking here: which features are Basic versus Premium, and what your free entry route actually is. Your 30-day money back guarantee and your refund clause do agree with each other, which is worth saying, because that is the pair that most often does not.*

### ScreenshotOne

https://screenshotone.com · media API · found via category sweep: screenshot APIs

Read **15** usable pages of 15 fetched, extracted **17** commercial promises, produced **3** findings. 27 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Free ($0, 100 screenshots per month); Basic ($17 per month); Growth ($79 per month); Scale ($259 per month)

<details><summary>Pages read</summary>

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
| [Fail rendering if the content contains a string - Screen](https://screenshotone.com/docs/guides/fail-if-content-contains) | Help centre | 282 | read |
| [Upload to S3 - ScreenshotOne Docs](https://screenshotone.com/docs/guides/upload-to-s3) | Help centre | 873 | read |
| [The Screenshot API for Airtable](https://screenshotone.com/integrations/airtable) | Add-ons & integrations | 169 | read |
| [The Screenshot API for Make](https://screenshotone.com/integrations/make) | Add-ons & integrations | 183 | read |
| [The Screenshot API for Bubble](https://screenshotone.com/integrations/bubble) | Add-ons & integrations | 167 | read |
| https://dash.screenshotone.com/sign-up | | | blocked by robots.txt |
| https://screenshotone.com/faq | | | HTTP 404 |
| https://screenshotone.com/terms | | | HTTP 404 |

</details>

**1. Three pages give three answers to what happens when you exceed your plan.**  
`high impact` · `Ambiguity` · `high confidence`

A third page says overage is billed only if extra charging is enabled, and never says what happens when it is not.

- **Claim A:** $0.009 per extra screenshot
  - Evidence: “$0.009 per extra”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** Throttling or suspension
  - Evidence: “throttling, or temporary suspension of access”
  - Source: [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)
- *Why this is not just wording: Paying more, being slowed, and losing access are three different outcomes for the same event.*
- *What would make this a non-issue: Overage billing is likely the normal path and throttling a reserve power for abuse. The sentence that needs finishing is if extra charging is enabled.*

**2. Terms allow you to change quotas, not just prices.**  
`medium impact` · `Missing information` · `high confidence`

The allowances are the product, so this says what a customer bought can be redefined mid-subscription.

- **Claim A:** Scale includes 50,000 screenshots
  - Evidence: “50,000 screenshots”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** Quotas may change at any time
  - Evidence: “We reserve the right to modify pricing, features, usage limits, quotas, or plan structures at any time.”
  - Source: [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)
- *Why this is not just wording: A right to change quotas can reduce what a customer receives without changing what they pay.*
- *What would make this a non-issue: A notice commitment on the pricing page would neutralise this entirely.*

**3. Pricing page promises a full refund. Docs say unused credits are not refunded.**  
`medium impact` · `Likely contradiction` · `medium confidence`

A customer who buys Scale, uses a fraction of the 50,000 screenshots and asks for their money back inside a month has been told both.

- **Claim A:** Full refund within 30 days
  - Evidence: “email us at support@screenshotone.com within 30 days, and we will refund you in full, no questions asked”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** No refunds for unused credits
  - Evidence: “No refunds for unused credits”
  - Source: [https://screenshotone.com/docs/credits](https://screenshotone.com/docs/credits)
- *Why this is not just wording: One page promises money back for any reason inside 30 days and the other rules it out for the most common case.*
- *What would make this a non-issue: These probably address different things, the subscription fee and the cash value of credits. The credits page is where a cancelling customer lands.*

*Not checkable from these pages: This is the most complete set of pages of the ten companies: fifteen pages all readable, a pricing page that publishes per-plan quotas, rate limits and overage rates inline, and a credits page that explains reset and rollover behaviour properly. What we could not check is what actually happens when extra charging is disabled and the quota runs out. No page we read says. We also could not confirm whether the free tier survives cancellation. The credits page says a cancelled customer is downgraded to the free plan, or loses access if the free plan is not available, without saying when that would be the case.*

### Umami

https://umami.is · web analytics · found via category sweep: open-source analytics with a hosted tier

Read **0** usable pages of 3 fetched, extracted **0** commercial promises, produced **0** findings. 0 quotes verified, 0 candidate finding(s) discarded.

<details><summary>Pages read</summary>

| Page | Type | Words | Status |
|---|---|---|---|
| [Pricing – Umami](https://umami.is/pricing) | Pricing page | 0 | too little text to read |
| [Introduction – umami](https://umami.is/docs) | Product documentation | 0 | too little text to read |
| [Terms of Service – Umami](https://umami.is/terms) | Terms / legal | 0 | too little text to read |

</details>

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

*Not checkable from these pages: Nothing could be checked. All three pages we reached, including the pricing page, returned a page shell with no readable text at all. The site builds its content in the browser, and the headless-browser fallback could not run in the environment this experiment was executed in. This is a failure of our tool, not a finding about Umami, and it should be counted as a miss rather than as a clean result. Roughly one company in ten in this sample was invisible for this reason.*

### Unkey

https://www.unkey.com · API management · found via category sweep: API key management

Read **10** usable pages of 11 fetched, extracted **14** commercial promises, produced **2** findings. 23 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Starter ($5 / mo); Pro ($25 / mo); Business ($50 / mo); Enterprise (Contact the team; annual contracts available); Free plan (documented only in the docs) (not published on the pricing page)

<details><summary>Pages read</summary>

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

</details>

**1. Free plan keeps logs longer than the $5 plan.**  
`high impact` · `Likely contradiction` · `high confidence`

Pro at $25 still has less audit retention than free. Only Business at $50 matches it.

- **Claim A:** Free: 7 days logs, 30 audit
  - Evidence: “| Audit log retention | 30 days | Varies by plan |”
  - Source: [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)
- **Claim B:** Starter: 3 days logs, 7 audit
  - Evidence: “$5
1
3 days
7 days
Email”
  - Source: [https://www.unkey.com/pricing](https://www.unkey.com/pricing)
- *Why this is not just wording: The same two named metrics, in the same unit, are larger on the free tier than the paid one.*
- *What would make this a non-issue: Paid figures come from a grid built from divs, so we checked the column against the plan cards. It also gives Starter 1 vCPU, 2 GB, 1 domain and $5 credits, all matching.*

**2. Pricing page says start for free. No free plan is shown.**  
`medium impact` · `Missing information` · `high confidence`

The free plan exists with real numbers: 150,000 API requests a month, 7 days of log retention, no team members.

- **Claim A:** Start for free, twice on page
  - Evidence: “Start for free, scale as you go with predictable usage-based pricing.”
  - Source: [https://www.unkey.com/pricing](https://www.unkey.com/pricing)
- **Claim B:** Free plan is in the docs only
  - Evidence: “| API requests per month | 150,000 | Varies by plan |”
  - Source: [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)
- *Why this is not just wording: A whole plan with published quotas is missing from the page whose job is to list the plans.*
- *What would make this a non-issue: The free tier may be being retired, or offered only at signup. The pricing page still promises it twice.*

*Not checkable from these pages: The pricing page FAQ rendered as a heading with no questions, so anything it says about the free plan, trials or overage was not visible to us. The pricing page states API request allowances nowhere at all. The docs give the free plan 150,000 a month and say paid plans vary, but no page we read says by how much, so request quotas could not be checked against each other. The cost calculator produced a single $188 estimate from its default inputs rather than a price list.*

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
5. All ten were harvested with identical settings (`{"max_pages": 16}`) and analysed with the identical prompt from `prompts.py`. Nothing was changed for any individual company.

**Selected:** Baserow, Bento, Checkly, Cronitor, Fathom Analytics, Knock, SavvyCal, ScreenshotOne, Umami, Unkey.

### Complete candidate pool

| # | Company | Category | Where it was found | Why it qualifies | Eligible? |
|---|---|---|---|---|---|
| 1 | [Fathom Analytics](https://usefathom.com) | web analytics | category sweep: privacy-focused web analytics | Independent, founder-led analytics vendor with a public per-plan pricing page and a public documentation site. | **yes, selected** |
| 2 | [Simple Analytics](https://www.simpleanalytics.com) | web analytics | category sweep: privacy-focused web analytics | Small European analytics vendor publishing usage-based plans and public docs. | yes |
| 3 | [Pirsch Analytics](https://pirsch.io) | web analytics | category sweep: privacy-focused web analytics | Small independent analytics product with published pageview allowances and docs. | yes |
| 4 | [Umami](https://umami.is) | web analytics | category sweep: open-source analytics with a hosted tier | Open-source analytics with a commercial hosted plan and public documentation. | **yes, selected** |
| 5 | [Buttondown](https://buttondown.com) | email / newsletters | category sweep: independent newsletter platforms | Solo-founder newsletter tool with subscriber-tiered public pricing and docs. | yes |
| 6 | [EmailOctopus](https://emailoctopus.com) | email / newsletters | category sweep: independent email marketing | Small email marketing vendor with public contact-tiered pricing and a help centre. | yes |
| 7 | [Loops](https://loops.so) | email / newsletters | category sweep: modern SaaS email tools | Early-stage email platform with public per-contact pricing and public docs. | yes |
| 8 | [Bento](https://bentonow.com) | email / newsletters | category sweep: modern SaaS email tools | Small marketing-automation vendor with published plans and a help centre. | **yes, selected** |
| 9 | [Tally](https://tally.so) | forms | category sweep: independent form builders | Bootstrapped form builder with a public two-tier pricing page and a help centre. | yes |
| 10 | [Fillout](https://www.fillout.com) | forms | category sweep: independent form builders | Small form product with public plan tiers, response limits and documentation. | yes |
| 11 | [Formspree](https://formspree.io) | forms | category sweep: form back-end APIs | Long-running independent form back end with submission-limited plans and docs. | yes |
| 12 | [SavvyCal](https://savvycal.com) | scheduling | category sweep: independent scheduling tools | Bootstrapped scheduling product with public pricing and a help centre. | **yes, selected** |
| 13 | [Cal.com](https://cal.com) | scheduling | category sweep: open-source scheduling | Open-source scheduling vendor with a public seat-based pricing page and docs. | yes |
| 14 | [ScrapingBee](https://www.scrapingbee.com) | web data API | category sweep: web-scraping APIs | Small API vendor with credit-based public pricing and full API documentation. | yes |
| 15 | [Scrapfly](https://scrapfly.io) | web data API | category sweep: web-scraping APIs | Independent scraping API with published credit allowances and detailed docs. | yes |
| 16 | [ScreenshotOne](https://screenshotone.com) | media API | category sweep: screenshot APIs | Solo-founder screenshot API with request-quota pricing and public documentation. | **yes, selected** |
| 17 | [Bannerbear](https://www.bannerbear.com) | media API | category sweep: image generation APIs | Bootstrapped image-generation API with quota-based plans and public docs. | yes |
| 18 | [Placid](https://placid.app) | media API | category sweep: image generation APIs | Small creative-automation API with public usage tiers and documentation. | yes |
| 19 | [Baserow](https://baserow.io) | no-code database | category sweep: open-source Airtable alternatives | Open-core database vendor with public per-seat pricing and extensive docs. | **yes, selected** |
| 20 | [NocoDB](https://nocodb.com) | no-code database | category sweep: open-source Airtable alternatives | Open-source database platform with a public cloud pricing page and docs. | yes |
| 21 | [Chartbrew](https://chartbrew.com) | BI / dashboards | category sweep: small open-source BI tools | Small open-source dashboard product with a hosted paid tier and public docs. | yes |
| 22 | [Outseta](https://www.outseta.com) | subscription / CRM | category sweep: all-in-one SaaS back-office tools | Small vendor bundling billing, CRM and help desk, with public pricing and a KB. | yes |
| 23 | [Userlist](https://userlist.com) | lifecycle marketing | category sweep: SaaS lifecycle messaging | Bootstrapped lifecycle email tool with user-count pricing and a help centre. | yes |
| 24 | [Encharge](https://encharge.io) | lifecycle marketing | category sweep: SaaS lifecycle messaging | Small marketing-automation vendor with public tiered pricing and documentation. | no: no public pricing page could be discovered |
| 25 | [Resend](https://resend.com) | email API | category sweep: developer email APIs | Early-stage transactional email API with public volume pricing and docs. | yes |
| 26 | [Knock](https://knock.app) | notifications API | category sweep: notification infrastructure | Small notifications-infrastructure vendor with public MAU pricing and docs. | **yes, selected** |
| 27 | [Svix](https://www.svix.com) | webhooks API | category sweep: webhook infrastructure | Small webhooks-as-a-service vendor with public message-volume pricing and docs. | yes |
| 28 | [Hookdeck](https://hookdeck.com) | webhooks API | category sweep: webhook infrastructure | Independent event-gateway vendor with public request-volume pricing and docs. | yes |
| 29 | [Cronitor](https://cronitor.io) | monitoring | category sweep: independent uptime and cron monitoring | Small monitoring vendor with public per-monitor pricing and documentation. | **yes, selected** |
| 30 | [Checkly](https://www.checklyhq.com) | monitoring | category sweep: synthetic monitoring | Mid-size independent monitoring vendor with usage-based pricing and full docs. | **yes, selected** |
| 31 | [Instatus](https://instatus.com) | status pages | category sweep: status page vendors | Small status-page vendor with public tiered pricing and a help centre. | yes |
| 32 | [Tinybird](https://www.tinybird.co) | data infrastructure | category sweep: real-time analytics back ends | Independent real-time data platform with public usage pricing and docs. | yes |
| 33 | [Turso](https://turso.tech) | data infrastructure | category sweep: hosted database startups | Early-stage hosted database with public row/storage allowances and docs. | yes |
| 34 | [Doppler](https://www.doppler.com) | secrets management | category sweep: developer secrets management | Small secrets-management vendor with public per-seat pricing and documentation. | yes |
| 35 | [Infisical](https://infisical.com) | secrets management | category sweep: open-source secrets management | Open-source secrets platform with a public cloud pricing page and docs. | yes |
| 36 | [Unkey](https://www.unkey.com) | API management | category sweep: API key management | Early-stage API management vendor with public request-volume pricing and docs. | **yes, selected** |
