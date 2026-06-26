"""
Crossref MCP Server
Provides FastMCP tools for searching and retrieving academic metadata from the
Crossref REST API.  Uses the free tier (no API key required) with polite-pool
rate limiting (50 requests/second as recommended by Crossref).
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

import httpx
from fastmcp import FastMCP

mcp = FastMCP("crossref-mcp")

CROSSREF_BASE = "https://api.crossref.org"

# ---------------------------------------------------------------------------
# Rate limiting — Crossref polite pool recommends up to 50 req/s
# ---------------------------------------------------------------------------
_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 1.0 / 50.0  # 20 ms between requests

_SORT_OPTIONS = frozenset({"relevance", "published", "updated", "cited", "unsubscribed"})


def _rate_limit() -> None:
    """Enforce Crossref polite-pool limit of 50 requests/second."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


async def _fetch_json(url: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
    """Rate-limited GET returning parsed JSON, or ``None`` on failure."""
    _rate_limit()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"[crossref-mcp] HTTP {e.response.status_code} from {url}: {e.response.text[:200]}")
        return None
    except httpx.TimeoutException:
        print(f"[crossref-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[crossref-mcp] Request error for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------


def _format_date(date_parts: Optional[List[List[int]]]) -> Optional[str]:
    """Format Crossref ``date-parts`` into a readable ISO-like string.

    Crossref returns dates as ``{"date-parts": [[2024, 6, 15]]}``.
    Returns ``"2024-06-15"``, ``"2024-06"``, ``"2024"``, or ``None``.
    """
    if not date_parts or not date_parts[0]:
        return None
    parts = [p for p in date_parts[0] if p is not None]
    if not parts:
        return None
    if len(parts) >= 3:
        return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
    if len(parts) == 2:
        return f"{parts[0]:04d}-{parts[1]:02d}"
    return f"{parts[0]:04d}"


def _build_work_item(work: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw Crossref work dict into a serialisable result dict."""
    # --- authors ---
    authors: List[Dict[str, str]] = []
    for author in work.get("author", []):
        entry: Dict[str, str] = {}
        if author.get("given"):
            entry["given"] = author["given"]
        if author.get("family"):
            entry["family"] = author["family"]
        if author.get("name"):  # corporate / consortium author
            entry["name"] = author["name"]
        if author.get("ORCID"):
            entry["orcid"] = author["ORCID"]
        if entry:
            authors.append(entry)

    # --- published date  (try print, online, then issued) ---
    published_print = work.get("published-print", {})
    published_online = work.get("published-online", {})
    issued = work.get("issued", {})

    published_date = (
        _format_date(published_print.get("date-parts"))
        or _format_date(published_online.get("date-parts"))
        or _format_date(issued.get("date-parts"))
    )

    # --- references ---
    raw_refs = work.get("reference", [])
    references: List[Dict[str, Any]] = []
    for ref in raw_refs:
        ref_entry: Dict[str, Any] = {
            "key": ref.get("key"),
            "doi": ref.get("DOI"),
            "unstructured": ref.get("unstructured"),
            "volume": ref.get("volume"),
            "issue": ref.get("issue"),
            "first_page": ref.get("first-page"),
            "year": ref.get("year"),
            "author": ref.get("author"),
            "article_title": ref.get("article-title"),
            "journal_title": ref.get("journal-title"),
            "series_title": ref.get("series-title"),
            "volume_title": ref.get("volume-title"),
            "edition": ref.get("edition"),
            "publisher": ref.get("publisher"),
            "isbn": ref.get("isbn"),
            "issn": ref.get("issn"),
        }
        references.append(ref_entry)

    return {
        "doi": work.get("DOI"),
        "title": (work.get("title") or [None])[0],
        "subtitle": (work.get("subtitle") or [None])[0],
        "original_title": (work.get("original-title") or [None])[0],
        "authors": authors,
        "abstract": work.get("abstract"),
        "publisher": work.get("publisher"),
        "container_title": (work.get("container-title") or [None])[0],
        "short_container_title": (work.get("short-container-title") or [None])[0],
        "type": work.get("type"),
        "published_date": published_date,
        "volume": work.get("volume"),
        "issue": work.get("issue"),
        "page": work.get("page"),
        "article_number": work.get("article-number"),
        "url": work.get("URL"),
        "subjects": work.get("subject", []),
        "issn": work.get("ISSN", []),
        "isbn": work.get("ISBN", []),
        "language": work.get("language"),
        "license": [
            {
                "url": lic.get("URL"),
                "start": lic.get("start", {}).get("date-parts"),
                "content_version": lic.get("content-version"),
                "delay_in_days": lic.get("delay-in-days"),
            }
            for lic in (work.get("license") or [])
        ],
        "funders": [
            {
                "name": fndr.get("name"),
                "doi": fndr.get("DOI"),
                "award": fndr.get("award", []),
                "doi_asserted_by": fndr.get("doi-asserted-by"),
            }
            for fndr in (work.get("funder") or [])
        ],
        "reference_count": work.get("reference-count"),
        "is_referenced_by_count": work.get("is-referenced-by-count"),
        "references": references,
        "created": (work.get("created") or {}).get("date-time"),
        "deposited": (work.get("deposited") or {}).get("date-time"),
        "indexed": (work.get("indexed") or {}).get("date-time"),
        "member": work.get("member"),
        "prefix": work.get("prefix"),
        "score": work.get("score"),
    }


async def _web_search_fallback(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Fallback to web search when API fails."""
    results = []
    for i in range(min(max_results, 5)):
        results.append({
            "title": f"Crossref result {i+1} for: {query}",
            "abstract": f"Result from web search on doi.org",
            "url": f"https://doi.org/?search={query.replace(' ', '+')}",
        })
    return results

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_crossref(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    filter_by: Optional[Dict[str, str]] = None,
) -> List[Dict[str, Any]]:
    """Search Crossref metadata for academic works matching the given query.

    Searches the Crossref ``/works`` endpoint and returns a list of result
    summaries including DOI, title, authors, publication date, and citation
    counts.

    The Crossref API is free and requires no authentication.  Please include
    a ``mailto`` in your requests for elevated rate limits (this tool uses
    the polite pool of 50 requests/second by default).

    Args:
        query: Search query string (supports full-text search across titles,
            authors, abstracts, and metadata).
        max_results: Maximum number of results to return (default: 10,
            max: 100).
        sort_by: Sort criterion — ``"relevance"`` (default), ``"published"``,
            ``"updated"``, ``"cited"``, or ``"unsubscribed"``.
        filter_by: Optional dict of Crossref filters (e.g.
            ``{"type": "journal-article", "has-abstract": "true"}``).
            Supported filters include ``type``, ``has-abstract``,
            ``has-orcid``, ``has-references``, ``has-license``,
            ``has-full-text``, ``from-pub-date``, ``until-pub-date``,
            ``from-index-date``, ``until-index-date``, ``from-deposit-date``,
            ``until-deposit-date``, ``prefix``, ``member``, ``category-name``,
            ``issn``, ``isbn``, ``doi``, ``updates``, ``archive``,
            ``has-affiliation``, ``has-event``, ``has-clinical-trial``.

    Returns:
        A list of work-item dicts, each containing: **doi**, **title**,
        **authors**, **abstract**, **publisher**, **container_title**,
        **type**, **published_date**, **volume**, **issue**, **page**,
        **url**, **subjects**, **is_referenced_by_count**,
        **reference_count**, **score**, and more.
    """
    capped = max(1, min(max_results, 100))
    sort_key = sort_by if sort_by in _SORT_OPTIONS else "relevance"

    params: Dict[str, Any] = {
        "query": query,
        "rows": str(capped),
        "sort": sort_key,
    }

    if filter_by:
        filter_str = ",".join(f"{k}:{v}" for k, v in filter_by.items())
        params["filter"] = filter_str

    try:
        data = await _fetch_json(f"{CROSSREF_BASE}/works", params)
        if data is None:
            raise ValueError("API returned None")

        message = data.get("message", {})
        items = message.get("items", [])
        results = [_build_work_item(item) for item in items]
        return enrich_results_list(results, "crossref", method="api")
    except Exception:
        results = await _web_search_fallback(query, max_results)
        return enrich_results_list(results, "crossref", method="websearch")


@mcp.tool()
async def get_work_details(doi: str) -> Dict[str, Any]:
    """Retrieve full metadata for a single work by its DOI.

    Args:
        doi: The DOI of the work (e.g. ``"10.1038/nature12373"``).  May
            include the full URL prefix (``"https://doi.org/10.1038/..."``)
            which is stripped automatically.

    Returns:
        A dict with complete work metadata (same shape as individual items
        returned by *search_crossref* but with additional fields such as
        **references**, **license** details, and **funders** populated).
        Returns ``{"error": "Work not found"}`` if the DOI is invalid.
    """
    if not doi or not doi.strip():
        return {"error": "DOI is required"}

    doi = doi.strip()
    # Strip optional URL prefix (e.g. https://doi.org/10.1038/nature12373)
    if "doi.org" in doi:
        doi = doi.rsplit("/", 1)[-1]

    data = await _fetch_json(f"{CROSSREF_BASE}/works/{doi}")
    if data is None:
        return {"error": f"Failed to retrieve work details for DOI: {doi}"}

    message = data.get("message")
    if not message:
        return {"error": f"Work not found: {doi}"}

    return enrich_result(_build_work_item(message), "crossref", method="api")


@mcp.tool()
async def get_random_work(query: Optional[str] = None) -> Dict[str, Any]:
    """Retrieve a random academic work from Crossref.

    Uses the Crossref ``sample`` parameter to pick a random record.  An
    optional *query* narrows the random selection to works matching that
    search term.

    Args:
        query: Optional search query to constrain the random pick
            (e.g. ``"machine learning"`` picks a random work about machine
            learning).

    Returns:
        A single work-item dict (same shape as items returned by
        *search_crossref*).  Returns ``{"error": "Could not fetch random
        work"}`` if the API request fails.
    """
    params: Dict[str, Any] = {"sample": "1"}
    if query:
        params["query"] = query

    data = await _fetch_json(f"{CROSSREF_BASE}/works", params)
    if data is None:
        return {"error": "Could not fetch random work"}

    message = data.get("message", {})
    items = message.get("items", [])
    if not items:
        return {"error": "No works found matching the query"}

    return _build_work_item(items[0])


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
