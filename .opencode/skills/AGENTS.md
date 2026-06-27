# AGENTS.md — Skills

## Purpose
Skill definitions for the Academic Research Assistant.

## Skill Categories

### Core Academic Skills

| Skill | Purpose | MCP Servers |
|-------|---------|-------------|
| `paper-search` | Multi-database paper search | arxiv, semantic-scholar, pubmed, ieee, acm, openalex, crossref, ssrn, dblp, biorxiv, europepmc, google-scholar, zotero |
| `paper-writing` | Section drafting with citations | citation-manager, latex-assistant, reference-validator, paper-search |
| `literature-review` | PRISMA-compliant reviews | paper-search, citation-manager, document-converter |
| `citation-manager` | Citation formatting (6 styles) | crossref, semantic-scholar, zotero |

### Quality Assurance Skills

| Skill | Purpose | MCP Servers |
|-------|---------|-------------|
| `paper-review` | Expert paper critique | document-converter, paper-search, citation-manager |
| `anti-hallucination` | Citation verification | reference-validator, paper-search |
| `reference-validator` | DOI validation | crossref, semantic-scholar |

### Support Skills

| Skill | Purpose | MCP Servers |
|-------|---------|-------------|
| `email-composer` | Academic correspondence | None |
| `document-converter` | PDF/DOCX conversion | None |
| `latex-assistant` | LaTeX support | None |
| `deep-research` | Structured research | All academic MCPs |
| `academic-pipeline` | 7-stage orchestration | All academic MCPs |
| `summarize-paper` | Paper summaries | document-converter |
| `teach-subject` | Concept explanation | paper-search |
| `zotero-integration` | Reference management | zotero |

## Development Guidelines

### Adding a New Skill

1. Create directory: `.opencode/skills/{skill-name}/`
2. Create `SKILL.md` with required frontmatter:

```yaml
---
name: skill-name
description: Brief description for triggering (include trigger phrases)
hidden: false  # optional
---
```

3. Document MCP server dependencies in frontmatter:

```yaml
---
name: paper-search
description: Search for academic papers...
mcp:
  arxiv:
    command: python
    args: ["mcp_servers/arxiv-mcp/server.py"]
  semantic-scholar:
    command: python
    args: ["mcp_servers/semantic-scholar-mcp/server.py"]
---
```

4. Include trigger phrases in description
5. Document expected input/output formats
6. Add examples of usage

### Skill Frontmatter Requirements

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Lowercase, hyphenated (e.g., `paper-search`) |
| `description` | Yes | Include trigger phrases for auto-detection |
| `hidden` | No | Hide from available skills list |
| `mcp` | No | MCP server dependencies |

### Skill Content Structure

```markdown
# Skill Title

Brief overview of what the skill does.

## How It Works

1. Step 1
2. Step 2
3. Step 3

## Input

Describe expected input format.

## Output

Describe output format.

## Examples

Show usage examples.

## Dependencies

List MCP servers and other skills required.
```

## Trigger Phrase Guidelines

Include natural language triggers in descriptions:

- "search for papers", "find research", "look up studies"
- "write paper", "draft section", "abstract", "introduction"
- "review literature", "systematic review", "survey papers"
- "format citation", "bibliography", "reference list"
- "compose email", "send to professor", "submission email"

## Dependencies

- Skills depend on: MCP servers, other skills
- Skills are used by: Agents, commands
- Skills are discovered from: `.opencode/skills/**/SKILL.md`
