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
