# MCP Servers

This directory contains MCP (Model Context Protocol) servers for academic database integration.

## Overview

MCP servers provide a standardized way to interact with academic databases. Each server implements search and retrieval functionality with automatic web search fallback when APIs fail.

## Servers

| Server | Database | API Key Required | Coverage |
|--------|----------|------------------|----------|
| arxiv-mcp | arXiv | No | Physics, CS, Math |
| semantic-scholar-mcp | Semantic Scholar | Optional | All fields |
| pubmed-mcp | PubMed | Optional | Biomedical |
| ieee-xplore-mcp | IEEE Xplore | Yes | Engineering, CS |
| acm-dl-mcp | ACM Digital Library | No | CS, Computing |
| openalex-mcp | OpenAlex | Optional | Cross-discipline |
| crossref-mcp | Crossref | Optional | DOI registry |
| ssrn-mcp | SSRN | No | Social Sciences |
| dblp-mcp | DBLP | No | CS Bibliography |
| biorxiv-mcp | bioRxiv | No | Biology |
| europepmc-mcp | Europe PMC | No | Biomedical |
| google-scholar-mcp | Google Scholar | No | All fields |
| zotero-mcp | Zotero | Yes | Reference management |
| document-converter | PDF/DOCX | No | Document conversion |
| scopus-mcp | Scopus | Yes | 27,000+ journals |
| acl-anthology-mcp | ACL Anthology | No | NLP/CL papers |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Server Layer                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ │
│  │arXiv│ │IEEE │ │PubMed│ │S2   │ │OAlex│ │Cross│ │SSRN │ │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ │
│     │       │       │       │       │       │       │      │
│     └───────┴───────┴───────┴───────┴───────┴───────┘      │
│                          │                                   │
│                    Fallback Layer                            │
│              (web search via Jina Reader API)                │
└─────────────────────────────────────────────────────────────┘
```

## Fallback System

All servers use `fallback_utils.py` for web search fallback:

1. **API Call** - Try the primary API
2. **Failure Detection** - Catch errors, rate limits, timeouts
3. **Web Search Fallback** - Use Jina Reader API for site-specific search
4. **Result Enrichment** - Add standard metadata (`_metadata` field)

### Result Format

Every result includes:

```python
{
    "title": "Paper Title",
    "authors": ["Author1", "Author2"],
    "abstract": "Abstract text...",
    "doi": "10.xxxx/xxxxx",
    "url": "https://...",
    "year": 2024,
    "_metadata": {
        "mcp_name": "server-name",
        "method": "api",  # or "websearch"
        "weblink": "https://..."
    }
}
```

## API Keys

Required keys are configured in `.env`:

| Server | Environment Variable | How to Get |
|--------|---------------------|------------|
| IEEE Xplore | `IEEE_API_KEY` | [developer.ieee.org](https://developer.ieee.org/) |
| Zotero | `ZOTERO_API_KEY` | [zotero.org/settings/keys](https://www.zotero.org/settings/keys) |
| Scopus | `SCOPUS_API_KEY` | [dev.elsevier.com](https://dev.elsevier.com/) |
| Semantic Scholar | `SEMANTIC_SCHOLAR_API_KEY` | [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api) |
| PubMed | `NCBI_API_KEY` | [ncbi.nlm.nih.gov/labs/account](https://www.ncbi.nlm.nih.gov/labs/account/) |

## Development

See `AGENTS.md` for development guidelines.

### Adding a New Server

1. Create directory: `mcp_servers/{name}-mcp/`
2. Create `server.py` using FastMCP framework
3. Import and use `fallback_utils.py`
4. Add to `.mcp.json`
5. Update documentation

### Testing

```bash
# Test individual server
python mcp_servers/arxiv-mcp/server.py

# Test with Python
python -c "
import asyncio
from mcp_servers.arxiv_mcp import server
asyncio.run(server.search_arxiv('transformer attention'))
"
```

## Dependencies

- `fastmcp` - MCP server framework
- `httpx` - HTTP client
- `fallback_utils.py` - Shared fallback utilities
- `.env` - API keys
