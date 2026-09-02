"""Command line entry point.

    promise-audit harvest https://example.com --name Example
    promise-audit analyse example            # after the agent writes the JSON
    promise-audit run https://example.com --backend api    # unattended, needs a key
"""

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

from .analyze import AnalysisPending, analyse, analysis_path, write_request
from .fetcher import Fetcher, registered_domain
from .harvest import Dossier, harvest
from .render import render_terminal, write_all


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:60] or "company"


def _dossier_path(workdir: Path, slug: str) -> Path:
    return workdir / f"{slug}.dossier.json"


def cmd_harvest(args) -> int:
    workdir = Path(args.work)
    workdir.mkdir(parents=True, exist_ok=True)
    cache_dir = args.cache_dir
    if getattr(args, "no_cache", False):
        cache_dir = tempfile.mkdtemp(prefix="promise-audit-")
        print(f"Cache bypassed. Fetching everything fresh into {cache_dir}")
    fetcher = Fetcher(cache_dir=cache_dir, delay=args.delay,
                      allow_render=not args.no_render)
    try:
        print(f"Harvesting {args.url} ...")
        dossier = harvest(args.url, company=args.name, max_pages=args.max_pages,
                          extra_urls=args.add_url, fetcher=fetcher)
    finally:
        fetcher.close()
    slug = args.slug or slugify(args.name or registered_domain(dossier.root_url))
    dossier.save(_dossier_path(workdir, slug))
    req = write_request(dossier, workdir, slug)
    print(f"\n{dossier.stats['pages_usable']} usable pages, "
          f"{dossier.stats['dossier_chars']:,} characters of dossier.")
    print(f"  dossier  {_dossier_path(workdir, slug)}")
    print(f"  request  {req}")
    print(f"\nNext: have the Claude session read {req} and write its JSON answer to")
    print(f"      {analysis_path(workdir, slug)}")
    print(f"Then:  promise-audit analyse {slug} --work {workdir}")
    return 0


def cmd_analyse(args) -> int:
    workdir = Path(args.work)
    slug = args.slug
    dpath = _dossier_path(workdir, slug)
    if not dpath.exists():
        print(f"No dossier at {dpath}. Run `promise-audit harvest <url> --slug {slug}` first.")
        return 1
    dossier = Dossier.load(dpath)
    try:
        analysis, report = analyse(dossier, backend=args.backend, workdir=workdir,
                                   slug=slug, model=args.model)
    except AnalysisPending as exc:
        print(exc)
        return 2
    paths = write_all(analysis, dossier, args.out, slug)
    print(render_terminal(analysis, dossier))
    if report.rejections:
        print("Discarded during verification:")
        for r in report.rejections:
            print(f"  - {r.where}: {r.reason}" + (f" ({r.detail[:70]})" if r.detail else ""))
        print()
    for k, p in paths.items():
        print(f"  {k:9} {p}")
    return 0


def cmd_run(args) -> int:
    """Harvest and analyse in one go. Only sensible with the API backend."""
    rc = cmd_harvest(args)
    if rc != 0:
        return rc
    args.slug = args.slug or slugify(args.name or registered_domain(
        args.url if "://" in args.url else "https://" + args.url))
    return cmd_analyse(args)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="promise-audit",
        description="Find where a SaaS company's public pages contradict each other "
                    "about what customers receive.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p, with_url: bool = True):
        if with_url:
            p.add_argument("url", help="the company's main website URL")
            p.add_argument("--name", help="company name for the report")
            p.add_argument("--max-pages", type=int, default=16)
            p.add_argument("--add-url", action="append", default=[], metavar="URL",
                           help="extra page to include if discovery misses it (repeatable)")
            p.add_argument("--no-render", action="store_true",
                           help="skip the headless-browser fallback for JS-only pages")
            p.add_argument("--cache-dir", default=".promise_audit_cache")
            p.add_argument("--no-cache", action="store_true",
                           help="refetch every page instead of reusing the disk cache")
            p.add_argument("--delay", type=float, default=1.0)
        p.add_argument("--work", default="work", help="where dossiers and requests live")
        p.add_argument("--slug", help="short id for this company (default: derived from name)")

    h = sub.add_parser("harvest", help="crawl the public pages and write the analysis request")
    common(h)
    h.set_defaults(func=cmd_harvest)

    a = sub.add_parser("analyse", help="verify and render an analysis")
    a.add_argument("slug")
    a.add_argument("--work", default="work")
    a.add_argument("--out", default="results")
    a.add_argument("--backend", choices=("agent", "api"), default="agent")
    a.add_argument("--model", default="claude-opus-5")
    a.set_defaults(func=cmd_analyse)

    r = sub.add_parser("run", help="harvest and analyse in one command (API backend)")
    common(r)
    r.add_argument("--out", default="results")
    r.add_argument("--backend", choices=("agent", "api"), default="api")
    r.add_argument("--model", default="claude-opus-5")
    r.set_defaults(func=cmd_run)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
