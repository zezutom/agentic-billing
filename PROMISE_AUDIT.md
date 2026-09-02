# Public Commercial-Consistency Auditor

> **Where does your SaaS contradict itself?**
> Give us your website and we'll find conflicting promises about what customers receive.

Point it at a SaaS company's homepage. It finds the pricing page, discovers the other
public pages that make commercial promises (plan comparisons, docs, help articles, FAQs,
usage-limit pages, trial and signup pages, add-ons, billing terms), extracts what each
page promises, compares them, and reports where the company's own pages disagree.

Everything it reports is backed by two verbatim quotes and two links. It reads public
pages only — no login, no billing system, no customer data.

---

## What it looks for

| Finding type | Meaning |
|---|---|
| **Likely contradiction** | Two public statements that cannot both be true. |
| **Ambiguity** | Both can be true, but a customer cannot tell what they get. |
| **Possibly out of date** | Content left over from earlier packaging. |
| **Missing information** | Something that changes the deal, published where the buyer won't look. |

The rules currently implemented:

| Rule | Fires when |
|---|---|
| `unlimited_vs_limit` | "Unlimited X" is advertised while a numeric ceiling on X is documented elsewhere. |
| `unlimited_vs_fair_use` | "Unlimited" is advertised while a fair-use restriction sits on another page. |
| `trial_length_conflict` | Two different trial lengths are published. |
| `trial_card_conflict` | One page says no credit card is needed, another says payment details are required. |
| `price_conflict` | The same plan is priced differently on two pages, same currency and period. |
| `annual_costs_more` | The annual per-month price is higher than the monthly price. |
| `annual_total_exceeds_monthly` | The yearly price exceeds twelve monthly payments. |
| `limit_conflict` | Two different allowances are published for the same metric. |
| `feature_plan_conflict` | Pricing assigns a feature to one plan, documentation to a higher one. |
| `plan_name_drift` | Help content still refers to a plan the pricing page no longer sells. |
| `condition_off_pricing` | Overage charges, seat minimums, fair use, no-refund or auto-renewal terms appear only away from the pricing page. |
| `vague_entitlement` | Features are gated to "paid plans" without naming which one. |
| `unpriced_plan` | Documentation refers to a plan that has no published price. |

Each rule degrades its own confidence when the evidence is thin — for example when only
one of the two statements names a plan — and says so in the report. Tier ordering is
understood, so "unlimited on Enterprise, 25 seats on Starter" is normal tiering, not a
contradiction.

---

## Install

Python 3.11+.

```bash
pip install requests beautifulsoup4 lxml          # required
pip install playwright && playwright install chromium   # optional, for JS-only pricing pages
```

Or from the repository:

```bash
pip install -e ".[audit]"          # add ",audit-js" for the headless-browser fallback
```

## Run a single company

```bash
PYTHONPATH=src python -m promise_audit.cli https://example.com --name "Example"
```

Writes three files to `results/`:

* `example.html` — the report to read or send (open it in a browser)
* `example.md` — the same report in Markdown
* `example.json` — every extracted claim and finding with its source URL

Useful options:

```
--max-pages N       how many public pages to read (default 16)
--add-url URL       include a page automatic discovery missed (repeatable)
--no-render         skip the headless-browser fallback
--no-cache          ignore the local page cache
--delay SECONDS     politeness delay per host (default 1.0)
--open              open the HTML report when finished
```

If discovery misses something, supply it directly:

```bash
PYTHONPATH=src python -m promise_audit.cli https://example.com \
  --add-url https://docs.example.com/limits \
  --add-url https://example.com/help/billing
```

## Run the batch experiment

```bash
PYTHONPATH=src python -m promise_audit.experiment.run_batch --out results/experiment
PYTHONPATH=src python -m promise_audit.experiment.report results/experiment
```

The first command pre-checks the frozen candidate pool, draws ten companies with a fixed
random seed, and audits all ten with identical settings. The second assembles
`results/experiment/EXPERIMENT_REPORT.md`.

`--skip-precheck` reuses an existing `eligibility.json`; `--precheck-only` stops after
the eligibility pass.

---

## Results from the ten-company experiment

* `results/experiment/EXPERIMENT_REPORT.md` — the full write-up: candidate pool, selection
  method and seed, pages read per company, claims extracted, every finding with its
  evidence and links, failures, and an honest assessment of false positives.
* `results/experiment/<company>.json` — structured claims and findings per company.
* `results/experiment/<company>.html` — the report a founder would receive.
* `RECOMMENDATION.md` — whether this is worth publishing (short answer: not yet, and why).

Headline: 119 public pages read across ten companies, 386 commercial claims extracted,
8 findings — two of which a founder would act on, five correct but unsurprising, one wrong.

## How it works

```
URL
 ├─ discover.py   robots.txt → sitemap → homepage nav → one hop from the pricing page
 │                and from the docs hub → score and cap ~16 pages across categories
 ├─ fetcher.py    polite cached HTTP; headless Chromium only when a page comes back
 │                as an empty client-rendered shell
 ├─ extract.py    pricing cards, comparison tables and prose → structured claims
 │                (plans, prices, billing periods, trials, limits, unlimited claims,
 │                entitlements, add-ons, conditions), each tied to a literal quote
 ├─ rules.py      pairwise comparison across pages → findings with severity,
 │                confidence, both claims, both sources and a caveat
 └─ report.py     HTML / Markdown / terminal
```

Politeness: robots.txt is honoured, one request per second per host by default, a 20
second timeout, and pages are cached on disk for seven days in `.promise_audit_cache/`.
Roughly 10–20 pages are read per company.

## Deliberate limits

* It reads public HTML. Promises inside images, videos, tooltips, PDFs or logged-in
  areas are invisible to it.
* **Client-side rendering is the biggest gap.** A pricing page that ships an empty shell and
  builds itself in the browser returns no readable text. The headless-Chromium fallback
  exists for exactly this and runs automatically when a page comes back thin — but in the
  sandbox the experiment ran in, the browser had no outbound network access, so one of the
  ten companies (Umami) could not be analysed at all. Use `--no-render` to skip the attempt
  where it cannot work; the run is much faster without it.
* Absence-based findings (`condition_off_pricing`) can be wrong if the pricing page
  states the condition in a collapsed accordion the parser did not expand.
* It does not know which of two conflicting statements is correct — only that they
  disagree.
* It cannot see your billing system, your entitlement service or your customer records.
  That is the point of the closing question, not an oversight.
