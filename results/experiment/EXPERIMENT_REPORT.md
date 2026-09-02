# Do SaaS companies contradict themselves in public?

### A ten-company experiment with the commercial-consistency auditor

Harvested 2026-09-02 07:57:41 UTC · analysed 2026-09-02 08:10:40 UTC · analyst backend `agent` · random seed `20260902` · candidate pool 36 · eligible 35 · analysed 10

## The short version

Ten smaller SaaS companies, drawn at random from a frozen pool of 36. Nine could be read.
**111 public pages fetched, 90 of them readable, 140 commercial promises extracted,
19 findings, and 208 quotes verified against the pages they were taken from.**

Eight of the nine readable companies had at least one thing worth checking. The strongest
five:

* **Unkey** documents a free plan that keeps logs for 7 days and audit logs for 30 days.
  Its pricing page gives the $5 Starter plan 3 days and 7 days. Paying moves you backwards
  on both, and you have to reach the $50 plan before audit retention matches what free
  already gave you.
* **Fathom** promises on its pricing page that it will *never* switch your analytics off
  for going over. Its terms let it suspend the account seven days after an upgrade request,
  and delete it two months later, with no refund.
* **Fathom** again: "Full API access with 600 requests per hour included" sits in a feature
  list whose neighbours advertise "No extra fees". A separate page prices the next five
  rungs of API throughput at $19, $39, $79, $199 and $399 a month — the top rung nearly
  nine times the price of the plan it sits on.
* **ScreenshotOne** answers "what happens when I exceed my plan?" three different ways on
  three pages: pay $0.009 per extra, or be billed automatically *if extra charging is
  enabled*, or be throttled or suspended.
* **Bento** builds its whole pricing argument on Active Users, explicitly so that dormant
  contacts do not inflate the bill. Its documentation FAQ says it charges on the number of
  subscribers, defined as every unique email address in the account.

None of these is a gotcha. Every one is two real sentences that a customer could read in
either order, quoted verbatim, with both links in the report.

## Does a recurring public commercial-consistency problem exist?

**Yes, and it is more common than we expected — but it is a drift problem, not a dishonesty
problem.**

Eight of nine readable companies had something. The pattern that recurs is not a company
misleading anyone; it is a company whose pricing page and documentation were written at
different times by different people and never reconciled. Unkey's free-plan table almost
certainly predates a repackaging. Bento's FAQ answer is older copy from before the Active
Users model. Fathom's terms were last updated in 2021 and its FAQ is current marketing.

Three shapes came up more than once:

1. **The pricing page and the docs disagree about a number** (Unkey's retention, Bento's
   billing metric, Baserow's payment methods). Four findings.
2. **"Unlimited" or "full" meets a documented limit** (Cronitor, Knock, Fathom's API).
   Four findings. Never technically false, always the thing a developer wants to know.
3. **A commercial condition lives only in the terms or a docs page** (Fathom's suspension
   rights, ScreenshotOne's right to change quotas, Baserow's API concurrency, Knock's
   Enterprise guides default). Six findings.

The third group is the one to be careful with. Some of it is genuinely load-bearing —
ScreenshotOne reserving the right to change *usage limits and quotas*, not just prices, is
a real term about what you receive. Some of it is ordinary boilerplate we rated low on
purpose.

## Is it telling companies anything they did not already know?

For roughly half of the findings, yes, and we can say which half.

Nobody at Unkey has sat down with the docs table and the pricing table side by side; if
they had, the retention inversion would already be fixed. The same goes for Knock's
Enterprise guides default, ScreenshotOne's three answers, and Bento's billing metric. These
are all invisible from inside the company because no single person reads both pages in one
sitting — which is exactly the job worth automating.

The other half — auto-renewal clauses, price-change rights, refund wording — every founder
knows those are in their terms. Reported as "a contradiction we found", that is padding.
Reported as "your buyer never sees this", it is a fair point about placement, and we rated
those findings low or medium accordingly rather than dressing them up.

## Likely false positives, honestly

**No finding in this run cites evidence that does not exist.** All 208 quotes were located
character-by-character in the harvested page, and no finding was discarded at verification.
That number needs a caveat, which we come back to below.

The real risk with this design is not fabricated evidence. It is **over-reading**: two real
sentences, correctly quoted, that anyone at the company would reconcile in a second. Our own
assessment of the 19:

* **Nine we would defend to a founder without hedging** — Unkey ×2, Fathom ×2, ScreenshotOne
  (overage), Bento (billing metric), Knock (Enterprise guides), Cronitor ×2.
* **Seven that are real but modest** — placement problems, boilerplate in the right place,
  things a founder will say "yes, we know" to.
* **Three we would expect an informed reader to push back on**: Fathom's discount-codes item
  (we saw only a navigation link, and said so in the finding), SavvyCal's price-change clause
  (ordinary boilerplate), and Bento's "no feature gating" item (where "tier" almost certainly
  means volume tier, which we flagged in the caveat).

Call it **three soft findings in nineteen, about 16%**, with none of them fabricated and all
three carrying a caveat that says what would make them wrong. That is a different and better
failure mode than the alternative, but it is not zero.

Two things would have been false positives and were deliberately not reported, which is
worth as much as the findings themselves:

* Knock publishes an endpoint rate-limit tier table on two documentation pages. Read
  mechanically, "60 requests / second" on one page and "200 requests / second" on another
  looks like a contradiction. It is one table of endpoint scales reproduced twice.
* Checkly, Baserow and Unkey all render their comparison tables as styled divs. Flattened to
  text, a monthly/annual toggle or a mis-aligned column produces convincing nonsense. We
  reported a retention finding for Unkey only after cross-checking the column against the
  plan cards — the same column that gives Starter 3 days also gives it 1 vCPU, 2 GB, 1 custom
  domain and $5 of credits, all matching the Starter card — and we said so in the caveat.

## What actually limits the tool

**Client-side rendering, by a wide margin.** Umami returned *zero* readable words from all
three pages we reached, including the pricing page, so it could not be analysed at all. That
is a miss, not a clean result, and we have counted it as one. SavvyCal's comparison table
rendered as feature names with no values and its FAQ as an empty heading, so its report is
visibly thinner than the rest. Twenty-one of the 111 pages we fetched came back effectively empty, and a further 29 could
not be fetched at all. The
headless-browser fallback is implemented and Chromium launches, but the browser had no
outbound network access in the sandbox this ran in, so it could never be exercised.

**Flattened tables.** Every comparison grid on these sites is divs, not `<table>`. An early
version of the harvester de-duplicated repeated text lines, which silently destroyed those
grids — "1", "2" and "Unlimited" repeat down a column and were being dropped. Unkey's
retention finding, the best in the run, was invisible until that was fixed. There are almost
certainly equivalent findings we are still missing at the other companies.

**Discovery spends its budget in the wrong place.** For Checkly, the crawler returned twelve
pages of which eleven were product documentation and integration guides that make no
commercial claims at all; it never found a billing or usage-limits article. Checkly's zero is
partly a real result — their pricing page is the best of the ten, publishing overage rates
and retention inline — and partly an artefact of having had almost nothing to compare it to.

**The honest caveat about the verification numbers.** Zero rejections out of 208 quotes is
not evidence that the model does not fabricate. In this run the analyst and the verifier were
the same model in the same session, and quotes were checked as they were written. The
verifier was tested adversarially instead: fabricated quotes, paraphrased quotes, quotes
split from one passage, missing schema fields and invalid severities are all rejected, and a
real quote attributed to the wrong page is corrected rather than dropped. An unattended API
run would produce a non-zero rejection rate, and that number is the one worth reporting next
time.

**Two conflicts of interest we cannot design away here.** The analyst had already seen these
same ten companies during an earlier rule-based version of this tool, so this was not a blind
read. And the assessment above — which findings are strong, which are soft — is the analyst
grading its own work. Both need an independent reviewer before any of this is published.

## Would a SaaS founder try this?

**Yes, and on this evidence they would get something worth their time.**

The offer costs one URL. Eight of nine readable companies got back at least one finding, and
five got something a founder would forward to whoever owns the docs. The report quotes their
own words, links both pages, and says in one line what would make each finding wrong — so the
whole thing is checkable in about two minutes, which is the only standard that matters for a
cold audit of someone else's website.

The weakest outcome in the set is instructive. Checkly got zero findings and a paragraph
explaining that their pricing page publishes more than most companies disclose anywhere. That
is a perfectly good thing to receive, and it is not an embarrassing result for the tool.

What would make us cautious about promising a hit rate: this sample was small, independent,
mostly developer-tool companies with three or four tiers. That is the easy case. It is also
not the case with the most money in it.

## What to improve before publishing

1. **Make JavaScript rendering work end to end.** One company in ten was invisible and
   another was read at a quarter depth. These are the modern, JS-heavy pricing pages most
   likely to have drifted, so the tool is currently blindest exactly where it should be
   sharpest.
2. **Parse comparison grids properly instead of flattening them.** Every one of these sites
   builds its plan table from divs. Reconstructing the column structure — rather than
   inferring it and cross-checking against the plan cards by hand, as we did for Unkey —
   would turn the single richest source of per-plan promises from a hazard into an asset.
3. **Spend the page budget on billing and limits content.** Discovery gave Checkly eleven
   documentation pages that make no commercial claims. Prefer billing, quota, plan-change and
   FAQ articles over SDK references and installation guides.
4. **Run it unattended through the API backend and report the rejection rate.** The verifier
   is the reason to trust this design and it has not yet been tested where it matters, with
   an analyst that has not been double-checking its own quotes as it writes them.
5. **Separate the two products in the output.** "Your pricing page and your docs disagree"
   and "this condition is not where your buyer will see it" are different claims with
   different value. Lead with the first; keep the second as a secondary list so six placement
   notes cannot read as six contradictions.
6. **Get an independent reviewer before publishing any hit-rate claim.** The analyst wrote
   the findings and then graded them, having already seen these companies once. Nothing in
   the numbers above survives that objection on its own.

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

**Verification** — every quote the analyst produced was checked against the page it was attributed to:

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
| https://baserow.io/help | — | — | HTTP 404 |
| https://baserow.io/terms | — | — | HTTP 404 |

</details>

**1. Your pricing page offers Enterprise customers payment by invoice; your FAQ says you only accept credit cards**  
`medium impact` · `Likely contradiction` · `high confidence`

"Payment by invoice" is listed as a reason to choose Enterprise, and it appears again in the plan comparison table. Your FAQ answers the question of what payment methods are accepted with a flat statement that credit card is currently the only option. An enterprise buyer doing diligence — exactly the buyer who cannot put a five-figure annual contract on a corporate card — will read the FAQ and conclude that you cannot invoice them.

- **Claim A:** Enterprise customers can pay by invoice
  - Evidence: “Payment by invoice”
  - Source: [https://baserow.io/pricing](https://baserow.io/pricing)
- **Claim B:** Credit card is the only payment method accepted
  - Evidence: “Currently, you can pay only with a credit card. We plan to add more payment methods in the future.”
  - Source: [https://baserow.io/faq](https://baserow.io/faq)
- *Why this is not just wording: One page names invoicing as a purchasable Enterprise benefit and the other states that no payment method other than credit card exists; those are different facts, not different phrasings.*
- *What would make this a non-issue: The FAQ answer is almost certainly about self-serve checkout, where credit card genuinely is the only route, and invoicing is arranged through sales. As written, though, neither page says so, and the FAQ is the page a buyer searches.*

**2. Every paid plan is capped at the same 10 concurrent API requests, and your plan comparison never mentions it**  
`medium impact` · `Missing information` · `medium confidence`

Your pricing page sells usage that scales with price: rows go from 3,000 to 1,000,000 and automation credits from 2,000 to 2,000,000 across the tiers. API throughput does not scale at all. The FAQ discloses a flat ceiling of 10 concurrent requests for every Baserow Cloud plan, adds that it is subject to fair use, and reserves the right to lower it. For a product that markets itself as API-first, a customer sizing an integration against the Advanced tier has no way of learning from the pricing page that paying nine times more buys no additional API concurrency.

- **Claim A:** Usage allowances scale by plan on the pricing page — Advanced buys 250,000 rows per workspace
  - Evidence: “250,000 rows per workspace”
  - Source: [https://baserow.io/pricing](https://baserow.io/pricing)
- **Claim B:** API concurrency is fixed at 10 for every Cloud plan and may be reduced at Baserow's discretion
  - Evidence: “In Baserow Cloud, there's a limit of 10 concurrent API requests. This limit is subject to a fair use policy, and we reserve the right to lower it if it affects overall performance.”
  - Source: [https://baserow.io/faq](https://baserow.io/faq)
- *Why this is not just wording: The plan comparison lists every other usage dimension by tier and omits this one entirely, so a reader cannot infer either the cap or the fact that it does not improve with price.*
- *What would make this a non-issue: Your pricing page does carry a collapsed FAQ item titled "What are the limitations in records, rows, and API requests?", so the answer may be one click away rather than on another page. We could not read the collapsed panel, only its heading.*

*Not checkable from these pages: The plan comparison table on the pricing page is built from styled divs rather than a real table, so when it is flattened to text the values lose their column alignment. Several rows publish three values for four plans (row change history, application users), which may be a genuine gap or may just be how the grid collapses — we could not tell, and did not report it. The Premium plan advertises a "Free trial" with no length stated on any page we read, and nothing anywhere states whether a credit card is required to start it.*

### Bento

https://bentonow.com · email / newsletters · found via category sweep: modern SaaS email tools

Read **13** usable pages of 13 fetched, extracted **13** commercial promises, produced **2** findings. 20 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Marketing Platform ($29/mo up to 5,000 Active Users, then tiered from $0.01 per Active User); Transactional Email ($0/mo — first 100 emails free, then $5/mo to 12,500 and $0.09 per 1,000 after); Bento Chat (add-on) (+$30/mo, requires Marketing Platform)

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
| https://bentonow.com/pricing.md | — | — | skipped: content-type text/markdown; charset= |
| https://bentonow.com/faq | — | — | HTTP 404 |
| https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000 | — | — | blocked by robots.txt |
| https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0 | — | — | blocked by robots.txt |
| https://bentonow.com/docs/integrations/cli.md | — | — | skipped: content-type text/markdown; charset= |

</details>

**1. Your pricing page bills on active users; your FAQ says you bill on total subscribers**  
`high impact` · `Likely contradiction` · `high confidence`

The entire argument of your pricing page is that you charge for Active Users — people who are subscribed or who did something in the last 30 days — and that dormant contacts do not inflate the bill. Your documentation FAQ answers "How does pricing work?" with a flat statement that you charge on the number of subscribers, and then defines a subscriber as any unique email address in the account. For a list with a long tail of dormant addresses those two rules produce materially different invoices, and the difference is the single reason a prospect would choose you over the competitors your own comparison table names.

- **Claim A:** Billing is based on Active Users — subscribed, or active in the last 30 days
  - Evidence: “Subscribed users or people with an event in the last 30 days.”
  - Source: [https://bentonow.com/pricing](https://bentonow.com/pricing)
- **Claim B:** Billing is based on the total number of subscribers, meaning every unique email address held
  - Evidence: “Bento charges based on the number of subscribers you have.”
  - Source: [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)
- *Why this is not just wording: "Active Users in the last 30 days" and "every unique email address in your account" are two different countable populations, so they are two different prices for the same list.*
- *What would make this a non-issue: The FAQ answer is probably just older copy written before the Active Users model, and "subscriber" may be intended loosely. That is exactly the problem: it is the page a customer searches when they want to know what drives their bill.*

**2. Your FAQ says every feature is included with no gating, while your pricing page sells chat as a $30/month add-on**  
`medium impact` · `Ambiguity` · `medium confidence`

"All features are included at every tier - no feature gating" is a strong promise, and it is the answer a prospect gets when they ask how pricing works. Your pricing page then sells Bento Chat — shared inbox, live chat, SMS, routing, AI agents — for an extra $30 a month, and requires the Marketing Platform underneath it. Someone who reads the FAQ first will budget $29 and be surprised at $59.

- **Claim A:** No feature is gated; everything is included at every tier
  - Evidence: “All features are included at every tier”
  - Source: [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)
- **Claim B:** Chat, SMS and AI agents cost an additional $30/month on top of the Marketing Platform
  - Evidence: “+$30/mo adds shared inbox, live chat, SMS, routing, saved replies, and AI agents. Requires Marketing Platform.”
  - Source: [https://bentonow.com/pricing](https://bentonow.com/pricing)
- *Why this is not just wording: One page states that nothing is behind a paywall while the other puts a named set of features behind a separate monthly charge.*
- *What would make this a non-issue: "Tier" almost certainly means volume tier — the features genuinely do not change as your list grows — and Chat is arguably a separate product rather than a gated feature. Adding four words to the FAQ answer would remove the ambiguity.*

*Not checkable from these pages: The FAQ's answer to "What's the API rate limit?" is collapsed and did not render, though a table of per-endpoint limits appears on the same page. Nothing we read states whether a credit card is required to start the 30-day trial, or what happens to a list that exceeds fair use on marketing sends — the term is used but never defined anywhere we could read.*

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
| https://app.checklyhq.com/signup | — | — | blocked by robots.txt |
| https://www.checklyhq.com/faq | — | — | HTTP 404 |
| https://www.checklyhq.com/help | — | — | HTTP 404 |
| https://www.checklyhq.com/docs/llms.txt | — | — | skipped: content-type text/plain; charset=utf |

</details>

**No findings.** Nothing on the pages read contradicted anything else with enough evidence to report.

*Not checkable from these pages: Nothing on the pages we read contradicts anything else, and this is a genuinely tidy set of pages: the pricing page publishes included volumes, the pre-purchase rate AND the higher automatic overage rate for both check types, retention periods, SMS credits and seat counts inline, which is more than most companies disclose anywhere. Two caveats on coverage. First, the plan comparison is built from styled divs rather than a real table, so when flattened to text the per-plan values lose their column alignment; we could read the numbers but not always which plan each belongs to, so most allowances above are recorded without a plan. Second, discovery found no billing or usage-limit help article — the other pages we reached are product documentation and integration guides that make no commercial claims — so there was little opportunity for the documentation to disagree with the pricing page. A tidier way to say it: we found nothing wrong, but we also had less to compare than at most companies. The 'Try for Free' button on Starter is not explained anywhere we read: no trial length, and no statement about whether a card is required.*

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
| https://cronitor.io/terms | — | — | blocked by robots.txt |
| https://cronitor.io/faq | — | — | HTTP 404 |

</details>

**1. Your pricing page sells "unlimited API requests" while your API documentation says the API is rate limited**  
`medium impact` · `Ambiguity` · `high confidence`

The Business plan is advertised as including unlimited API requests, which a buyer will read as "I will never be cut off". Your API documentation tells a different story: there are rate limits, and exceeding them returns a 429. Both statements can be true at once — a rate limit throttles the speed of requests rather than capping the total — but nothing on either page says so, and the documentation never publishes the actual numbers. The customer who finds out is a developer whose integration has just started failing in production.

- **Claim A:** The Business plan includes unlimited API requests
  - Evidence: “Unlimited API requests”
  - Source: [https://cronitor.io/pricing](https://cronitor.io/pricing)
- **Claim B:** The API is rate limited and rejects requests above the limit
  - Evidence: “The API has rate limits to ensure fair usage. If you exceed these limits, you'll receive a 429 Too Many Requests response.”
  - Source: [https://cronitor.io/docs/api](https://cronitor.io/docs/api)
- *Why this is not just wording: "Unlimited" and "you will be refused with a 429 past a limit we do not publish" are different commercial promises, not two phrasings of one.*
- *What would make this a non-issue: A throughput limit and a volume allowance really are different things, so this is a clarity problem rather than a broken promise. One sentence on the pricing page, and the actual numbers in the docs, would close it.*

**2. Your SSO documentation tells customers they need the Business plan, without mentioning that SSO costs an extra $5 per user on top**  
`medium impact` · `Missing information` · `medium confidence`

Your pricing page is clear that SAML single sign-on is a paid add-on for Business customers at $5 per user per month. Your SSO setup guide tells an administrator who finds the button greyed out simply to make sure the team is on the Business plan. An admin following the documentation reasonably concludes that upgrading to Business is all that is required, and only discovers the per-user surcharge when the bill changes. On a twenty-person team that is an unbudgeted $100 a month.

- **Claim A:** SAML SSO is an add-on costing $5 per user per month on Business
  - Evidence: “SAML SSO (+$5/mo per user)”
  - Source: [https://cronitor.io/pricing](https://cronitor.io/pricing)
- **Claim B:** The SSO setup guide gives a Business subscription as the requirement, and says nothing about an additional charge
  - Evidence: “Note: If the button is disabled, ensure your team is subscribed to the Business plan.”
  - Source: [https://cronitor.io/docs/saml-sso](https://cronitor.io/docs/saml-sso)
- *Why this is not just wording: One page states a per-user charge that the other page omits entirely while answering the exact question of what a customer needs in order to use the feature.*
- *What would make this a non-issue: The documentation is not wrong — a Business subscription genuinely is required. It is incomplete rather than contradictory, and adding six words to that note would fix it.*

*Not checkable from these pages: Both signup pages and the help centre returned almost no readable text, so we could not check whether the 14-day trial requires a credit card, or whether the help centre repeats the pricing page's figures. The API documentation states that rate limits exist but never publishes the numbers, so we could not check them against the 'unlimited' claim or against each other. We also saw no terms of service page, so renewal, refund and price-change terms were not reviewed.*

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
| https://usefathom.com/api/llms.txt | — | — | skipped: content-type text/plain; charset=utf |
| https://usefathom.com/faq | — | — | HTTP 404 |
| https://usefathom.com/help | — | — | HTTP 404 |

</details>

**1. Your pricing page promises you will never switch analytics off for going over; your terms reserve the right to suspend the account**  
`high impact` · `Likely contradiction` · `high confidence`

The FAQ on your pricing page is written to remove exactly this worry: you will never turn someone's analytics off over a traffic spike, and if they go over two months running you simply offer an upgrade, which they can take or leave with no hard feelings. Your terms and conditions describe a different process. There, a customer who does not upgrade within seven days of being asked can have their account suspended, and an account left suspended for two months can be deleted — with no refund. The terms also add a trigger the FAQ never mentions: significantly exceeding the limit inside the first month, judged at your sole discretion. For a company whose whole brand is candour about pricing, this is the one page where the reassurance does not hold.

- **Claim A:** Analytics are never switched off for going over; the customer chooses whether to upgrade or leave
  - Evidence: “We'll never turn your analytics off for occasional traffic spikes or if a payment fails the first time”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Failing to upgrade within seven days can lead to suspension, and continued suspension to deletion, with no refund
  - Evidence: “In the event you fail to upgrade your account within seven days of our request, we reserve the right to suspend your account and restrict your use of our Services anytime after the seventh day following our notice to you.”
  - Source: [https://usefathom.com/legal/terms](https://usefathom.com/legal/terms)
- *Why this is not just wording: "We'll never turn your analytics off" and "we reserve the right to suspend your account and restrict your use of our Services" describe opposite outcomes for the same customer in the same situation.*
- *What would make this a non-issue: The terms describe a right you may never exercise, and the FAQ describes what you actually do in practice. Most companies have this gap; it is more visible here because the FAQ makes such a specific promise. Softening "never" to "we won't" and mentioning the first-month trigger would close it.*

**2. "Full API access" is on the pricing page; the $19–$399 a month you may need to pay for it is not**  
`high impact` · `Missing information` · `high confidence`

Your pricing page lists "Full API access with 600 requests per hour included" as a plan feature, in a list whose other entries end with reassurances like "No extra fees". A separate page reveals that 600 requests an hour is Tier 1 of a six-tier paid ladder, and that going beyond it costs $19, $39, $79, $199 or $399 a month. The top tier is nearly nine times the price of the $45 plan it sits on top of. Anyone sizing a real integration — the person most likely to care about the API at all — will build their business case from the pricing page and find the ladder only after they hit a 429.

- **Claim A:** The plan includes full API access with 600 requests per hour
  - Evidence: “Full API access with 600 requests per hour included.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** API throughput above the included allowance is a paid upgrade costing up to $399 a month
  - Evidence: “Tier 6 | $399/mo | 16,000 | 25”
  - Source: [https://usefathom.com/api/v1/rate-limits](https://usefathom.com/api/v1/rate-limits)
- *Why this is not just wording: The pricing page names no price for API capacity at all, while the other page prices it in six steps up to $399 a month, so a reader of the pricing page cannot arrive at the real cost of the product they are buying.*
- *What would make this a non-issue: 600 requests an hour is generous for dashboard-style use, and most customers will never leave Tier 1. The issue is that the word "Full" is doing a lot of work in a list that otherwise advertises the absence of extra fees.*

**3. Event tracking is advertised with "no extra fees", but events are counted as pageviews, which is what your price is based on**  
`medium impact` · `Ambiguity` · `medium confidence`

Your feature list says conversions, revenue and custom events are tracked on every plan with no extra fees. An FAQ answer much further down the same page confirms that custom events and API requests are counted as if they were pageviews. Since the plan price is set entirely by monthly pageviews, heavy event tracking does raise the bill — it moves the customer into a higher band, and by the terms it can eventually force an upgrade. Both statements are true; read in sequence they land as a contradiction.

- **Claim A:** Event and ecommerce tracking is included on every plan with no extra fees
  - Evidence: “Track conversions, revenue, and custom events on every plan. No extra fees.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** Custom events and API requests consume the pageview allowance that sets the price
  - Evidence: “those requests will be counted as if they were pageviews”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- *Why this is not just wording: "No extra fees" and "counted as if they were pageviews" have different consequences for the invoice, because pageviews are the only thing your price depends on.*
- *What would make this a non-issue: "No extra fees" is fair if it means there is no separate line item for events, which is true. The two statements are roughly two thousand words apart on the page, so few readers will see both — which is also why it is worth a sentence next to the feature.*

**4. You state you have never given a discount, while your help centre carries an article called "Discount codes"**  
`low impact` · `Ambiguity` · `medium confidence`

Your pricing FAQ is emphatic: never any sales or discounts, not even Black Friday, because everyone pays exactly the same price. That claim is part of your positioning. Every documentation page we read carries a help-centre link titled "Discount codes". If discount codes exist for partners, non-profits or migrations, then "everyone pays the exact same price" needs a qualifier; if they do not, the article title is misleading.

- **Claim A:** There have never been and will never be discounts; everyone pays the same price
  - Evidence: “We've never done discounts, nor will we ever.”
  - Source: [https://usefathom.com/pricing](https://usefathom.com/pricing)
- **Claim B:** The help centre documents discount codes
  - Evidence: “Discount codes”
  - Source: [https://usefathom.com/docs/integrations](https://usefathom.com/docs/integrations)
- *Why this is not just wording: A help article dedicated to discount codes implies a mechanism for paying less than list price, which is what the pricing FAQ says does not exist.*
- *What would make this a non-issue: This is the weakest item here and we want to be straight about why: we only saw the article's title in a navigation sidebar, not its contents. The article may explain that Fathom does not issue discount codes, or cover codes from a bundle or acquisition. Thirty seconds of checking settles it.*

*Not checkable from these pages: Discovery did not reach the help articles behind the sidebar titles — "Exceeding your plan limits", "Billing FAQ", "How do free trials work?", "Discount codes" and "Upgrading or downgrading" — which are the pages most likely either to resolve or to worsen the findings above. Nothing we read says whether a credit card is required to begin the 7-day trial. The pricing page's slider shows one pageview band at a time, so we could only read the $45 / 500,000 band and not the prices of the other tiers.*

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
| https://dashboard.knock.app/signup | — | — | blocked by robots.txt |

</details>

**1. Your pricing page says workflow triggers are unlimited on every plan; your API reference rate limits every endpoint**  
`medium impact` · `Ambiguity` · `high confidence`

"Unlimited" appears against workflow triggers, notification workflows, channels and recipients for all three plans, including the free one. Triggering a workflow is an API call, and your API reference states plainly that every endpoint is rate limited, on a five-tier scale that starts at one request per second, and returns a 429 when exceeded. The two statements are compatible — a rate limit caps the rate, not the total — but the pricing page does not say so, and the rate-limit tiers are never mapped to plans or to specific endpoints, so a developer sizing a launch cannot work out what throughput they have actually bought.

- **Claim A:** Workflow triggers are unlimited on every plan, including the free one
  - Evidence: “Workflow triggers | Unlimited | Unlimited | Unlimited”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- **Claim B:** Every API endpoint is rate limited on a tier scale beginning at one request per second, returning 429 when exceeded
  - Evidence: “Each endpoint in the Knock API is rate limited. Knock uses a tier system to determine the rate limit scale for each endpoint.”
  - Source: [https://docs.knock.app/api-reference/overview/rate-limits](https://docs.knock.app/api-reference/overview/rate-limits)
- *Why this is not just wording: "Unlimited triggers" and "one to a thousand requests per second depending on an unpublished endpoint tier" answer the same buyer question — how much can I send — with different numbers.*
- *What would make this a non-issue: This is a clarity problem, not a broken promise: rate limits and volume allowances genuinely are different, and your docs invite customers to ask for a higher rate. Naming which tier the trigger endpoint sits in would resolve it in one line.*

**2. Enterprise customers get the same guides allowance as the $250 Starter plan, and only the FAQ says so**  
`medium impact` · `Missing information` · `high confidence`

In your comparison table the Enterprise column for guide active users says "Contact us", alongside a note about volume discounts. Every reasonable reading of that is "this number is negotiated, and it will be bigger than Starter's". An FAQ answer near the bottom of the same page says something different: unless guides were explicitly written into the enterprise agreement, an Enterprise customer gets 2,500 active users a month — exactly what Starter includes for $250. A customer paying well above Starter, who assumed guides scaled with their contract, finds out when you ask them to get in touch mid-quarter.

- **Claim A:** The Enterprise guides allowance is presented as something to negotiate, with volume discounts available
  - Evidence: “Contact us Volume-based discounts and monthly notified user pricing available.”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- **Claim B:** Enterprise defaults to the Starter allowance of 2,500 guide active users a month
  - Evidence: “you'll have the same guides limit as our Starter plan: 2,500 active users a month”
  - Source: [https://knock.app/pricing](https://knock.app/pricing)
- *Why this is not just wording: "Contact us" invites the reader to assume a negotiated, larger number, while the FAQ states a specific default equal to the tier below — that is a fact about the deal, not a phrasing choice.*
- *What would make this a non-issue: The FAQ is on the same page as the table, so a thorough reader will find it. It is 40 rows below, under a question addressed to existing Enterprise customers rather than to buyers, and the table itself gives no hint that a default exists.*

*Not checkable from these pages: We deliberately did not report the rate-limit tier table appearing on two documentation pages with different numbers in view — it is one table of endpoint scales reproduced on both pages, not two conflicting limits, and an automated reader could easily mistake it for a contradiction. We could not check which tier any given endpoint belongs to, since that mapping is not on the pages we read. Your pricing table promises unlimited feed retention while the API reference refers to data 'subject to deletion according to the data retention policy associated with your account'; the retention policy page was not reachable from our crawl, so we could not tell whether these describe the same data and did not report it. The signup page is blocked by robots.txt, so we could not check trial or card-requirement terms.*

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
| https://savvycal.com/faq | — | — | HTTP 404 |
| https://savvycal.com/help | — | — | HTTP 404 |
| https://savvycal.com/docs | — | — | HTTP 404 |

</details>

**1. Your pricing page invites people to "kick the tires for free", then shows only two paid plans and never explains what free means**  
`medium impact` · `Missing information` · `medium confidence`

The first line above your plans offers a free way in and tells the reader they can upgrade when they are ready to "activate". The plans underneath start at $10 per user per month, and nothing on the page says whether free means a free tier, a time-limited trial, or an unactivated account with reduced functionality. There is no trial length, no statement about whether a card is required, and no explanation of what activation changes. This is the first question a visitor has and the page raises it without answering it.

- **Claim A:** You can start for free and upgrade only when ready to activate
  - Evidence: “Kick the tires for free and only upgrade when you're ready to activate.”
  - Source: [https://savvycal.com/pricing](https://savvycal.com/pricing)
- **Claim B:** The only prices published are $10 and $17 per user per month, with no free option shown
  - Evidence: “$ 10 /user/mo”
  - Source: [https://savvycal.com/pricing](https://savvycal.com/pricing)
- *Why this is not just wording: One sentence offers a free route into the product and the rest of the page documents only paid ones, so the reader cannot find out what they would actually be signing up for.*
- *What would make this a non-issue: The answer is very likely in the FAQ at the bottom of the page, which is collapsed and did not render for us — so this may be a rendering limitation on our side rather than a gap on yours. The plan comparison table on the same page also rendered as feature names with no values, which is why this report is thinner for SavvyCal than for other companies.*

**2. Your terms reserve the right to change prices at any time, with no notice period, and your pricing page does not mention it**  
`low impact` · `Missing information` · `high confidence`

A single sentence in the Fees & Payment section lets you change prices at any time. Unlike most terms of this kind it commits to no notice period at all — not 30 days, not one billing cycle. Combined with automatic renewal, a customer's price can in principle change between one renewal and the next without warning. This is standard drafting and probably not how you behave, but it is the sort of clause a procurement reviewer flags, and nothing on the pricing page sets an expectation either way.

- **Claim A:** Prices may be changed at any time, with no notice period stated
  - Evidence: “We may change prices at any time.”
  - Source: [https://savvycal.com/terms](https://savvycal.com/terms)
- **Claim B:** Subscriptions renew automatically unless cancelled before the period ends
  - Evidence: “Subscriptions will automatically renew for the same subscription period unless you cancel the account by the end of the then-current subscription period.”
  - Source: [https://savvycal.com/terms](https://savvycal.com/terms)
- *Why this is not just wording: The two clauses combine into a commercial term — an automatically renewing subscription whose price can move without notice — that appears nowhere the buyer is asked to decide.*
- *What would make this a non-issue: This is ordinary legal boilerplate in the place boilerplate belongs, and your 30-day money back guarantee already gives customers a way out. We are flagging placement, not conduct.*

*Not checkable from these pages: This is the weakest coverage of the ten companies and we would rather say so than pad the report. The plan comparison table on your pricing page rendered as a list of feature names with no per-plan values, so we could not check a single feature entitlement against your documentation. The FAQ section rendered as a heading with no questions or answers. Your help site returned almost no readable text. As a result we could not check the two things most worth checking here: which features are Basic versus Premium, and what your free entry route actually is. Your 30-day money back guarantee and your refund clause do agree with each other, which is worth saying, because that is the pair that most often does not.*

### ScreenshotOne

https://screenshotone.com · media API · found via category sweep: screenshot APIs

Read **15** usable pages of 15 fetched, extracted **17** commercial promises, produced **3** findings. 27 quotes verified, 0 candidate finding(s) discarded.

**Plans found:** Free ($0 — 100 screenshots per month); Basic ($17 per month); Growth ($79 per month); Scale ($259 per month)

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
| https://dash.screenshotone.com/sign-up | — | — | blocked by robots.txt |
| https://screenshotone.com/faq | — | — | HTTP 404 |
| https://screenshotone.com/terms | — | — | HTTP 404 |

</details>

**1. Three of your pages give three different answers to what happens when a customer exceeds their plan**  
`high impact` · `Ambiguity` · `high confidence`

This is the question every API customer asks before they build on you, and your site answers it three ways. The pricing page presents it as a simple per-unit price — go over, pay $0.009 each. The credits documentation adds a condition the pricing page never mentions: overage is billed automatically only if extra charging is enabled, leaving the reader to guess what happens when it is not. The terms of service describe a third outcome, where exceeding plan limits may bring throttling or temporary suspension of access. A developer whose product depends on your API cannot tell whether hitting the limit costs them money, degrades their service, or stops it.

- **Claim A:** Going over the plan is simply billed at a per-screenshot rate
  - Evidence: “$0.009 per extra”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** Exceeding plan limits may instead result in throttling or temporary suspension of access
  - Evidence: “throttling, or temporary suspension of access”
  - Source: [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)
- *Why this is not just wording: Paying a few tenths of a cent more, having requests slowed, and losing access are three different outcomes for the same event, not three descriptions of one.*
- *What would make this a non-issue: The likely reality is that overage billing is the normal path and throttling is a reserve power for abuse. The docs page's "if extra charging is enabled" is the sentence that most needs finishing: it is the only hint that a customer might have the option switched off, and it never says what happens then.*

**2. Your terms let you change the usage limits and quotas themselves at any time, not just the price**  
`medium impact` · `Missing information` · `high confidence`

Most terms of service reserve the right to change prices. Yours goes further and reserves the right to modify usage limits, quotas and plan structures too. The screenshot allowances are the product — 2,000, 10,000 and 50,000 a month are the reason a customer picks one plan over another — so this clause says the thing being bought can be redefined mid-subscription. Nothing on the pricing page hints at it, and no notice period is given anywhere we could read.

- **Claim A:** Each plan is sold on a specific monthly screenshot allowance
  - Evidence: “50,000 screenshots”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** Pricing, features, usage limits, quotas and plan structures may all be changed at any time
  - Evidence: “We reserve the right to modify pricing, features, usage limits, quotas, or plan structures at any time.”
  - Source: [https://screenshotone.com/terms-of-service](https://screenshotone.com/terms-of-service)
- *Why this is not just wording: A right to change quotas is materially different from a right to change prices, because it can reduce what a customer receives without changing what they pay.*
- *What would make this a non-issue: This is a clause you probably have no intention of using against existing customers, and a notice commitment on the pricing page would neutralise it entirely.*

**3. Your pricing page offers a full refund within 30 days, no questions asked; your credits documentation says unused credits are never refunded**  
`medium impact` · `Likely contradiction` · `medium confidence`

"Email us within 30 days and we will refund you in full, no questions asked" is an unconditional promise, and it is one of the reasons someone signs up. Your credits page carries a heading that says the opposite for the most common case: no refunds for unused credits. A customer who buys a Scale plan, uses a fraction of the 50,000 screenshots and asks for their money back inside the first month has been told both that they get everything back and that unused credits simply expire.

- **Claim A:** A full refund is available for any reason within 30 days
  - Evidence: “email us at support@screenshotone.com within 30 days, and we will refund you in full, no questions asked”
  - Source: [https://screenshotone.com/pricing](https://screenshotone.com/pricing)
- **Claim B:** Unused credits are not refunded; they expire at the end of the cycle
  - Evidence: “No refunds for unused credits”
  - Source: [https://screenshotone.com/docs/credits](https://screenshotone.com/docs/credits)
- *Why this is not just wording: One page promises money back for any reason inside 30 days and the other rules out a refund in the situation where a customer would most often ask for one.*
- *What would make this a non-issue: These probably address different things — the 30-day guarantee refunds the subscription fee, while the credits page is explaining that credit balances have no cash value on cancellation. Read in that order they still conflict, and the credits page is the one a cancelling customer lands on.*

*Not checkable from these pages: This is the most complete set of pages of the ten companies: fifteen pages all readable, with a pricing page that publishes per-plan quotas, rate limits and overage rates inline, and a credits page that explains reset and rollover behaviour properly. What we could not check is what actually happens when extra charging is disabled and the quota runs out — no page we read says. We also could not confirm whether the free tier survives cancellation: the credits page says a cancelled customer is downgraded to the free plan "or if the free plan is not available, you will lose access", without saying when the free plan would not be available.*

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

*Not checkable from these pages: Nothing could be checked. All three pages we reached, including the pricing page, returned a page shell with no readable text at all: the site builds its content in the browser, and the headless-browser fallback could not run in the environment this experiment was executed in. This is a failure of our tool, not a finding about Umami, and it should be counted as a miss rather than as a clean result. Roughly one company in ten in this sample was invisible for this reason.*

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
| https://www.unkey.com/docs/llms.txt | — | — | skipped: content-type text/plain; charset=utf |
| https://www.unkey.com/faq | — | — | HTTP 404 |
| https://app.unkey.com/auth/sign-up | — | — | HTTP 429 |
| https://app.unkey.com/ | — | — | HTTP 429 |
| https://www.unkey.com/help | — | — | HTTP 404 |
| https://www.unkey.com/terms | — | — | HTTP 404 |

</details>

**1. Your free plan keeps logs longer than the $5 plan and audit logs longer than the $25 plan**  
`high impact` · `Likely contradiction` · `high confidence`

Your documentation says the free plan retains logs for 7 days and audit logs for 30 days. Your pricing page's comparison table gives Starter, at $5 a month, 3 days of log retention and 7 days of audit log retention — less than free on both counts. Pro, at $25 a month, gets 7 days and 14 days, so it too has less audit log retention than the free plan, and only matches free on ordinary logs. Only Business at $50 finally reaches the free plan's 30 days of audit retention. A customer who upgrades from free to Starter to get a production-grade service will find their observability window has shrunk, which is the opposite of what upgrading is supposed to do.

- **Claim A:** The free plan retains logs for 7 days and audit logs for 30 days
  - Evidence: “| Audit log retention | 30 days | Varies by plan |”
  - Source: [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)
- **Claim B:** The paid comparison table gives Starter 3 days of log retention and 7 days of audit log retention, rising to 14 and 30 only on Business
  - Evidence: “$5
1
3 days
7 days
Email”
  - Source: [https://www.unkey.com/pricing](https://www.unkey.com/pricing)
- *Why this is not just wording: These are the same two named metrics, measured in the same unit, and the free tier's numbers are larger than the paid tier's — one of the two pages must be wrong about what a paying customer receives.*
- *What would make this a non-issue: We read the paid figures from a comparison grid that is built from styled divs rather than a real table, so column alignment had to be inferred. We checked it against the plan cards and it holds — the same column that gives Starter 3 days also gives it 1 vCPU, 2 GB, 1 custom domain and $5 of usage credits, all of which match the Starter card exactly. Still worth thirty seconds with the live page before acting.*

**2. Your pricing page says "start for free" but never shows the free plan or what it includes**  
`medium impact` · `Missing information` · `high confidence`

"Start for free, scale as you go" is the first line of your pricing page and the closing call to action repeats it. The plans below begin at $5 a month, and no free tier appears anywhere on the page. The free plan does exist, and it is specified in your billing documentation with real numbers — 150,000 API requests a month, 7 days of log retention, no team members. A developer evaluating you is told twice that they can start for free and then shown nothing they can start with, which turns the most important question on the page into a support conversation.

- **Claim A:** The pricing page invites developers to start for free
  - Evidence: “Start for free, scale as you go with predictable usage-based pricing.”
  - Source: [https://www.unkey.com/pricing](https://www.unkey.com/pricing)
- **Claim B:** The free plan and its allowances exist, but are documented only in the billing docs
  - Evidence: “| API requests per month | 150,000 | Varies by plan |”
  - Source: [https://unkey.com/docs/platform/workspaces/billing](https://unkey.com/docs/platform/workspaces/billing)
- *Why this is not just wording: A whole plan with published quotas is absent from the page whose job is to list the plans, so the pricing page cannot answer what "free" means.*
- *What would make this a non-issue: The free tier may be in the process of being retired, or may be offered only at signup. Either way the pricing page still promises it twice.*

*Not checkable from these pages: The pricing page's FAQ rendered as a heading with no questions, so anything it says about the free plan, trials or overage was not visible to us. The pricing page states API request allowances nowhere at all — the docs give the free plan 150,000 a month and say paid plans vary, but no page we read says by how much, so we could not check request quotas against each other. The interactive cost calculator produced a single $188 estimate from its default inputs rather than a price list.*

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
