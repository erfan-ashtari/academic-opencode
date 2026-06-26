---
name: search-papers
description: Search for academic papers across 13 databases
arguments:
  - name: query
    description: Search query (keywords, title, author, DOI)
    required: true
  - name: database
    description: Specific database(s) to search (comma-separated, or 'all')
    required: false
    default: all
  - name: year
    description: Year range filter (e.g., '2020-2024' or '2023')
    required: false
  - name: max-results
    description: Maximum number of results to return
    required: false
    default: 25
  - name: sort
    description: Sort order (relevance, citations, date)
    required: false
    default: relevance
---

# Search Papers Command

Search for academic papers across multiple databases with deduplication and relevance ranking.

## Usage

```bash
/search-papers "transformer attention mechanism"
/search-papers "deep learning" --database arxiv,semantic-scholar
/search-papers "CRISPR" --year 2023-2024 --max-results 50
```

## Databases

| Database | Best For |
|----------|----------|
| arxiv | CS, Physics, Math |
| semantic-scholar | Cross-discipline |
| pubmed | Medical, Biomedical |
| ieee-xplore | EE, Engineering |
| acm-dl | CS, Computing |
| openalex | Cross-discipline |
| crossref | DOI metadata |
| ssrn | Social Science |
| dblp | CS Bibliography |
| biorxiv | Biology, Biotech |
| europepmc | Biomedical |
| google-scholar | Cross-discipline (⚠️ unofficial) |

## Output

Returns JSON with:
- `papers`: Array of paper objects with title, authors, abstract, year, doi, citations, url, pdf_url, pdf_available
- `total`: Total results found
- `returned`: Results returned
- `sources_queried`: Databases searched

## Skill Used

`paper-search`
