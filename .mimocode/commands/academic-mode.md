---
description: Check academic mode status (auto-detected with agent spawning)
---

# /academic-mode

Academic tools are **auto-detected** with automatic agent spawning and skill loading. No manual toggle needed.

## How It Works

When you ask a research-related question, the agent automatically:

1. **Detects intent** from your query
2. **Spawns the right subagent** (research-agent, review-agent, writing-agent, etc.)
3. **Loads relevant skills** (paper-search, citation-manager, etc.)
4. **Executes the workflow** in parallel

## Auto-Spawning Rules

| Intent | Spawn Agent | Load Skills |
|--------|-------------|-------------|
| "search for papers", "find research" | `research-agent` | `["paper-search"]` |
| "review literature", "systematic review" | `review-agent` | `["literature-review", "paper-search"]` |
| "write paper", "draft section" | `writing-agent` | `["paper-writing", "citation-manager"]` |
| "format citation", "bibliography" | `Sisyphus-Junior` | `["citation-manager"]` |
| "compose email", "send to professor" | `Sisyphus-Junior` | `["email-composer"]` |
| "review paper", "critique" | `review-agent` | `["paper-review"]` |
| "explain paper", "summarize findings" | `Sisyphus-Junior` | `["paper-review"]` |
| "convert PDF", "extract text" | `Sisyphus-Junior` | `["document-converter"]` |
| "find LaTeX template" | `Sisyphus-Junior` | `["latex-assistant"]` |
| Query with DOI (10.xxxx/xxxxx) | `research-agent` | `["paper-search", "citation-manager"]` |

## Example

**User:** "find recent papers on transformer attention"

**Agent auto-executes:**
1. Detects: paper search intent
2. Spawns: `research-agent`
3. Loads: `["paper-search"]`
4. Runs: parallel search across arXiv, Semantic Scholar, IEEE

No commands needed. Just ask naturally.
