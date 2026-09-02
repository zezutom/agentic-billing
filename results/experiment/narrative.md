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
