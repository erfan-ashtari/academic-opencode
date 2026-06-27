"""
Scopus MCP Server

Elsevier Scopus database integration for academic paper search.
Provides access to 27,000+ journal titles across all disciplines.

Requires: SCOPUS_API_KEY environment variable
"""

import os
import sys
from typing import Optional
from fastmcp import FastMCP

# Add parent directory to path for fallback_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fallback_utils import (
    web_search_fallback,
    enrich_result,
    enrich_results_list,
    get_api_key,
    handle_http_error,
)

mcp = FastMCP("scopus-search")

SCOPUS_API_BASE = "https://api.elsevier.com/content"


@mcp.tool()
async def search_scopus(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    year_range: Optional[str] = None,
) -> list[dict]:
    """
    Search Scopus for academic papers.

    Args:
        query: Search query string
        max_results: Maximum results (default 10, max 25)
        sort_by: Sort by "relevance" or "citedby"
        year_range: Publication year range (e.g., "2020-2024")

    Returns:
        List of paper dictionaries with metadata
    """
    api_key = get_api_key("SCOPUS_API_KEY")

    if not api_key:
        return await web_search_fallback(query, "scopus", max_results)

    try:
        import httpx

        headers = {
            "X-ELS-APIKey": api_key,
            "Accept": "application/json"
        }

        params = {
            "query": query,
            "count": min(max_results, 25),
            "sort": sort_by,
        }

        if year_range:
            params["date"] = year_range

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SCOPUS_API_BASE}/search/scopus",
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("search-results", {}).get("entry", [])

                papers = []
                for entry in results:
                    # Skip count entries
                    if "opensearch:totalResults" in entry:
                        continue

                    paper = {
                        "title": entry.get("dc:title", "Unknown Title"),
                        "authors": _extract_authors(entry),
                        "abstract": entry.get("dc:description", ""),
                        "doi": entry.get("prism:doi"),
                        "url": entry.get("prism:url"),
                        "publication_date": entry.get("prism:coverDate"),
                        "citation_count": int(entry.get("citedby-count", 0)),
                        "source": entry.get("prism:publicationName"),
                        "volume": entry.get("prism:volume"),
                        "issue": entry.get("prism:issueIdentifier"),
                        "pages": entry.get("prism:pageRange"),
                        "_metadata": {
                            "mcp_name": "scopus",
                            "method": "api",
                            "weblink": entry.get("link", [{}])[0].get("@href", ""),
                        }
                    }
                    papers.append(paper)

                return papers
            else:
                error_msg = handle_http_error(response.status_code, "Scopus")
                return await web_search_fallback(query, "scopus", max_results)

    except Exception as e:
        print(f"Scopus API error: {e}", file=sys.stderr)
        return await web_search_fallback(query, "scopus", max_results)


def _extract_authors(entry: dict) -> list[str]:
    """Extract author names from Scopus entry."""
    creators = entry.get("dc:creator", [])
    if isinstance(creators, dict):
        creators = [creators]

    authors = []
    for creator in creators:
        if isinstance(creator, dict):
            name = f"{creator.get('ce:given-name', '')} {creator.get('ce:surname', '')}".strip()
            if name:
                authors.append(name)

    return authors if authors else ["Unknown"]


@mcp.tool()
async def get_scopus_details(
    scopus_id: str,
) -> dict:
    """
    Get detailed information about a specific Scopus paper.

    Args:
        scopus_id: Scopus article ID (e.g., "000027045100005")

    Returns:
        Detailed paper information
    """
    api_key = get_api_key("SCOPUS_API_KEY")

    if not api_key:
        return {"error": "SCOPUS_API_KEY not configured"}

    try:
        import httpx

        headers = {
            "X-ELS-APIKey": api_key,
            "Accept": "application/json"
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SCOPUS_API_BASE}/abstract/scopus_id/{scopus_id}",
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                entry = data.get("abstract-retrieval-response", {}).get("coredata", {})

                paper = {
                    "title": entry.get("dc:title", "Unknown Title"),
                    "authors": _extract_authors(entry),
                    "abstract": entry.get("dc:description", ""),
                    "doi": entry.get("prism:doi"),
                    "url": entry.get("prism:url"),
                    "publication_date": entry.get("prism:coverDate"),
                    "source": entry.get("prism:publicationName"),
                    "volume": entry.get("prism:volume"),
                    "issue": entry.get("prism:issueIdentifier"),
                    "pages": entry.get("prism:pageRange"),
                    "citation_count": int(entry.get("citedby-count", 0)),
                    "_metadata": {
                        "mcp_name": "scopus",
                        "method": "api",
                        "weblink": entry.get("prism:url", ""),
                    }
                }

                return paper
            else:
                return {"error": f"Paper not found: {scopus_id}"}

    except Exception as e:
        return {"error": f"Scopus API error: {str(e)}"}


if __name__ == "__main__":
    mcp.run()
