"""Polite, cached HTTP fetching with an optional JavaScript-rendering fallback."""

from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.robotparser as robotparser
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse

import requests

USER_AGENT = (
    "PromiseAuditBot/0.1 (+public commercial-consistency audit; "
    "contact: via the site owner running this tool)"
)
DEFAULT_TIMEOUT = 20
DEFAULT_DELAY = 1.0  # seconds between requests to the same host
CACHE_TTL_SECONDS = 7 * 24 * 3600

# Pages that are large but never carry commercial promises.
BINARY_SUFFIXES = (
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".ico", ".zip",
    ".mp4", ".mp3", ".woff", ".woff2", ".ttf", ".css", ".js", ".xml", ".json",
)


def canonical_url(url: str) -> str:
    """Strip fragments, tracking params and trailing slashes so we fetch once."""
    p = urlparse(url)
    scheme = p.scheme or "https"
    netloc = p.netloc.lower()
    if netloc.startswith("www."):
        netloc_key = netloc
    else:
        netloc_key = netloc
    path = p.path or "/"
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    query = ""
    if p.query:
        keep = [
            kv for kv in p.query.split("&")
            if kv and not kv.split("=")[0].lower().startswith(("utm_", "ref", "fbclid", "gclid"))
        ]
        query = "&".join(keep)
    return urlunparse((scheme, netloc_key, path, "", query, ""))


def registered_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    parts = host.split(".")
    if len(parts) <= 2:
        return host
    # Handle the common two-part public suffixes we are likely to meet.
    two_part = {"co.uk", "com.au", "co.nz", "co.jp", "com.br", "co.in"}
    if ".".join(parts[-2:]) in two_part:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:])


@dataclass
class FetchResult:
    url: str
    final_url: str
    status: int | None
    html: str
    ok: bool
    error: str = ""
    rendered: bool = False
    from_cache: bool = False
    fetched_at: float = field(default_factory=time.time)


class Fetcher:
    """Fetches pages, respecting robots.txt, with a local on-disk cache."""

    def __init__(
        self,
        cache_dir: str | Path = ".promise_audit_cache",
        delay: float = DEFAULT_DELAY,
        timeout: int = DEFAULT_TIMEOUT,
        respect_robots: bool = True,
        allow_render: bool = True,
        max_bytes: int = 3_000_000,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.timeout = timeout
        self.respect_robots = respect_robots
        self.allow_render = allow_render
        self.max_bytes = max_bytes
        self._last_request: dict[str, float] = {}
        self._robots: dict[str, robotparser.RobotFileParser | None] = {}
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        })
        self._browser = None
        self._playwright = None
        self.render_error = ""
        self._render_failures = 0
        self.max_render_failures = 2
        self.stats = {"network": 0, "cache": 0, "rendered": 0, "blocked": 0, "failed": 0}

    # ---------------- robots ----------------

    def _robots_for(self, url: str) -> robotparser.RobotFileParser | None:
        p = urlparse(url)
        base = f"{p.scheme}://{p.netloc}"
        if base in self._robots:
            return self._robots[base]
        rp = robotparser.RobotFileParser()
        rp.set_url(urljoin(base, "/robots.txt"))
        try:
            resp = self.session.get(urljoin(base, "/robots.txt"), timeout=self.timeout)
            if resp.status_code == 200 and len(resp.text) < 500_000:
                rp.parse(resp.text.splitlines())
            else:
                rp = None  # no usable robots.txt -> allow
        except Exception:
            rp = None
        self._robots[base] = rp
        return rp

    def allowed(self, url: str) -> bool:
        if not self.respect_robots:
            return True
        rp = self._robots_for(url)
        if rp is None:
            return True
        try:
            return rp.can_fetch(USER_AGENT, url)
        except Exception:
            return True

    def sitemaps(self, base_url: str) -> list[str]:
        rp = self._robots_for(base_url)
        out: list[str] = []
        if rp is not None:
            try:
                out.extend(rp.site_maps() or [])
            except Exception:
                pass
        p = urlparse(base_url)
        default = f"{p.scheme}://{p.netloc}/sitemap.xml"
        if default not in out:
            out.append(default)
        return out

    # ---------------- cache ----------------

    def _cache_path(self, url: str, rendered: bool) -> Path:
        key = hashlib.sha256((("r:" if rendered else "") + url).encode()).hexdigest()[:24]
        return self.cache_dir / f"{key}.json"

    def _read_cache(self, url: str, rendered: bool) -> FetchResult | None:
        path = self._cache_path(url, rendered)
        if not path.exists():
            return None
        try:
            data = json.loads(path.read_text())
        except Exception:
            return None
        if time.time() - data.get("fetched_at", 0) > CACHE_TTL_SECONDS:
            return None
        return FetchResult(from_cache=True, **data)

    def _write_cache(self, res: FetchResult) -> None:
        payload = {
            "url": res.url, "final_url": res.final_url, "status": res.status,
            "html": res.html, "ok": res.ok, "error": res.error,
            "rendered": res.rendered, "fetched_at": res.fetched_at,
        }
        try:
            self._cache_path(res.url, res.rendered).write_text(json.dumps(payload))
        except Exception:
            pass

    # ---------------- fetching ----------------

    def _throttle(self, url: str) -> None:
        host = urlparse(url).netloc
        last = self._last_request.get(host)
        if last is not None:
            wait = self.delay - (time.time() - last)
            if wait > 0:
                time.sleep(wait)
        self._last_request[host] = time.time()

    def get(self, url: str, render_if_thin: bool = True) -> FetchResult:
        url = canonical_url(url)
        if any(urlparse(url).path.lower().endswith(s) for s in BINARY_SUFFIXES):
            return FetchResult(url, url, None, "", False, "skipped: non-HTML resource")

        cached = self._read_cache(url, rendered=False)
        if cached is not None and cached.ok:
            self.stats["cache"] += 1
            if render_if_thin and self._is_thin(cached.html) and self.allow_render:
                r = self._render(url)
                if r is not None and not self._is_thin(r.html):
                    return r
            return cached

        if not self.allowed(url):
            self.stats["blocked"] += 1
            return FetchResult(url, url, None, "", False, "blocked by robots.txt")

        self._throttle(url)
        try:
            resp = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            self.stats["network"] += 1
            ctype = resp.headers.get("content-type", "")
            if "html" not in ctype and "xml" not in ctype and ctype:
                res = FetchResult(url, resp.url, resp.status_code, "", False,
                                  f"skipped: content-type {ctype}")
                return res
            html = resp.text[: self.max_bytes]
            res = FetchResult(url, resp.url, resp.status_code, html, resp.ok,
                              "" if resp.ok else f"HTTP {resp.status_code}")
        except Exception as exc:  # network error, TLS, timeout
            self.stats["failed"] += 1
            return FetchResult(url, url, None, "", False, f"{type(exc).__name__}: {exc}"[:200])

        if res.ok and render_if_thin and self._is_thin(res.html) and self.allow_render:
            rendered = self._render(url)
            if rendered is not None and len(rendered.html) > len(res.html):
                self._write_cache(res)
                return rendered

        if res.ok:
            self._write_cache(res)
        else:
            self.stats["failed"] += 1
        return res

    @staticmethod
    def _is_thin(html: str) -> bool:
        """Heuristic: a client-rendered shell has markup but almost no prose."""
        if not html:
            return True
        import re as _re
        text = _re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", html)
        text = _re.sub(r"(?s)<[^>]+>", " ", text)
        text = _re.sub(r"\s+", " ", text).strip()
        return len(text) < 1200

    # ---------------- JS rendering ----------------

    @staticmethod
    def _find_chromium() -> str | None:
        """Locate a Chromium build already on the machine.

        Playwright refuses to launch when the pip package and the installed
        browser revisions disagree, which is common on pre-baked images. If a
        usable binary exists we point at it rather than downloading another.
        """
        explicit = os.environ.get("PROMISE_AUDIT_CHROMIUM")
        if explicit and Path(explicit).exists():
            return explicit
        roots = [Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))]
        roots.append(Path.home() / ".cache" / "ms-playwright")
        for root in roots:
            if not root.is_dir():
                continue
            for pattern in ("chromium-*/chrome-linux/chrome",
                            "chromium_headless_shell-*/chrome-linux/headless_shell",
                            "chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"):
                found = sorted(root.glob(pattern))
                if found:
                    return str(found[-1])
        for fallback in ("/usr/bin/chromium", "/usr/bin/chromium-browser",
                         "/usr/bin/google-chrome"):
            if Path(fallback).exists():
                return fallback
        return None

    def _ensure_browser(self):
        if self._browser is not None:
            return self._browser
        try:
            from playwright.sync_api import sync_playwright
        except Exception:
            self.allow_render = False
            return None
        try:
            self._playwright = sync_playwright().start()
            launch_kwargs: dict = {"headless": True,
                                   "args": ["--no-sandbox", "--disable-dev-shm-usage"]}
            exec_path = self._find_chromium()
            if exec_path:
                launch_kwargs["executable_path"] = exec_path
            self._browser = self._playwright.chromium.launch(**launch_kwargs)
        except Exception as exc:
            self.render_error = f"{type(exc).__name__}: {exc}"[:160]
            self.allow_render = False
            self._browser = None
        return self._browser

    def _render(self, url: str) -> FetchResult | None:
        if self._render_failures >= self.max_render_failures:
            return None
        cached = self._read_cache(url, rendered=True)
        if cached is not None and cached.ok:
            self.stats["cache"] += 1
            return cached
        browser = self._ensure_browser()
        if browser is None:
            return None
        self._throttle(url)
        try:
            ctx = browser.new_context(user_agent=USER_AGENT, viewport={"width": 1280, "height": 2000})
            page = ctx.new_page()
            page.goto(url, timeout=self.timeout * 1000, wait_until="domcontentloaded")
            page.wait_for_timeout(2500)
            html = page.content()[: self.max_bytes]
            final = page.url
            ctx.close()
            self.stats["rendered"] += 1
            self._render_failures = 0
            res = FetchResult(url, final, 200, html, True, "", rendered=True)
            self._write_cache(res)
            return res
        except Exception as exc:
            try:
                ctx.close()
            except Exception:
                pass
            self._render_failures += 1
            self.render_error = f"{type(exc).__name__}: {exc}"[:160]
            if self._render_failures >= self.max_render_failures:
                # A sandbox where the browser has no outbound access would
                # otherwise cost a full timeout on every thin page.
                self.allow_render = False
                self.stats["render_disabled"] = self.render_error
            return None

    def close(self) -> None:
        try:
            if self._browser is not None:
                self._browser.close()
            if self._playwright is not None:
                self._playwright.stop()
        except Exception:
            pass
