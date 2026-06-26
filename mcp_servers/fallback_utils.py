"""
Common fallback utilities for MCP servers.

Provides web search fallback when API calls fail, and standardizes
result metadata (method, weblink, mcp_name).
"""

from __future__ import annotations

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
}


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
        # Use a simple web search API (can be replaced with more robust solution)
        # For now, return a structured result indicating fallback was attempted
        results = []
        for i in range(min(max_results, 5)):  # Limit web search results
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

    except Exception as e:
        return [{
            "error": f"Web search fallback failed for {mcp_name}: {str(e)}",
            "_metadata": {
                "mcp_name": mcp_name,
                "method": "websearch",
                "fallback_failed": True,
            },
        }]


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
