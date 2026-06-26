---
name: review-agent
description: Automates systematic literature review workflows with PRISMA compliance
type: agent
capabilities:
  - screening-automation
  - quality-assessment
  - data-extraction
  - synthesis-support
  - prisma-reporting
---

# Review Agent

Automates systematic literature review workflows including screening, quality assessment, data extraction, and synthesis.

## Capabilities

| Capability | Description |
|------------|-------------|
| screening-automation | Title/abstract and full-text screening |
| quality-assessment | Evaluate methodology using validated tools |
| data-extraction | Pull findings from papers into structured forms |
| synthesis-support | Identify themes, gaps, and patterns |
| prisma-reporting | Generate PRISMA-compliant flow diagrams |

## Configuration

```yaml
agent:
  name: review-agent
  criteria:
    - sample_size
    - methodology
    - validity
    - reliability
    - generalizability
  quality_tools:
    - cochrane_rob
    - newcastle_ottawa
    - jbi_appraisal
    - casp_checklist
```

## Workflow

```
Review Request
    │
    ▼
┌─────────────────┐
│ Define Scope     │
│ Set Criteria     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Execute         │
│ Searches        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Screen          │
│ Papers          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Extract Data    │
│ from Papers     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Assess          │
│ Quality         │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Synthesize      │
│ Findings        │
└────────┬────────┘
         │
         ▼
    Review Report
```

## Inter-Agent Communication

```json
{
  "agent": "review-agent",
  "action": "screen_batch",
  "params": {
    "papers": [...],
    "criteria": {
      "include": ["peer-reviewed", "english", "2010-2024"],
      "exclude": ["case-reports", "editorials"]
    }
  },
  "result": {
    "included": [...],
    "excluded": [...],
    "reasons": {...}
  }
}
```

## Dependencies

- `skills/literature-review`
- `skills/paper-search` (with web fallback)
- `skills/paper-review`
- `skills/reference-validator`

## Fallback Behavior

When MCP servers are unavailable, the review-agent delegates to `paper-search`'s web fallback mode.
Search results from web fallback are tagged with `source: "web-fallback"` and `fallback: true`.

**Fallback sites** (only sites covered by our MCPs):
- arxiv.org, pubmed.ncbi.nlm.nih.gov, semanticscholar.org
- ieeexplore.ieee.org, dl.acm.org, openalex.org
- doi.org, ssrn.com, dblp.org
- biorxiv.org, europepmc.org, scholar.google.com

**Limitations:**
- Abstracts may be truncated or missing
- No citation count data
- Full-text access requires manual retrieval
