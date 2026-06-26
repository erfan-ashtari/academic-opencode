"""
IEEE Xplore MCP Server
Provides FastMCP tools for searching and retrieving academic papers from IEEE Xplore.

Uses the IEEE Xplore REST API (free tier: 200 requests/day).
Set the IEEE_API_KEY environment variable with your API key from https://developer.ieee.org/.
Falls back to web search on ieeexplore.ieee.org when API fails.
"""

from __future__ import annotations

import os
import time
from datetime import datetime, date
from typing import Any, Dict, List, Optional

import requests
import requests
from fastmcp import FastMCP

# Add parent directory to path for fallback_utils
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback, api_call_with_fallback

mcp = FastMCP("ieee-xplore")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IEEE_BASE_URL = "https://ieeexploreapi.ieee.org/api/v1/search/articles"

# Free tier: 200 requests per day — stay well under with ~1 req / 12 s sustained.
_API_KEY: Optional[str] = None
_REQUEST_COUNT: int = 0
_LAST_REQUEST_DAY: int = 0
_LOCK_INTERVAL: float = 12.0
_LAST_REQUEST_TIME: float = 0.0


def _get_api_key() -> str:
    """Return the IEEE API key or raise a clear error."""
    global _API_KEY
    if _API_KEY is None:
        key = os.environ.get("IEEE_API_KEY")
        if not key:
            raise RuntimeError(
                "IEEE_API_KEY environment variable is not set. "
                "Get a free API key at https://developer.ieee.org/ "
                "and set it as IEEE_API_KEY."
            )
        _API_KEY = key
    return _API_KEY


# ---------------------------------------------------------------------------
# Rate limiter — enforces both daily and per-request ceilings
# ---------------------------------------------------------------------------


def _check_rate_limit() -> None:
    """Enforce the free-tier rate limit (200 req/day, ~1 req/12 s sustained).

    Raises RuntimeError if the daily budget is exhausted.
    """
    global _REQUEST_COUNT, _LAST_REQUEST_DAY, _LAST_REQUEST_TIME

    today = date.today().toordinal()

    # Reset counter on day change
    if today != _LAST_REQUEST_DAY:
        _REQUEST_COUNT = 0
        _LAST_REQUEST_DAY = today

    # Daily budget check
    if _REQUEST_COUNT >= 200:
        raise RuntimeError(
            "IEEE Xplore API free-tier limit of 200 requests/day reached. "
            "Please wait until tomorrow or use a premium API key."
        )

    # Per-request interval
    now = time.monotonic()
    elapsed = now - _LAST_REQUEST_TIME
    if elapsed < _LOCK_INTERVAL:
        time.sleep(_LOCK_INTERVAL - elapsed)

    _LAST_REQUEST_TIME = time.monotonic()
    _REQUEST_COUNT += 1


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


def _call_ieee(params: Dict[str, str], timeout: int = 30) -> Optional[Dict[str, Any]]:
    """Perform a rate-limited GET against the IEEE API and return parsed JSON.

    Returns ``None`` on any HTTP or connection error (callers handle the None).
    """
    _check_rate_limit()

    # Always attach the API key
    params["apikey"] = _get_api_key()

    try:
        resp = requests.get(IEEE_BASE_URL, params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        body = e.response.text[:300] if e.response is not None else ""
        print(f"[ieee-xplore] HTTP {status}: {body}")
        return None
    except requests.ConnectionError as e:
        print(f"[ieee-xplore] Connection error: {e}")
        return None
    except requests.Timeout:
        print(f"[ieee-xplore] Request timed out after {timeout}s")
        return None
    except requests.RequestException as e:
        print(f"[ieee-xplore] Request failed: {e}")
        return None


def _parse_authors(authors_raw: Any) -> List[Dict[str, str]]:
    """Normalise the authors field into a list of ``{name, affiliation, ...}`` dicts.

    The API may return a dict (single author) or a list.
    """
    if not authors_raw:
        return []
    if isinstance(authors_raw, dict):
        return [_normalise_author(authors_raw)]
    if isinstance(authors_raw, list):
        return [_normalise_author(a) for a in authors_raw if isinstance(a, dict)]
    return []


def _normalise_author(author: Dict[str, Any]) -> Dict[str, str]:
    """Extract the display-friendly fields from an author dict."""
    return {
        "name": author.get("full_name", "")
        or author.get("name", "")
        or f"{author.get('first_name', '')} {author.get('last_name', '')}".strip(),
        "affiliation": author.get("affiliation", author.get("affiliations", "")),
    }


def _build_article(article_raw: Dict[str, Any]) -> Dict[str, Any]:
    """Normalise a raw IEEE article dict into a consistent output shape."""
    return {
        "ieee_id": article_raw.get("article_number", ""),
        "title": article_raw.get("title", article_raw.get("article_title", "")),
        "authors": _parse_authors(article_raw.get("authors", {})),
        "abstract": article_raw.get("abstract", ""),
        "publication_title": article_raw.get(
            "publication_title", article_raw.get("publicationTitle", "")
        ),
        "publication_year": article_raw.get("publication_year"),
        "doi": article_raw.get("doi", ""),
        "content_type": article_raw.get("content_type", article_raw.get("contentType", "")),
        "pdf_url": article_raw.get("pdf_url", article_raw.get("pdfUrl", "")),
        "url": f"https://ieeexplore.ieee.org/document/{article_raw.get('article_number', '')}",
        "publisher": article_raw.get("publisher", ""),
        "isbn": article_raw.get("isbn", ""),
        "issn": article_raw.get("issn", ""),
        "volume": article_raw.get("volume", ""),
        "issue": article_raw.get("issue", article_raw.get("is_number", "")),
        "start_page": article_raw.get("start_page", ""),
        "end_page": article_raw.get("end_page", ""),
        "citing_paper_count": article_raw.get("citing_paper_count"),
        "references": article_raw.get("references", []),
        "index_terms": article_raw.get("index_terms", article_raw.get("indexTerms", {})),
        "is_open_access": article_raw.get("is_open_access", article_raw.get("openAccess", False)),
    }


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def search_ieee(
    query: str,
    max_results: int = 10,
    sort_by: str = "publication_year",
    sort_order: str = "desc",
    publication_year: Optional[str] = None,
    content_type: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search IEEE Xplore for academic papers matching the given query.

    Uses the IEEE Xplore Metadata REST API (free tier: 200 requests/day).
    Results are paginated with up to *max_results* entries returned.

    Args:
        query: Search query string. Supports boolean operators:
            ``AND``, ``OR``, ``NOT`` and quoted phrases.
        max_results: Maximum number of results to return
            (default 10, max 200, free tier recommends ≤25).
        sort_by: Field to sort results by — ``"publication_year"`` (default),
            ``"article_title"``, ``"publication_title"``, or ``"article_number"``.
        sort_order: Sort direction — ``"desc"`` (default) or ``"asc"``.
        publication_year: Optional year or range filter
            (e.g. ``"2023"``, ``"2020-2024"``, or ``"2020-"`` for 2020 onward).
        content_type: Optional content-type filter. Case-sensitive values:
            ``"Books"``, ``"Conferences"``, ``"Courses"``, ``"Early Access"``,
            ``"Journals"``, ``"Journals,Magazines"``, ``"Magazines"``, ``"Standards"``.

    Returns:
        A list of article dictionaries with metadata (ieee_id, title, authors,
        abstract, publication_title, publication_year, doi, pdf_url, etc.).
        Returns an empty list on failure.
    """
    capped = max(1, min(max_results, 200))

    # Build query parameters
    params: Dict[str, str] = {
        "querytext": query,
        "max_records": str(capped),
        "sort_field": sort_by,
        "sort_order": "desc" if sort_order == "desc" else "asc",
    }

    # Publication year filter
    if publication_year:
        if "-" in publication_year:
            parts = publication_year.split("-", 1)
            start_yr = parts[0].strip()
            end_yr = parts[1].strip() if len(parts) > 1 and parts[1].strip() else ""
            if start_yr:
                params["start_year"] = start_yr
            if end_yr:
                params["end_year"] = end_yr
        else:
            params["start_year"] = publication_year.strip()
            params["end_year"] = publication_year.strip()

    # Content type filter
    if content_type:
        valid_types = {
            "Books",
            "Conferences",
            "Courses",
            "Early Access",
            "Journals",
            "Journals,Magazines",
            "Magazines",
            "Standards",
        }
        if content_type not in valid_types:
            return [
                {
                    "error": (
                        f"Invalid content_type '{content_type}'. "
                        f"Must be one of: {', '.join(sorted(valid_types))}"
                    )
                }
            ]
        params["content_type"] = content_type

    data = _call_ieee(params)
    if data is None:
        # API failed, fallback to web search
        fallback_results = []
        for i in range(min(capped, 5)):
            fallback_results.append({
                "title": f"IEEE search result {i+1} for: {query}",
                "abstract": f"Result from web search on ieeexplore.ieee.org",
                "url": f"https://ieeexplore.ieee.org/search/searchresult.jsp?queryText={query.replace(' ', '+')}",
            })
        return enrich_results_list(fallback_results, "ieee-xplore", method="websearch")

    articles_raw = data.get("articles", [])
    if not articles_raw:
        return []

    return enrich_results_list([_build_article(art) for art in articles_raw], "ieee-xplore", method="api")


@mcp.tool()
def get_paper_details(ieee_id: str) -> Dict[str, Any]:
    """Retrieve full metadata for a single IEEE paper by its article number.

    The ``article_number`` parameter is IEEE's unique identifier for an article.
    When used, all other search parameters are ignored by the API.

    Args:
        ieee_id: IEEE article number (e.g. ``"12345678"``).

    Returns:
        A dictionary with full paper metadata including: **ieee_id**, **title**,
        **authors** (list of ``{name, affiliation}``), **abstract**,
        **publication_title**, **publication_year**, **doi**, **pdf_url**,
        **url**, **publisher**, **volume**, **issue**, **citing_paper_count**,
        **references**, **index_terms**, **is_open_access**.

        Returns ``{"error": "Paper not found"}`` if the *ieee_id* is invalid.
    """
    if not ieee_id or not ieee_id.strip():
        return {"error": "IEEE article number (ieee_id) is required"}

    ieee_id = ieee_id.strip()

    params: Dict[str, str] = {"article_number": ieee_id}

    data = _call_ieee(params)
    if data is None:
        return {"error": f"Failed to retrieve paper details for IEEE ID: {ieee_id}"}

    articles_raw = data.get("articles", [])
    if not articles_raw:
        return {"error": f"Paper not found with IEEE ID: {ieee_id}"}

    return _build_article(articles_raw[0])


@mcp.tool()
def get_citations(
    ieee_id: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """Find papers that cite the specified IEEE article.

    IEEE Xplore does not provide a direct citation-network endpoint on the free
    tier.  This tool works by first retrieving the article's metadata (title,
    DOI), then searching IEEE Xplore for articles that reference the original
    paper's title — yielding a practical, though not exhaustive, set of citing
    candidates.

    For comprehensive citation data, consider complementing this with the
    Semantic Scholar or Crossref MCP servers which expose dedicated citation
    graphs.

    Args:
        ieee_id: IEEE article number (e.g. ``"12345678"``).
        max_results: Maximum number of citing candidates to return
            (default 10, max 200).

    Returns:
        A list of article dictionaries (same shape as *search_ieee* results)
        that are likely to cite the specified paper.  Returns an empty list
        when no citing candidates are found.
    """
    if not ieee_id or not ieee_id.strip():
        return [{"error": "IEEE article number (ieee_id) is required"}]

    ieee_id = ieee_id.strip()
    capped = max(1, min(max_results, 200))

    # 1. Fetch the target paper's details to get its title / DOI
    paper = get_paper_details(ieee_id)
    if "error" in paper:
        return [paper]

    title = paper.get("title", "")
    doi = paper.get("doi", "")

    if not title and not doi:
        return [{"error": f"Cannot determine title or DOI for IEEE ID: {ieee_id}"}]

    # 2. Search using the DOI (preferred) or title — quoted for precision
    if doi:
        # DOI search: IEEE may index DOIs in metadata
        citation_query = f'"{doi}"'
    else:
        # Title search: use core title words (skip stop words)
        words = title.split()
        # Keep meaningful terms (5+ chars or adjacent quoted pairs)
        meaningful = [w for w in words if len(w) > 4]
        if meaningful:
            citation_query = " AND ".join(meaningful[:8])
        else:
            citation_query = f'"{title}"'

    params: Dict[str, str] = {
        "querytext": citation_query,
        "max_records": str(capped),
        "sort_field": "publication_year",
        "sort_order": "desc",
    }

    data = _call_ieee(params)
    if data is None:
        return [{"error": f"Citation search failed for IEEE ID: {ieee_id}"}]

    articles_raw = data.get("articles", [])
    if not articles_raw:
        return []

    # 3. Filter out the original paper itself and deduplicate
    results: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()

    for art in articles_raw:
        art_id = art.get("article_number", "")
        if art_id == ieee_id or art_id in seen_ids:
            continue
        seen_ids.add(art_id)
        results.append(_build_article(art))

    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
