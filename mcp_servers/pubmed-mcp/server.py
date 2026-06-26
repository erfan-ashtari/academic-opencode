"""
PubMed MCP Server
Provides tools for searching biomedical literature via NCBI E-utilities API.
Implements rate limiting (3 req/sec max) and proper error handling.
"""

import time
from typing import Any, Dict, List, Optional
from xml.etree import ElementTree as ET

import httpx
from fastmcp import FastMCP

mcp = FastMCP("pubmed-mcp")

PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# Rate limiting: NCBI allows max 3 requests per second without an API key
_last_request_time: float = 0.0
_MIN_REQUEST_INTERVAL: float = 1.0 / 3.0

SORT_MAP: Dict[str, str] = {
    "relevance": "relevance",
    "date": "pub_date",
    "pub_date": "pub_date",
}


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------


def _rate_limit() -> None:
    """Enforce NCBI rate limit of 3 requests per second (shared global state)."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < _MIN_REQUEST_INTERVAL:
        time.sleep(_MIN_REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


async def _fetch_json(url: str, params: Dict[str, str]) -> Optional[Dict[str, Any]]:
    """Rate-limited GET returning parsed JSON, or None on failure."""
    _rate_limit()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"[pubmed-mcp] HTTP {e.response.status_code} from {url}: {e.response.text[:200]}")
        return None
    except httpx.TimeoutException:
        print(f"[pubmed-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[pubmed-mcp] Request error for {url}: {e}")
        return None


async def _fetch_text(url: str, params: Dict[str, str]) -> Optional[str]:
    """Rate-limited GET returning raw text, or None on failure."""
    _rate_limit()
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.text
    except httpx.HTTPStatusError as e:
        print(f"[pubmed-mcp] HTTP {e.response.status_code} from {url}: {e.response.text[:200]}")
        return None
    except httpx.TimeoutException:
        print(f"[pubmed-mcp] Timeout from {url}")
        return None
    except httpx.RequestError as e:
        print(f"[pubmed-mcp] Request error for {url}: {e}")
        return None


async def _fetch_summaries(pmids: List[str]) -> Dict[str, Any]:
    """Fetch ESummary data for a list of PMIDs (capped at 100 per request)."""
    if not pmids:
        return {}
    result = await _fetch_json(
        f"{PUBMED_BASE}/esummary.fcgi",
        {"db": "pubmed", "id": ",".join(pmids), "retmode": "json"},
    )
    if result is None:
        return {}
    return result.get("result", {})


# ---------------------------------------------------------------------------
# Date-range parsing
# ---------------------------------------------------------------------------


def _parse_date_range(date_range: str) -> Dict[str, str]:
    """Parse 'YYYY:YYYY' or 'YYYY/MM:YYYY/MM' into ESearch date params.

    Returns a dict with keys mindate, maxdate, datetype, or empty dict on failure.
    """
    parts = date_range.split(":")
    if len(parts) != 2:
        return {}

    mindate_str, maxdate_str = parts[0].strip(), parts[1].strip()
    if not mindate_str or not maxdate_str:
        return {}

    # Determine format from presence of '/'
    if "/" in mindate_str:
        # Expect YYYY/MM format
        return {
            "mindate": mindate_str,
            "maxdate": maxdate_str,
            "datetype": "pdat",
        }
    # YYYY format
    return {
        "mindate": mindate_str,
        "maxdate": maxdate_str,
        "datetype": "pdat",
    }


# ---------------------------------------------------------------------------
# Response builders
# ---------------------------------------------------------------------------


def _build_article_summary(pmid: str, article: Dict[str, Any]) -> Dict[str, Any]:
    """Build a summary dict from an ESummary result entry."""
    authors: List[str] = []
    for author in article.get("authors", []):
        name = author.get("name", "")
        if name:
            authors.append(name)

    # Extract DOI from elocationid (format: "doi: 10.xxxx/xxxx")
    doi = ""
    elocation = article.get("elocationid", "")
    if elocation.lower().startswith("doi:"):
        doi = elocation.split(":", 1)[1].strip()

    return {
        "pmid": pmid,
        "title": article.get("title", ""),
        "authors": authors,
        "journal": article.get("fulljournalname", ""),
        "pub_date": article.get("pubdate", ""),
        "doi": doi,
        "abstract": "",  # Abstract requires efetch — use get_article_details
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def _build_article_detail(pmid: str, article: ET.Element) -> Dict[str, Any]:
    """Build a full detail dict from an EFetch XML PubmedArticle element."""
    # Title
    title = article.findtext(".//ArticleTitle", "")

    # Abstract
    abstract_parts: List[str] = []
    for elem in article.findall(".//AbstractText"):
        label = elem.get("Label", "")
        text = _elem_text_content(elem)
        if label:
            abstract_parts.append(f"{label}: {text}")
        else:
            abstract_parts.append(text)
    abstract = " ".join(abstract_parts)

    # Authors
    authors: List[str] = []
    for author in article.findall(".//Author"):
        last = author.findtext("LastName", "")
        fore = author.findtext("ForeName", "")
        collective = author.findtext("CollectiveName", "")
        if collective:
            authors.append(collective)
        elif last:
            authors.append(f"{last} {fore}" if fore else last)

    # Journal
    journal = article.findtext(".//Journal/Title", "")
    journal_iso = article.findtext(".//Journal/ISOAbbreviation", "")

    # Publication date
    pub_date = _extract_pub_date(article)

    # Identifiers
    doi = article.findtext(".//ArticleId[@IdType='doi']", "")
    pmc = article.findtext(".//ArticleId[@IdType='pmc']", "")
    pii = article.findtext(".//ArticleId[@IdType='pii']", "")

    # Publication types
    pub_types: List[str] = []
    for pt in article.findall(".//PublicationType"):
        text = pt.text
        if text:
            pub_types.append(text)

    # MeSH terms
    mesh_terms: List[str] = []
    for mesh in article.findall(".//MeshHeading"):
        desc = mesh.findtext("DescriptorName", "")
        qualifiers: List[str] = []
        for qual in mesh.findall("QualifierName"):
            q_text = qual.text
            if q_text:
                qualifiers.append(q_text)
        if desc:
            if qualifiers:
                mesh_terms.append(f"{desc}/{'; '.join(qualifiers)}")
            else:
                mesh_terms.append(desc)

    return {
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "journal": journal,
        "journal_iso": journal_iso,
        "pub_date": pub_date,
        "doi": doi,
        "pmc": pmc,
        "pii": pii,
        "publication_types": pub_types,
        "mesh_terms": mesh_terms,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
    }


def _elem_text_content(elem: ET.Element) -> str:
    """Collect all text content from an element including nested tags."""
    parts: List[str] = []
    if elem.text:
        parts.append(elem.text)
    for child in elem:
        if child.tail:
            parts.append(child.tail)
    return "".join(parts)


def _extract_pub_date(article: ET.Element) -> str:
    """Extract publication date string from a PubmedArticle element."""
    # Try PubDate with Year/Month/Day structure
    pub_date = article.find(".//Journal/JournalIssue/PubDate")
    if pub_date is not None:
        year = pub_date.findtext("Year", "")
        month = pub_date.findtext("Month", "")
        day = pub_date.findtext("Day", "")
        parts = [p for p in [year, month, day] if p]
        if parts:
            return " ".join(parts)

    # Fallback to MedlineDate
    if pub_date is not None:
        medline = pub_date.findtext("MedlineDate", "")
        if medline:
            return medline

    return ""


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
async def search_pubmed(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    date_range: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search PubMed for biomedical literature.

    Uses NCBI ESearch to find matching PMIDs, then ESummary to retrieve
    summaries.  Results are sorted and capped at *max_results*.

    Args:
        query: Search query string (supports PubMed syntax:
            AND, OR, NOT, [au], [tiab], [mesh], etc.)
        max_results: Maximum number of results to return (default: 10,
            max: 100)
        sort_by: Sort order — ``"relevance"`` (default), ``"date"``,
            or ``"pub_date"``
        date_range: Optional filter in ``"YYYY:YYYY"`` or
            ``"YYYY/MM:YYYY/MM"`` format (publication-date based)

    Returns:
        A list of article-summary dicts, each containing: **pmid**, **title**,
        **authors**, **journal**, **pub_date**, **doi**, **abstract**
        (empty — use *get_article_details* for the full abstract), **url**
    """
    capped = max(1, min(max_results, 100))
    sort_key = SORT_MAP.get(sort_by, "relevance")

    # Build ESearch params
    params: Dict[str, str] = {
        "db": "pubmed",
        "term": query,
        "retmax": str(capped),
        "sort": sort_key,
        "retmode": "json",
    }

    if date_range:
        date_params = _parse_date_range(date_range)
        if date_params and date_params.get('mindate') and date_params.get('maxdate'):
            params.update(date_params)

    search_data = await _fetch_json(f"{PUBMED_BASE}/esearch.fcgi", params)
    if search_data is None:
        return [{"error": f"Search request failed for query: {query}"}]

    id_list: List[str] = (
        search_data.get("esearchresult", {}).get("idlist", [])
    )
    if not id_list:
        return []

    # Fetch summaries via ESummary
    summary_data = await _fetch_summaries(id_list)

    results: List[Dict[str, Any]] = []
    for pmid in id_list:
        article = summary_data.get(pmid)
        if article:
            results.append(_build_article_summary(pmid, article))
        else:
            results.append({
                "pmid": pmid,
                "title": "",
                "authors": [],
                "journal": "",
                "pub_date": "",
                "doi": "",
                "abstract": "",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            })

    return results


@mcp.tool()
async def get_article_details(pmid: str) -> Dict[str, Any]:
    """Retrieve full details for a single PubMed article by PMID.

    Uses NCBI EFetch with XML mode to obtain the complete record including
    abstract, authors, MeSH terms, publication types, and identifiers.

    Args:
        pmid: PubMed ID (numeric identifier for the article)

    Returns:
        A dict containing: **pmid**, **title**, **authors**, **abstract**,
        **journal**, **journal_iso**, **pub_date**, **doi**, **pmc**, **pii**,
        **publication_types**, **mesh_terms**, **url**.
        Returns ``{"error": "Article not found"}`` if the PMID is invalid.
    """
    if not pmid or not pmid.strip():
        return {"error": "PMID is required"}

    pmid = pmid.strip()

    xml_text = await _fetch_text(
        f"{PUBMED_BASE}/efetch.fcgi",
        {"db": "pubmed", "id": pmid, "retmode": "xml"},
    )
    if xml_text is None:
        return {"error": f"Failed to retrieve article details for PMID: {pmid}"}

    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        return {"error": f"Failed to parse XML response: {e}"}

    article = root.find(".//PubmedArticle")
    if article is None:
        return {"error": "Article not found"}

    return _build_article_detail(pmid, article)


@mcp.tool()
async def get_related_articles(
    pmid: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """Find articles related to a given PubMed article.

    Uses NCBI ELink with ``cmd=neighbor`` to discover related PMIDs, then
    fetches summaries via ESummary.

    Args:
        pmid: PubMed ID to find related articles for
        max_results: Maximum number of related articles to return
            (default: 10, max: 100)

    Returns:
        A list of article-summary dicts (same shape as *search_pubmed*
        results).
    """
    if not pmid or not pmid.strip():
        return [{"error": "PMID is required"}]

    pmid = pmid.strip()
    capped = max(1, min(max_results, 100))

    # ELink to find related PMIDs
    link_data = await _fetch_json(
        f"{PUBMED_BASE}/elink.fcgi",
        {
            "dbfrom": "pubmed",
            "db": "pubmed",
            "id": pmid,
            "cmd": "neighbor",
            "retmode": "json",
        },
    )
    if link_data is None:
        return [{"error": f"Failed to find related articles for PMID: {pmid}"}]

    # Extract related IDs from the response
    related_ids: List[str] = []
    linksets = link_data.get("linksets", [])
    for linkset in linksets:
        for link_db in linkset.get("linksetdbs", []):
            if link_db.get("dbto") == "pubmed":
                for link in link_db.get("links", []):
                    related_ids.append(str(link))

    if not related_ids:
        return []

    # Cap and deduplicate
    seen: set[str] = set()
    unique_ids: List[str] = []
    for rid in related_ids:
        if rid not in seen and rid != pmid:
            seen.add(rid)
            unique_ids.append(rid)
    unique_ids = unique_ids[:capped]

    if not unique_ids:
        return []

    # Fetch summaries
    summary_data = await _fetch_summaries(unique_ids)

    results: List[Dict[str, Any]] = []
    for rid in unique_ids:
        article = summary_data.get(rid)
        if article:
            results.append(_build_article_summary(rid, article))
        else:
            results.append({
                "pmid": rid,
                "title": "",
                "authors": [],
                "journal": "",
                "pub_date": "",
                "doi": "",
                "abstract": "",
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{rid}/",
            })

    return results


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    mcp.run()
