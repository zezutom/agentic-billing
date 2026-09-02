# Is this worth publishing?

**Yes, as a lead magnet, after one engineering fix and one independent review.**

That is a change of answer. An earlier version used a deterministic rule engine instead of a
model, ran against the same ten companies, and produced two findings a founder would act on
out of twelve. This version produces nine out of nineteen. Same pipeline, same crawler, same
sample. Different analyst.

## The numbers

Ten smaller SaaS companies, drawn at random from a frozen pool of 36 with a fixed seed. Nine
could be read. 111 pages fetched, 140 commercial promises extracted, 19 findings, 208 quotes
verified character-by-character against their source pages.

| Measure | Value |
|---|---|
| Companies with at least one finding | 8 of 9 readable |
| Findings we would defend without hedging | 9 |
| Findings that are real but modest | 7 |
| Findings an informed reader would push back on | 3 |
| Findings citing evidence that does not exist | 0 |
| Companies that could not be analysed at all | 1 (Umami, client-rendered pricing page) |

The best one is the argument for the whole idea. **Unkey's documentation gives its free plan
7 days of log retention and 30 days of audit log retention. Its pricing page gives the $5
Starter plan 3 days and 7 days.** Paying moves you backwards on both. Nobody inside the
company has read those two tables side by side.

## Why this version works and the last one did not

The rule engine mostly found that auto-renewal clauses live in terms of service. True,
checkable, not news. Nine of these nineteen are things the company does not know, because
seeing them means holding two pages in mind at once and understanding what each promises.

Two examples. The rule engine reported Knock as having conflicting API rate limits, 60 per
second on one page and 200 on another. They are two rows of one endpoint tier table
reproduced on two pages. A false positive. This version did not report it and said why in its
coverage notes. Conversely the rule engine found nothing at Unkey. The retention inversion
needs someone to align a flattened comparison grid against the plan cards and notice that the
cheaper tier wins.

## Fix first: JavaScript rendering

Umami returned zero readable words from its pricing page and could not be analysed. SavvyCal's
comparison table rendered as feature names with no values. One company in ten invisible is
survivable in an experiment and not in a public tool where the first thing a founder does is
enter their own URL. The fallback is written and Chromium launches. It had no outbound network
access in the sandbox this ran in.

Close behind: parse comparison grids instead of flattening them. Every one of these sites
builds its plan table from styled divs. An early version of the harvester de-duplicated
repeated lines and silently destroyed those grids. The Unkey finding was invisible until that
was fixed, and there are almost certainly equivalent findings still being missed.

## Review first: someone who did not write the findings

The analyst wrote the findings and then graded them, having already seen these ten companies
during the earlier rule-based run. Zero rejections out of 208 quotes is also not evidence that
the model does not fabricate. The analyst and the verifier were the same model in the same
session, checking quotes as it wrote them. The verifier was tested adversarially and does
reject fabricated quotes, paraphrases, split passages and schema violations, but it has not
been tested on an unattended run.

Before publishing any hit-rate claim: run the same ten dossiers through the API backend, report
the rejection rate, and have someone independent mark the findings.

## What to publish

Both, in this order.

1. **The tool**, once rendering works. The offer costs a founder one URL. The report quotes
   their own words, links both pages, and states in one line what would make each finding
   wrong. Checkable in two minutes, which is the only standard that matters for a cold audit
   of someone else's website.
2. **The experiment write-up**, including the company that could not be read, the two false
   positives that were caught and suppressed, and the three findings we think are soft. Every
   competitor in this space publishes only its best case.

Do not lead with "most SaaS companies contradict themselves". Lead with what the evidence
supports: pricing pages and documentation drift apart, nobody inside the company can see it,
and it is visible from outside in about two minutes. Then ask the question the tool cannot
answer:

> These are the promises your customers can see. Do your billing system and product deliver
> the same thing?

## In one line

Fix rendering, get an independent mark, then publish. The finding quality is there, and the
verified-quote format is the part that would be hard for anyone else to copy well.
