"""
Google Scholar MCP Server
Provides FastMCP tools for searching Google Scholar via the scholarly library.

WARNING: Google Scholar results may be incomplete and need human review.
This uses an unofficial API. Rate limits may apply. Use at your own risk.
"""

from __future__ import annotations

import asyncio
import time
from typing import Any, Dict, List, Optional

from fastmcp import FastMCP

mcp = FastMCP("google-scholar-mcp")

_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 5.0  # Conservative: 1 req per 5 seconds

SCHOLAR_WARNING = (
    "⚠️ GOOGLE SCHOLAR WARNING: Results may be incomplete, outdated, or inaccurate. "
    "Google Scholar uses an unofficial API that may block automated access. "
    "Always verify results with official academic databases."
)


def _rate_limit() -> None:
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


def _format_paper(paper: Any) -> Dict[str, Any]:
    """Convert a scholarly paper object to a serializable dict."""
    bib = getattr(paper, "bib", {}) or {}
    bib_dict = dict(bib) if bib else {}

    return {
        "title": bib_dict.get("title", getattr(paper, "title", "")),
        "authors": bib_dict.get("author", []) if isinstance(bib_dict.get("author"), list) else [bib_dict.get("author", "")],
        "abstract": bib_dict.get("abstract", ""),
        "year": bib_dict.get("pub_year", ""),
        "venue": bib_dict.get("venue", ""),
        "journal": bib_dict.get("journal", ""),
        "citations": getattr(paper, "num_citations", 0),
        "url": getattr(paper, "url", ""),
        "eprint_url": getattr(paper, "eprint_url", ""),
        "pdf_url": getattr(paper, "eprint_url", ""),
        "pdf_available": bool(getattr(paper, "eprint_url", "")),
        "source": "Google Scholar",
    }


@mcp.tool()
async def search_google_scholar(
    query: str,
    max_results: int = 10,
    year_low: Optional[int] = None,
    year_high: Optional[int] = None,
) -> Dict[str, Any]:
    """Search Google Scholar for academic papers.

    Args:
        query: Search query.
        max_results: Maximum results to return (max 20 recommended).
        year_low: Minimum publication year filter.
        year_high: Maximum publication year filter.

    Returns:
        Dict with papers and warning about result reliability.
    """
    try:
        from scholarly import scholarly
    except ImportError:
        return {
            "error": "scholarly library not installed. Run: pip install scholarly",
            "papers": [],
        }

    max_results = min(max_results, 20)
    papers = []

    try:
        _rate_limit()
        search_query = scholarly.search_pubs(query)

        for i, result in enumerate(search_query):
            if i >= max_results:
                break

            # Apply year filters
            if year_low or year_high:
                year = int(result.get("bib", {}).get("pub_year", 0) or 0)
                if year_low and year < year_low:
                    continue
                if year_high and year > year_high:
                    continue

            papers.append(_format_paper(result))

    except StopIteration:
        pass  # No more results
    except Exception as e:
        error_msg = str(e)
        if "429" in error_msg or "captcha" in error_msg.lower():
            return {
                "error": "Rate limited by Google Scholar. Try again later or use fewer requests.",
                "papers": [],
                "warning": SCHOLAR_WARNING,
            }
        return {"error": error_msg, "papers": [], "warning": SCHOLAR_WARNING}

    return {
        "papers": papers,
        "total": len(papers),
        "returned": len(papers),
        "warning": SCHOLAR_WARNING,
        "query": query,
    }


@mcp.tool()
async def get_paper_details(paper_url: str) -> Dict[str, Any]:
    """Get detailed info for a specific paper by Google Scholar URL.

    Args:
        paper_url: Google Scholar URL of the paper.

    Returns:
        Dict with paper details.
    """
    try:
        from scholarly import scholarly
    except ImportError:
        return {"error": "scholarly library not installed. Run: pip install scholarly"}

    try:
        _rate_limit()
        result = scholarly.search_single_article(paper_url)
        paper = _format_paper(result)

        return {"article": paper, "warning": SCHOLAR_WARNING}
    except Exception as e:
        return {"error": str(e), "warning": SCHOLAR_WARNING}


@mcp.tool()
async def get_author_papers(
    author_name: str,
    max_results: int = 10,
) -> Dict[str, Any]:
    """Get papers by a specific author from Google Scholar.

    Args:
        author_name: Name of the author to search for.
        max_results: Maximum results (max 20 recommended).

    Returns:
        Dict with author info and their papers.
    """
    try:
        from scholarly import scholarly
    except ImportError:
        return {"error": "scholarly library not installed. Run: pip install scholarly"}

    max_results = min(max_results, 20)

    try:
        _rate_limit()
        author = scholarly.search_author(author_name)
        if not author:
            return {"error": f"Author not found: {author_name}", "papers": []}

        scholarly.fill(author)
        publications = author.get("publications", [])

        papers = []
        for pub in publications[:max_results]:
            bib = pub.get("bib", {})
            papers.append({
                "title": bib.get("title", ""),
                "year": bib.get("pub_year", ""),
                "venue": bib.get("venue", ""),
                "citations": pub.get("num_citations", 0),
            })

        return {
            "author": {
                "name": author.get("name", ""),
                "affiliation": author.get("affiliation", ""),
                "scholar_id": author.get("scholar_id", ""),
                "h_index": author.get("hindex", 0),
                "citations": author.get("citedby", 0),
            },
            "papers": papers,
            "returned": len(papers),
            "warning": SCHOLAR_WARNING,
        }
    except Exception as e:
        return {"error": str(e), "papers": [], "warning": SCHOLAR_WARNING}
