---
name: research-agent
description: Orchestrates multi-source paper search and aggregation across academic databases
type: agent
capabilities:
  - parallel-search
  - result-deduplication
  - relevance-ranking
  - citation-network-analysis
  - metadata-enrichment
---

# Research Agent

Orchestrates multi-source paper search, deduplication, relevance ranking, and citation network analysis across 13 academic databases.

## Capabilities

| Capability | Description |
|------------|-------------|
| parallel-search | Query multiple databases simultaneously |
| result-deduplication | Identify and merge duplicate papers by DOI/title |
| relevance-ranking | Sort by citations, recency, or topic relevance |
| citation-network-analysis | Map citation relationships between papers |
| metadata-enrichment | Fill missing metadata from multiple sources |

## Configuration

```yaml
agent:
  name: research-agent
  databases:
    - arxiv
    - semantic-scholar
    - pubmed
    - ieee-xplore
    - acm-dl
    - openalex
    - crossref
    - ssrn
    - dblp
    - biorxiv
    - europepmc
    - google-scholar
  ranking:
    - citations
    - recency
    - relevance
  max_results: 50
  timeout: 30
```

## Workflow

```
User Query
    │
    ▼
┌─────────────────┐
│ Parse Query     │
│ Extract terms   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Identify        │
│ Databases       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Parallel Search │
│ (asyncio.gather)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Deduplicate     │
│ Results         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Rank by         │
│ Relevance       │
└────────┬────────┘
         │
         ▼
    Unified Results
```

## Inter-Agent Communication

```json
{
  "agent": "research-agent",
  "action": "search",
  "params": {
    "query": "transformer attention",
    "databases": ["arxiv", "semantic-scholar"]
  },
  "result": {
    "papers": [...],
    "metadata": {...}
  }
}
```

## Dependencies

- `skills/paper-search`
- All 13 MCP servers (with web search fallback)
- `skills/citation-manager` (for citation formatting)

## Fallback Behavior

When MCP servers are unavailable, the research-agent uses `websearch` + `webfetch` to search the academic sites directly.
Each result is tagged with `source: "web-fallback"` and `source_url` for provenance.

**Fallback sites** (only sites covered by our MCPs):
- arxiv.org, pubmed.ncbi.nlm.nih.gov, semanticscholar.org
- ieeexplore.ieee.org, dl.acm.org, openalex.org
- doi.org, ssrn.com, dblp.org
- biorxiv.org, europepmc.org, scholar.google.com

**Fallback limitations:**
- Less structured results (no citation counts, truncated abstracts)
- Rate limits apply (respect website ToS)
- Results tagged with `fallback: true` so downstream consumers know
