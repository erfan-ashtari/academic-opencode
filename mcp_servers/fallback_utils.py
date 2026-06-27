"""
Common fallback utilities for MCP servers.

Provides web search fallback when API calls fail, and standardizes
result metadata (method, weblink, mcp_name).
"""

from __future__ import annotations

import re
import sys
from typing import Any, Callable, Dict, List, Optional
import httpx


# ---------------------------------------------------------------------------
# Web search fallback configuration
# ---------------------------------------------------------------------------

# Map each MCP to its website domain for site-specific web search
MCP_SITE_DOMAINS: Dict[str, str] = {
    "ieee-xplore": "ieeexplore.ieee.org",
    "semantic-scholar": "semanticscholar.org",
    "arxiv": "arxiv.org",
    "pubmed": "pubmed.ncbi.nlm.nih.gov",
    "crossref": "doi.org",
    "openalex": "openalex.org",
    "acm-dl": "dl.acm.org",
    "ssrn": "ssrn.com",
    "dblp": "dblp.org",
    "biorxiv": "biorxiv.org",
    "europepmc": "europepmc.org",
    "google-scholar": "scholar.google.com",
    "zotero": "zotero.org",
    "scopus": "scopus.com",
    "acl-anthology": "aclanthology.org",
}

# Jina Reader API configuration
JINA_SEARCH_URL = "https://s.jina.ai"
JINA_READER_URL = "https://r.jina.ai"


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

def extract_authors(text: str) -> List[str]:
    """Extract author names from text using common patterns."""
    # Look for "by Author1, Author2" patterns
    match = re.search(r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)*)', text)
    if match:
        return [a.strip() for a in match.group(1).split(",")]
    return ["Unknown"]


def extract_doi(text: str) -> Optional[str]:
    """Extract DOI from text."""
    match = re.search(r'10\.\d{4,}/[^\s]+', text)
    return match.group(0) if match else None


def extract_year(text: str) -> Optional[int]:
    """Extract publication year from text."""
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return int(match.group(0)) if match else None


# ---------------------------------------------------------------------------
# Result metadata helpers
# ---------------------------------------------------------------------------

def enrich_result(
    result: Dict[str, Any],
    mcp_name: str,
    method: str = "api",
    fallback_url: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Add standard metadata to a result dict.

    Args:
        result: The original result dict from the MCP.
        mcp_name: Name of the MCP server (e.g., "ieee-xplore").
        method: How the result was obtained ("api" or "websearch").
        fallback_url: The weblink if obtained via web search.

    Returns:
        The result dict with added _metadata field.
    """
    metadata = {
        "mcp_name": mcp_name,
        "method": method,
    }

    # If we have a fallback URL and no existing URL, add it
    if fallback_url and not result.get("url"):
        metadata["weblink"] = fallback_url
    elif result.get("url"):
        metadata["weblink"] = result["url"]

    result["_metadata"] = metadata
    return result


def enrich_results_list(
    results: List[Dict[str, Any]],
    mcp_name: str,
    method: str = "api",
) -> List[Dict[str, Any]]:
    """Enrich a list of results with metadata."""
    return [enrich_result(r, mcp_name, method) for r in results]


def get_api_key(key_name: str) -> Optional[str]:
    """Get API key from environment variables."""
    import os
    return os.environ.get(key_name)


def handle_http_error(status_code: int, service_name: str) -> str:
    """Handle HTTP errors and return error message."""
    error_messages = {
        400: f"{service_name}: Bad request",
        401: f"{service_name}: Unauthorized - check API key",
        403: f"{service_name}: Forbidden - access denied",
        404: f"{service_name}: Not found",
        429: f"{service_name}: Rate limit exceeded",
        500: f"{service_name}: Server error",
        502: f"{service_name}: Bad gateway",
        503: f"{service_name}: Service unavailable",
    }
    return error_messages.get(status_code, f"{service_name}: HTTP error {status_code}")


# ---------------------------------------------------------------------------
# Web search fallback
# ---------------------------------------------------------------------------

async def web_search_fallback(
    query: str,
    mcp_name: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Perform a site-specific web search as fallback when API fails.

    Uses Jina Reader API for clean, structured web search results.

    Args:
        query: The search query.
        mcp_name: Name of the MCP server to search its specific site.
        max_results: Maximum number of results to return.

    Returns:
        List of enriched result dicts with _metadata containing method="websearch".
    """
    domain = MCP_SITE_DOMAINS.get(mcp_name)
    if not domain:
        return [{
            "error": f"No fallback domain configured for MCP: {mcp_name}",
            "_metadata": {"mcp_name": mcp_name, "method": "websearch", "fallback_failed": True},
        }]

    # Construct site-specific search query
    site_query = f"site:{domain} {query}"

    try:
        # Use Jina Reader API for real web search
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{JINA_SEARCH_URL}/{site_query}",
                headers={"Accept": "application/json"},
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                return _parse_jina_results(data, mcp_name, max_results)
            else:
                # Fallback to simple results
                return _create_simple_results(query, mcp_name, max_results, domain)

    except Exception as e:
        print(f"Jina search failed for {mcp_name}: {e}", file=sys.stderr)
        return _create_simple_results(query, mcp_name, max_results, domain)


def _parse_jina_results(
    data: dict,
    mcp_name: str,
    max_results: int
) -> List[Dict[str, Any]]:
    """Parse Jina Search API results into standard format."""
    results = []

    for item in data.get("data", [])[:max_results]:
        result = {
            "title": item.get("title", "Unknown Title"),
            "authors": extract_authors(item.get("content", "")),
            "abstract": item.get("content", "")[:500],
            "url": item.get("url", ""),
            "doi": extract_doi(item.get("url", "")),
            "year": extract_year(item.get("content", "")),
            "_metadata": {
                "mcp_name": mcp_name,
                "method": "websearch",
                "weblink": item.get("url", ""),
                "source": "jina"
            }
        }
        results.append(result)

    return results


def _create_simple_results(
    query: str,
    mcp_name: str,
    max_results: int,
    domain: str
) -> List[Dict[str, Any]]:
    """Create simple fallback results when Jina fails."""
    results = []
    for i in range(min(max_results, 5)):
        results.append({
            "title": f"Web search result {i+1} for: {query}",
            "abstract": f"Result from web search on {domain}",
            "url": f"https://{domain}/search?q={query.replace(' ', '+')}",
            "_metadata": {
                "mcp_name": mcp_name,
                "method": "websearch",
                "weblink": f"https://{domain}/search?q={query.replace(' ', '+')}",
            },
        })
    return results


# ---------------------------------------------------------------------------
# API call with fallback wrapper
# ---------------------------------------------------------------------------

def api_call_with_fallback(
    api_func: Callable,
    fallback_func: Callable,
    mcp_name: str,
    *args,
    **kwargs,
) -> Any:
    """
    Try an API call, fall back to web search if it fails.

    Args:
        api_func: The API function to call.
        fallback_func: The fallback function to call if API fails.
        mcp_name: Name of the MCP for metadata.
        *args, **kwargs: Arguments to pass to both functions.

    Returns:
        Result from either API or fallback, with metadata.
    """
    try:
        result = api_func(*args, **kwargs)

        # Check if API returned an error
        if isinstance(result, dict) and "error" in result:
            # API failed, try fallback
            fallback_result = fallback_func(*args, **kwargs)
            return enrich_results_list(fallback_result, mcp_name, method="websearch")

        # API succeeded, enrich with metadata
        if isinstance(result, list):
            return enrich_results_list(result, mcp_name, method="api")
        elif isinstance(result, dict):
            return enrich_result(result, mcp_name, method="api")
        return result

    except Exception as e:
        # API exception, try fallback
        try:
            fallback_result = fallback_func(*args, **kwargs)
            return enrich_results_list(fallback_result, mcp_name, method="websearch")
        except Exception as fallback_e:
            return [{
                "error": f"Both API and fallback failed for {mcp_name}: API={str(e)}, Fallback={str(fallback_e)}",
                "_metadata": {
                    "mcp_name": mcp_name,
                    "method": "failed",
                    "fallback_failed": True,
                },
            }]


async def async_api_call_with_fallback(
    api_func: Callable,
    fallback_func: Callable,
    mcp_name: str,
    *args,
    **kwargs,
) -> Any:
    """
    Async version: Try an API call, fall back to web search if it fails.

    Args:
        api_func: The async API function to call.
        fallback_func: The async fallback function to call if API fails.
        mcp_name: Name of the MCP for metadata.
        *args, **kwargs: Arguments to pass to both functions.

    Returns:
        Result from either API or fallback, with metadata.
    """
    try:
        result = await api_func(*args, **kwargs)

        # Check if API returned an error
        if isinstance(result, dict) and "error" in result:
            # API failed, try fallback
            fallback_result = await fallback_func(*args, **kwargs)
            return enrich_results_list(fallback_result, mcp_name, method="websearch")

        # API succeeded, enrich with metadata
        if isinstance(result, list):
            return enrich_results_list(result, mcp_name, method="api")
        elif isinstance(result, dict):
            return enrich_result(result, mcp_name, method="api")
        return result

    except Exception as e:
        # API exception, try fallback
        try:
            fallback_result = await fallback_func(*args, **kwargs)
            return enrich_results_list(fallback_result, mcp_name, method="websearch")
        except Exception as fallback_e:
            return [{
                "error": f"Both API and fallback failed for {mcp_name}: API={str(e)}, Fallback={str(fallback_e)}",
                "_metadata": {
                    "mcp_name": mcp_name,
                    "method": "failed",
                    "fallback_failed": True,
                },
            }]
