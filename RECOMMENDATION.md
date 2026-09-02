# Is this worth publishing?

**Yes — as a lead magnet, after one engineering fix and one independent review.**

That is a change of answer. An earlier version of this tool used a deterministic rule engine
instead of a model, ran against the same ten companies, and produced two findings a founder
would act on out of twelve. This version produces nine out of nineteen. The pipeline, the
crawler and the sample are the same; the analyst is not.

## What the experiment showed

Ten smaller SaaS companies, drawn at random from a frozen pool of 36 with a fixed seed. Nine
could be read. 111 pages fetched, 140 commercial promises extracted, **19 findings**, 208
quotes verified character-by-character against the pages they came from.

| | |
|---|---|
| Companies with at least one finding | **8 of 9 readable** |
| Findings we would defend to a founder without hedging | **9** |
| Findings that are real but modest (placement, boilerplate) | 7 |
| Findings an informed reader would push back on | 3 |
| Findings citing evidence that does not exist | **0** |
| Companies that could not be analysed at all | 1 (Umami — client-rendered pricing page) |

The best of them is worth quoting in full, because it is the argument for the whole idea:
**Unkey's documentation gives its free plan 7 days of log retention and 30 days of audit log
retention. Its pricing page gives the $5 Starter plan 3 days and 7 days.** Paying moves you
backwards on both. Nobody inside the company has read those two tables side by side, which is
precisely the job worth automating.

## Why this is a lead magnet and the earlier version was not

The earlier rule engine mostly found that auto-renewal clauses live in terms of service. True,
checkable, and not news to anyone. Nine of these nineteen are things the company does not
know, because seeing them requires holding two pages in mind at once and understanding what
each is promising — reading comprehension, not pattern matching.

Two examples of the difference. The rule engine reported Knock as having conflicting API rate
limits, 60/second on one page and 200/second on another; they are two rows of one endpoint
tier table reproduced on two pages, and it was a false positive. This version did not report
it, and said in its coverage notes why not. Conversely the rule engine found nothing at Unkey;
the retention inversion needs someone to align a flattened comparison grid against the plan
cards and notice that the cheaper tier wins.

## The one thing that must be fixed first

**JavaScript rendering.** Umami returned zero readable words from its pricing page and could
not be analysed at all. SavvyCal's comparison table rendered as feature names with no values,
so its report is visibly thinner. One company in ten currently invisible is survivable in an
experiment and not survivable in a public tool where the first thing a founder does is enter
their own URL. The fallback is written and Chromium launches; it simply had no outbound
network access in the sandbox this ran in.

Close behind it: parse comparison grids properly rather than flattening them. Every one of
these sites builds its plan table from styled divs. An early version of the harvester
de-duplicated repeated lines and silently destroyed those grids — the Unkey finding was
invisible until that was fixed, and there are almost certainly equivalent findings still
being missed elsewhere.

## The one review that must happen first

The analyst wrote the findings and then graded them, having already seen these ten companies
during the earlier rule-based run. Zero rejections out of 208 quotes is also not evidence that
the model does not fabricate: the analyst and the verifier were the same model in the same
session, checking quotes as it wrote them. The verifier itself was tested adversarially and
does reject fabricated quotes, paraphrases, split passages and schema violations — but it has
not yet been tested where it matters, on an unattended API run.

Before publishing any hit-rate claim: run the same ten dossiers through the API backend, report
the rejection rate, and have someone who did not write the findings mark them.

## What to publish

Publish both, in this order.

1. **The tool**, once rendering works. The offer costs a founder one URL. The report quotes
   their own words, links both pages, and states in one line what would make each finding
   wrong — checkable in two minutes, which is the only standard that matters for a cold audit
   of somebody else's website.
2. **The experiment write-up**, including the company that could not be read, the two false
   positives that were caught and suppressed, and the three findings we think are soft. The
   honesty is the differentiator. Every competitor in this space publishes only its best case.

Do not lead with "most SaaS companies contradict themselves". Lead with what the evidence
actually supports: *pricing pages and documentation drift apart, nobody inside the company can
see it, and it is visible from outside in about two minutes.* Then ask the question the tool
cannot answer:

> These are the promises your customers can see. Do your billing system and product deliver
> the same thing?

## Recommendation in one line

Fix rendering, get an independent mark, then publish — the finding quality is there, and the
verified-quote format is the part that would be hard for anyone else to copy well.
