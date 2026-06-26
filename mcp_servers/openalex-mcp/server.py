"""
OpenAlex MCP Server

Provides FastMCP tools for searching and analyzing academic research
via the OpenAlex API (free, no API key required).
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

mcp = FastMCP("openalex-search")

# ---------------------------------------------------------------------------
# API configuration
# ---------------------------------------------------------------------------
OPENALEX_BASE = "https://api.openalex.org"

# Rate limiting: OpenAlex polite pool allows 10 req/s.
# We use a conservative 0.11 s interval (~9 req/s) to stay safe.
_RATE_LIMIT_INTERVAL = 0.11
_last_request_time: float = 0.0
_lock = asyncio.Lock()

# Default field selections (OpenAlex returns everything by default,
# but we can hint at what we care about via select= parameter).
DEFAULT_WORK_SELECT = (
    "id,doi,title,display_name,publication_year,publication_date,"
    "primary_location,authorships,cited_by_count,type,open_access,"
    "keywords,concepts,abstract_inverted_index,referenced_works,"
    "related_works,cited_by_api_url"
)

DEFAULT_AUTHOR_SELECT = (
    "id,display_name,orcid,works_count,cited_by_count,"
    "last_known_institutions,topics,counts_by_year,works_api_url,"
    "2yr_mean_citedness,h_index"
)

DEFAULT_INSTITUTION_SELECT = (
    "id,display_name,ror,country_code,type,works_count,"
    "cited_by_count,homepage_url,image_url,image_thumbnail_url,"
    "topics,counts_by_year,geo"
)


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------


async def _rate_limit() -> None:
    """Enforce OpenAlex polite-pool rate limit (~9 requests/second)."""
    global _last_request_time
    async with _lock:
        now = time.monotonic()
        elapsed = now - _last_request_time
        if elapsed < _RATE_LIMIT_INTERVAL:
            await asyncio.sleep(_RATE_LIMIT_INTERVAL - elapsed)
        _last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


async def _get(endpoint: str, params: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Rate-limited GET request to OpenAlex API returning parsed JSON."""
    await _rate_limit()
    url = f"{OPENALEX_BASE}/{endpoint}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"[openalex-mcp] HTTP {e.response.status_code} "
            f"from {url}: {e.response.text[:200]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[openalex-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[openalex-mcp] Request error for {url}: {e}")
        return None


async def _get_single(endpoint: str, select: str) -> Optional[Dict[str, Any]]:
    """Fetch a single resource by ID with the given field selection."""
    params: Dict[str, str] = {"select": select}
    return await _get(endpoint, params)


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def _rebuild_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> str:
    """Rebuild plain-text abstract from OpenAlex inverted-index format."""
    if not inverted_index:
        return ""
    # Build a list of (position, word) tuples, sort by position, join
    word_positions: List[tuple[int, str]] = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort(key=lambda x: x[0])
    return " ".join(word for _, word in word_positions)


def _summarise_work(work: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key fields from an OpenAlex work response."""
    authors: List[Dict[str, Any]] = []
    for a in work.get("authorships", []):
        author_data = a.get("author", {})
        authors.append({
            "id": author_data.get("id", ""),
            "name": author_data.get("display_name", ""),
            "orcid": a.get("raw_author_orcid", ""),
            "institutions": [
                inst.get("display_name", "")
                for inst in a.get("institutions", [])
            ],
        })

    concepts: List[Dict[str, Any]] = [
        {
            "id": c.get("id", ""),
            "name": c.get("display_name", ""),
            "score": c.get("score", 0),
            "level": c.get("level", 0),
        }
        for c in work.get("concepts", [])
    ]

    location = work.get("primary_location") or {}
    source = location.get("source") or {}
    pdf_url = None
    if location.get("pdf_url"):
        pdf_url = location["pdf_url"]
    elif location.get("landing_page_url"):
        pdf_url = location["landing_page_url"]

    return {
        "id": work.get("id", ""),
        "doi": work.get("doi", ""),
        "title": work.get("display_name", work.get("title", "")),
        "publication_year": work.get("publication_year"),
        "publication_date": work.get("publication_date"),
        "type": work.get("type", ""),
        "cited_by_count": work.get("cited_by_count", 0),
        "abstract": _rebuild_abstract(work.get("abstract_inverted_index")),
        "authors": authors,
        "concepts": concepts,
        "keywords": [k.get("display_name", "") for k in work.get("keywords", [])],
        "source": {
            "name": source.get("display_name", ""),
            "issn_l": source.get("issn_l"),
            "type": source.get("type"),
        },
        "url": pdf_url or "",
        "open_access": work.get("open_access", {}).get("oa_url", ""),
        "referenced_works_count": len(work.get("referenced_works", [])),
        "referenced_works": work.get("referenced_works", []),
    }


def _summarise_author(author: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key fields from an OpenAlex author response."""
    institutions = [
        {
            "id": inst.get("id", ""),
            "name": inst.get("display_name", ""),
            "ror": inst.get("ror", ""),
            "country_code": inst.get("country_code", ""),
            "type": inst.get("type", ""),
        }
        for inst in author.get("last_known_institutions", [])
    ]

    return {
        "id": author.get("id", ""),
        "name": author.get("display_name", ""),
        "orcid": author.get("orcid", ""),
        "works_count": author.get("works_count", 0),
        "cited_by_count": author.get("cited_by_count", 0),
        "h_index": author.get("h_index"),
        "2yr_mean_citedness": author.get("2yr_mean_citedness"),
        "last_known_institutions": institutions,
        "counts_by_year": author.get("counts_by_year", []),
        "works_api_url": author.get("works_api_url", ""),
    }


def _summarise_institution(institution: Dict[str, Any]) -> Dict[str, Any]:
    """Extract key fields from an OpenAlex institution response."""
    return {
        "id": institution.get("id", ""),
        "name": institution.get("display_name", ""),
        "ror": institution.get("ror", ""),
        "country_code": institution.get("country_code", ""),
        "type": institution.get("type", ""),
        "works_count": institution.get("works_count", 0),
        "cited_by_count": institution.get("cited_by_count", 0),
        "homepage_url": institution.get("homepage_url", ""),
        "image_url": institution.get("image_url", ""),
        "image_thumbnail_url": institution.get("image_thumbnail_url", ""),
        "geo": institution.get("geo", {}),
        "counts_by_year": institution.get("counts_by_year", []),
    }


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_openalex(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    filter_by: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search academic works (papers, books, datasets) via OpenAlex.

    OpenAlex indexes over 250M scholarly works from all disciplines.
    Results are fetched from ``https://api.openalex.org/works``.

    Args:
        query: Free-text search query (e.g. ``"transformer attention"``).
            Supports OpenAlex search syntax including quoted phrases.
        max_results: Maximum number of results to return (default 10, max 200).
        sort_by: Sort order — ``"relevance"`` (default), ``"cited_by_count"``,
            ``"publication_year"``, or ``"publication_date"``.
        filter_by: Optional OpenAlex filter expression
            (e.g. ``"publication_year:2020-2024,type:article"``).
            See https://docs.openalex.org/api-entities/filters for syntax.

    Returns:
        A list of work dictionaries, each containing: **id**, **doi**,
        **title**, **publication_year**, **publication_date**, **type**,
        **cited_by_count**, **abstract**, **authors**, **concepts**,
        **keywords**, **source**, **url**, **open_access**, and
        **referenced_works_count**.
    """
    capped = max(1, min(max_results, 200))
    params: Dict[str, str] = {
        "search": query,
        "per_page": str(capped),
        "sort": sort_by,
        "select": DEFAULT_WORK_SELECT,
    }
    if filter_by:
        params["filter"] = filter_by

    data = await _get("works", params)
    if data is None:
        return [{"error": f"Search request failed for query: {query}"}]

    results = data.get("results", [])
    return [_summarise_work(w) for w in results]


@mcp.tool()
async def get_work_details(work_id: str) -> Dict[str, Any]:
    """Retrieve detailed information about a specific academic work.

    Accepts OpenAlex IDs (``W3123456789``) or DOIs
    (``10.xxxx/xxxxx``).  When a DOI is passed, the server
    automatically resolves it to the OpenAlex ``doi:`` identifier
    format.

    Args:
        work_id: Work identifier — an OpenAlex ID (e.g. ``W3123456789``),
            a DOI (e.g. ``10.1038/s41586-023-06198-6``), or the full
            OpenAlex API URL for the work.

    Returns:
        A dictionary with full work metadata including: **id**, **doi**,
        **title**, **publication_year**, **publication_date**, **type**,
        **cited_by_count**, **abstract**, **authors**, **concepts**,
        **keywords**, **source**, **url**, **open_access**,
        **referenced_works_count**, **referenced_works**, and
        **related_works**.  Returns ``{"error": "Work not found"}`` if the
        identifier is invalid.
    """
    # Normalise identifier: DOI → "doi:10.xxxx/xxxxx"
    orig_id = work_id.strip()
    normalised = _normalise_identifier(orig_id)

    data = await _get_single(f"works/{normalised}", DEFAULT_WORK_SELECT)
    if data is None:
        return {"error": f"Work not found: {orig_id}"}

    return _summarise_work(data)


@mcp.tool()
async def get_author_details(author_id: str) -> Dict[str, Any]:
    """Retrieve detailed information about a specific author.

    Accepts OpenAlex author IDs (``A5123456789``) or ORCID iDs
    (``0000-0002-1234-5678``).  When an ORCID is passed, the server
    automatically resolves it to the OpenAlex ``orcid:`` identifier
    format.

    Args:
        author_id: Author identifier — an OpenAlex ID (e.g.
            ``A5123456789``), an ORCID iD (e.g.
            ``0000-0002-1234-5678``), or the full OpenAlex API URL
            for the author.

    Returns:
        A dictionary with author metadata including: **id**, **name**,
        **orcid**, **works_count**, **cited_by_count**, **h_index**,
        **2yr_mean_citedness**, **last_known_institutions**,
        **counts_by_year**, and **works_api_url**.  Returns
        ``{"error": "Author not found"}`` if the identifier is invalid.
    """
    orig_id = author_id.strip()
    normalised = _normalise_identifier(orig_id)

    data = await _get_single(f"authors/{normalised}", DEFAULT_AUTHOR_SELECT)
    if data is None:
        return {"error": f"Author not found: {orig_id}"}

    return _summarise_author(data)


@mcp.tool()
async def get_institution_details(institution_id: str) -> Dict[str, Any]:
    """Retrieve detailed information about a specific institution.

    Accepts OpenAlex institution IDs (``I5123456789``) or ROR IDs
    (``https://ror.org/xxxxx``).  When a ROR is passed, the server
    automatically resolves it to the OpenAlex ``ror:`` identifier
    format.

    Args:
        institution_id: Institution identifier — an OpenAlex ID
            (e.g. ``I5123456789``), a ROR ID (e.g.
            ``https://ror.org/03yrm5c26``), or the full OpenAlex API
            URL for the institution.

    Returns:
        A dictionary with institution metadata including: **id**,
        **name**, **ror**, **country_code**, **type**, **works_count**,
        **cited_by_count**, **homepage_url**, **image_url**,
        **image_thumbnail_url**, **geo**, and **counts_by_year**.
        Returns ``{"error": "Institution not found"}`` if the identifier
        is invalid.
    """
    orig_id = institution_id.strip()
    normalised = _normalise_identifier(orig_id)

    data = await _get_single(
        f"institutions/{normalised}", DEFAULT_INSTITUTION_SELECT
    )
    if data is None:
        return {"error": f"Institution not found: {orig_id}"}

    return _summarise_institution(data)


# ---------------------------------------------------------------------------
# Identifier normalisation helpers
# ---------------------------------------------------------------------------


def _normalise_identifier(raw: str) -> str:
    """Normalise a user-provided identifier into the format OpenAlex expects.

    - ``https://api.openalex.org/works/W3123456789`` → ``W3123456789``
    - ``10.1038/s41586-023-06198-6`` → ``doi:10.1038/s41586-023-06198-6``
    - ``0000-0002-1234-5678`` → ``orcid:0000-0002-1234-5678``
    - ``https://ror.org/03yrm5c26`` → ``ror:https://ror.org/03yrm5c26``
    """
    # Strip full API URLs down to the ID segment
    if raw.startswith(OPENALEX_BASE):
        path = raw[len(OPENALEX_BASE):].lstrip("/")
        segments = path.split("/")
        if len(segments) >= 2:
            # e.g. works/W3123456789 → W3123456789
            return segments[1] if segments[0] in (
                "works", "authors", "institutions", "sources",
                "concepts", "funders", "publishers",
            ) else raw

    # DOI without explicit prefix → doi:...
    if raw.startswith("10.") and "/" in raw:
        return f"doi:{raw}"

    # ORCID (bare digits or full URL)
    if _looks_like_orcid(raw):
        orcid = raw.strip()
        if orcid.startswith("https://"):
            orcid = orcid.rstrip("/").split("/")[-1]
        # Also handle "orcid:0000-..." already prefixed
        if orcid.startswith("orcid:"):
            return orcid
        return f"orcid:{orcid}"

    # ROR URL
    if raw.startswith("https://ror.org/"):
        return f"ror:{raw}"

    return raw


def _looks_like_orcid(value: str) -> bool:
    """Heuristic: check if the string looks like an ORCID iD."""
    import re

    # ORCID pattern: 4-4-4-4 hex digits
    pattern = re.compile(
        r"^(https://orcid\.org/)?(\d{4}-\d{4}-\d{4}-\d{3}[\dX])$"
    )
    return bool(pattern.match(value.strip()))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
