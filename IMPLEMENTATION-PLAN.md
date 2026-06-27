# Academic Research Assistant - Implementation Plan

## Date: June 27, 2026
## Status: IN PROGRESS

---

## EXECUTIVE SUMMARY

This plan covers the implementation of 9 major improvements to the Academic Research Assistant project. The work is organized into parallel workstreams where possible.

---

## WORKSTREAM 1: HIERARCHICAL AGENTS.MD FILES

### Goal
Create AGENTS.md files in key subdirectories to provide context-specific guidance.

### Files to Create

#### 1.1 `mcp_servers/AGENTS.md`
```markdown
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

## Dependencies
- Depends on: `fallback_utils.py`, `.env` (API keys)
- Used by: All academic skills (paper-search, citation-manager, etc.)
```

#### 1.2 `templates/AGENTS.md`
```markdown
# AGENTS.md — Templates

## Purpose
Document templates for academic communications and papers.

## File Structure
- `email/` — Email templates (inquiry, collaboration, submission, etc.)
- `latex/` — LaTeX templates (article, conference, thesis)
- `markdown/` — Markdown templates (paper, proposal, review)

## Usage
Templates are used by:
- `email-composer` skill → `email/` templates
- `paper-writing` skill → `latex/` and `markdown/` templates
- `latex-assistant` skill → `latex/` templates

## Adding Templates
1. Follow existing naming conventions
2. Include placeholder variables: `{TITLE}`, `{AUTHOR}`, `{DATE}`, etc.
3. Update relevant skill documentation
```

#### 1.3 `.opencode/skills/AGENTS.md`
```markdown
# AGENTS.md — Skills

## Purpose
Skill definitions for the Academic Research Assistant.

## Skill Categories

### Core Academic Skills
- `paper-search` — Multi-database paper search
- `paper-writing` — Section drafting with citations
- `literature-review` — PRISMA-compliant reviews
- `citation-manager` — Citation formatting (6 styles)

### Quality Assurance Skills
- `paper-review` — Expert paper critique
- `anti-hallucination` — Citation verification
- `reference-validator` — DOI validation

### Support Skills
- `email-composer` — Academic correspondence
- `document-converter` — PDF/DOCX conversion
- `latex-assistant` — LaTeX support
- `deep-research` — Structured research
- `academic-pipeline` — 7-stage orchestration
- `summarize-paper` — Paper summaries
- `teach-subject` — Concept explanation
- `zotero-integration` — Reference management

## Development Guidelines

### Adding a New Skill
1. Create directory: `.opencode/skills/{skill-name}/`
2. Create `SKILL.md` with required frontmatter:
   ```yaml
   ---
   name: skill-name
   description: Brief description for triggering
   ---
   ```
3. Include trigger phrases in description
4. Document MCP server dependencies
5. Add to relevant command definitions

### Skill Frontmatter Requirements
- `name` (required) — Lowercase, hyphenated
- `description` (required) — Include trigger phrases
- `hidden` (optional) — Hide from available skills list

## Dependencies
- Skills depend on: MCP servers, other skills
- Skills are used by: Agents, commands
```

#### 1.4 `.opencode/agents/AGENTS.md`
```markdown
# AGENTS.md — Agents

## Purpose
Agent definitions for specialized academic tasks.

## Agent Categories

### Research Agents
- `research-agent` — Multi-source paper search
- `writing-agent` — Paper writing pipeline
- `review-agent` — Systematic literature review

### Support Agents
- `teacher` — Academic tutoring
- `summarizer` — Paper summarization

### Orchestration
- `sisyphus` — Main orchestrator (routes to specialized agents)

## Development Guidelines

### Adding a New Agent
1. Create directory: `.opencode/agents/{agent-name}/`
2. Create `AGENT.md` with frontmatter:
   ```yaml
   ---
   model: opencode/mimo-v2.5-free
   temperature: 0.7
   ---
   ```
3. Document skills the agent uses
4. Add routing rules to `AGENTS.md` root

## Dependencies
- Agents depend on: Skills, MCP servers
- Agents are used by: Commands, Sisyphus orchestrator
```

---

## WORKSTREAM 2: ENHANCE OH-MY-OPENAGENT.JSONC

### Goal
Add academic-specific categories and optimize agent configurations.

### Changes to `.opencode/oh-my-openagent.jsonc`

```jsonc
{
  // ... existing config ...
  
  // Add academic-specific categories
  "categories": {
    // ... existing categories ...
    
    "academic-research": {
      "model": "opencode/mimo-v2.5-free",
      "temperature": 0.3,
      "reasoningEffort": "high",
      "thinking": { "type": "enabled", "budgetTokens": 16000 },
      "prompt_append": "You are an academic research specialist. Prioritize accuracy, cite sources, and follow academic standards."
    },
    "academic-writing": {
      "model": "opencode/mimo-v2.5-free",
      "temperature": 0.5,
      "reasoningEffort": "medium",
      "thinking": { "type": "enabled", "budgetTokens": 8000 },
      "prompt_append": "You are an academic writer. Use formal tone, proper citations, and follow venue guidelines."
    }
  },
  
  // Add thinking configurations for key agents
  "agents": {
    "sisyphus": {
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    },
    "oracle": {
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    },
    "research-agent": {
      "thinking": { "type": "enabled", "budgetTokens": 16000 }
    },
    "writing-agent": {
      "thinking": { "type": "enabled", "budgetTokens": 16000 }
    }
  }
}
```

---

## WORKSTREAM 3: CLEAN UP EMPTY/REDUNDANT FILES

### Goal
Remove empty directories and consolidate redundant files.

### Actions

#### 3.1 Remove empty `templates/emails/` directory
- Current: `templates/emails/` is empty
- Action: Delete directory

#### 3.2 Document or remove `.opencode/skills/.dev/`
- Current: `.opencode/skills/.dev/` exists but is undocumented
- Action: Check contents, either document or remove

#### 3.3 Consolidate duplicate documentation
- Current: `AGENTS.md`, `CLAUDE.md`, and `ACADEMIC-REFERENCE.md` overlap
- Action: Clarify purpose of each:
  - `AGENTS.md` — Auto-detection rules for agent spawning
  - `CLAUDE.md` — Agent identity and behavioral standards
  - `ACADEMIC-REFERENCE.md` — Comprehensive reference guide

---

## WORKSTREAM 4: IMPROVE FALLBACK_UTILS.PY

### Goal
Enhance fallback utilities with real web search capabilities.

### Changes to `mcp_servers/fallback_utils.py`

```python
# Add to existing fallback_utils.py

import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional

# Add Jina Reader API for real web search
JINA_SEARCH_URL = "https://s.jina.ai"
JINA Reader_API = "https://r.jina.ai"

async def real_web_search_fallback(
    query: str,
    mcp_name: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """
    Perform actual web search using Jina Reader API.
    Returns structured results similar to API responses.
    """
    domain = MCP_SITE_DOMAINS.get(mcp_name)
    if not domain:
        return []
    
    search_query = f"site:{domain} {query}"
    
    try:
        async with httpx.AsyncClient() as client:
            # Use Jina Search API
            response = await client.get(
                f"{JINA_SEARCH_URL}/{search_query}",
                headers={"Accept": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return parse_jina_results(data, mcp_name, max_results)
    except Exception as e:
        print(f"Jina search failed: {e}", file=sys.stderr)
    
    # Fallback to existing placeholder behavior
    return []

def parse_jina_results(
    data: dict,
    mcp_name: str,
    max_results: int
) -> List[Dict[str, Any]]:
    """Parse Jina Search API results into standard format."""
    results = []
    
    for item in data.get("data", [])[:max_results]:
        result = {
            "title": item.get("title", "Unknown Title"),
            "authors": extract_authors(item.get("content", "")),
            "abstract": item.get("content", "")[:500],
            "url": item.get("url", ""),
            "doi": extract_doi(item.get("url", "")),
            "year": extract_year(item.get("content", "")),
            "_metadata": {
                "mcp_name": mcp_name,
                "method": "websearch",
                "weblink": item.get("url", ""),
                "source": "jina"
            }
        }
        results.append(result)
    
    return results

def extract_authors(text: str) -> List[str]:
    """Extract author names from text."""
    # Simple heuristic - look for "by Author1, Author2" patterns
    import re
    match = re.search(r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:,\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)*)', text)
    if match:
        return [a.strip() for a in match.group(1).split(",")]
    return ["Unknown"]

def extract_doi(text: str) -> Optional[str]:
    """Extract DOI from text."""
    import re
    match = re.search(r'10\.\d{4,}/[^\s]+', text)
    return match.group(0) if match else None

def extract_year(text: str) -> Optional[int]:
    """Extract publication year from text."""
    import re
    match = re.search(r'\b(19|20)\d{2}\b', text)
    return int(match.group(0)) if match else None
```

---

## WORKSTREAM 5: ADD SKILL-EMBEDDED MCPS

### Goal
Update SKILL.md files to include MCP server configuration.

### Files to Update

#### 5.1 `.opencode/skills/paper-search/SKILL.md`
Add to frontmatter:
```yaml
---
name: paper-search
description: Search for academic papers across multiple databases...
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
---
```

#### 5.2 Other skills to update
- `citation-manager` → crossref, semantic-scholar, zotero
- `literature-review` → paper-search, citation-manager, document-converter
- `paper-writing` → citation-manager, latex-assistant, reference-validator, paper-search
- `paper-review` → document-converter, paper-search, citation-manager
- `anti-hallucination` → reference-validator, paper-search
- `reference-validator` → crossref, semantic-scholar

---

## WORKSTREAM 6: ADD MISSING MCP SERVERS

### Goal
Add Scopus and ACL Anthology MCP servers.

### 6.1 Scopus MCP Server

#### `mcp_servers/scopus-mcp/server.py`
```python
"""Scopus MCP Server - Elsevier Scopus database integration."""
import sys
import os
from typing import Optional
from fastmcp import FastMCP

# Add parent directory to path for fallback_utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fallback_utils import (
    web_search_fallback,
    enrich_result,
    enrich_results_list,
    get_api_key,
    handle_http_error,
)

mcp = FastMCP("scopus-search")

SCOPUS_API_BASE = "https://api.elsevier.com/content"

@mcp.tool()
async def search_scopus(
    query: str,
    max_results: int = 10,
    sort_by: str = "relevance",
    year_range: Optional[str] = None,
) -> list[dict]:
    """
    Search Scopus for academic papers.

    Args:
        query: Search query string
        max_results: Maximum results (default 10, max 25)
        sort_by: Sort by "relevance" or "citedby"
        year_range: Publication year range (e.g., "2020-2024")
    """
    api_key = get_api_key("SCOPUS_API_KEY")
    
    if not api_key:
        return await web_search_fallback(query, "scopus", max_results)
    
    try:
        import httpx
        
        headers = {
            "X-ELS-APIKey": api_key,
            "Accept": "application/json"
        }
        
        params = {
            "query": query,
            "count": min(max_results, 25),
            "sort": sort_by,
        }
        
        if year_range:
            params["date"] = year_range
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{SCOPUS_API_BASE}/search/scopus",
                headers=headers,
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("search-results", {}).get("entry", [])
                
                papers = []
                for entry in results:
                    paper = {
                        "title": entry.get("dc:title", "Unknown Title"),
                        "authors": [
                            a.get("ce:given-name", "") + " " + a.get("ce:surname", "")
                            for a in entry.get("dc:creator", []) if a
                        ] or ["Unknown"],
                        "abstract": entry.get("dc:description", ""),
                        "doi": entry.get("prism:doi"),
                        "url": entry.get("prism:url"),
                        "publication_date": entry.get("prism:coverDate"),
                        "citation_count": int(entry.get("citedby-count", 0)),
                        "source": entry.get("prism:publicationName"),
                        "_metadata": {
                            "mcp_name": "scopus",
                            "method": "api",
                            "weblink": entry.get("link", [{}])[0].get("@href", ""),
                        }
                    }
                    papers.append(paper)
                
                return papers
            else:
                return await web_search_fallback(query, "scopus", max_results)
                
    except Exception as e:
        print(f"Scopus API error: {e}", file=sys.stderr)
        return await web_search_fallback(query, "scopus", max_results)

if __name__ == "__main__":
    mcp.run()
```

#### Add to `.mcp.json`
```json
{
  "scopus": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/scopus-mcp/server.py"]
  }
}
```

### 6.2 ACL Anthology MCP Server

#### `mcp_servers/acl-anthology-mcp/server.py`
```python
"""ACL Anthology MCP Server - ACL/EMNLP/NAACL papers integration."""
import sys
import os
from typing import Optional
from fastmcp import FastMCP

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fallback_utils import (
    web_search_fallback,
    enrich_result,
    enrich_results_list,
)

mcp = FastMCP("acl-anthology-search")

ACL_ANTHOLOGY_API = "https://api.aclanthology.org"

@mcp.tool()
async def search_acl_anthology(
    query: str,
    max_results: int = 10,
    venue: Optional[str] = None,
    year: Optional[int] = None,
) -> list[dict]:
    """
    Search ACL Anthology for NLP/CL papers.

    Args:
        query: Search query string
        max_results: Maximum results (default 10)
        venue: Filter by venue (acl, emnlp, naacl, coling, etc.)
        year: Filter by year
    """
    try:
        import httpx
        
        params = {
            "q": query,
            "rows": max_results,
        }
        
        if venue:
            params["venue"] = venue
        if year:
            params["year"] = year
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ACL_ANTHOLOGY_API}/search",
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("hits", [])
                
                papers = []
                for hit in results:
                    paper = {
                        "title": hit.get("title", "Unknown Title"),
                        "authors": [a.get("name", "Unknown") for a in hit.get("authors", [])],
                        "abstract": hit.get("abstract", ""),
                        "doi": hit.get("doi"),
                        "url": hit.get("url", ""),
                        "publication_date": hit.get("date"),
                        "venue": hit.get("venue", ""),
                        "citation_count": hit.get("citedby", 0),
                        "_metadata": {
                            "mcp_name": "acl-anthology",
                            "method": "api",
                            "weblink": hit.get("url", ""),
                        }
                    }
                    papers.append(paper)
                
                return papers
            else:
                return await web_search_fallback(query, "acl-anthology", max_results)
                
    except Exception as e:
        print(f"ACL Anthology API error: {e}", file=sys.stderr)
        return await web_search_fallback(query, "acl-anthology", max_results)

if __name__ == "__main__":
    mcp.run()
```

#### Add to `.mcp.json`
```json
{
  "acl-anthology": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/acl-anthology-mcp/server.py"]
  }
}
```

---

## WORKSTREAM 7: ENHANCE MODEL FALLBACK CHAINS

### Goal
Add comprehensive fallback chains for all agents.

### Changes to `.opencode/oh-my-openagent.jsonc`

```jsonc
{
  // ... existing config ...
  
  // Enhanced agent configurations with fallbacks
  "agents": {
    "sisyphus": {
      "model": "opencode/mimo-v2.5-free",
      "fallback_models": ["opencode/deepseek-v4-flash-free", "opencode/mimo-v2.5-free"],
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    },
    "oracle": {
      "model": "opencode/mimo-v2.5-free",
      "fallback_models": ["opencode/deepseek-v4-flash-free"],
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    },
    "research-agent": {
      "model": "opencode/mimo-v2.5-free",
      "fallback_models": ["opencode/deepseek-v4-flash-free"],
      "thinking": { "type": "enabled", "budgetTokens": 16000 }
    },
    "writing-agent": {
      "model": "opencode/mimo-v2.5-free",
      "fallback_models": ["opencode/deepseek-v4-flash-free"],
      "thinking": { "type": "enabled", "budgetTokens": 16000 }
    },
    "review-agent": {
      "model": "opencode/mimo-v2.5-free",
      "fallback_models": ["opencode/deepseek-v4-flash-free"],
      "thinking": { "type": "enabled", "budgetTokens": 16000 }
    }
  }
}
```

---

## WORKSTREAM 8: ADD MISSING DOCUMENTATION

### Goal
Create comprehensive documentation files.

### Files to Create

#### 8.1 `CONTRIBUTING.md`
```markdown
# Contributing to Academic Research Assistant

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.10+
- Node.js 18+
- OpenCode CLI

### Installation
```bash
# Clone
git clone https://github.com/your-username/academic-opencode.git
cd academic-opencode

# Install dependencies
pip install httpx fastmcp scholarly

# Copy environment template
cp .env.example .env
```

## Adding a New MCP Server

1. Create directory: `mcp_servers/{name}-mcp/`
2. Create `server.py` using the template in `mcp_servers/AGENTS.md`
3. Add to `.mcp.json`
4. Update documentation

## Adding a New Skill

1. Create directory: `.opencode/skills/{skill-name}/`
2. Create `SKILL.md` with required frontmatter
3. Document MCP dependencies
4. Add trigger phrases to description

## Code Style

- Follow PEP 8 for Python
- Use type hints
- Add docstrings to all public functions
- Keep functions focused and small

## Testing

- Test MCP servers individually
- Test fallback behavior
- Test skill triggering

## Questions?

Open an issue or start a discussion.
```

#### 8.2 `CHANGELOG.md`
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.2.0] - 2026-06-27

### Added
- Scopus MCP server
- ACL Anthology MCP server
- Hierarchical AGENTS.md files
- Academic-specific categories in oh-my-openagent.jsonc
- Skill-embedded MCP configurations
- Enhanced fallback utilities with Jina Reader API
- Model fallback chains for all agents
- CONTRIBUTING.md
- CHANGELOG.md

### Changed
- Improved fallback_utils.py with real web search
- Enhanced oh-my-openagent.jsonc with thinking configurations
- Updated SKILL.md files with MCP dependencies

### Fixed
- Empty templates/emails/ directory removed
- Documentation consolidation

## [0.1.0] - 2026-06-20

### Added
- Initial release
- 14 MCP servers
- 15 skills
- 15 agents
- 19 commands
- Automatic intent detection
- Web search fallback system
```

#### 8.3 `mcp_servers/README.md`
```markdown
# MCP Servers

This directory contains MCP (Model Context Protocol) servers for academic database integration.

## Servers

| Server | Database | API Key Required |
|--------|----------|------------------|
| arxiv-mcp | arXiv | No |
| semantic-scholar-mcp | Semantic Scholar | Optional |
| pubmed-mcp | PubMed | Optional |
| ieee-xplore-mcp | IEEE Xplore | Yes |
| acm-dl-mcp | ACM Digital Library | No |
| openalex-mcp | OpenAlex | Optional |
| crossref-mcp | Crossref | Optional |
| ssrn-mcp | SSRN | No |
| dblp-mcp | DBLP | No |
| biorxiv-mcp | bioRxiv | No |
| europepmc-mcp | Europe PMC | No |
| google-scholar-mcp | Google Scholar | No |
| zotero-mcp | Zotero | Yes |
| scopus-mcp | Scopus | Yes |
| acl-anthology-mcp | ACL Anthology | No |

## Development

See `AGENTS.md` for development guidelines.

## Fallback System

All servers use `fallback_utils.py` for web search fallback when APIs fail.
```

#### 8.4 `templates/README.md`
```markdown
# Templates

Document templates for academic communications and papers.

## Email Templates

Located in `email/`:

- `inquiry.md` — Initial inquiry to professors
- `collaboration.md` — Research collaboration request
- `submission.md` — Paper submission notification
- `revision.md` — Revision submission
- `thank_you.md` — Thank you notes
- `follow_up.md` — Follow-up emails

## LaTeX Templates

Located in `latex/`:

- `article.md` — Standard article format
- `conference.md` — Conference paper format
- `thesis.md` — Thesis/dissertation format
- `elsevier/` — Elsevier journal templates
- `ieee/` — IEEE conference templates

## Markdown Templates

Located in `markdown/`:

- `paper.md` — Paper draft template
- `proposal.md` — Research proposal template
- `review.md` — Paper review template

## Usage

Templates are used by:
- `email-composer` skill → `email/` templates
- `paper-writing` skill → `latex/` and `markdown/` templates
- `latex-assistant` skill → `latex/` templates

## Placeholder Variables

- `{TITLE}` — Paper/project title
- `{AUTHOR}` — Author name(s)
- `{DATE}` — Date
- `{DOI}` — DOI identifier
- `{VENUE}` — Journal/conference name
- `{ABSTRACT}` — Abstract text
```

---

## WORKSTREAM 9: OPTIMIZE CONFIGURATION

### Goal
Optimize configurations for performance and reliability.

### 9.1 Update `.mcp.json` with new servers

```json
{
  "arxiv": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/arxiv-mcp/server.py"]
  },
  "semantic-scholar": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/semantic-scholar-mcp/server.py"]
  },
  "pubmed": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/pubmed-mcp/server.py"]
  },
  "ieee-xplore": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/ieee-xplore-mcp/server.py"]
  },
  "acm-dl": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/acm-dl-mcp/server.py"]
  },
  "openalex": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/openalex-mcp/server.py"]
  },
  "crossref": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/crossref-mcp/server.py"]
  },
  "ssrn": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/ssrn-mcp/server.py"]
  },
  "dblp": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/dblp-mcp/server.py"]
  },
  "biorxiv": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/biorxiv-mcp/server.py"]
  },
  "europepmc": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/europepmc-mcp/server.py"]
  },
  "google-scholar": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/google-scholar-mcp/server.py"]
  },
  "zotero": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/zotero-mcp/server.py"]
  },
  "scopus": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/scopus-mcp/server.py"]
  },
  "acl-anthology": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/acl-anthology-mcp/server.py"]
  }
}
```

### 9.2 Update `.env.example` with new keys

```bash
# Academic API Keys

# IEEE Xplore (Required)
IEEE_API_KEY=your_key_here

# Zotero (Required)
ZOTERO_API_KEY=your_key_here
ZOTERO_USER_ID=your_id_here

# Scopus (Required)
SCOPUS_API_KEY=your_key_here

# Optional - Improves reliability
SEMANTIC_SCHOLAR_API_KEY=your_key_here
NCBI_API_KEY=your_key_here
OPENALEX_EMAIL=your@email.com
CROSSREF_MAILTO=your@email.com
```

---

## IMPLEMENTATION ORDER

### Phase 1: Foundation (Immediate)
1. ✅ Save current plan to ACADEMIC-AUDIT-PLAN.md
2. Research OpenCode vs MiMo Code differences
3. Create hierarchical AGENTS.md files
4. Clean up empty/redundant files

### Phase 2: Core Enhancements
5. Improve fallback_utils.py with real web search
6. Add skill-embedded MCPs to SKILL.md files
7. Enhance oh-my-openagent.jsonc with academic categories

### Phase 3: New Capabilities
8. Add Scopus MCP server
9. Add ACL Anthology MCP server
10. Enhance model fallback chains

### Phase 4: Documentation
11. Add CONTRIBUTING.md
12. Add CHANGELOG.md
13. Add mcp_servers/README.md
14. Add templates/README.md

### Phase 5: Optimization
15. Update .mcp.json with new servers
16. Update .env.example with new keys
17. Final testing and validation

---

## SUCCESS CRITERIA

- [ ] All hierarchical AGENTS.md files created
- [ ] oh-my-openagent.jsonc enhanced with academic categories
- [ ] Empty/redundant files cleaned up
- [ ] fallback_utils.py enhanced with real web search
- [ ] All SKILL.md files updated with MCP dependencies
- [ ] Scopus MCP server implemented
- [ ] ACL Anthology MCP server implemented
- [ ] Model fallback chains configured
- [ ] All documentation files created
- [ ] .mcp.json updated with new servers
- [ ] .env.example updated with new keys
