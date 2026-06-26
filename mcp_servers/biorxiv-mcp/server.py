"""
bioRxiv MCP Server

Provides FastMCP tools for searching and retrieving preprints from bioRxiv and
medRxiv via the free bioRxiv API (no API key required).

API reference: https://api.biorxiv.org/
"""

from __future__ import annotations

import re
import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

mcp = FastMCP("biorxiv-search")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BIORXIV_BASE = "https://api.biorxiv.org"

# Rate limiting — conservatively stay at ~3 requests/second to avoid 429s
_RATE_LIMIT_INTERVAL = 0.35
_last_request_time: float = 0.0

_VALID_SERVERS = frozenset({"biorxiv", "medrxiv"})


# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------


def _rate_limit() -> None:
    """Enforce a minimum interval between consecutive API calls."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _RATE_LIMIT_INTERVAL:
        time.sleep(_RATE_LIMIT_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


async def _fetch_json(url: str) -> Optional[Dict[str, Any]]:
    """Rate-limited GET returning parsed JSON, or ``None`` on failure."""
    _rate_limit()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, follow_redirects=True)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"[biorxiv-mcp] HTTP {e.response.status_code} from {url}: {e.response.text[:200]}")
        return None
    except httpx.TimeoutException:
        print(f"[biorxiv-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[biorxiv-mcp] Request error for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------


def _parse_authors(authors_str: Optional[str]) -> List[str]:
    """Parse a semicolon-separated author string into a list of names."""
    if not authors_str or not authors_str.strip():
        return []
    return [a.strip() for a in authors_str.split(";") if a.strip()]


def _format_article(item: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw bioRxiv API item into a serialisable dictionary."""
    return {
        "doi": item.get("doi"),
        "title": item.get("title"),
        "authors": _parse_authors(item.get("authors")),
        "author_corresponding": item.get("author_corresponding"),
        "author_corresponding_institution": item.get("author_corresponding_institution"),
        "date": item.get("date"),
        "version": item.get("version"),
        "type": item.get("type"),
        "license": item.get("license"),
        "category": item.get("category"),
        "abstract": item.get("abstract"),
        "published": item.get("published"),
        "server": item.get("server"),
    }


# ---------------------------------------------------------------------------
# URL construction helpers
# ---------------------------------------------------------------------------

_DATE_RANGE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}/\d{4}-\d{2}-\d{2}$")


def _is_date_range(interval: str) -> bool:
    """Return ``True`` if *interval* looks like ``YYYY-MM-DD/YYYY-MM-DD``."""
    return bool(_DATE_RANGE_RE.match(interval))


def _build_details_url(server: str, interval: str) -> str:
    """Build the appropriate ``/details/`` URL for the given interval format.

    The bioRxiv API accepts three interval formats:

    * A plain number (``"100"``) — the N most recent posts.
    * A number with ``d`` (``"7d"``) — posts from the last N days.
    * A date range (``"2024-01-01/2024-01-31"``) — optionally followed by
      */*cursor*/*/*format* for pagination.
    """
    if _is_date_range(interval):
        # Date ranges support cursor and format for pagination
        return f"{BIORXIV_BASE}/details/{server}/{interval}/0/json"
    # Numeric and duration intervals are passed as-is (cursor/format not
    # supported by the API for these formats)
    return f"{BIORXIV_BASE}/details/{server}/{interval}"


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_biorxiv(
    query: str,
    max_results: int = 10,
    server: str = "biorxiv",
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """Search bioRxiv or medRxiv for preprints matching the query.

    **Note:** The bioRxiv API does **not** provide a native keyword-search
    endpoint.  This tool fetches a large batch of recently posted preprints
    and filters them locally by matching the query string (case-insensitive)
    against titles, abstracts, and author lists.  For best results use
    specific, distinctive query terms.

    If you know the DOI of the paper you are looking for, use
    ``get_article_details`` instead — it is both faster and guarantees
    retrieval regardless of age.

    Args:
        query: The search term or phrase to match (case-insensitive).
            Multi-word queries are treated as a single sub-string to match.
        max_results: Maximum number of matching results to return
            (default: 10, max: 50).
        server: The preprint server — ``"biorxiv"`` (default) or
            ``"medrxiv"``.
        sort_by: Sort order — ``"relevance"`` (default, keeps API-returned
            order) or ``"date"`` (descending by posting date).

    Returns:
        A list of preprint dictionaries, each containing: **doi**, **title**,
        **authors**, **abstract**, **date**, **category**, **license**,
        **version**, **type**, **published**, and **server**.
    """
    if server not in _VALID_SERVERS:
        return [{"error": f"Invalid server '{server}'. Must be 'biorxiv' or 'medrxiv'."}]

    capped = max(1, min(max_results, 50))

    # Fetch a pool of recent articles to search through locally.
    # The multiplier gives us enough candidates for a meaningful match.
    fetch_count = min(max(capped * 10, 200), 1000)

    url = f"{BIORXIV_BASE}/details/{server}/{fetch_count}"
    data = await _fetch_json(url)
    if data is None:
        return [{"error": f"Search request failed for query: {query}"}]

    collection = data.get("collection", [])
    query_lower = query.lower()

    matched: List[Dict[str, Any]] = []
    for item in collection:
        title = (item.get("title") or "").lower()
        abstract = (item.get("abstract") or "").lower()
        authors = (item.get("authors") or "").lower()

        if query_lower in title or query_lower in abstract or query_lower in authors:
            matched.append(_format_article(item))

    if sort_by == "date":
        matched.sort(key=lambda x: x.get("date") or "", reverse=True)

    return matched[:capped]


@mcp.tool()
async def get_article_details(doi: str, server: str = "biorxiv") -> Dict[str, Any]:
    """Retrieve full metadata for a specific preprint by its DOI.

    Args:
        doi: The DOI of the preprint (e.g. ``"10.1101/2023.01.01.123456"``).
            May include the full URL prefix
            (``"https://doi.org/10.1101/2023.01.01.123456"``) which is
            stripped automatically.
        server: The preprint server — ``"biorxiv"`` (default) or
            ``"medrxiv"``.

    Returns:
        A dict with complete preprint metadata.  Returns
        ``{"error": "Article not found"}`` if the DOI is invalid or no
        article exists for that DOI on the specified server.
    """
    if not doi or not doi.strip():
        return {"error": "DOI is required"}

    if server not in _VALID_SERVERS:
        return {"error": f"Invalid server '{server}'. Must be 'biorxiv' or 'medrxiv'."}

    doi = doi.strip()
    # Strip optional URL prefix (e.g. https://doi.org/10.1101/...)
    if "doi.org/" in doi:
        doi = doi.split("doi.org/")[-1]

    url = f"{BIORXIV_BASE}/details/{server}/{doi}"
    data = await _fetch_json(url)
    if data is None:
        return {"error": f"Failed to retrieve article details for DOI: {doi}"}

    collection = data.get("collection", [])
    if not collection:
        return {"error": f"Article not found: {doi}"}

    # When a version-2 of an article exists, the API returns both versions.
    # Return the latest version (first entry in the collection).
    return _format_article(collection[0])


@mcp.tool()
async def get_recent_articles(
    server: str = "biorxiv",
    interval: str = "7d",
    max_results: int = 30,
) -> List[Dict[str, Any]]:
    """Get recently posted preprints from bioRxiv or medRxiv.

    The *interval* parameter supports three formats matching the bioRxiv API:

      1. **A plain number** (e.g. ``"100"``) — the N most recent preprints.
      2. **A number followed by ``d``** (e.g. ``"7d"``) — preprints from
         the last N days.
      3. **A date range** ``"YYYY-MM-DD/YYYY-MM-DD"`` (e.g.
         ``"2024-01-01/2024-01-31"``) — preprints posted in that window.

    Results are paginated at 30 items per page for date-range queries.

    Args:
        server: The preprint server — ``"biorxiv"`` (default) or
            ``"medrxiv"``.
        interval: The time window or count of posts to retrieve
            (default: ``"7d"`` — last 7 days).
        max_results: Maximum number of results to return (default: 30,
            max: 100).

    Returns:
        A list of preprint dicts (same shape as items returned by
        ``search_biorxiv``).  Returns an error-list if the request fails.
    """
    if server not in _VALID_SERVERS:
        return [{"error": f"Invalid server '{server}'. Must be 'biorxiv' or 'medrxiv'."}]

    capped = max(1, min(max_results, 100))
    url = _build_details_url(server, interval)

    data = await _fetch_json(url)
    if data is None:
        return [{"error": f"Failed to fetch recent articles for {server} ({interval})"}]

    collection = data.get("collection", [])
    results = [_format_article(item) for item in collection]
    return results[:capped]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
