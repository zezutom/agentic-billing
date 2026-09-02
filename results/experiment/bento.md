# Bento: commercial consistency audit

**We found 2 commercial promises worth checking.**

https://bentonow.com/ | 13 pages read | 13 promises extracted | 20 quotes verified | 2026-09-02 07:57:10 UTC

## What you appear to sell

- **Marketing Platform**: $29/mo up to 5,000 Active Users, then tiered from $0.01 per Active User
- **Transactional Email**: $0/mo, first 100 emails free, then $5/mo to 12,500 and $0.09 per 1,000 after
- **Bento Chat (add-on)**: +$30/mo, requires Marketing Platform

## 1. Pricing page bills on active users. FAQ says total subscribers.

`high` `Likely contradiction` `high confidence`

On a list with a long dormant tail those two rules produce different invoices. It is also the reason a prospect picks you over the competitors in your own table.

**What one page says:** Active users, last 30 days
> Subscribed users or people with an event in the last 30 days.
> [https://bentonow.com/pricing](https://bentonow.com/pricing)

**What another page says:** Every unique email address
> Bento charges based on the number of subscribers you have.
> [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)

*Why this is not just wording: Active users in the last 30 days and every email address on file are different countable populations.*

*What would make this a non-issue: The FAQ is probably older copy from before the Active Users model. It is still the page customers search when they want to know what drives their bill.*

## 2. FAQ says nothing is gated. Pricing page sells chat at $30 a month.

`medium` `Ambiguity` `medium confidence`

Someone who reads the FAQ first budgets $29 and is surprised at $59.

**What one page says:** No feature gating at any tier
> All features are included at every tier
> [https://bentonow.com/docs/faq](https://bentonow.com/docs/faq)

**What another page says:** Chat costs $30 a month extra
> +$30/mo adds shared inbox, live chat, SMS, routing, saved replies, and AI agents. Requires Marketing Platform.
> [https://bentonow.com/pricing](https://bentonow.com/pricing)

*Why this is not just wording: One page says nothing is behind a paywall, the other puts a named feature set behind a separate charge.*

*What would make this a non-issue: Tier almost certainly means volume tier, and Chat is arguably a separate product. Four words in the FAQ would settle it.*

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
| https://bentonow.com/pricing.md | | | skipped: content-type text/markdown; charset= |
| https://bentonow.com/faq | | | HTTP 404 |
| https://app.bentonow.com/pricing?source=pricing&plan=starter&users=5000 | | | blocked by robots.txt |
| https://app.bentonow.com/pricing?source=pricing&package=transactional-email&emails=0 | | | blocked by robots.txt |
| https://bentonow.com/docs/integrations/cli.md | | | skipped: content-type text/markdown; charset= |

## What we could not check

The FAQ answer to "What's the API rate limit?" is collapsed and did not render, though a table of per-endpoint limits sits on the same page. Nothing we read says whether a card is required to start the 30-day trial, or what happens to a list that exceeds fair use on marketing sends. The term is used but never defined anywhere we could reach.

---

**These are the promises your customers can see. Do your billing system and product deliver the same thing?**

This audit reads your public pages only. It cannot see what your billing system meters, what your product enforces, or what your customer records entitle people to. If the findings above are news to you, the question worth asking is what else is out of step behind them.