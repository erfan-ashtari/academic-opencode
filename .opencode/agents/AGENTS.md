# AGENTS.md — Agents

## Purpose
Agent definitions for specialized academic tasks.

## Agent Categories

### Research Agents

| Agent | Purpose | Skills Used |
|-------|---------|-------------|
| `research-agent` | Multi-source paper search | paper-search, citation-manager |
| `writing-agent` | Paper writing pipeline | paper-writing, citation-manager, latex-assistant, reference-validator |
| `review-agent` | Systematic literature review | literature-review, paper-search, paper-review, reference-validator |

### Support Agents

| Agent | Purpose | Skills Used |
|-------|---------|-------------|
| `teacher` | Academic tutoring | teach-subject, paper-search |
| `summarizer` | Paper summarization | summarize-paper, document-converter |

### Orchestration

| Agent | Purpose | Skills Used |
|-------|---------|-------------|
| `sisyphus` | Main orchestrator | ALL skills and agents |

### Consultation

| Agent | Purpose | Skills Used |
|-------|---------|-------------|
| `oracle` | Architecture consultant | None (read-only) |
| `librarian` | External docs search | None (web search) |
| `explore` | Fast codebase grep | None (code search) |
| `multimodal-looker` | Media analysis | None (visual analysis) |
| `metis` | Pre-planning consultant | None (analysis) |
| `momus` | Plan critic | None (review) |
| `atlas` | Code search | None (code search) |

## Development Guidelines

### Adding a New Agent

1. Create directory: `.opencode/agents/{agent-name}/`
2. Create `AGENT.md` with frontmatter:

```yaml
---
model: opencode/mimo-v2.5-free
temperature: 0.7
thinking:
  type: enabled
  budgetTokens: 16000
---
```

3. Document agent purpose and capabilities
4. List skills the agent uses
5. Add routing rules to root `AGENTS.md`

### Agent Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `model` | Yes | Model to use |
| `temperature` | No | Temperature setting (0.0-1.0) |
| `thinking` | No | Extended thinking configuration |
| `reasoningEffort` | No | Reasoning effort level |

### Agent Content Structure

```markdown
# Agent Name

## Purpose
Brief description of what this agent does.

## Capabilities
- Capability 1
- Capability 2

## Skills Used
- skill-1
- skill-2

## When to Use
Describe scenarios where this agent should be spawned.

## Output Format
Describe expected output format.

## Examples
Show usage examples.
```

## Agent Routing Rules

Agents are spawned based on query intent:

| Query Pattern | Agent Spawned | Skills Loaded |
|---------------|---------------|---------------|
| "search for papers", "find research" | `research-agent` | `paper-search` |
| "review literature", "systematic review" | `review-agent` | `literature-review`, `paper-search` |
| "write paper", "draft section" | `writing-agent` | `paper-writing`, `citation-manager` |
| "format citation", "bibliography" | `Sisyphus-Junior` | `citation-manager` |
| "compose email", "submission email" | `Sisyphus-Junior` | `email-composer` |
| "review paper", "critique methodology" | `review-agent` | `paper-review` |
| "explain paper", "summarize findings" | `Sisyphus-Junior` | `paper-review` |
| "convert PDF", "extract text" | `Sisyphus-Junior` | `document-converter` |
| "find LaTeX template" | `Sisyphus-Junior` | `latex-assistant` |
| Any DOI (10.xxxx/xxxxx) | `research-agent` | `paper-search`, `citation-manager` |

## Dependencies

- Agents depend on: Skills, MCP servers
- Agents are used by: Commands, Sisyphus orchestrator
- Agents are discovered from: `.opencode/agents/*/AGENT.md`
