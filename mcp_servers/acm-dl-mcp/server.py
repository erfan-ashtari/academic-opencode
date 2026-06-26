"""
ACM Digital Library MCP Server.

Provides FastMCP tools for searching and retrieving academic papers from
the ACM Digital Library via the Crossref REST API.

ACM is Crossref member 320 — all ACM publications indexed by Crossref are
searchable through the member/320/works endpoint.  The Crossref API is free
and openly accessible to all researchers; no API key is required for basic
use.

Set the ``ACM_API_KEY`` environment variable if you have an ACM Digital
Library API key (institutional access) — it is stored for future use when
ACM-authenticated endpoints become available.
"""

from __future__ import annotations

import os
import re
import time
from typing import Any, Dict, List, Optional

import requests
from fastmcp import FastMCP

mcp = FastMCP("acm-dl")

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

CROSSREF_BASE_URL = "https://api.crossref.org"
CROSSREF_MEMBER_ACM = "320"  # ACM's Crossref member identifier

# CrossRef polite pool recommends 50 req/s max (non-commercial).  We use a
# conservative 0.5 s interval (~2 req/s) to stay well within the limit.
_LOCK_INTERVAL: float = 0.5
_LAST_REQUEST_TIME: float = 0.0

# Optional ACM API key (stored for future authenticated endpoints).
_ACM_API_KEY: Optional[str] = os.environ.get("ACM_API_KEY")


# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------


def _check_rate_limit() -> None:
    """Enforce a conservative per-request interval for the CrossRef API."""
    global _LAST_REQUEST_TIME
    now = time.monotonic()
    elapsed = now - _LAST_REQUEST_TIME
    if elapsed < _LOCK_INTERVAL:
        time.sleep(_LOCK_INTERVAL - elapsed)
    _LAST_REQUEST_TIME = time.monotonic()


# ---------------------------------------------------------------------------
# Low-level HTTP helpers
# ---------------------------------------------------------------------------


def _call_crossref(
    path: str,
    params: Optional[Dict[str, str]] = None,
    timeout: int = 30,
) -> Optional[Dict[str, Any]]:
    """Perform a rate-limited GET against the Crossref REST API.

    Returns the parsed JSON body on success, or ``None`` on any HTTP /
    connection / timeout error.
    """
    _check_rate_limit()

    url = f"{CROSSREF_BASE_URL}{path}"

    # Polite pool: identify the client so Crossref can contact us if needed.
    headers = {
        "User-Agent": (
            "AcademicResearchAssistant/1.0 "
            "(mailto:acm-dl-mcp@example.com; Crossref polite pool)"
        ),
        "Accept": "application/json",
    }

    try:
        resp = requests.get(url, params=params, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        status = e.response.status_code if e.response is not None else "unknown"
        body = e.response.text[:300] if e.response is not None else ""
        print(f"[acm-dl] HTTP {status} from {path}: {body}")
        return None
    except requests.ConnectionError as e:
        print(f"[acm-dl] Connection error on {path}: {e}")
        return None
    except requests.Timeout:
        print(f"[acm-dl] Request timed out after {timeout}s: {path}")
        return None
    except requests.RequestException as e:
        print(f"[acm-dl] Request failed on {path}: {e}")
        return None


# ---------------------------------------------------------------------------
# Data normalisation helpers
# ---------------------------------------------------------------------------


def _strip_jats(text: Optional[str]) -> str:
    """Strip JATS / XML markup from an abstract string.

    Many Crossref deposits include abstracts wrapped in JATS XML tags.
    This helper strips the tags and normalises whitespace.
    """
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", "", text)
    text = (
        text.replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&quot;", '"')
        .replace("&apos;", "'")
    )
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _parse_authors(authors_raw: Any) -> List[Dict[str, str]]:
    """Normalise a Crossref ``author`` list into ``[{name, affiliation}]``.

    Returns an empty list when no authors are present or the input is
    malformed.
    """
    if not isinstance(authors_raw, list):
        return []

    result: List[Dict[str, str]] = []
    for entry in authors_raw:
        if not isinstance(entry, dict):
            continue
        given = entry.get("given", "") or ""
        family = entry.get("family", "") or ""
        name = f"{given} {family}".strip() if given or family else ""
        if not name:
            name = entry.get("name", "") or ""

        affiliations_raw = entry.get("affiliation") or []
        parts: List[str] = []
        for aff in affiliations_raw:
            if isinstance(aff, dict):
                parts.append(aff.get("name", ""))
            elif isinstance(aff, str):
                parts.append(aff)
        affiliation = "; ".join(p for p in parts if p)

        result.append({"name": name, "affiliation": affiliation})
    return result


def _date_parts_to_str(work: Dict[str, Any], key: str) -> str:
    """Extract an ISO-formatted date string from Crossref's ``date-parts``.

    Returns an empty string when the date key is absent.
    """
    date_info = work.get(key)
    if not isinstance(date_info, dict):
        return ""
    parts = date_info.get("date-parts")
    if not isinstance(parts, list) or not parts:
        return ""
    p = parts[0]
    if not isinstance(p, list):
        return ""
    if len(p) >= 3:
        return f"{p[0]:04d}-{p[1]:02d}-{p[2]:02d}"
    if len(p) >= 2:
        return f"{p[0]:04d}-{p[1]:02d}"
    if len(p) >= 1:
        return f"{p[0]:04d}"
    return ""


def _extract_year(work: Dict[str, Any]) -> Optional[int]:
    """Extract the best-available publication year from a Crossref work."""
    for key in ("published-print", "published-online", "published", "issued", "created"):
        date_info = work.get(key)
        if not isinstance(date_info, dict):
            continue
        parts = date_info.get("date-parts")
        if isinstance(parts, list) and parts and isinstance(parts[0], list) and parts[0]:
            try:
                return int(parts[0][0])
            except (ValueError, IndexError):
                continue
    return None


def _build_work(work: Dict[str, Any]) -> Dict[str, Any]:
    """Normalise a raw Crossref work dictionary into a consistent output shape.

    Fields returned are designed to mirror the structure used by sibling MCP
    servers (IEEE Xplore, Semantic Scholar, arXiv) for easy aggregation.
    """
    doi: str = work.get("DOI") or ""

    # Title — Crossref stores it as a list (usually one element).
    title_list = work.get("title") or []
    title: str = title_list[0] if title_list else ""

    # Abstract — may be JATS XML; strip tags.
    abstract = _strip_jats(work.get("abstract"))

    # Publication date — prefer online, fall back to print, then created.
    pub_date = (
        _date_parts_to_str(work, "published-online")
        or _date_parts_to_str(work, "published-print")
        or _date_parts_to_str(work, "published")
        or _date_parts_to_str(work, "issued")
        or _date_parts_to_str(work, "created")
    )

    pub_year = _extract_year(work)

    # Container / venue title (journal or conference proceedings name).
    container = work.get("container-title") or []
    publication_title: str = container[0] if container else ""

    # URL
    url: str = work.get("URL") or f"https://doi.org/{doi}" if doi else ""

    # PDF link — prefer the first link tagged as PDF or the first text-mining link.
    pdf_url: str = ""
    links = work.get("link") or []
    if isinstance(links, list):
        for lnk in links:
            if not isinstance(lnk, dict):
                continue
            lurl = lnk.get("URL") or ""
            ct = (lnk.get("content-type") or "").lower()
            if "pdf" in ct or lnk.get("intended-application") == "similarity-checking":
                pdf_url = lurl
                break
        if not pdf_url and links:
            first = links[0]
            if isinstance(first, dict):
                pdf_url = first.get("URL") or ""

    # ACM DL landing page
    acm_url: str = f"https://dl.acm.org/doi/{doi}" if doi else url

    # Type mapping
    raw_type: str = work.get("type") or ""
    type_map: Dict[str, str] = {
        "journal-article": "Journal Article",
        "proceedings-article": "Conference Paper",
        "book-chapter": "Book Chapter",
        "book": "Book",
        "monograph": "Monograph",
        "dissertation": "Dissertation",
        "report": "Report",
        "reference-book": "Reference Book",
        "posted-content": "Preprint",
        "dataset": "Dataset",
    }
    content_type: str = type_map.get(raw_type, raw_type.replace("-", " ").title())

    # ISBN / ISSN — lists stored in Crossref
    isbn_list = work.get("ISBN") or []
    issn_list = work.get("ISSN") or []

    return {
        "doi": doi,
        "title": title,
        "authors": _parse_authors(work.get("author")),
        "abstract": abstract,
        "publication_title": publication_title,
        "publication_date": pub_date,
        "publication_year": pub_year,
        "publisher": work.get("publisher") or "ACM",
        "type": content_type,
        "volume": str(work.get("volume") or ""),
        "issue": str(work.get("issue") or ""),
        "page": str(work.get("page") or ""),
        "isbn": isbn_list[0] if isbn_list else "",
        "issn": issn_list[0] if issn_list else "",
        "citation_count": work.get("is-referenced-by-count") or 0,
        "reference_count": work.get("references-count") or 0,
        "subjects": work.get("subject") or [],
        "url": url,
        "acm_url": acm_url,
        "pdf_url": pdf_url,
        "doi_url": f"https://doi.org/{doi}" if doi else "",
        # Internal type for advanced filtering; not part of the stable API.
        "_raw_type": raw_type,
    }


def _parse_date_filter(date_str: str) -> Optional[str]:
    """Parse a publication_date parameter into a CrossRef filter string.

    CrossRef uses a single ``filter`` parameter with comma-separated
    ``key:value`` pairs.  Available date filters:
    ``from-pub-date`` and ``until-pub-date``.

    Supported date formats:
    - ``"2023"``  -> single year
    - ``"2020-2024"`` -> range (inclusive)
    - ``"2020-"`` -> open start
    - ``"-2020"`` -> open end

    Returns ``None`` when the input cannot be parsed.
    """
    if not date_str or not date_str.strip():
        return None

    ds = date_str.strip()
    parts: List[str] = []

    if "-" in ds:
        spl = ds.split("-", 1)
        start = spl[0].strip()
        end = spl[1].strip() if len(spl) > 1 else ""

        if start and end:
            parts.append(f"from-pub-date:{start}-01-01")
            parts.append(f"until-pub-date:{end}-12-31")
        elif start:
            parts.append(f"from-pub-date:{start}-01-01")
        elif end:
            parts.append(f"until-pub-date:{end}-12-31")
    else:
        # Single year
        parts.append(f"from-pub-date:{ds}-01-01")
        parts.append(f"until-pub-date:{ds}-12-31")

    return ",".join(parts) if parts else None


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def search_acm(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    publication_date: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Search the ACM Digital Library for academic papers matching the given query.

    Uses the Crossref REST API under the hood — ACM is Crossref member 320,
    and every ACM publication indexed by Crossref is searchable through this
    endpoint.  No API key is required.

    Args:
        query: Search query string.  Supports boolean operators (``AND``,
            ``OR``, ``NOT``), quoted phrases, and fielded search prefixes
            such as ``title:``, ``author:``, ``doi:``.
        max_results: Maximum number of results to return
            (default 10, max 200).
        sort_by: Sort criterion.  One of:

            - ``"relevance"`` — score-based ranking (default)
            - ``"published"`` — publication date
            - ``"cited"`` — citation count (``is-referenced-by-count``)
            - ``"title"`` — title alphabetically

        publication_date: Optional date-range filter.  Examples:

            - ``"2023"`` → papers published in 2023
            - ``"2020-2024"`` → papers from 2020 through 2024 (inclusive)
            - ``"2020-"`` → papers from 2020 onward
            - ``"-2020"`` → papers up to and including 2020

    Returns:
        A list of paper dictionaries.  Each dictionary contains **doi**,
        **title**, **authors** (a list of ``{name, affiliation}``),
        **abstract**, **publication_title**, **publication_date**,
        **publication_year**, **publisher**, **type**, **citation_count**,
        **reference_count**, **subjects**, **url**, **acm_url**,
        **pdf_url**, and **doi_url**.  Returns an empty list on failure.
    """
    # Validate and cap max_results.
    capped = max(1, min(max_results, 200))

    # Sort mapping.
    sort_map: Dict[str, str] = {
        "relevance": "score",
        "published": "published",
        "cited": "is-referenced-by-count",
        "title": "title",
    }
    sort_field = sort_map.get(sort_by, "score")

    params: Dict[str, str] = {
        "query": query,
        "rows": str(capped),
        "sort": sort_field,
        "order": "desc",
    }

    # Apply date filter if provided.
    date_filters = _parse_date_filter(publication_date) if publication_date else None
    if date_filters:
        params["filter"] = date_filters

    data = _call_crossref(f"/members/{CROSSREF_MEMBER_ACM}/works", params)
    if data is None:
        return [{"error": f"Search request failed for query: {query}"}]

    message = data.get("message")
    if not isinstance(message, dict):
        return []

    items = message.get("items") or []
    if not items:
        return []

    return [_build_work(item) for item in items]


@mcp.tool()
def get_paper_details(doi: str) -> Dict[str, Any]:
    """Retrieve full metadata for a single ACM paper by its DOI.

    Looks up the paper in the Crossref database and returns comprehensive
    bibliographic metadata including authors, abstract (when available),
    citation counts, references, and links.

    Args:
        doi: The DOI of the paper.  Accepts full URLs
            (e.g. ``"https://doi.org/10.1145/3487553.3524258"``) and bare
            DOIs (e.g. ``"10.1145/3487553.3524258"``).

    Returns:
        A dictionary with full paper metadata including **doi**, **title**,
        **authors** (list of ``{name, affiliation}``), **abstract**,
        **publication_title**, **publication_date**, **publication_year**,
        **publisher**, **type**, **volume**, **issue**, **page**,
        **citation_count**, **reference_count**, **subjects**, **url**,
        **acm_url**, **pdf_url**, and **doi_url**.

        Returns ``{"error": "Paper not found"}`` if the DOI is invalid.
    """
    if not doi or not doi.strip():
        return {"error": "A DOI is required to look up a paper."}

    doi = doi.strip()

    # Strip common prefix if user passes a full DOI URL.
    for prefix in ("https://doi.org/", "http://doi.org/", "doi.org/", "doi:"):
        if doi.lower().startswith(prefix.lower()):
            doi = doi[len(prefix):]
            break

    if not doi:
        return {"error": "DOI is empty after URL prefix stripping."}

    data = _call_crossref(f"/works/{doi}")
    if data is None:
        return {"error": f"Failed to retrieve paper details for DOI: {doi}"}

    message = data.get("message")
    if not isinstance(message, dict):
        return {"error": f"Paper not found with DOI: {doi}"}

    return _build_work(message)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
