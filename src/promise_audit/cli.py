"""Command line entry point."""

from __future__ import annotations

import argparse
import re
import sys
import webbrowser
from pathlib import Path

from .audit import audit_site
from .fetcher import Fetcher, registered_domain
from .report import render_terminal, write_all


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="promise-audit",
        description="Find where a SaaS company's public pages contradict each other "
                    "about what customers receive.")
    ap.add_argument("url", help="the company's main website URL")
    ap.add_argument("--name", help="company name for the report (default: the domain)")
    ap.add_argument("--max-pages", type=int, default=16,
                    help="how many public pages to read (default 16)")
    ap.add_argument("--add-url", action="append", default=[], metavar="URL",
                    help="extra page to include if automatic discovery misses it (repeatable)")
    ap.add_argument("--out", default="results", help="output directory (default: results/)")
    ap.add_argument("--no-render", action="store_true",
                    help="skip the headless-browser fallback for JavaScript-only pages")
    ap.add_argument("--no-cache", action="store_true", help="ignore the local page cache")
    ap.add_argument("--cache-dir", default=".promise_audit_cache")
    ap.add_argument("--delay", type=float, default=1.0,
                    help="seconds between requests to the same host (default 1.0)")
    ap.add_argument("--max-findings", type=int, default=12)
    ap.add_argument("--open", action="store_true", help="open the HTML report when done")
    args = ap.parse_args(argv)

    cache_dir = args.cache_dir
    if args.no_cache:
        import tempfile
        cache_dir = tempfile.mkdtemp(prefix="promise-audit-")

    fetcher = Fetcher(cache_dir=cache_dir, delay=args.delay,
                      allow_render=not args.no_render)
    print(f"Auditing {args.url} ...")
    try:
        result = audit_site(args.url, company=args.name, max_pages=args.max_pages,
                            extra_urls=args.add_url, fetcher=fetcher,
                            max_findings=args.max_findings)
    finally:
        fetcher.close()

    slug = slugify(args.name or registered_domain(result.root_url))
    paths = write_all(result, args.out, slug)
    print(render_terminal(result))
    for k, p in paths.items():
        print(f"  {k:9} {p}")
    if args.open:
        webbrowser.open(paths["html"].resolve().as_uri())
    return 0


if __name__ == "__main__":
    sys.exit(main())
