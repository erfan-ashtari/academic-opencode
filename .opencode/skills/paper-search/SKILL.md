---
name: paper-search
description: Search for academic papers across multiple databases (arXiv, PubMed, Semantic Scholar, IEEE Xplore, ACM, OpenAlex, Crossref, SSRN, DBLP, bioRxiv, Europe PMC, Google Scholar, Scopus, ACL Anthology) with unified results, deduplication, and PDF availability tagging.
version: 1.0.0
author: OpenCode Community
triggers:
  - "Find papers about..."
  - "Search for research on..."
  - "Look up academic papers on..."
  - "Search papers"
  - "Search for recent papers on..."
  - "Find articles about..."
  - "Look up scholarly articles on..."
  - "Find related work on..."
  - "What papers exist on..."
  - "Search literature for..."
mcp:
  arxiv:
    command: python
    args: ["mcp_servers/arxiv-mcp/server.py"]
  semantic-scholar:
    command: python
    args: ["mcp_servers/semantic-scholar-mcp/server.py"]
  pubmed:
    command: python
    args: ["mcp_servers/pubmed-mcp/server.py"]
  ieee-xplore:
    command: python
    args: ["mcp_servers/ieee-xplore-mcp/server.py"]
  acm-dl:
    command: python
    args: ["mcp_servers/acm-dl-mcp/server.py"]
  openalex:
    command: python
    args: ["mcp_servers/openalex-mcp/server.py"]
  crossref:
    command: python
    args: ["mcp_servers/crossref-mcp/server.py"]
  ssrn:
    command: python
    args: ["mcp_servers/ssrn-mcp/server.py"]
  dblp:
    command: python
    args: ["mcp_servers/dblp-mcp/server.py"]
  biorxiv:
    command: python
    args: ["mcp_servers/biorxiv-mcp/server.py"]
  europepmc:
    command: python
    args: ["mcp_servers/europepmc-mcp/server.py"]
  google-scholar:
    command: python
    args: ["mcp_servers/google-scholar-mcp/server.py"]
  zotero:
    command: python
    args: ["mcp_servers/zotero-mcp/server.py"]
  scopus:
    command: python
    args: ["mcp_servers/scopus-mcp/server.py"]
  acl-anthology:
    command: python
    args: ["mcp_servers/acl-anthology-mcp/server.py"]
---
name: paper-search
description: Search for academic papers across multiple databases (arXiv, PubMed, Semantic Scholar, IEEE Xplore, ACM, OpenAlex, Crossref, SSRN, DBLP, bioRxiv, Europe PMC, Google Scholar, Scopus) with unified results, deduplication, and PDF availability tagging.
version: 1.0.0
author: OpenCode Community
triggers:
  - "Find papers about..."
  - "Search for research on..."
  - "Look up academic papers on..."
  - "Search papers"
  - "Search for recent papers on..."
  - "Find articles about..."
  - "Look up scholarly articles on..."
  - "Find related work on..."
  - "What papers exist on..."
  - "Search literature for..."
---

# Paper Search Skill

Search for academic papers across multiple databases simultaneously with unified results, relevance ranking, and PDF availability tagging.

## How It Works

1. **Parse Query**: Extract key terms, filters, and parameters from the search request
2. **Check MCP Availability**: Probe each MCP server; if unavailable, switch to web fallback
3. **Select Sources**: Identify relevant databases based on query scope
4. **Execute Parallel Searches**: Dispatch concurrent search requests to each MCP server (or web fallback)
5. **Deduplicate Results**: Merge results by DOI, arXiv ID, or title similarity
6. **Tag PDF Availability**: Check and annotate each result with open-access status
7. **Rank Results**: Sort by relevance, citations, recency, or weighted combination
8. **Present Unified Output**: Return aggregated results with source attribution

## Fallback Mode (MCP Unavailable)

When MCP servers are not running or configured, the skill automatically falls back to **web search**.
It searches the actual academic websites directly and parses results from the HTML.

**Allowed fallback sites** (only websites we have MCPs for):

| Site | URL Pattern | Search Query Format |
|------|-------------|---------------------|
| arXiv | `arxiv.org/search/{query}` | site:arxiv.org {query} |
| PubMed | `pubmed.ncbi.nlm.nih.gov/?term={query}` | site:pubmed.ncbi.nlm.nih.gov {query} |
| Semantic Scholar | `semanticscholar.org/search?q={query}` | site:semanticscholar.org {query} |
| IEEE Xplore | `ieeexplore.ieee.org/search/searchresult.jsp?queryText={query}` | site:ieeexplore.ieee.org {query} |
| ACM DL | `dl.acm.org/action/doSearch?AllField={query}` | site:dl.acm.org {query} |
| OpenAlex | `openalex.org/works?search={query}` | site:openalex.org {query} |
| Crossref | `search.crossref.org/search/works?q={query}` | site:doi.org {query} |
| SSRN | `ssrn.com/index.cfm/ja_index/paper_search/{query}` | site:ssrn.com {query} |
| DBLP | `dblp.org/search?q={query}` | site:dblp.org {query} |
| bioRxiv | `biorxiv.org/search/{query}` | site:biorxiv.org {query} |
| Europe PMC | `europepmc.org/search?query={query}` | site:europepmc.org {query} |
| Google Scholar | `scholar.google.com/scholar?q={query}` | site:scholar.google.com {query} |

**Fallback workflow:**
1. Use `websearch` tool with `site:` operator targeting the academic domain
2. Use `webfetch` to scrape the search results page
3. Parse titles, authors, abstracts, DOIs, and PDF links from HTML
4. Return results in the same JSON format as MCP results
5. Tag each result with `source: "web-fallback"` and `source_url` for provenance

**⚠️ Fallback limitations:**
- Results may be less structured than MCP responses
- Abstracts may be truncated or missing
- Citation counts may not be available
- Rate limits still apply (respect website ToS)

## Supported Databases

| Database | Coverage | MCP Server |
|----------|----------|------------|
| arXiv | Physics, CS, Math | `arxiv-mcp` |
| PubMed | Biomedical | `pubmed-mcp` |
| Semantic Scholar | All fields | `semantic-scholar-mcp` |
| IEEE Xplore | Engineering, CS | `ieee-xplore-mcp` |
| ACM DL | CS, Computing | `acm-dl-mcp` |
| OpenAlex | Cross-discipline | `openalex-mcp` |
| Crossref | DOI registry | `crossref-mcp` |
| SSRN | Social Sciences | `ssrn-mcp` |
| DBLP | CS Bibliography | `dblp-mcp` |
| bioRxiv | Biology | API fallback |
| Europe PMC | Biomedical | API fallback |
| Google Scholar | All fields | Web fallback |

## Query Syntax

### Basic Search
```bash
/search-papers "transformer attention mechanism"
```

### Advanced Search
```bash
/search-papers --query "deep learning" --sources arxiv,semantic-scholar --year 2023-2024 --limit 20
```

### Boolean Operators
- `AND` - Both terms must appear
- `OR` - Either term may appear
- `NOT` - Excludes term
- `"..."` - Exact phrase match

## Output Format

Returns JSON with:
- `papers`: Array of paper objects with title, authors, abstract, year, doi, citations, url, pdf_url, pdf_available
- `metadata`: Total results, sources searched, deduplication stats

## Integration

| Component | Integration Point |
|-----------|-------------------|
| Citation Manager | Pass paper metadata for citation generation |
| Literature Review | Feed search results into review workflows |
| Paper Writing | Provide references for citation insertion |
| Zotero Integration | Save search results to Zotero |
