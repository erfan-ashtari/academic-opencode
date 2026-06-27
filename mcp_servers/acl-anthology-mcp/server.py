"""
ACL Anthology MCP Server

Integration with the ACL Anthology for NLP/Computational Linguistics papers.
Covers ACL, EMNLP, NAACL, COLING, and other top NLP venues.

No API key required - uses public API.
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
)

mcp = FastMCP("acl-anthology-search")

ACL_ANTHOLOGY_API = "https://api.aclanthology.org"

# Venue mappings
VENUE_MAP = {
    "acl": "ACL",
    "emnlp": "EMNLP",
    "naacl": "NAACL",
    "naacl-hlt": "NAACL-HLT",
    "coling": "COLING",
    "eacl": "EACL",
    "semeval": "SemEval",
    "conll": "CoNLL",
    "wnlp": "WNLP",
    "bioNLP": "BioNLP",
}


@mcp.tool()
async def search_acl_anthology(
    query: str,
    max_results: int = 10,
    venue: Optional[str] = None,
    year: Optional[int] = None,
) -> list[dict]:
    """
    Search ACL Anthology for NLP/CL papers.

    Args:
        query: Search query string
        max_results: Maximum results (default 10)
        venue: Filter by venue (acl, emnlp, naacl, coling, etc.)
        year: Filter by year

    Returns:
        List of paper dictionaries with metadata
    """
    try:
        import httpx

        params = {
            "q": query,
            "rows": max_results,
        }

        if venue:
            venue_upper = VENUE_MAP.get(venue.lower(), venue.upper())
            params["venue"] = venue_upper

        if year:
            params["year"] = year

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ACL_ANTHOLOGY_API}/search",
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("hits", [])

                papers = []
                for hit in results:
                    paper = {
                        "title": hit.get("title", "Unknown Title"),
                        "authors": [a.get("name", "Unknown") for a in hit.get("authors", [])],
                        "abstract": hit.get("abstract", ""),
                        "doi": hit.get("doi"),
                        "url": hit.get("url", ""),
                        "publication_date": hit.get("date"),
                        "venue": hit.get("venue", ""),
                        "citation_count": hit.get("citedby", 0),
                        "biblio": hit.get("biblio", {}),
                        "_metadata": {
                            "mcp_name": "acl-anthology",
                            "method": "api",
                            "weblink": hit.get("url", ""),
                        }
                    }
                    papers.append(paper)

                return papers
            else:
                return await web_search_fallback(query, "acl-anthology", max_results)

    except Exception as e:
        print(f"ACL Anthology API error: {e}", file=sys.stderr)
        return await web_search_fallback(query, "acl-anthology", max_results)


@mcp.tool()
async def get_acl_paper_details(
    paper_id: str,
) -> dict:
    """
    Get detailed information about a specific ACL Anthology paper.

    Args:
        paper_id: ACL Anthology paper ID (e.g., "P17-1001")

    Returns:
        Detailed paper information
    """
    try:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ACL_ANTHOLOGY_API}/paper/{paper_id}",
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                paper = {
                    "title": data.get("title", "Unknown Title"),
                    "authors": [a.get("name", "Unknown") for a in data.get("authors", [])],
                    "abstract": data.get("abstract", ""),
                    "doi": data.get("doi"),
                    "url": data.get("url", ""),
                    "publication_date": data.get("date"),
                    "venue": data.get("venue", ""),
                    "citation_count": data.get("citedby", 0),
                    "biblio": data.get("biblio", {}),
                    "_metadata": {
                        "mcp_name": "acl-anthology",
                        "method": "api",
                        "weblink": data.get("url", ""),
                    }
                }

                return paper
            else:
                return {"error": f"Paper not found: {paper_id}"}

    except Exception as e:
        return {"error": f"ACL Anthology API error: {str(e)}"}


@mcp.tool()
async def search_acl_by_venue(
    venue: str,
    year: Optional[int] = None,
    max_results: int = 10,
) -> list[dict]:
    """
    Search papers from a specific ACL venue.

    Args:
        venue: Venue name (acl, emnlp, naacl, coling, etc.)
        year: Filter by year
        max_results: Maximum results (default 10)

    Returns:
        List of paper dictionaries
    """
    try:
        import httpx

        venue_upper = VENUE_MAP.get(venue.lower(), venue.upper())

        params = {
            "venue": venue_upper,
            "rows": max_results,
        }

        if year:
            params["year"] = year

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ACL_ANTHOLOGY_API}/search",
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()
                results = data.get("hits", [])

                papers = []
                for hit in results:
                    paper = {
                        "title": hit.get("title", "Unknown Title"),
                        "authors": [a.get("name", "Unknown") for a in hit.get("authors", [])],
                        "abstract": hit.get("abstract", ""),
                        "doi": hit.get("doi"),
                        "url": hit.get("url", ""),
                        "publication_date": hit.get("date"),
                        "venue": hit.get("venue", ""),
                        "citation_count": hit.get("citedby", 0),
                        "_metadata": {
                            "mcp_name": "acl-anthology",
                            "method": "api",
                            "weblink": hit.get("url", ""),
                        }
                    }
                    papers.append(paper)

                return papers
            else:
                return await web_search_fallback(f"{venue} papers", "acl-anthology", max_results)

    except Exception as e:
        print(f"ACL Anthology API error: {e}", file=sys.stderr)
        return await web_search_fallback(f"{venue} papers", "acl-anthology", max_results)


if __name__ == "__main__":
    mcp.run()
