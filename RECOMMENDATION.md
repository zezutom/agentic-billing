# Is this worth publishing?

**Short answer: not as it stands. Publish the idea, not this version of the tool — and only
after two specific fixes.**

## What the experiment actually showed

Ten smaller SaaS companies, chosen at random from a frozen pool of 36 with a fixed seed.
119 public pages read, 386 commercial claims extracted, **8 findings**.

| | |
|---|---|
| Findings a founder would act on | **2** (Cronitor, Knock) |
| Findings that are correct but not news | 5 |
| Findings that are wrong | 1 |
| Companies producing something worth a second look | 5 of 10 |
| Companies producing a *strong* finding | 2 of 10 |
| Companies that could not be analysed at all | 1 (Umami — client-rendered pricing page) |

The two strong ones are genuinely good. Knock publishes 60 requests/second on one
documentation page and 200 requests/second on another. Cronitor sells "Unlimited API
requests" and documents rate limits "to ensure fair usage". Neither is visible without
reading two pages side by side, which is exactly the job a machine should do.

## Why that is not yet a lead magnet

The hook promises contradictions. The data delivers **disclosure drift** — five of the eight
findings are ordinary terms-of-service clauses (auto-renewal, no refunds, the right to change
quotas) that simply are not repeated on the pricing page. True, checkable, and not
surprising to the person receiving the report.

None of the headline categories the concept was built around — a feature assigned to
different plans on different pages, mismatched trial lengths, prices that do not reconcile,
old plan names still live in the help centre — occurred once in ten companies. The rules for
all of them work; they fire correctly on the test fixture. Small, tidy, founder-led SaaS
companies were simply more consistent than the premise assumed.

A prospect whose report says "your terms mention auto-renewal and your pricing page doesn't"
does not book a call. Publishing at this hit rate risks the tool being remembered as the one
that found nothing.

## The two fixes that would change the answer

1. **Make JavaScript rendering work end to end.** One company in ten was invisible and
   another was analysed at a quarter depth, and those are precisely the modern, JS-heavy
   pricing pages most likely to have drifted. The fallback is implemented and Chromium
   launches; it simply had no outbound network access in the environment this ran in.
2. **Point it at the right companies.** The pool was deliberately small and independent.
   The audience with the actual problem is mid-market: six tiers, add-ons, grandfathered
   plans, a help centre nobody has audited since the last repackaging. Run the same
   experiment against twenty of those before deciding anything. If the hit rate there is
   still 2 in 10, the premise is wrong. If it is 6 in 10, this is a very good lead magnet.

Also worth doing before publishing: split the output into "contradictions" and "conditions
your buyer never sees" so five terms-of-service notes cannot read as five contradictions,
and fix the confidence calibration — the single best finding in the run is currently
labelled *low confidence* because neither statement happens to name a plan.

## What is worth publishing today

Not the tool. **The finding.**

"We read 119 public pages across ten SaaS companies looking for contradictions in what they
promise customers. We found two real ones — and something more common: the conditions that
change what you actually pay are almost never on the page where you decide to pay." That is
a short, honest, checkable post, every claim of which links to a public page. It earns
attention without over-claiming, and it sets up the real question the tool cannot answer:

> These are the promises your customers can see. Do your billing system and product deliver
> the same thing?

## Recommendation

* **Do not publish the tool as a public lead magnet yet.** The median result is too thin.
* **Do fix rendering and re-run against 20 mid-market companies.** That is roughly a day of
  work and it decides the question.
* **Do publish the experiment write-up**, including the false positive and the company that
  could not be read. The honesty is the differentiator; every competitor in this space
  publishes only its best case.
* **Keep the two-quote, two-link evidence format whatever happens.** It is the reason the
  findings survive being checked, and it is the only part of this that would be hard for
  someone else to copy well.
