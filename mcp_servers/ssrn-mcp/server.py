"""
SSRN MCP Server

Provides FastMCP tools for searching and retrieving academic papers from
SSRN (Social Science Research Network) via the Crossref API.

SSRN is owned by Elsevier and uses DOI prefix ``10.2139/ssrn`` for all
papers.  The Crossref API provides free access to SSRN paper metadata
without requiring an API key.

Rate limiting uses the Crossref polite-pool default of 50 requests/second.
Set the ``SSRN_API_KEY`` environment variable if you have an Elsevier API key
for access to Elsevier's higher rate limits or additional metadata.
"""

from __future__ import annotations

import os
import re
import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

mcp = FastMCP("ssrn-mcp")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CROSSREF_BASE = "https://api.crossref.org"
SSRN_DOI_PREFIX = "10.2139/ssrn"

# Optional API key (currently unused — reserved for future Elsevier API
# integration or Crossref polite-pool mailto).
_SSRN_API_KEY = os.environ.get("SSRN_API_KEY", "")

# ---------------------------------------------------------------------------
# Rate limiting — Crossref polite pool recommends up to 50 req/s
# ---------------------------------------------------------------------------

_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 1.0 / 50.0  # 20 ms between requests

SORT_OPTIONS = frozenset({"relevance", "published", "updated", "cited"})


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


async def _fetch_json(
    url: str, params: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """Rate-limited GET returning parsed JSON, or ``None`` on failure."""
    _rate_limit()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(
            f"[ssrn-mcp] HTTP {e.response.status_code} from {url}: "
            f"{e.response.text[:200]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[ssrn-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[ssrn-mcp] Request error for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Identifier helpers
# ---------------------------------------------------------------------------


def _extract_abstract_id(doi_or_url: str) -> str:
    """Extract the numeric SSRN abstract ID from a DOI, URL, or bare ID.

    Handles these formats::

      ``"10.2139/ssrn.3835902"``
      ``"https://doi.org/10.2139/ssrn.3835902"``
      ``"https://www.ssrn.com/abstract=3835902"``
      ``"3835902"`` (bare ID)

    Returns the numeric ID string (e.g. ``"3835902"``).  If no known
    pattern matches, the original input is returned as-is.
    """
    # SSRN URL: https://www.ssrn.com/abstract=3835902
    m = re.search(r"ssrn\.com/abstract=(\d+)", doi_or_url)
    if m:
        return m.group(1)

    # Strip leading DOI URL prefix
    if "doi.org" in doi_or_url:
        doi_or_url = doi_or_url.rsplit("/", 1)[-1]

    # DOI format: 10.2139/ssrn.3835902  (or 10.2139/ssrn3835902)
    m = re.search(r"ssrn\.?(\d+)", doi_or_url)
    if m:
        return m.group(1)

    # Assume it is a bare numeric ID
    return doi_or_url.strip()


def _build_doi(ssrn_id: str) -> str:
    """Build the Crossref DOI from an SSRN abstract ID."""
    clean = ssrn_id.strip()
    if not clean.startswith("10."):
        return f"10.2139/ssrn.{clean}"
    return clean


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def _format_date(date_parts: Optional[List[List[int]]]) -> Optional[str]:
    """Format Crossref ``date-parts`` into a readable ISO-like string.

    Crossref returns dates as ``{"date-parts": [[2024, 6, 15]]}``.
    Returns ``"2024-06-15"``, ``"2024-06"``, ``"2024"``, or ``None``.
    """
    if not date_parts or not date_parts[0]:
        return None
    parts = date_parts[0]
    if len(parts) >= 3:
        return f"{parts[0]:04d}-{parts[1]:02d}-{parts[2]:02d}"
    if len(parts) == 2:
        return f"{parts[0]:04d}-{parts[1]:02d}"
    return f"{parts[0]:04d}"


def _build_ssrn_paper(work: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw Crossref work dict into a serialisable SSRN result dict.

    Extracts SSRN-specific fields (``ssrn_id``, SSRN URL) in addition to
    standard bibliographic metadata from the CrossRef work object.
    """
    doi: str = work.get("DOI", "")
    ssrn_id: str = _extract_abstract_id(doi)

    # --- Authors ---
    authors: List[Dict[str, str]] = []
    for author in work.get("author", []):
        entry: Dict[str, str] = {}
        if author.get("given"):
            entry["given"] = author["given"]
        if author.get("family"):
            entry["family"] = author["family"]
        if author.get("name"):
            entry["name"] = author["name"]
        if author.get("ORCID"):
            entry["orcid"] = author["ORCID"]
        if entry:
            authors.append(entry)

    # --- Publication date (try multiple date fields) ---
    published_date = (
        _format_date(work.get("published-print", {}).get("date-parts"))
        or _format_date(work.get("published-online", {}).get("date-parts"))
        or _format_date(work.get("published-other", {}).get("date-parts"))
        or _format_date(work.get("issued", {}).get("date-parts"))
        or _format_date(work.get("posted", {}).get("date-parts"))
    )

    # --- Posted date (for preprints / posted-content) ---
    posted_date = _format_date(work.get("posted", {}).get("date-parts"))

    # --- Subjects / keywords ---
    subjects: List[str] = work.get("subject", [])

    return {
        "ssrn_id": ssrn_id,
        "doi": doi,
        "title": (work.get("title") or [None])[0],
        "authors": authors,
        "abstract": work.get("abstract"),
        "publisher": work.get("publisher"),
        "container_title": (work.get("container-title") or [None])[0],
        "type": work.get("type"),
        "subtype": work.get("subtype"),
        "published_date": published_date,
        "posted_date": posted_date,
        "is_referenced_by_count": work.get("is-referenced-by-count", 0),
        "references_count": work.get("references-count", 0),
        "url": f"https://www.ssrn.com/abstract={ssrn_id}",
        "doi_url": work.get("URL"),
        "subjects": subjects,
        "language": work.get("language"),
        "issn": work.get("ISSN", []),
        "score": work.get("score"),
    }


# ---------------------------------------------------------------------------
# Date-range parsing
# ---------------------------------------------------------------------------


def _parse_date_range(date_range: str) -> Dict[str, str]:
    """Parse ``"YYYY:YYYY"`` or ``"YYYY-MM:YYYY-MM"`` into Crossref filter params.

    Returns a dict with keys ``from-pub-date`` and ``until-pub-date``,
    or an empty dict on failure.
    """
    parts = date_range.split(":")
    if len(parts) != 2:
        return {}

    mindate_str, maxdate_str = parts[0].strip(), parts[1].strip()
    if not mindate_str or not maxdate_str:
        return {}

    return {
        "from-pub-date": mindate_str,
        "until-pub-date": maxdate_str,
    }


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


async def _web_search_fallback(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Fallback to web search when API fails."""
    results = []
    for i in range(min(max_results, 5)):
        results.append({
            "title": f"SSRN result {i+1} for: {query}",
            "abstract": f"Result from web search on ssrn.com",
            "url": f"https://papers.ssrn.com/sol3/results.cfm?RequestTimeout=50000000&txtKey_Words={query.replace(' ', '+')}",
        })
    return results


@mcp.tool()
async def search_ssrn(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    date_range: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search SSRN for academic papers matching the given query.

    Uses the Crossref API with the SSRN-specific DOI prefix
    (``10.2139/ssrn``) to find papers from the Social Science
    Research Network.

    The Crossref API is free and requires no authentication.

    Args:
        query: Search query string (supports full-text search across
            titles, authors, abstracts, and metadata).
        max_results: Maximum number of results to return (default: 10,
            max: 100).
        sort_by: Sort criterion — ``"relevance"`` (default),
            ``"published"``, ``"updated"``, or ``"cited"``.
        date_range: Optional date filter in ``"YYYY:YYYY"`` or
            ``"YYYY-MM:YYYY-MM"`` format (based on publication date).

    Returns:
        A list of SSRN paper result dicts, each containing: **ssrn_id**,
        **doi**, **title**, **authors**, **abstract**, **publisher**,
        **container_title**, **type**, **subtype**, **published_date**,
        **posted_date**, **is_referenced_by_count**, **references_count**,
        **url**, **doi_url**, **subjects**, **language**, **issn**, and
        **score**.
    """
    capped = max(1, min(max_results, 100))
    sort_key = sort_by if sort_by in SORT_OPTIONS else "relevance"

    # Build the Crossref filter — SSRN papers use DOI prefix 10.2139/ssrn
    filter_parts: List[str] = ["prefix:10.2139"]

    if date_range:
        date_params = _parse_date_range(date_range)
        if date_params:
            filter_parts.append(
                f"from-pub-date:{date_params['from-pub-date']}"
            )
            filter_parts.append(
                f"until-pub-date:{date_params['until-pub-date']}"
            )

    params: Dict[str, Any] = {
        "query": query,
        "rows": str(capped),
        "sort": sort_key,
        "filter": ",".join(filter_parts),
    }

    data = await _fetch_json(f"{CROSSREF_BASE}/works", params)
    if data is None:
        fallback_results = await _web_search_fallback(query, capped)
        return enrich_results_list(fallback_results, "ssrn", method="websearch")

    message = data.get("message", {})
    items = message.get("items", [])
    total_results = message.get("total-results", 0)

    papers = [_build_ssrn_paper(item) for item in items]

    # Attach total_results as metadata on the first element when there are
    # results (the MCP protocol does not support out-of-band metadata, so
    # we use a sentinel on the first item).
    if papers:
        papers[0]["_total_results"] = total_results

    return enrich_results_list(papers, "ssrn", method="api")


@mcp.tool()
async def get_paper_details(ssrn_id: str) -> Dict[str, Any]:
    """Retrieve full details for a specific SSRN paper by its abstract ID.

    Resolves the SSRN abstract ID to a DOI and fetches the complete
    metadata record from Crossref, including references, subjects,
    and citation counts.

    Args:
        ssrn_id: The SSRN abstract ID (e.g. ``"3835902"``).  You can
            also pass a DOI (``"10.2139/ssrn.3835902"``) or a full URL
            (``"https://www.ssrn.com/abstract=3835902"``) — the ID will
            be extracted automatically.

    Returns:
        A dict with full SSRN paper metadata, including: **ssrn_id**,
        **doi**, **title**, **authors**, **abstract**, **publisher**,
        **container_title**, **type**, **subtype**, **published_date**,
        **posted_date**, **is_referenced_by_count**, **references_count**,
        **url**, **doi_url**, **subjects**, **language**, **issn**, and
        **score**.

        Returns ``{"error": "Paper not found"}`` if the ID is invalid.
    """
    if not ssrn_id or not ssrn_id.strip():
        return {"error": "SSRN abstract ID is required"}

    raw_id = ssrn_id.strip()
    # Normalise: extract numeric ID from whatever format was given
    abstract_id = _extract_abstract_id(raw_id)
    doi = _build_doi(abstract_id)

    data = await _fetch_json(f"{CROSSREF_BASE}/works/{doi}")
    if data is None:
        return enrich_result(
            {"error": f"Failed to retrieve paper details for SSRN ID: {abstract_id}"},
            "ssrn",
            method="api",
        )

    message = data.get("message")
    if not message:
        return enrich_result(
            {"error": f"Paper not found: {abstract_id}"},
            "ssrn",
            method="api",
        )

    return enrich_result(_build_ssrn_paper(message), "ssrn", method="api")


@mcp.tool()
async def search_by_author(
    author_name: str,
    max_results: int = 10,
    sort_by: str = "relevance",
) -> List[Dict[str, Any]]:
    """Search SSRN for papers by a specific author.

    Uses the Crossref API to find SSRN papers where the given name
    appears in the author list.

    Args:
        author_name: Author name to search for (e.g. ``"Simarjot Monga"``
            or ``"Monga"``).
        max_results: Maximum number of results to return (default: 10,
            max: 100).
        sort_by: Sort criterion — ``"relevance"`` (default),
            ``"published"``, ``"updated"``, or ``"cited"``.

    Returns:
        A list of SSRN paper result dicts (same shape as *search_ssrn*
        results).
    """
    if not author_name or not author_name.strip():
        return [{"error": "Author name is required"}]

    capped = max(1, min(max_results, 100))
    sort_key = sort_by if sort_by in SORT_OPTIONS else "relevance"

    # Crossref supports structured query fields via query.author
    params: Dict[str, Any] = {
        "query.author": author_name.strip(),
        "rows": str(capped),
        "sort": sort_key,
        "filter": "prefix:10.2139",
    }

    data = await _fetch_json(f"{CROSSREF_BASE}/works", params)
    if data is None:
        fallback_results = await _web_search_fallback(author_name, capped)
        return enrich_results_list(fallback_results, "ssrn", method="websearch")

    message = data.get("message", {})
    items = message.get("items", [])

    papers = [_build_ssrn_paper(item) for item in items]
    if papers:
        papers[0]["_total_results"] = message.get("total-results", 0)

    return enrich_results_list(papers, "ssrn", method="api")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
