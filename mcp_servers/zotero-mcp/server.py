"""
Zotero MCP Server
Provides FastMCP tools for searching, managing, and exporting references
via the Zotero Web API v3 (REST API).
"""

from __future__ import annotations

import os
import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

mcp = FastMCP("zotero")

# ---------------------------------------------------------------------------
# Configuration from environment variables
# ---------------------------------------------------------------------------
ZOTERO_API_KEY = os.environ.get("ZOTERO_API_KEY", "")
ZOTERO_USER_ID = os.environ.get("ZOTERO_USER_ID", "")
ZOTERO_LIBRARY_TYPE = os.environ.get("ZOTERO_LIBRARY_TYPE", "users")
ZOTERO_GROUP_ID = os.environ.get("ZOTERO_GROUP_ID", "")

BASE_URL = "https://api.zotero.org"

# Determine library path based on type
if ZOTERO_LIBRARY_TYPE == "groups" and ZOTERO_GROUP_ID:
    _LIBRARY_PATH = f"/groups/{ZOTERO_GROUP_ID}"
elif ZOTERO_USER_ID:
    _LIBRARY_PATH = f"/users/{ZOTERO_USER_ID}"
else:
    _LIBRARY_PATH = ""

_HEADERS: Dict[str, str] = {
    "Zotero-API-Key": ZOTERO_API_KEY,
    "Zotero-API-Version": "3",
}

# Rate limiting: stay conservative (max ~4 requests/second)
_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 0.25

# Valid Zotero item types for create_item validation
_VALID_ITEM_TYPES: List[str] = [
    "artwork",
    "attachment",
    "audioRecording",
    "bill",
    "blogPost",
    "book",
    "bookSection",
    "case",
    "computerProgram",
    "conferencePaper",
    "dictionaryEntry",
    "document",
    "email",
    "encyclopediaArticle",
    "film",
    "forumPost",
    "hearing",
    "instantMessage",
    "interview",
    "journalArticle",
    "letter",
    "magazineArticle",
    "manuscript",
    "map",
    "newspaperArticle",
    "note",
    "patent",
    "podcast",
    "preprint",
    "presentation",
    "radioBroadcast",
    "report",
    "standard",
    "statute",
    "tvBroadcast",
    "thesis",
    "videoRecording",
    "webpage",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _rate_limit() -> None:
    """Enforce a conservative request interval to respect Zotero API limits."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


def _check_config() -> Optional[str]:
    """Return an error string if required configuration is missing, else None."""
    if not ZOTERO_API_KEY:
        return "ZOTERO_API_KEY environment variable is not set"
    if ZOTERO_LIBRARY_TYPE == "users" and not ZOTERO_USER_ID:
        return "ZOTERO_USER_ID environment variable is not set"
    if ZOTERO_LIBRARY_TYPE == "groups" and not ZOTERO_GROUP_ID:
        return "ZOTERO_GROUP_ID must be set when ZOTERO_LIBRARY_TYPE=groups"
    if not _LIBRARY_PATH:
        return (
            "Could not determine library path from environment variables. "
            "Set ZOTERO_USER_ID or ZOTERO_LIBRARY_TYPE=groups with ZOTERO_GROUP_ID."
        )
    return None


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------


async def _api_get(
    path: str,
    params: Optional[Dict[str, str]] = None,
) -> Any:
    """Rate-limited GET request returning parsed JSON, or None on failure."""
    _rate_limit()
    url = f"{BASE_URL}{path}"
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=_HEADERS, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"[zotero-mcp] HTTP {e.response.status_code} from {url}: "
            f"{e.response.text[:300]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[zotero-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[zotero-mcp] Request error for {url}: {e}")
        return None


async def _api_get_text(
    path: str,
    params: Optional[Dict[str, str]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Rate-limited GET request returning raw text, or None on failure.

    Accepts optional *extra_headers* merged on top of the default headers.
    """
    _rate_limit()
    url = f"{BASE_URL}{path}"
    headers = {**_HEADERS, **(extra_headers or {})}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        print(
            f"[zotero-mcp] HTTP {e.response.status_code} from {url}: "
            f"{e.response.text[:300]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[zotero-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[zotero-mcp] Request error for {url}: {e}")
        return None


async def _api_post(
    path: str,
    data: Any,
    params: Optional[Dict[str, str]] = None,
) -> Any:
    """Rate-limited POST with JSON body, returning parsed JSON or None."""
    _rate_limit()
    url = f"{BASE_URL}{path}"
    headers = {**_HEADERS, "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url, headers=headers, json=data, params=params
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(
            f"[zotero-mcp] HTTP {e.response.status_code} from {url}: "
            f"{e.response.text[:300]}"
        )
        return None
    except httpx.TimeoutException:
        print(f"[zotero-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[zotero-mcp] Request error for {url}: {e}")
        return None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_library(
    query: str,
    collection: Optional[str] = None,
    limit: int = 20,
    sort_by: str = "dateAdded",
) -> List[Dict[str, Any]]:
    """Search items in the Zotero library.

    Searches across titles, creators, years, tags, and other metadata.

    Args:
        query: Search query string (searches title, creators, year, tags,
            and other metadata fields).
        collection: Optional collection key to restrict results to a specific
            collection (e.g. ``"ABCD1234"``).  Omit to search the entire
            library.
        limit: Maximum number of results to return (default: 20, max: 100).
        sort_by: Sort field — choose from ``"dateAdded"`` (default),
            ``"dateModified"``, ``"title"``, ``"creator"``, ``"date"``,
            ``"year"``, ``"publisher"``, ``"type"``, or ``"accessedDate"``.

    Returns:
        A list of item dictionaries.  Each item contains keys such as
        ``key`` (the item's unique Zotero key), ``data`` (with nested
        title, creators, itemType, date, tags, collections, etc.),
        ``meta`` (creatorSummary, parsedDate, etc.), and ``links``.
    """
    config_err = _check_config()
    if config_err:
        return [{"error": config_err}]

    capped = max(1, min(limit, 100))
    params: Dict[str, str] = {
        "q": query,
        "limit": str(capped),
        "sort": sort_by,
        "format": "json",
    }
    if collection:
        params["collectionKey"] = collection

    data = await _api_get(f"{_LIBRARY_PATH}/items", params)
    if data is None:
        return [{"error": f"Search request failed for query: {query}"}]
    return data if isinstance(data, list) else [data]


@mcp.tool()
async def get_item_details(item_key: str) -> Dict[str, Any]:
    """Get detailed information about a specific Zotero library item.

    Args:
        item_key: Zotero item key (e.g. ``"ABCD1234"``).

    Returns:
        A dictionary with the item's complete data:
        ``data`` (title, creators, itemType, date, tags, collections,
        relations, extra fields), ``meta`` (creatorSummary, parsedDate,
        etc.), ``links`` (self, alternate, enclosure), and ``version``.
        Returns ``{"error": "..."}`` if the item is not found.
    """
    config_err = _check_config()
    if config_err:
        return {"error": config_err}

    key = item_key.strip() if item_key else ""
    if not key:
        return {"error": "item_key is required"}

    data = await _api_get(f"{_LIBRARY_PATH}/items/{key}")
    if data is None:
        return {"error": f"Item not found: {item_key}"}
    return data


@mcp.tool()
async def create_item(
    item_type: str,
    title: str,
    creators: Optional[List[Dict[str, str]]] = None,
    fields: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a new item in the Zotero library.

    Args:
        item_type: Zotero item type.  Common values:
            ``"journalArticle"``, ``"book"``, ``"bookSection"``,
            ``"conferencePaper"``, ``"thesis"``, ``"report"``,
            ``"webpage"``, ``"preprint"``, ``"patent"``,
            ``"document"``, ``"presentation"``, ``"interview"``,
            ``"videoRecording"``, ``"audioRecording"``.
            See the Zotero API docs for the full list.
        title: The item title.
        creators: Optional list of creator dicts, each containing:
            - ``firstName`` (str): Creator's first name.
            - ``lastName`` (str): Creator's last name.
            - ``creatorType`` (str): Role — ``"author"`` (default),
              ``"editor"``, ``"translator"``, ``"contributor"``,
              ``"seriesEditor"``, etc.
        fields: Optional dict of additional item fields. Common keys:
            - ``date`` (str): Publication date (e.g. ``"2024"``,
              ``"2024-06"``, ``"2024-06-15"``).
            - ``publicationTitle`` (str): Journal or venue name.
            - ``DOI`` (str): Digital Object Identifier.
            - ``abstractNote`` (str): Abstract or summary.
            - ``volume`` (str): Volume number.
            - ``issue`` (str): Issue number.
            - ``pages`` (str): Page range (e.g. ``"1-10"``).
            - ``publisher`` (str): Publisher name.
            - ``place`` (str): Publication place.
            - ``ISBN`` (str): ISBN identifier.
            - ``url`` (str): Associated URL.
            - ``language`` (str): Language code (e.g. ``"en"``).
            - ``tags`` (list[dict]): Tags, e.g.
              ``[{"tag": "keyword"}]``.
            - ``extra`` (str): Extra notes or custom fields.

    Returns:
        The created item dictionary including the new item's ``key``,
        ``data``, ``meta``, ``links``, and ``version``.
        Returns ``{"error": "..."}`` on failure.
    """
    config_err = _check_config()
    if config_err:
        return {"error": config_err}

    if item_type not in _VALID_ITEM_TYPES:
        return {
            "error": (
                f"Invalid item type: '{item_type}'. "
                f"Valid types: {', '.join(sorted(_VALID_ITEM_TYPES))}"
            )
        }

    if not title or not title.strip():
        return {"error": "title is required"}

    item_data: Dict[str, Any] = {
        "itemType": item_type,
        "title": title.strip(),
    }
    if creators:
        item_data["creators"] = creators
    if fields:
        item_data.update(fields)

    # Zotero API expects a JSON array in the request body
    payload: List[Dict[str, Any]] = [item_data]

    result = await _api_post(f"{_LIBRARY_PATH}/items", payload)
    if result is None:
        return {"error": "Failed to create item"}

    if isinstance(result, list) and len(result) > 0:
        return result[0]
    return {"error": "Unexpected response format", "response": result}


@mcp.tool()
async def export_bibtex(item_keys: List[str]) -> str:
    """Export Zotero library items as BibTeX.

    Args:
        item_keys: List of Zotero item keys to export
            (e.g. ``["ABCD1234", "EFGH5678"]``).

    Returns:
        A BibTeX-formatted string containing the exported references.
        If the export fails the returned string starts with ``"% Error:"``.
    """
    config_err = _check_config()
    if config_err:
        return config_err

    if not item_keys:
        return "% Error: No item keys provided"

    keys_str = ",".join(k.strip() for k in item_keys if k.strip())
    if not keys_str:
        return "% Error: No valid item keys provided"

    result = await _api_get_text(
        f"{_LIBRARY_PATH}/items",
        {"itemKey": keys_str, "format": "bibtex"},
        extra_headers={"Accept": "application/x-bibtex"},
    )
    if result is None:
        return "% Error: Failed to export items as BibTeX"
    return result


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
