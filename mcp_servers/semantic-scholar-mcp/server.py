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
from typing import Optional
import os

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
            return [_paper_to_dict(p) for p in results.items]

        # Single Paper returned (match_title=True edge case)
        return [_paper_to_dict(results)]

    except ObjectNotFoundException:
        return []
    except BadQueryParametersException as e:
        return [{"error": f"Invalid query parameters: {e}"}]
    except SemanticScholarException as e:
        return [{"error": f"Semantic Scholar API error: {e}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {e}"}]


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
        return _paper_to_dict(paper)

    except ObjectNotFoundException:
        return {"error": f"Paper not found: {paper_id}"}
    except BadQueryParametersException as e:
        return {"error": f"Invalid paper ID: {e}"}
    except SemanticScholarException as e:
        return {"error": f"Semantic Scholar API error: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}


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

        return [item.raw_data for item in results.items]

    except ObjectNotFoundException:
        return []
    except BadQueryParametersException as e:
        return [{"error": f"Invalid paper ID: {e}"}]
    except SemanticScholarException as e:
        return [{"error": f"Semantic Scholar API error: {e}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {e}"}]


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

        return [item.raw_data for item in results.items]

    except ObjectNotFoundException:
        return []
    except BadQueryParametersException as e:
        return [{"error": f"Invalid paper ID: {e}"}]
    except SemanticScholarException as e:
        return [{"error": f"Semantic Scholar API error: {e}"}]
    except Exception as e:
        return [{"error": f"Unexpected error: {e}"}]


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    mcp.run()
