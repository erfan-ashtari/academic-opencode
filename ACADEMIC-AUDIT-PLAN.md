# Academic Research Assistant - Comprehensive Audit & Improvement Plan

## Date: June 27, 2026
## Project: Academic Research Assistant (v0.1)

---

## 1. PROJECT OVERVIEW

**What this project is:** An academic research workspace powered by OpenCode + oh-my-openagent with 14 MCP servers covering all major academic fields. It transforms a coding assistant into a full-featured research powerhouse with automatic intent detection and intelligent agent routing.

**What it does:**
- Searches 13+ academic databases simultaneously
- Manages citations in 6 styles (APA, IEEE, Chicago, MLA, Harvard, Vancouver)
- Writes paper sections with proper structure and citations
- Conducts systematic literature reviews with PRISMA methodology
- Reviews papers with expert-level critique
- Composes professional academic emails
- Converts PDFs/Office documents to Markdown
- Provides LaTeX templates and compilation support
- Detects academic intent automatically and routes to specialized agents

---

## 2. DIRECTORY STRUCTURE & DEPENDENCY MAP

```
first_academic_project/
├── .opencode/                          # PRIMARY: OpenCode configuration
│   ├── oh-my-openagent.jsonc           # Agent/model/category configuration
│   ├── academic-mode.json              # Auto-detection config
│   ├── package.json                    # Plugin dependency (@opencode-ai/plugin)
│   ├── agents/                         # 15 agent definitions
│   │   ├── sisyphus.md                 # Main orchestrator
│   │   ├── research-agent/AGENT.md     # Multi-source paper search
│   │   ├── writing-agent/AGENT.md      # Paper writing pipeline
│   │   ├── review-agent/AGENT.md       # Systematic literature review
│   │   ├── oracle.md                   # Architecture consultant
│   │   ├── librarian.md                # External docs search
│   │   ├── explore.md                  # Fast codebase grep
│   │   ├── teacher.md                  # Academic tutor
│   │   ├── summarizer.md              # Paper summarizer
│   │   └── [7 more agents]
│   ├── skills/                         # 15 skill definitions
│   │   ├── paper-search/SKILL.md       # Core: Multi-database search
│   │   ├── paper-writing/SKILL.md      # Core: Section drafting
│   │   ├── literature-review/SKILL.md  # Core: PRISMA reviews
│   │   ├── citation-manager/SKILL.md   # Core: Citation formatting
│   │   ├── paper-review/SKILL.md       # Expert paper critique
│   │   ├── anti-hallucination/SKILL.md # Citation verification
│   │   ├── reference-validator/SKILL.md# DOI validation
│   │   ├── email-composer/SKILL.md     # Academic emails
│   │   ├── document-converter/SKILL.md # PDF/DOCX conversion
│   │   ├── latex-assistant/SKILL.md    # LaTeX support
│   │   ├── deep-research/SKILL.md      # Structured research
│   │   ├── academic-pipeline/SKILL.md  # 7-stage orchestration
│   │   ├── summarize-paper/SKILL.md    # Paper summaries
│   │   ├── teach-subject/SKILL.md      # Concept explanation
│   │   └── zotero-integration/SKILL.md # Reference management
│   ├── commands/                       # 19 slash commands
│   │   ├── search-papers.md
│   │   ├── write-paper.md
│   │   ├── review-literature.md
│   │   ├── format-citations.md
│   │   ├── verify-citations.md
│   │   ├── compose-email.md
│   │   ├── deep-research.md
│   │   ├── start-pipeline.md
│   │   └── [11 more commands]
│   ├── rules/                          # 5 context-specific rules
│   │   ├── papers.md
│   │   ├── thesis.md
│   │   ├── proposals.md
│   │   ├── research.md
│   │   └── emails.md
│   └── shared/                         # 2 shared resources
│       ├── protocols.md                # Standard operating procedures
│       └── schemas.md                  # Data formats and contracts
├── .mimocode/                          # SECONDARY: Mimicode configuration
│   ├── oh-my-openagent.jsonc           # Agent/model/category configuration
│   ├── skills/                         # Skill definitions
│   ├── agents/                         # Agent definitions
│   └── shared/                         # Shared protocols
├── mcp_servers/                        # 14 MCP server implementations
│   ├── fallback_utils.py               # Shared fallback utilities
│   ├── arxiv-mcp/server.py
│   ├── semantic-scholar-mcp/server.py
│   ├── pubmed-mcp/server.py
│   ├── ieee-xplore-mcp/server.py
│   ├── acm-dl-mcp/server.py
│   ├── openalex-mcp/server.py
│   ├── crossref-mcp/server.py
│   ├── ssrn-mcp/server.py
│   ├── dblp-mcp/server.py
│   ├── biorxiv-mcp/server.py
│   ├── europepmc-mcp/server.py
│   ├── google-scholar-mcp/server.py
│   ├── zotero-mcp/server.py
│   └── document-converter/
├── templates/                          # Document templates
│   ├── email/                          # 6 email templates
│   ├── emails/                         # Empty directory
│   ├── latex/                          # LaTeX templates
│   └── markdown/                       # Markdown templates
├── .env                                # Environment variables
├── .mcp.json                           # MCP server definitions
├── opencode.json                       # OpenCode config
├── mimocode.json                       # Mimicode config
├── AGENTS.md                           # Agent auto-detection rules
├── CLAUDE.md                           # Agent identity/behavioral standards
├── ACADEMIC-REFERENCE.md               # Comprehensive reference guide
├── README.md                           # Project documentation
└── .gitignore
```

---

## 3. DEPENDENCY ANALYSIS

### Critical Dependencies (Layered)

```
Layer 0: Foundation
├── fallback_utils.py                    # Used by ALL MCP servers
├── .env                                # API keys for MCP servers
└── .mcp.json                           # MCP server definitions

Layer 1: MCP Servers (depend on Layer 0)
├── arxiv-mcp → fallback_utils.py
├── semantic-scholar-mcp → fallback_utils.py
├── pubmed-mcp → fallback_utils.py
├── [10 more MCP servers] → fallback_utils.py

Layer 2: Skills (depend on Layer 1)
├── paper-search → MCP servers (13) OR web fallback
├── citation-manager → Crossref MCP, Semantic Scholar MCP, Zotero MCP
├── literature-review → paper-search, citation-manager, document-converter
├── paper-writing → citation-manager, latex-assistant, reference-validator, paper-search
├── paper-review → document-converter, paper-search, citation-manager
├── anti-hallucination → reference-validator, paper-search
└── academic-pipeline → ALL academic skills

Layer 3: Agents (depend on Layer 2)
├── research-agent → paper-search skill, ALL MCP servers
├── writing-agent → paper-writing, citation-manager, latex-assistant, reference-validator
├── review-agent → literature-review, paper-search, paper-review, reference-validator
├── teacher → teach-subject skill, paper-search
├── summarizer → summarize-paper skill, document-converter
└── sisyphus → ALL skills and agents

Layer 4: Commands (depend on Layer 3)
├── /search-papers → research-agent → paper-search → MCP servers
├── /write-paper → writing-agent → paper-writing, citation-manager
├── /review-literature → review-agent → literature-review, paper-search
├── /verify-citations → anti-hallucination + reference-validator
└── [14 more commands]

Layer 5: Configuration (depends on all layers)
├── AGENTS.md → Defines routing rules for all agents/skills
├── CLAUDE.md → Behavioral standards for all agents
├── ACADEMIC-REFERENCE.md → Comprehensive reference for all components
├── oh-my-openagent.jsonc → Agent/model/category configuration
└── academic-mode.json → Auto-detection configuration
```

---

## 4. ISSUES & GAPS IDENTIFIED

### 4.1 Structural Issues

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| 1 | **Duplicate configuration**: `.opencode/` and `.mimocode/` are nearly identical mirrors | Medium | `.mimocode/` |
| 2 | **Empty directory**: `templates/emails/` is empty while `templates/email/` has templates | Low | `templates/emails/` |
| 3 | **Missing AGENTS.md in subdirectories**: No hierarchical AGENTS.md files | Medium | `mcp_servers/`, `templates/` |
| 4 | **Inconsistent naming**: `email/` vs `emails/`, `email-composer` vs `compose-email` | Low | `templates/`, `commands/` |
| 5 | **Missing `.dev/` skill**: `.opencode/skills/.dev/` exists but is not documented | Low | `.opencode/skills/.dev/` |

### 4.2 Functional Gaps

| # | Gap | Impact | Related Feature |
|---|-----|--------|-----------------|
| 1 | **No citation network visualization** | Missing from roadmap | Literature review |
| 2 | **No automated related work generation** | Missing from roadmap | Paper writing |
| 3 | **No journal/conference recommendation engine** | Missing from roadmap | Paper submission |
| 4 | **No figure/table extraction from PDFs** | Missing from roadmap | Document conversion |
| 5 | **No multi-language paper support** | Missing from roadmap | International research |
| 6 | **No Zotero library synchronization** | Missing from roadmap | Reference management |
| 7 | **No BibTeX auto-generation from search results** | Missing from roadmap | Citation management |
| 8 | **No full-text access/download** | Only metadata/search | MCP servers |
| 9 | **No plagiarism detection** | Critical for academic integrity | Quality assurance |
| 10 | **No research data management** | Missing workflow | Research projects |

### 4.3 Configuration Issues

| # | Issue | Impact | Fix Required |
|---|-------|--------|--------------|
| 1 | **Model fallback chains incomplete** | Agents may fail without fallback | Add comprehensive fallback chains |
| 2 | **Missing `reasoningEffort` for deep tasks** | Suboptimal reasoning | Configure reasoning effort levels |
| 3 | **No `thinking` configuration** | Missing extended thinking support | Add thinking budget configs |
| 4 | **Team mode disabled** | Cannot leverage parallel agents | Enable with proper config |
| 5 | **Missing custom categories** | No academic-specific categories | Add `academic-research`, `academic-writing` categories |

### 4.4 Skill Issues

| # | Issue | Impact | Location |
|---|-------|--------|----------|
| 1 | **Skills lack embedded MCPs** | Skills don't auto-configure MCP servers | All SKILL.md files |
| 2 | **Missing skill dependencies declaration** | Unclear which skills need which | SKILL.md frontmatter |
| 3 | **No skill versioning** | Cannot track skill evolution | All skills |
| 4 | **Incomplete fallback documentation** | Inconsistent fallback behavior | Multiple skills |

---

## 5. IMPROVEMENT RECOMMENDATIONS

### 5.1 High Priority (Critical for Functionality)

#### 5.1.1 Consolidate Configuration Files
**Problem**: `.opencode/` and `.mimocode/` are near-identical mirrors, causing maintenance burden.

**Solution**: 
- Remove `.mimocode/` directory entirely
- Update `mimocode.json` to reference `.opencode/` paths
- OR: Keep both but use symlinks for shared content

**Files to modify**:
- Delete: `.mimocode/` entire directory
- Modify: `mimocode.json` → change `skills.paths` to `[".opencode/skills"]`
- Modify: `.gitignore` → update `.mimicode/` references

#### 5.1.2 Add Hierarchical AGENTS.md Files
**Problem**: No directory-specific context files for subdirectories.

**Solution**: Create AGENTS.md files in:
- `mcp_servers/AGENTS.md` — MCP server development guidelines
- `templates/AGENTS.md` — Template usage guidelines
- `.opencode/skills/AGENTS.md` — Skill development guidelines
- `.opencode/agents/AGENTS.md` — Agent definition guidelines

**Template for each**:
```markdown
# AGENTS.md — [Directory Name]

## Purpose
[What this directory contains and why]

## File Structure
[Key files and their roles]

## Development Guidelines
[How to add/modify files here]

## Dependencies
[What this directory depends on and what depends on it]
```

#### 5.1.3 Enhance oh-my-openagent.jsonc Configuration
**Problem**: Missing advanced features from oh-my-openagent.

**Solution**: Add to `.opencode/oh-my-openagent.jsonc`:

```jsonc
{
  // Add academic-specific categories
  "categories": {
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
      "thinking": { "type: "enabled", "budgetTokens": 8000 },
      "prompt_append": "You are an academic writer. Use formal tone, proper citations, and follow venue guidelines."
    }
  },
  
  // Add thinking configurations for agents
  "agents": {
    "sisyphus": {
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    },
    "oracle": {
      "thinking": { "type": "enabled", "budgetTokens": 32000 }
    }
  },
  
  // Enable tmux visualization
  "tmux": {
    "enabled": true,
    "layout": "main-vertical"
  },
  
  // Add ralph loop configuration
  "ralph_loop": {
    "enabled": true,
    "default_max_iterations": 100
  }
}
```

### 5.2 Medium Priority (Enhance Capabilities)

#### 5.2.1 Add Missing MCP Servers
**Problem**: Missing key academic databases and tools.

**New MCP Servers to Add**:

| Server | Purpose | Priority |
|--------|---------|----------|
| `scopus-mcp` | Elsevier Scopus database | High |
| `acl-anthology-mcp` | ACL/EMNLP/NAACL papers | Medium |
| `open-citations-mcp` | Citation graph traversal | Medium |
| `unpaywall-mcp` | Open access PDF resolution | Medium |
| `wikipedia-mcp` | Concept background | Low |

**Implementation Template**:
```python
# mcp_servers/scopus-mcp/server.py
from fastmcp import FastMCP
from fallback_utils import enrich_result, enrich_results_list, web_search_fallback

mcp = FastMCP("scopus-search")

@mcp.tool()
async def search_scopus(query: str, max_results: int = 10) -> list[dict]:
    """Search Scopus for academic papers."""
    # Implementation with fallback
    pass
```

**Add to `.mcp.json`**:
```json
{
  "scopus": {
    "type": "stdio",
    "command": "python",
    "args": ["mcp_servers/scopus-mcp/server.py"]
  }
}
```

#### 5.2.2 Enhance Fallback Utilities
**Problem**: Current fallback returns placeholder data, not real results.

**Solution**: Improve `fallback_utils.py`:

```python
# Add to fallback_utils.py
import httpx
from bs4 import BeautifulSoup

async def real_web_search_fallback(
    query: str,
    mcp_name: str,
    max_results: int = 10,
) -> List[Dict[str, Any]]:
    """Perform actual web search and parse results."""
    domain = MCP_SITE_DOMAINS.get(mcp_name)
    if not domain:
        return []
    
    # Use Jina Reader API for clean extraction
    search_url = f"https://s.jina.ai/site:{domain} {query}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(search_url, timeout=30)
        if response.status_code == 200:
            # Parse results using BeautifulSoup or regex
            return parse_search_results(response.text, mcp_name)
    
    return []
```

#### 5.2.3 Add Skill-Embedded MCPs
**Problem**: Skills don't auto-configure their required MCP servers.

**Solution**: Update SKILL.md files to include MCP configuration:

```markdown
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
  # ... other MCPs
---

# Paper Search Skill
[content...]
```

#### 5.2.4 Add Missing Skills
**Problem**: Missing skills for common academic tasks.

**New Skills to Add**:

| Skill | Purpose | Trigger Phrases |
|-------|---------|-----------------|
| `plagiarism-check` | Detect potential plagiarism | "check plagiarism", "detect copied text" |
| `citation-network` | Visualize citation relationships | "citation graph", "who cites this" |
| `research-gap` | Identify research gaps | "research gaps", "what's missing" |
| `methodology-advisor` | Recommend research methods | "which method", "research design" |
| `statistical-analysis` | Help with statistical analysis | "statistical test", "analyze data" |
| `figure-generator` | Create publication-ready figures | "create figure", "generate chart" |

**Example: `plagiarism-check/SKILL.md`**:
```markdown
---
name: plagiarism-check
description: Detect potential plagiarism and verify originality in academic writing
triggers:
  - "check plagiarism"
  - "detect copied text"
  - "verify originality"
  - "plagiarism scan"
---

# Plagiarism Check Skill

Detects potential plagiarism by comparing text against academic databases and web sources.

## How It Works

1. Extract text from document
2. Break into searchable chunks
3. Search each chunk against:
   - Academic databases (via MCP servers)
   - Web sources (via websearch)
4. Compare and score similarity
5. Generate report with flagged sections

## Report Format

[template...]
```

### 5.3 Low Priority (Polish & Optimization)

#### 5.3.1 Clean Up Empty/Redundant Files
**Files to Remove/Consolidate**:
- `templates/emails/` (empty) → merge into `templates/email/`
- `.opencode/skills/.dev/` → document or remove
- Duplicate documentation between `AGENTS.md`, `CLAUDE.md`, and `ACADEMIC-REFERENCE.md`

#### 5.3.2 Add Missing Documentation
**Files to Create**:
- `CONTRIBUTING.md` — How to contribute to the project
- `CHANGELOG.md` — Version history
- `mcp_servers/README.md` — MCP server development guide
- `templates/README.md` — Template usage guide

#### 5.3.3 Optimize Configuration
**Improvements**:
- Add model fallback chains for all agents
- Configure thinking budgets for complex tasks
- Enable tmux visualization for parallel agents
- Add custom error handling rules

---

## 6. IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1)
1. Consolidate `.opencode/` and `.mimicode/` configurations
2. Create hierarchical AGENTS.md files
3. Enhance `oh-my-openagent.jsonc` with academic categories
4. Clean up empty/redundant files

### Phase 2: Core Enhancements (Week 2)
1. Improve `fallback_utils.py` with real web search
2. Add skill-embedded MCPs to SKILL.md files
3. Add missing MCP servers (scopus, acl-anthology)
4. Enhance model fallback chains

### Phase 3: New Capabilities (Week 3)
1. Add `plagiarism-check` skill
2. Add `citation-network` skill
3. Add `research-gap` skill
4. Add `figure-generator` skill

### Phase 4: Polish (Week 4)
1. Add missing documentation files
2. Optimize configuration for performance
3. Test all workflows end-to-end
4. Create usage examples and tutorials

---

## 7. DEPENDENCY GRAPH (VISUAL)

```
                    ┌─────────────────────────────────────┐
                    │           oh-my-openagent           │
                    │         (orchestration layer)       │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────┴──────────────────────┐
                    │              Sisyphus               │
                    │         (main orchestrator)         │
                    └──────────────┬──────────────────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
        ▼                          ▼                          ▼
┌───────────────┐        ┌───────────────┐        ┌───────────────┐
│ research-agent│        │ writing-agent │        │ review-agent  │
└───────┬───────┘        └───────┬───────┘        └───────┬───────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐        ┌───────────────┐        ┌───────────────┐
│ paper-search  │        │ paper-writing │        │literature-rev │
└───────┬───────┘        └───────┬───────┘        └───────┬───────┘
        │                        │                        │
        ▼                        ▼                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                         MCP Servers                            │
│  arxiv │ semantic-scholar │ pubmed │ ieee │ acm │ openalex │ ...│
└─────────────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│                       fallback_utils.py                         │
│              (shared fallback utilities)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. SUCCESS METRICS

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| MCP Servers | 14 | 18+ | Count in `.mcp.json` |
| Skills | 15 | 20+ | Count in `.opencode/skills/` |
| Agents | 15 | 15 (optimize existing) | Count in `.opencode/agents/` |
| Commands | 19 | 25+ | Count in `.opencode/commands/` |
| Fallback Success Rate | ~50% | 90%+ | Test each MCP server |
| Documentation Coverage | 70% | 95% | Files with README/AGENTS.md |
| Configuration Completeness | 60% | 90% | Missing fields in configs |
