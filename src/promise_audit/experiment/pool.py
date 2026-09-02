"""The candidate pool for the batch experiment.

How this pool was built
-----------------------
The pool was assembled by sweeping eleven SaaS categories (web analytics,
email/newsletter tooling, forms and scheduling, web-data and screenshot APIs,
no-code databases, subscription and lifecycle marketing, developer messaging
infrastructure, monitoring and status pages, data infrastructure, secrets and
API management, and internal tooling) and listing independent or bootstrapped
vendors known to publish a public pricing page. It is a knowledge-driven
sweep, not a scrape of a directory: that is a real limitation and is stated
plainly in the experiment report.

The controls that matter for the experiment are the ones applied afterwards:

* the pool is frozen in this file before any company is analysed;
* every candidate is put through the same automated eligibility pre-check
  (reachable homepage, discoverable pricing page, discoverable documentation
  or help content) BEFORE selection;
* the ten companies analysed are drawn by a seeded random sample from
  whichever candidates pass, so no company enters the run because of what it
  was found to contain.

`plausible.io` is deliberately absent. It was used as the development fixture
while the extraction rules were being written, so including it in the
experiment would report tuned-on results as if they were out-of-sample.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

RANDOM_SEED = 20260902
SAMPLE_SIZE = 10

# Widely known platforms are excluded by name: they have large content teams,
# heavily reviewed pricing pages, and are not the audience for this tool.
EXCLUDED_LARGE_PLATFORMS = [
    "stripe", "slack", "notion", "figma", "hubspot", "salesforce", "atlassian",
    "zapier", "airtable", "shopify", "intercom", "mailchimp", "twilio", "datadog",
    "vercel", "github", "gitlab", "zoom", "asana", "monday", "clickup", "calendly",
    "typeform", "webflow", "squarespace", "canva", "miro", "linear", "loom",
    "dropbox", "box", "zendesk", "freshworks", "surveymonkey", "docusign", "okta",
    "cloudflare", "digitalocean", "heroku", "sendgrid", "segment", "amplitude",
    "mixpanel", "hotjar", "semrush", "ahrefs", "activecampaign", "klaviyo",
]


@dataclass
class Candidate:
    name: str
    url: str
    category: str
    discovered_via: str
    why_qualifies: str

    def to_dict(self) -> dict:
        return asdict(self)


CANDIDATE_POOL: list[Candidate] = [
    # --- web analytics -----------------------------------------------------
    Candidate("Fathom Analytics", "https://usefathom.com", "web analytics",
              "category sweep: privacy-focused web analytics",
              "Independent, founder-led analytics vendor with a public per-plan pricing "
              "page and a public documentation site."),
    Candidate("Simple Analytics", "https://www.simpleanalytics.com", "web analytics",
              "category sweep: privacy-focused web analytics",
              "Small European analytics vendor publishing usage-based plans and public docs."),
    Candidate("Pirsch Analytics", "https://pirsch.io", "web analytics",
              "category sweep: privacy-focused web analytics",
              "Small independent analytics product with published pageview allowances and docs."),
    Candidate("Umami", "https://umami.is", "web analytics",
              "category sweep: open-source analytics with a hosted tier",
              "Open-source analytics with a commercial hosted plan and public documentation."),

    # --- email and newsletters --------------------------------------------
    Candidate("Buttondown", "https://buttondown.com", "email / newsletters",
              "category sweep: independent newsletter platforms",
              "Solo-founder newsletter tool with subscriber-tiered public pricing and docs."),
    Candidate("EmailOctopus", "https://emailoctopus.com", "email / newsletters",
              "category sweep: independent email marketing",
              "Small email marketing vendor with public contact-tiered pricing and a help centre."),
    Candidate("Loops", "https://loops.so", "email / newsletters",
              "category sweep: modern SaaS email tools",
              "Early-stage email platform with public per-contact pricing and public docs."),
    Candidate("Bento", "https://bentonow.com", "email / newsletters",
              "category sweep: modern SaaS email tools",
              "Small marketing-automation vendor with published plans and a help centre."),

    # --- forms and scheduling ---------------------------------------------
    Candidate("Tally", "https://tally.so", "forms",
              "category sweep: independent form builders",
              "Bootstrapped form builder with a public two-tier pricing page and a help centre."),
    Candidate("Fillout", "https://www.fillout.com", "forms",
              "category sweep: independent form builders",
              "Small form product with public plan tiers, response limits and documentation."),
    Candidate("Formspree", "https://formspree.io", "forms",
              "category sweep: form back-end APIs",
              "Long-running independent form back end with submission-limited plans and docs."),
    Candidate("SavvyCal", "https://savvycal.com", "scheduling",
              "category sweep: independent scheduling tools",
              "Bootstrapped scheduling product with public pricing and a help centre."),
    Candidate("Cal.com", "https://cal.com", "scheduling",
              "category sweep: open-source scheduling",
              "Open-source scheduling vendor with a public seat-based pricing page and docs."),

    # --- web data and media APIs ------------------------------------------
    Candidate("ScrapingBee", "https://www.scrapingbee.com", "web data API",
              "category sweep: web-scraping APIs",
              "Small API vendor with credit-based public pricing and full API documentation."),
    Candidate("Scrapfly", "https://scrapfly.io", "web data API",
              "category sweep: web-scraping APIs",
              "Independent scraping API with published credit allowances and detailed docs."),
    Candidate("ScreenshotOne", "https://screenshotone.com", "media API",
              "category sweep: screenshot APIs",
              "Solo-founder screenshot API with request-quota pricing and public documentation."),
    Candidate("Bannerbear", "https://www.bannerbear.com", "media API",
              "category sweep: image generation APIs",
              "Bootstrapped image-generation API with quota-based plans and public docs."),
    Candidate("Placid", "https://placid.app", "media API",
              "category sweep: image generation APIs",
              "Small creative-automation API with public usage tiers and documentation."),

    # --- no-code databases and internal tools ------------------------------
    Candidate("Baserow", "https://baserow.io", "no-code database",
              "category sweep: open-source Airtable alternatives",
              "Open-core database vendor with public per-seat pricing and extensive docs."),
    Candidate("NocoDB", "https://nocodb.com", "no-code database",
              "category sweep: open-source Airtable alternatives",
              "Open-source database platform with a public cloud pricing page and docs."),
    Candidate("Chartbrew", "https://chartbrew.com", "BI / dashboards",
              "category sweep: small open-source BI tools",
              "Small open-source dashboard product with a hosted paid tier and public docs."),

    # --- subscription and lifecycle ---------------------------------------
    Candidate("Outseta", "https://www.outseta.com", "subscription / CRM",
              "category sweep: all-in-one SaaS back-office tools",
              "Small vendor bundling billing, CRM and help desk, with public pricing and a KB."),
    Candidate("Userlist", "https://userlist.com", "lifecycle marketing",
              "category sweep: SaaS lifecycle messaging",
              "Bootstrapped lifecycle email tool with user-count pricing and a help centre."),
    Candidate("Encharge", "https://encharge.io", "lifecycle marketing",
              "category sweep: SaaS lifecycle messaging",
              "Small marketing-automation vendor with public tiered pricing and documentation."),

    # --- developer messaging infrastructure --------------------------------
    Candidate("Resend", "https://resend.com", "email API",
              "category sweep: developer email APIs",
              "Early-stage transactional email API with public volume pricing and docs."),
    Candidate("Knock", "https://knock.app", "notifications API",
              "category sweep: notification infrastructure",
              "Small notifications-infrastructure vendor with public MAU pricing and docs."),
    Candidate("Svix", "https://www.svix.com", "webhooks API",
              "category sweep: webhook infrastructure",
              "Small webhooks-as-a-service vendor with public message-volume pricing and docs."),
    Candidate("Hookdeck", "https://hookdeck.com", "webhooks API",
              "category sweep: webhook infrastructure",
              "Independent event-gateway vendor with public request-volume pricing and docs."),

    # --- monitoring and status --------------------------------------------
    Candidate("Cronitor", "https://cronitor.io", "monitoring",
              "category sweep: independent uptime and cron monitoring",
              "Small monitoring vendor with public per-monitor pricing and documentation."),
    Candidate("Checkly", "https://www.checklyhq.com", "monitoring",
              "category sweep: synthetic monitoring",
              "Mid-size independent monitoring vendor with usage-based pricing and full docs."),
    Candidate("Instatus", "https://instatus.com", "status pages",
              "category sweep: status page vendors",
              "Small status-page vendor with public tiered pricing and a help centre."),

    # --- data infrastructure, secrets and API management -------------------
    Candidate("Tinybird", "https://www.tinybird.co", "data infrastructure",
              "category sweep: real-time analytics back ends",
              "Independent real-time data platform with public usage pricing and docs."),
    Candidate("Turso", "https://turso.tech", "data infrastructure",
              "category sweep: hosted database startups",
              "Early-stage hosted database with public row/storage allowances and docs."),
    Candidate("Doppler", "https://www.doppler.com", "secrets management",
              "category sweep: developer secrets management",
              "Small secrets-management vendor with public per-seat pricing and documentation."),
    Candidate("Infisical", "https://infisical.com", "secrets management",
              "category sweep: open-source secrets management",
              "Open-source secrets platform with a public cloud pricing page and docs."),
    Candidate("Unkey", "https://www.unkey.com", "API management",
              "category sweep: API key management",
              "Early-stage API management vendor with public request-volume pricing and docs."),
]


def pool_as_dicts() -> list[dict]:
    return [c.to_dict() for c in CANDIDATE_POOL]
