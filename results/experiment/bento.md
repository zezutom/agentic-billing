# Commercial consistency audit — Bento

**We found 2 commercial promises worth checking.**

Source: https://bentonow.com/ · 13 public pages read · 13 commercial promises extracted · 20 quotes verified against their source page · 2026-09-02 07:57:10 UTC

## What you appear to sell

- **Marketing Platform** — $29/mo up to 5,000 Active Users, then tiered from $0.01 per Active User
- **Transactional Email** — $0/mo — first 100 emails free, then $5/mo to 12,500 and $0.09 per 1,000 after
- **Bento Chat (add-on)** — +$30/mo, requires Marketing Platform

## 1. Your pricing page bills on active users; your FAQ says you bill on total subscribers

`high impact` · `Likely contradiction` · `high confidence`

The entire argument of your pricing page is that you charge for Active Users — people who are subscribed or who did something in the last 30 days — and that dormant contacts do not inflate the bill. Your documentation FAQ answers "How does pricing work?" with a flat statement that you charge on the number of subscribers, and then defines a subscriber as any unique email address in the account. For a list with a long tail of dormant addresses those two rules produce materially different invoices, and the difference is the single reason a prospect would choose you over the competitors your own comparison table names.

**What one page says:** Billing is based on Active Users — subscribed, or active in the last 30 days
> Subscribed users or people with an event in the last 30 days.
> — [https://bentonow.com/pricing](https://bentonow.com/pricing)

**What another page says:** Billing is based on the total number of subscribers, meaning every unique email address held
> Bento charges based on the number of subscribers you have.
> — [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)

*Why this is not just wording: "Active Users in the last 30 days" and "every unique email address in your account" are two different countable populations, so they are two different prices for the same list.*

*What would make this a non-issue: The FAQ answer is probably just older copy written before the Active Users model, and "subscriber" may be intended loosely. That is exactly the problem: it is the page a customer searches when they want to know what drives their bill.*

## 2. Your FAQ says every feature is included with no gating, while your pricing page sells chat as a $30/month add-on

`medium impact` · `Ambiguity` · `medium confidence`

"All features are included at every tier - no feature gating" is a strong promise, and it is the answer a prospect gets when they ask how pricing works. Your pricing page then sells Bento Chat — shared inbox, live chat, SMS, routing, AI agents — for an extra $30 a month, and requires the Marketing Platform underneath it. Someone who reads the FAQ first will budget $29 and be surprised at $59.

**What one page says:** No feature is gated; everything is included at every tier
> All features are included at every tier
> — [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)

**What another page says:** Chat, SMS and AI agents cost an additional $30/month on top of the Marketing Platform
> +$30/mo adds shared inbox, live chat, SMS, routing, saved replies, and AI agents. Requires Marketing Platform.
> — [https://bentonow.com/pricing](https://bentonow.com/pricing)

*Why this is not just wording: One page states that nothing is behind a paywall while the other puts a named set of features behind a separate monthly charge.*

*What would make this a non-issue: "Tier" almost certainly means volume tier — the features genuinely do not change as your list grows — and Chat is arguably a separate product rather than a gated feature. Adding four words to the FAQ answer would remove the ambiguity.*

## Pages we read

| Page | Type | Words | Status |
|---|---|---|---|
| [Bento Pricing - Email Marketing, Chat, and Transactional -](https://bentonow.com/pricing) | Pricing page | 814 | read |
| [Frequently Asked Questions - Bento Documentation](https://bentonow.com/docs/faq) | FAQ | 1201 | read |
| [Support - Bento Documentation](https://bentonow.com/docs/support) | Help centre | 347 | read |
| [Bento Documentation](https://bentonow.com/docs) | Product documentation | 176 | read |
| [Download Bento Apps - Mac, Windows, iOS, Android - Bento](https://bentonow.com/apps) | Add-ons & integrations | 237 | read |
| [Bento CLI - CLI for Email Marketing - Bento Documentation](https://bentonow.com/docs/integrations/cli) | Product documentation | 1677 | read |
| [Developer API Documentation - Bento Documentation](https://bentonow.com/docs/developer_guides/introduction) | Product documentation | 511 | read |
| [Bento MCP Server - AI-Powered Email Marketing - Bento Docu](https://bentonow.com/docs/integrations/mcp) | Add-ons & integrations | 2260 | read |
| [Email Marketing Glossary: 186 Terms & Definitions - Bento](https://bentonow.com/terms) | Terms / legal | 7456 | read |
| [Terms & Conditions - Bento](https://bentonow.com/legal/terms) | Terms / legal | 5035 | read |
| [Documentation & Help Center - Bento Email Marketing - Bent](https://bentonow.com/help) | Help centre | 2449 | read |
| [Bento Skills for AI Agents - Bento Documentation](https://bentonow.com/docs/integrations/skills) | Add-ons & integrations | 383 | read |
| [Acceptable Use Policy - Bento](https://bentonow.com/legal/acceptable-use-policy) | Terms / legal | 1281 | read |
| https://bentonow.com/pricing.md | — | — | skipped: content-type text/markdown; charset= |
| https://bentonow.com/faq | — | — | HTTP 404 |
| https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000 | — | — | blocked by robots.txt |
| https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0 | — | — | blocked by robots.txt |
| https://bentonow.com/docs/integrations/cli.md | — | — | skipped: content-type text/markdown; charset= |

## What we could not check

The FAQ's answer to "What's the API rate limit?" is collapsed and did not render, though a table of per-endpoint limits appears on the same page. Nothing we read states whether a credit card is required to start the 30-day trial, or what happens to a list that exceeds fair use on marketing sends — the term is used but never defined anywhere we could read.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit only reads what is published on your website. It cannot see what your billing system actually meters, what your product actually enforces, or what your customer records actually entitle people to. In most companies those three answers have drifted apart quietly, and the public pages are the only place the drift is visible from outside. If the contradictions above are news to you, the more expensive question is what else is out of step behind them.