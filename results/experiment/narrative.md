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
