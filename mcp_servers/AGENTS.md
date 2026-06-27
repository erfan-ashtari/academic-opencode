# AGENTS.md — MCP Servers

## Purpose
This directory contains 14+ MCP (Model Context Protocol) servers for academic database integration.

## File Structure
- `fallback_utils.py` — Shared fallback utilities (CRITICAL: used by all servers)
- `*-mcp/server.py` — Individual MCP server implementations

## Development Guidelines

### Adding a New MCP Server

1. Create directory: `mcp_servers/{name}-mcp/`
2. Create `server.py` using FastMCP framework
3. Import and use `fallback_utils.py` for web search fallback
4. Add server definition to `.mcp.json`
5. Update `AGENTS.md` root file if adding new search capabilities

### Server Template

```python
from fastmcp import FastMCP
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

mcp = FastMCP("server-name")

@mcp.tool()
async def search_tool(query: str, max_results: int = 10) -> list[dict]:
    """Search description."""
    try:
        # API implementation
        results = await api_search(query, max_results)
        return enrich_results_list(results, "server-name")
    except Exception:
        return await web_search_fallback(query, "server-name", max_results)
```

### Fallback Requirements

- ALL servers MUST import from `fallback_utils.py`
- ALL results MUST go through `enrich_result()` or `enrich_results_list()`
- Fallback MUST be triggered on any API error
- Every result MUST include `_metadata` field

### Result Format

Every result should follow this structure:

```python
{
    "title": "Paper Title",
    "authors": ["Author1", "Author2"],
    "abstract": "Abstract text...",
    "doi": "10.xxxx/xxxxx",
    "url": "https://...",
    "year": 2024,
    "citation_count": 10,
    "_metadata": {
        "mcp_name": "server-name",
        "method": "api",  # or "websearch"
        "weblink": "https://..."
    }
}
```

## API Keys

Required keys are configured in `.env`:

| Server | Environment Variable | Required |
|--------|---------------------|----------|
| ieee-xplore | `IEEE_API_KEY` | Yes |
| zotero | `ZOTERO_API_KEY` | Yes |
| scopus | `SCOPUS_API_KEY` | Yes |
| semantic-scholar | `SEMANTIC_SCHOLAR_API_KEY` | Optional |
| pubmed | `NCBI_API_KEY` | Optional |
| openalex | `OPENALEX_EMAIL` | Optional |
| crossref | `CROSSREF_MAILTO` | Optional |

## Dependencies

- Depends on: `fallback_utils.py`, `.env` (API keys)
- Used by: All academic skills (paper-search, citation-manager, etc.)

## Testing

Test each server individually:

```bash
# Test arxiv server
python mcp_servers/arxiv-mcp/server.py

# Test with query
python -c "
import asyncio
from mcp_servers.arxiv_mcp import server
asyncio.run(server.search_arxiv('transformer attention'))
"
```
