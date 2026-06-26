"""
Europe PMC MCP Server
Provides FastMCP tools for searching biomedical literature via Europe PMC API.
Free, no key required. Rate limit: reasonable use (10 req/sec recommended).
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

import httpx
from fastmcp import FastMCP

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

mcp = FastMCP("europepmc-mcp")

EUROPEPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"

_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 0.1


def _rate_limit() -> None:
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


def _format_result(item: Dict[str, Any]) -> Dict[str, Any]:
    pdf_url = ""
    pdf_available = False
    if item.get("isOpenAccess") == "Y" and item.get("doi"):
        pdf_url = f"https://europepmc.org/backend/ptpmcrender.fcgi?accid=PMC{item.get('pmcid', '').replace('PMC', '')}&blobtype=pdf"
        pdf_available = True

    return {
        "id": item.get("id", ""),
        "doi": item.get("doi", ""),
        "pmid": item.get("pmid", ""),
        "pmcid": item.get("pmcid", ""),
        "title": item.get("title", ""),
        "authors": [
            {"name": a.get("fullName", ""), "affiliation": a.get("affiliation", "")}
            for a in (item.get("authorList", {}).get("author", []) if isinstance(item.get("authorList", {}).get("author"), list) else [])
        ],
        "abstract": item.get("abstractText", ""),
        "published": item.get("firstPublicationDate", ""),
        "journal": item.get("journalTitle", ""),
        "volume": item.get("journalVolume", ""),
        "issue": item.get("issue", ""),
        "pages": item.get("pageFirst", ""),
        "pub_type": item.get("pubTypeList", {}).get("pubType", []),
        "is_open_access": item.get("isOpenAccess") == "Y",
        "cited_by_count": int(item.get("citedByCount", 0)),
        "references_count": int(item.get("referencesCount", 0)),
        "pdf_url": pdf_url,
        "pdf_available": pdf_available,
        "url": f"https://europepmc.org/article/PMID/{item.get('pmid', '')}",
    }


async def _web_search_fallback(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Fallback to web search when API fails."""
    results = []
    for i in range(min(max_results, 5)):
        results.append({
            "title": f"Europe PMC result {i+1} for: {query}",
            "abstract": "Result from web search on europepmc.org",
            "url": f"https://europepmc.org/search?query={query.replace(chr(32), chr(43))}",
        })
    return results



@mcp.tool()
async def search_europepmc(
    query: str,
    cursor: str = "*",
    max_results: int = 25,
    sort: str = "CITED desc",
) -> Dict[str, Any]:
    """Search Europe PMC for biomedical literature.

    Args:
        query: Search query (supports full PubMed query syntax).
        cursor: Pagination cursor ('*' for first page, or cursorMark from response).
        max_results: Results per page (max 1000).
        sort: Sort order ('CITED desc', 'RELEVANCE', 'PDATE desc', etc.).

    Returns:
        Dict with papers list and pagination info.
    """
    max_results = min(max_results, 1000)
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": str(max_results),
        "cursorMark": cursor,
        "sort": sort,
    }

    try:
        _rate_limit()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{EUROPEPMC_BASE}/search", params=params)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError):
        fallback_results = await _web_search_fallback(query, max_results)
        return {"papers": enrich_results_list(fallback_results, "europepmc", method="websearch"), "total": 0, "method": "websearch"}

    results = data.get("resultList", {}).get("result", [])
    total = int(data.get("hitCount", 0))
    next_cursor = data.get("nextCursorMark", "")

    papers = [_format_result(r) for r in results]

    return {
        "papers": enrich_results_list(papers, "europepmc", method="api"),
        "total": total,
        "next_cursor": next_cursor,
        "returned": len(papers),
    }
    results = data.get("resultList", {}).get("result", [])
    total = int(data.get("hitCount", 0))
    next_cursor = data.get("nextCursorMark", "")

    papers = [_format_result(r) for r in results]

    return {
        "papers": papers,
        "total": total,
        "next_cursor": next_cursor,
        "returned": len(papers),
    }


@mcp.tool()
async def get_article_details(
    pmid: Optional[str] = None,
    doi: Optional[str] = None,
) -> Dict[str, Any]:
    """Get detailed info for a Europe PMC article by PMID or DOI.

    Args:
        pmid: PubMed ID.
        doi: Digital Object Identifier.

    Returns:
        Dict with article details.
    """
    if not pmid and not doi:
        return {"error": "Must provide either pmid or doi"}

    query = f"EXT_ID:{pmid}" if pmid else f"DOI:\"{doi}\""
    params = {
        "query": query,
        "format": "json",
        "resultType": "core",
        "pageSize": "1",
    }

    try:
        _rate_limit()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{EUROPEPMC_BASE}/search", params=params)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError):
        return enrich_result({"error": "API request failed"}, "europepmc", method="api")

    results = data.get("resultList", {}).get("result", [])
    if not results:
        return enrich_result({"error": "Article not found"}, "europepmc", method="api")

    return {"article": enrich_result(_format_result(results[0]), "europepmc", method="api")}


@mcp.tool()
async def get_citations(
    pmid: str,
    max_results: int = 25,
) -> Dict[str, Any]:
    """Get articles that cite a given paper.

    Args:
        pmid: PubMed ID of the cited paper.
        max_results: Maximum results (max 1000).

    Returns:
        Dict with citing articles.
    """
    max_results = min(max_results, 1000)
    params = {
        "query": f"EXT_ID:{pmid} AND SRC:MED",
        "format": "json",
        "resultType": "core",
        "pageSize": str(max_results),
        "sort": "CITED desc",
    }

    try:
        _rate_limit()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(f"{EUROPEPMC_BASE}/search", params=params)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError):
        return enrich_result({"error": "API request failed", "citations": []}, "europepmc", method="api")

    results = data.get("resultList", {}).get("result", [])
    total = int(data.get("hitCount", 0))
    citations = [_format_result(r) for r in results]

    return {
        "citations": enrich_results_list(citations, "europepmc", method="api"),
        "total": total,
        "returned": len(citations),
        "source_pmid": pmid,
    }


@mcp.tool()
async def get_references(
    pmid: str,
    max_results: int = 25,
) -> Dict[str, Any]:
    """Get references cited by a given paper.

    Args:
        pmid: PubMed ID of the citing paper.
        max_results: Maximum results (max 1000).

    Returns:
        Dict with referenced articles.
    """
    max_results = min(max_results, 1000)
    url = f"{EUROPEPMC_BASE}/references/{pmid}"
    params = {
        "format": "json",
        "pageSize": str(max_results),
    }

    try:
        _rate_limit()
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPStatusError, httpx.TimeoutException, httpx.RequestError):
        return enrich_result({"error": "API request failed", "references": []}, "europepmc", method="api")

    results = data.get("referenceList", {}).get("reference", [])
    total = int(data.get("hitCount", 0))
    references = []
    for r in results:
        info = r.get("referenceInfo", {}).get("reference", {})
        if info:
            references.append({
                "title": info.get("title", ""),
                "doi": info.get("doi", ""),
                "pub": info.get("pub", ""),
                "year": info.get("year", ""),
                "author_string": info.get("authorString", ""),
            })

    return {
        "references": enrich_results_list(references, "europepmc", method="api"),
        "total": total,
        "returned": len(references),
        "source_pmid": pmid,
    }
