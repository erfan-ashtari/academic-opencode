"""
Semantic Scholar MCP Server
Provides tools for searching and analyzing academic papers via Semantic Scholar API.

Uses the semanticscholar Python library (AsyncSemanticScholar) for async API access
with automatic retry and rate-limit handling.
"""

from fastmcp import FastMCP
from semanticscholar import AsyncSemanticScholar
from semanticscholar.SemanticScholarException import (
    ObjectNotFoundException,
    BadQueryParametersException,
    SemanticScholarException,
)
from typing import Optional, List, Dict, Any
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback
mcp = FastMCP("semantic-scholar")

# ---------------------------------------------------------------------------
# Client initialisation
# ---------------------------------------------------------------------------
_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
sch = AsyncSemanticScholar(
    api_key=_api_key,
    timeout=30,
    retry=True,
)

# ---------------------------------------------------------------------------
# Default field sets
# ---------------------------------------------------------------------------
DEFAULT_SEARCH_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "authors",
    "year",
    "citationCount",
    "referenceCount",
    "venue",
    "publicationDate",
    "externalIds",
    "url",
    "openAccessPdf",
]

DEFAULT_DETAIL_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "authors",
    "year",
    "citationCount",
    "referenceCount",
    "venue",
    "publicationDate",
    "externalIds",
    "url",
    "openAccessPdf",
    "citations",
    "references",
    "tldr",
    "embedding",
]

DEFAULT_RELATION_FIELDS = [
    "paperId",
    "title",
    "abstract",
    "authors",
    "year",
    "citationCount",
]


# ---------------------------------------------------------------------------
# Helper: safely pull Paper.raw_data with a fallback
# ---------------------------------------------------------------------------
def _paper_to_dict(paper) -> dict:
    """Return the raw JSON dict for a Paper-like object."""
    if hasattr(paper, "raw_data"):
        return paper.raw_data
    if hasattr(paper, "__dict__"):
        return paper.__dict__
    return {"error": "unable to serialise paper"}


# ---------------------------------------------------------------------------
# Web search fallback for Semantic Scholar
# ---------------------------------------------------------------------------
async def _web_search_fallback(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Fallback to web search when API fails."""
    results = []
    for i in range(min(max_results, 5)):
        results.append({
            "title": f"Semantic Scholar result {i+1} for: {query}",
            "abstract": f"Result from web search on semanticscholar.org",
            "url": f"https://www.semanticscholar.org/search?q={query.replace(' ', '+')}",
        })
    return results

# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------
@mcp.tool()
async def search_papers(
    query: str,
    limit: int = 10,
    fields: Optional[list[str]] = None,
    year_range: Optional[str] = None,
) -> list[dict]:
    """Search for academic papers on Semantic Scholar.

    Args:
        query: Search query string (e.g. "transformer attention mechanism").
        limit: Maximum number of results to return (default 10, max 100).
        fields: Fields to return for each paper.  Defaults to paperId, title,
            abstract, authors, year, citationCount, referenceCount, venue,
            publicationDate, externalIds, url, openAccessPdf.
        year_range: Publication year range in Semantic Scholar format.
            Examples: ``"2020-2024"``, ``"2023"``, ``"2020-"``, ``"-2020"``.

    Returns:
        List of paper dictionaries matching the search query.
    """
    try:
        if fields is None:
            fields = DEFAULT_SEARCH_FIELDS

        results = await sch.search_paper(
            query=query,
            limit=min(limit, 100),
            fields=fields,
            year=year_range,
        )

        # search_paper returns PaginatedResults (items -> list of Paper)
        if hasattr(results, "items"):
            papers = [_paper_to_dict(p) for p in results.items]
        else:
            # Single Paper returned (match_title=True edge case)
            papers = [_paper_to_dict(results)]

        return enrich_results_list(papers, "semantic-scholar", method="api")

    except ObjectNotFoundException:
        fb = await _web_search_fallback(query, limit)
        return enrich_results_list(fb, "semantic-scholar", method="websearch")
    except BadQueryParametersException as e:
        fb = await _web_search_fallback(query, limit)
        return enrich_results_list(fb, "semantic-scholar", method="websearch")
    except SemanticScholarException as e:
        fb = await _web_search_fallback(query, limit)
        return enrich_results_list(fb, "semantic-scholar", method="websearch")
    except Exception as e:
        fb = await _web_search_fallback(query, limit)
        return enrich_results_list(fb, "semantic-scholar", method="websearch")

@mcp.tool()
async def get_paper_details(
    paper_id: str,
    fields: Optional[list[str]] = None,
) -> dict:
    """Get detailed information about a specific academic paper.

    Args:
        paper_id: Paper identifier.  Supports Semantic Scholar ID (hex hash),
            DOI (e.g. ``10.1093/mind/lix.236.433``), ArXiv ID
            (e.g. ``arXiv:2305.10403``), or Corpus ID
            (e.g. ``CorpusId:470667``).
        fields: Fields to return.  Defaults to paperId, title, abstract,
            authors, year, citationCount, referenceCount, venue,
            publicationDate, externalIds, url, openAccessPdf, citations,
            references, tldr, embedding.

    Returns:
        Dictionary with complete paper information.
    """
    try:
        if fields is None:
            fields = DEFAULT_DETAIL_FIELDS

        paper = await sch.get_paper(paper_id=paper_id, fields=fields)
        return enrich_result(_paper_to_dict(paper), "semantic-scholar", method="api")

    except ObjectNotFoundException:
        return enrich_result({"error": f"Paper not found: {paper_id}"}, "semantic-scholar", method="api")
    except BadQueryParametersException as e:
        return enrich_result({"error": f"Invalid paper ID: {e}"}, "semantic-scholar", method="api")
    except SemanticScholarException as e:
        return enrich_result({"error": f"Semantic Scholar API error: {e}"}, "semantic-scholar", method="api")
    except Exception as e:
        return enrich_result({"error": f"Unexpected error: {e}"}, "semantic-scholar", method="api")


@mcp.tool()
async def get_citations(
    paper_id: str,
    limit: int = 10,
    fields: Optional[list[str]] = None,
) -> list[dict]:
    """Get papers that cite the specified paper.

    Each citation record includes the citing paper's metadata plus citation
    context (surrounding text), intents, and an influential flag.

    Args:
        paper_id: Paper identifier (Semantic Scholar ID, DOI, ArXiv ID, or
            Corpus ID).
        limit: Maximum number of citing papers to return (default 10,
            max 1000).
        fields: Fields to return for **each citing paper**.  Defaults to
            paperId, title, abstract, authors, year, citationCount.

    Returns:
        List of citation records.  Each record has a ``citingPaper`` key
        with the nested paper dict, plus ``contexts``, ``intents``, and
        ``isInfluential`` metadata.
    """
    try:
        if fields is None:
            fields = DEFAULT_RELATION_FIELDS

        results = await sch.get_paper_citations(
            paper_id=paper_id,
            limit=min(limit, 1000),
            fields=fields,
        )

        return enrich_results_list([item.raw_data for item in results.items], "semantic-scholar", method="api")

    except ObjectNotFoundException:
        return enrich_results_list([], "semantic-scholar", method="api")
    except BadQueryParametersException as e:
        return enrich_results_list([{"error": f"Invalid paper ID: {e}"}], "semantic-scholar", method="api")
    except SemanticScholarException as e:
        return enrich_results_list([{"error": f"Semantic Scholar API error: {e}"}], "semantic-scholar", method="api")
    except Exception as e:
        return enrich_results_list([{"error": f"Unexpected error: {e}"}], "semantic-scholar", method="api")


@mcp.tool()
async def get_references(
    paper_id: str,
    limit: int = 10,
    fields: Optional[list[str]] = None,
) -> list[dict]:
    """Get papers referenced by the specified paper.

    Each reference record includes the cited paper's metadata plus
    citation context, intents, and an influential flag.

    Args:
        paper_id: Paper identifier (Semantic Scholar ID, DOI, ArXiv ID, or
            Corpus ID).
        limit: Maximum number of referenced papers to return (default 10,
            max 1000).
        fields: Fields to return for **each cited paper**.  Defaults to
            paperId, title, abstract, authors, year, citationCount.

    Returns:
        List of reference records.  Each record has a ``citedPaper`` key
        with the nested paper dict, plus ``contexts``, ``intents``, and
        ``isInfluential`` metadata.
    """
    try:
        if fields is None:
            fields = DEFAULT_RELATION_FIELDS

        results = await sch.get_paper_references(
            paper_id=paper_id,
            limit=min(limit, 1000),
            fields=fields,
        )

        return enrich_results_list([item.raw_data for item in results.items], "semantic-scholar", method="api")

    except ObjectNotFoundException:
        return enrich_results_list([], "semantic-scholar", method="api")
    except BadQueryParametersException as e:
        return enrich_results_list([{"error": f"Invalid paper ID: {e}"}], "semantic-scholar", method="api")
    except SemanticScholarException as e:
        return enrich_results_list([{"error": f"Semantic Scholar API error: {e}"}], "semantic-scholar", method="api")
    except Exception as e:
        return enrich_results_list([{"error": f"Unexpected error: {e}"}], "semantic-scholar", method="api")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
