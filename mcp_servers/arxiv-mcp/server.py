"""
arXiv MCP Server
Provides FastMCP tools for searching and retrieving academic papers from arXiv.
"""

from __future__ import annotations

import asyncio
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

import arxiv
from fastmcp import FastMCP

mcp = FastMCP("arxiv-search")

# Rate limiting: arXiv allows ~3 requests per second.
# Use a conservative 0.4s interval (~2.5 req/s) to stay safe.
_RATE_LIMIT_INTERVAL = 0.4
_last_request_time: float = 0.0
_lock = asyncio.Lock()


def _extract_arxiv_id(url_or_id: str) -> str:
    """Extract the arXiv ID from a URL or raw ID string.

    Handles these formats:
      - ``2301.07041``
      - ``http://arxiv.org/abs/2301.07041v2``
      - ``https://arxiv.org/pdf/2301.07041.pdf``
      - ``2301.07041v2``
    """
    # Try to match from URL first
    match = re.search(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv:)(\d{4}\.\d{4,5}(?:v\d+)?)", url_or_id)
    if match:
        return match.group(1)
    # Assume it's a raw ID
    return url_or_id.strip()


def _format_arxiv_paper(result: arxiv.Result) -> Dict[str, Any]:
    """Convert an arxiv.Result into a serialisable dictionary."""
    return {
        "id": result.entry_id,
        "arxiv_id": result.get_short_id(),
        "title": result.title,
        "authors": [a.name for a in result.authors],
        "abstract": result.summary,
        "published": result.published.isoformat() if result.published else None,
        "updated": result.updated.isoformat() if result.updated else None,
        "categories": list(result.categories),
        "pdf_url": result.pdf_url,
        "url": result.entry_id,
        "doi": result.doi,
        "journal_ref": result.journal_ref,
        "comment": result.comment,
        "primary_category": result.primary_category,
        "links": [link.href for link in result.links],
    }


async def _rate_limited_search(search: arxiv.Search, max_results: int) -> List[arxiv.Result]:
    """Execute an arXiv search respecting rate limits."""
    global _last_request_time
    async with _lock:
        now = datetime.now().timestamp()
        elapsed = now - _last_request_time
        if elapsed < _RATE_LIMIT_INTERVAL:
            await asyncio.sleep(_RATE_LIMIT_INTERVAL - elapsed)
        _last_request_time = datetime.now().timestamp()

    client = arxiv.Client(page_size=min(max_results, 100))
    return list(client.results(search))


@mcp.tool()
async def search_arxiv(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    sort_order: str = "descending",
    categories: Optional[List[str]] = None,
) -> List[Dict[str, Any]]:
    """Search arXiv for papers matching the given query.

    Args:
        query: Search query string (supports arXiv search syntax like ``au:`` or ``ti:``).
        max_results: Maximum number of results to return (default: 10, max: 100).
        sort_by: Sort criterion — ``"relevance"``, ``"lastUpdatedDate"``, or ``"submittedDate"``.
        sort_order: Sort order — ``"ascending"`` or ``"descending"``.
        categories: Optional list of arXiv category IDs to narrow results
            (e.g. ``["cs.AI", "cs.CL"]``).  When provided the query is prefixed
            with ``cat:(cat1 OR cat2 OR ...) AND`` so only papers from those
            categories are returned.

    Returns:
        A list of paper dictionaries with metadata (id, title, authors, abstract,
        published date, categories, pdf_url, doi, etc.).
    """
    sort_mapping = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }

    order_mapping = {
        "ascending": arxiv.SortOrder.Ascending,
        "descending": arxiv.SortOrder.Descending,
    }

    effective_query = query
    if categories:
        cat_filter = " OR ".join(f"cat:{c}" for c in categories)
        effective_query = f"({cat_filter}) AND ({query})"

    search = arxiv.Search(
        query=effective_query,
        max_results=min(max_results, 100),
        sort_by=sort_mapping.get(sort_by, arxiv.SortCriterion.Relevance),
        sort_order=order_mapping.get(sort_order, arxiv.SortOrder.Descending),
    )

    try:
        results = await _rate_limited_search(search, max_results)
        return [_format_arxiv_paper(r) for r in results]
    except arxiv.HTTPError as e:
        return [{"error": f"arXiv API error: {e}"}]
    except Exception as e:
        return [{"error": f"Search failed: {e}"}]


@mcp.tool()
async def get_paper_details(arxiv_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific arXiv paper.

    Args:
        arxiv_id: The arXiv paper ID — accepts bare IDs (``"2301.07041"``),
            full URLs (``"https://arxiv.org/abs/2301.07041"``), or versioned
            IDs (``"2301.07041v2"``).

    Returns:
        A dictionary with full paper metadata.  If the paper is not found
        the dictionary contains an ``"error"`` key.
    """
    paper_id = _extract_arxiv_id(arxiv_id)

    search = arxiv.Search(id_list=[paper_id], max_results=1)

    try:
        results = await _rate_limited_search(search, 1)
        for r in results:
            return _format_arxiv_paper(r)
        return {"error": f"Paper not found: {arxiv_id}"}
    except arxiv.HTTPError as e:
        return {"error": f"arXiv API error: {e}"}
    except Exception as e:
        return {"error": f"Failed to retrieve paper: {e}"}


@mcp.tool()
async def get_recent_papers(
    categories: List[str],
    max_results: int = 20,
) -> List[Dict[str, Any]]:
    """Get recently submitted papers from the specified arXiv categories.

    Args:
        categories: List of arXiv category IDs (e.g. ``["cs.AI", "cs.CL"]``).
        max_results: Maximum number of results to return (default: 20, max: 100).

    Returns:
        A list of recent paper dictionaries with key metadata.
    """
    query = " OR ".join(f"cat:{c}" for c in categories)

    search = arxiv.Search(
        query=query,
        max_results=min(max_results, 100),
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    try:
        results = await _rate_limited_search(search, max_results)
        papers = []
        for r in results:
            paper = _format_arxiv_paper(r)
            # Truncate abstract for listing view
            if paper["abstract"] and len(paper["abstract"]) > 500:
                paper["abstract"] = paper["abstract"][:500] + "..."
            papers.append(paper)
        return papers
    except arxiv.HTTPError as e:
        return [{"error": f"arXiv API error: {e}"}]
    except Exception as e:
        return [{"error": f"Failed to fetch recent papers: {e}"}]


if __name__ == "__main__":
    mcp.run()
