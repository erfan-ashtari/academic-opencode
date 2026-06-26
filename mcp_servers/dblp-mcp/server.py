"""
DBLP MCP Server

Provides FastMCP tools for searching and retrieving academic computer science
publications from the DBLP bibliography database.  The DBLP API is free and
requires no API key.

API documentation: https://dblp.org/faq/How+to+use+the+dblp+search+API.html
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

mcp = FastMCP("dblp-search")

# ---------------------------------------------------------------------------
# API endpoints
# ---------------------------------------------------------------------------
DBLP_SEARCH_PUBL = "https://dblp.org/search/publ/api"
DBLP_SEARCH_AUTHOR = "https://dblp.org/search/author/api"

# ---------------------------------------------------------------------------
# Rate limiting — DBLP asks for a maximum of 1 request/second
# ---------------------------------------------------------------------------
_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 1.0


def _rate_limit() -> None:
    """Enforce DBLP rate limit of 1 request per second."""
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
    url: str, params: Optional[Dict[str, str]] = None
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
            f"[dblp-mcp] HTTP {e.response.status_code} from {url}: "
            f"{e.response.text[:200]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[dblp-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[dblp-mcp] Request error for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Response helpers
# ---------------------------------------------------------------------------


def _ensure_list(value: Any) -> List[Any]:
    """Normalise a value that may be a single dict or a list of dicts into a list.

    DBLP's JSON representation encodes XML attributes with an ``@`` prefix
    and collapses single-element lists into bare objects.
    """
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def _extract_authors(info: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract an ordered list of authors from a DBLP search-result info block.

    The ``authors.author`` field may be a single dict (one author), a list of
    dicts (multiple authors), or absent entirely.
    """
    authors_raw = info.get("authors")
    if not authors_raw or not isinstance(authors_raw, dict):
        return []

    author_entries = _ensure_list(authors_raw.get("author"))
    result: List[Dict[str, str]] = []
    for entry in author_entries:
        if not isinstance(entry, dict):
            continue
        author: Dict[str, str] = {
            "name": entry.get("text", ""),
        }
        pid = entry.get("@pid")
        if pid:
            author["pid"] = pid
        result.append(author)
    return result


def _extract_aliases(info: Dict[str, Any]) -> List[str]:
    """Extract author aliases, handling string, list-of-string, or absent."""
    raw = info.get("aliases")
    if not raw:
        return []
    if isinstance(raw, str):
        return [a.strip() for a in raw.split(";") if a.strip()]
    if isinstance(raw, list):
        return [str(a).strip() for a in raw if a]
    return []


def _extract_notes(info: Dict[str, Any]) -> List[Dict[str, str]]:
    """Extract author notes (affiliations, awards, …) from search results.

    The ``notes.note`` field may be a single dict or a list.  Each note has
    a ``@type`` attribute and a ``text`` value.
    """
    notes_raw = info.get("notes")
    if not notes_raw or not isinstance(notes_raw, dict):
        return []

    note_entries = _ensure_list(notes_raw.get("note"))
    result: List[Dict[str, str]] = []
    for entry in note_entries:
        if not isinstance(entry, dict):
            continue
        result.append(
            {
                "type": entry.get("@type", ""),
                "text": entry.get("text", ""),
            }
        )
    return result


def _build_publication_item(hit: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a single DBLP search hit into a serialisable result dict."""
    info = hit.get("info", {})
    return {
        "key": info.get("key", ""),
        "title": info.get("title", ""),
        "authors": _extract_authors(info),
        "venue": info.get("venue", ""),
        "year": info.get("year"),
        "type": info.get("type", ""),
        "access": info.get("access", ""),
        "doi": info.get("doi", ""),
        "ee": info.get("ee", ""),
        "url": info.get("url", ""),
    }


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_dblp(
    query: str,
    max_results: int = 10,
    sort_by: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search DBLP for academic computer science publications.

    DBLP indexes over 6 million computer science publications from journals,
    conferences, and workshops.  Results are ordered by relevance (the DBLP
    API does not support server-side sorting over arbitrary fields).

    Args:
        query: Free-text search query.  Supports DBLP search syntax
            including quoted exact phrases and field prefixes such as
            ``author:``, ``venue:``, ``year:``, ``title:``, and ``key:``
            (e.g. ``"author:Yoshua_Bengio year:2023"``).
        max_results: Maximum number of hits to return (default: 10,
            max: 1000).
        sort_by: Accepted for interface compatibility but currently
            ignored — DBLP always returns results sorted by relevance.

    Returns:
        A list of publication dictionaries, each containing: **key**,
        **title**, **authors** (``[{name, pid?}, ...]``), **venue**,
        **year**, **type**, **access**, **doi**, **ee**, and **url**.
    """
    capped = max(1, min(max_results, 1000))
    params: Dict[str, str] = {
        "q": query,
        "format": "json",
        "h": str(capped),
    }

    data = await _fetch_json(DBLP_SEARCH_PUBL, params)
    if data is None:
        return [{"error": f"Search request failed for query: {query}"}]

    result = data.get("result", {})
    hits = result.get("hits", {})
    hit_list = hits.get("hit", [])
    if not isinstance(hit_list, list):
        hit_list = []

    return [_build_publication_item(hit) for hit in hit_list]


@mcp.tool()
async def get_publication_details(pubkey: str) -> Dict[str, Any]:
    """Retrieve full details for a specific publication by its DBLP key.

    Args:
        pubkey: The DBLP publication key (e.g.
            ``"conf/icml/VaswaniSPUJGKP17"``).  This is the ``key`` field
            returned by *search_dblp*.

    Returns:
        A dictionary with full publication metadata (same shape as
        individual items returned by *search_dblp*).  Returns
        ``{"error": "Publication not found"}`` if the key is invalid.
    """
    if not pubkey or not pubkey.strip():
        return {"error": "Publication key is required"}

    pubkey = pubkey.strip()

    params: Dict[str, str] = {
        "q": f"key:{pubkey}",
        "format": "json",
        "h": "1",
    }

    data = await _fetch_json(DBLP_SEARCH_PUBL, params)
    if data is None:
        return {"error": f"Failed to retrieve publication: {pubkey}"}

    result = data.get("result", {})
    hits = result.get("hits", {})
    hit_list = hits.get("hit", [])
    if not isinstance(hit_list, list) or not hit_list:
        return {"error": f"Publication not found: {pubkey}"}

    return _build_publication_item(hit_list[0])


@mcp.tool()
async def get_author_details(author_id: str) -> Dict[str, Any]:
    """Retrieve details about a DBLP author by their unique PID.

    Args:
        author_id: The DBLP author PID (e.g. ``"l/YannLeCun"`` or
            ``"p/YoshuaBengio"``).  These identifiers are stable across
            name changes and disambiguation updates.

    Returns:
        A dictionary with: **url**, **key** (the PID), **name**,
        **aliases** (list of alternate names), and **notes** (list of
        ``{type, text}`` entries such as affiliations and awards).
        Returns ``{"error": "Author not found"}`` if the PID is invalid.
    """
    if not author_id or not author_id.strip():
        return {"error": "Author ID is required"}

    author_id = author_id.strip()

    params: Dict[str, str] = {
        "q": f"pid:{author_id}",
        "format": "json",
        "h": "1",
    }

    data = await _fetch_json(DBLP_SEARCH_AUTHOR, params)
    if data is None:
        return {"error": f"Failed to retrieve author: {author_id}"}

    result = data.get("result", {})
    hits = result.get("hits", {})
    hit_list = hits.get("hit", [])
    if not isinstance(hit_list, list) or not hit_list:
        return {"error": f"Author not found: {author_id}"}

    info = hit_list[0].get("info", {})

    return {
        "url": info.get("url", ""),
        "key": info.get("key", ""),
        "name": info.get("author", ""),
        "aliases": _extract_aliases(info),
        "notes": _extract_notes(info),
    }


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
