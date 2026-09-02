# Public Commercial-Consistency Auditor

> **Where does your SaaS contradict itself?**
> Give us your website and we'll find conflicting promises about what customers receive.

Point it at a SaaS company's homepage. It finds the pricing page, discovers the other public
pages that make commercial promises — plan comparisons, product docs, help articles, FAQs,
usage-limit pages, trial and signup pages, add-ons, billing terms — and reports where the
company's own pages disagree about what a customer gets.

Every finding comes with two verbatim quotes and two links, and **every quote is checked
against the page it came from before you see it.**

---

## Architecture

```
URL
 │
 ├─ 1. harvest    deterministic. robots.txt → sitemap → homepage nav → one hop from the
 │                pricing page and the docs hub. ~16 pages, scored and capped across
 │                categories, rendered as readable Markdown-ish text with the size budget
 │                spent on the sections that talk about money.        → dossier.json
 │
 ├─ 2. analyse    an LLM reads the dossier and returns structured JSON: the plans, the
 │                individual promises, and the findings.              → analysis.json
 │
 ├─ 3. verify     deterministic. every quote is located character-by-character in the
 │                harvested text of the page it is attributed to. Unverifiable findings
 │                are discarded and counted.                          → verified analysis
 │
 └─ 4. render     HTML, Markdown and terminal output.                 → results/
```

**The model is the analyst; the verifier is why trusting it is reasonable.** The prompt
(`prompts.py`) does the judgement — telling apart real tiering from a contradiction, an API
pagination default from a plan allowance, standard legal boilerplate from a buried
condition. The verifier (`verify.py`) makes sure it cannot get away with inventing evidence.

A finding is discarded if:

* either quote cannot be found on any harvested page (fabricated or paraphrased);
* both sides cite the same quote, or the same page;
* the analyst could not say why the difference is more than wording;
* the type, severity or confidence is not one of the allowed values.

A quote that is real but attributed to the wrong page is **corrected**, not discarded, and
the correction is counted separately — that is a citation slip, not a fabrication.

## Two ways to run the analysis

| Backend | Analyst | When |
|---|---|---|
| `agent` (default) | the Claude session you are already in | Interactive. No API key, no spend beyond the subscription running the session. |
| `api` | the Claude API | Unattended and batch. Needs `ANTHROPIC_API_KEY`. |

Both use the same system prompt, the same task and the same schema from `prompts.py`, so
the two are comparable. The experiment in this repository was run on the `agent` backend.

---

## Install

Python 3.11+.

```bash
pip install requests beautifulsoup4 lxml          # required
pip install playwright && playwright install chromium   # optional, for JS-only pricing pages
```

Or from the repository: `pip install -e ".[audit]"` (add `,audit-js` for the browser fallback).

## Run one company — agent backend

```bash
# 1. crawl and build the dossier
PYTHONPATH=src python -m promise_audit.cli harvest https://example.com --name "Example"

# 2. the session reads work/example.request.md and writes work/example.analysis.json

# 3. verify the quotes and render the report
PYTHONPATH=src python -m promise_audit.cli analyse example
```

Step 1 prints the exact paths. Step 3 writes `results/example.{html,md,json}` plus the
dossier it was judged against, and tells you how many quotes were checked and how many
candidate findings were thrown away.

## Run one company — API backend

```bash
export ANTHROPIC_API_KEY=...
PYTHONPATH=src python -m promise_audit.cli run https://example.com --name "Example"
```

## Options

```
--max-pages N       how many public pages to read (default 16)
--add-url URL       include a page automatic discovery missed (repeatable)
--no-render         skip the headless-browser fallback for JS-only pages
--delay SECONDS     politeness delay per host (default 1.0)
--cache-dir DIR     on-disk page cache (default .promise_audit_cache, 7-day TTL)
--model NAME        model for the API backend (default claude-opus-5)
```

If discovery misses something, supply it directly:

```bash
PYTHONPATH=src python -m promise_audit.cli harvest https://example.com \
  --add-url https://docs.example.com/limits \
  --add-url https://example.com/help/billing
```

## Run the batch experiment

```bash
PYTHONPATH=src python -m promise_audit.experiment.run_batch harvest --out results/experiment
#   ... the session answers each work/<slug>.request.md ...
PYTHONPATH=src python -m promise_audit.experiment.run_batch finish --out results/experiment
PYTHONPATH=src python -m promise_audit.experiment.report results/experiment
```

With an API key the middle step is automatic: `finish --backend api`.

---

## Politeness and scope

robots.txt is honoured, one request per second per host by default, 20-second timeout,
pages cached on disk for seven days. Roughly 10–20 pages per company. Public information
only: no authentication, no billing systems, no customer records.

## Deliberate limits

* It reads public HTML. Promises inside images, videos, tooltips, PDFs or logged-in areas
  are invisible to it.
* **Client-side rendering is the biggest gap.** A pricing page that ships an empty shell
  returns no readable text; the dossier marks such pages unusable and tells the analyst so,
  and the report shows them. The headless-Chromium fallback exists for exactly this and runs
  automatically when a page comes back thin.
* It does not know which of two conflicting statements is correct — only that they disagree.
* It cannot see your billing system, entitlement service or customer records. That is the
  point of the closing question, not an oversight.
