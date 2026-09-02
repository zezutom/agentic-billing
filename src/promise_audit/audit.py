"""Orchestration: URL in, structured audit out."""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .claims import Claim
from .discover import DiscoveryResult, discover
from .extract import extract_claims, parse_page
from .fetcher import Fetcher, canonical_url, registered_domain
from .rules import Finding, run_rules


@dataclass
class PageRecord:
    url: str
    final_url: str
    title: str
    category: str
    why_selected: str
    discovered_via: str
    status: int | None
    ok: bool
    error: str
    rendered: bool
    word_count: int
    claim_count: int


@dataclass
class AuditResult:
    company: str
    root_url: str
    domain: str
    started_at: str
    duration_seconds: float
    pages: list[PageRecord] = field(default_factory=list)
    failures: list[dict] = field(default_factory=list)
    claims: list[dict] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)
    discovery_notes: list[str] = field(default_factory=list)
    pricing_urls: list[str] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def save(self, path: str | Path) -> Path:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))
        return path


def audit_site(
    root_url: str,
    company: str | None = None,
    max_pages: int = 16,
    extra_urls: list[str] | None = None,
    fetcher: Fetcher | None = None,
    max_findings: int = 12,
    verbose: bool = True,
) -> AuditResult:
    started = time.time()
    own_fetcher = fetcher is None
    fetcher = fetcher or Fetcher()
    root = canonical_url(root_url if "://" in root_url else "https://" + root_url)
    domain = registered_domain(root)
    result = AuditResult(
        company=company or domain, root_url=root, domain=domain,
        started_at=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime(started)),
        duration_seconds=0.0,
    )

    try:
        disc: DiscoveryResult = discover(fetcher, root, max_pages=max_pages, extra_urls=extra_urls)
        result.discovery_notes = disc.notes
        result.pricing_urls = disc.pricing_urls

        all_claims: list[Claim] = []
        queue = list(disc.selected)
        reserve = list(disc.backup)
        seen_urls: set[str] = set()
        while queue:
            cand = queue.pop(0)
            if cand.url in seen_urls:
                continue
            seen_urls.add(cand.url)
            res = fetcher.get(cand.url)
            if not res.ok:
                result.failures.append({
                    "url": cand.url, "category": cand.category,
                    "reason": res.error or f"HTTP {res.status}",
                })
                # Replace a dead page so the audit still reads its full budget.
                while reserve and len(seen_urls) + len(queue) < max_pages + len(result.failures):
                    nxt = reserve.pop(0)
                    if nxt.url not in seen_urls:
                        queue.append(nxt)
                        break
                result.pages.append(PageRecord(
                    url=cand.url, final_url=res.final_url, title="", category=cand.category,
                    why_selected=cand.reason, discovered_via=cand.source, status=res.status,
                    ok=False, error=res.error, rendered=res.rendered, word_count=0, claim_count=0))
                continue
            doc = parse_page(res.html, cand.url, cand.category, rendered=res.rendered)
            claims = extract_claims(doc)
            claims = [c for c in claims if c.kind != "extraction_error"]
            all_claims.extend(claims)
            result.pages.append(PageRecord(
                url=cand.url, final_url=res.final_url, title=doc.title, category=cand.category,
                why_selected=cand.reason, discovered_via=cand.source, status=res.status,
                ok=True, error="", rendered=res.rendered, word_count=doc.word_count,
                claim_count=len(claims)))
            if verbose:
                print(f"  [{cand.category:12}] {len(claims):3} claims  {cand.url}")

        result.claims = [c.to_dict() for c in all_claims]
        findings: list[Finding] = run_rules(all_claims, max_findings=max_findings)
        result.findings = [f.to_dict() for f in findings]
        result.stats = {
            "pages_selected": len(disc.selected),
            "pages_fetched_ok": sum(1 for p in result.pages if p.ok),
            "pages_failed": len(result.failures),
            "pages_js_rendered": sum(1 for p in result.pages if p.rendered),
            "urls_considered": disc.considered,
            "claims": len(all_claims),
            "claims_by_kind": _count(all_claims, lambda c: c.kind),
            "findings": len(findings),
            "findings_by_severity": _count(findings, lambda f: f.severity),
            "findings_by_confidence": _count(findings, lambda f: f.confidence),
            "findings_by_kind": _count(findings, lambda f: f.kind),
            "fetcher": dict(fetcher.stats),
        }
    finally:
        result.duration_seconds = round(time.time() - started, 1)
        if own_fetcher:
            fetcher.close()
    return result


def _count(items, key) -> dict[str, int]:
    out: dict[str, int] = {}
    for i in items:
        k = key(i)
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items(), key=lambda kv: -kv[1]))
