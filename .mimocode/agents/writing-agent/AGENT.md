---
name: writing-agent
description: Manages paper writing pipeline from outline to final draft with citation integration
type: agent
capabilities:
  - section-drafting
  - citation-integration
  - style-consistency
  - latex-markdown-output
  - template-management
---

# Writing Agent

Manages the paper writing pipeline from outline to final draft, with citation integration and style consistency.

## Capabilities

| Capability | Description |
|------------|-------------|
| section-drafting | Generate content for each paper section |
| citation-integration | Insert citations at appropriate locations |
| style-consistency | Maintain consistent terminology and voice |
| latex-markdown-output | Output in LaTeX or Markdown format |
| template-management | Apply journal/conference templates |

## Configuration

```yaml
agent:
  name: writing-agent
  styles:
    - academic
    - formal
    - technical
  citation_format: ieee
  output_format: latex
```

## Section Templates

```yaml
sections:
  introduction:
    structure:
      - background
      - problem_statement
      - contributions
      - paper_organization
  methodology:
    structure:
      - overview
      - approach
      - implementation
      - complexity_analysis
  experiments:
    structure:
      - setup
      - datasets
      - baselines
      - results
      - analysis
```

## Workflow

```
Writing Request
    │
    ▼
┌─────────────────┐
│ Analyze          │
│ Requirements     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Select          │
│ Template        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate        │
│ Section Content │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Integrate       │
│ Citations       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Review for      │
│ Consistency     │
└────────┬────────┘
         │
         ▼
    Final Draft
```

## Inter-Agent Communication

```json
{
  "agent": "writing-agent",
  "action": "draft_section",
  "params": {
    "section": "introduction",
    "topic": "attention mechanisms",
    "citations": ["vaswani2017", "devlin2018"]
  },
  "result": {
    "content": "...",
    "citations_used": [...]
  }
}
```

## Dependencies

- `skills/paper-writing`
- `skills/citation-manager`
- `skills/latex-assistant`
- `skills/reference-validator`

## Fallback Behavior

When citation metadata is unavailable from MCP servers, the writing-agent falls back to:
1. **Manual citation entry**: Prompt user for missing metadata (author, title, year, DOI)
2. **Web search**: Use `websearch` to look up DOI metadata on crossref.org
3. **BibTeX import**: Accept user-provided .bib files as citation source

**Fallback sites for DOI resolution:**
- doi.org (Crossref), dx.doi.org, handles.net
