---
name: literature-review
description: Conduct systematic literature reviews with PRISMA 2020 methodology, citation snowballing, quality assessment, screening workflows, data extraction, and evidence synthesis.
triggers:
  - "Review literature on..."
  - "Conduct systematic review..."
  - "Find related work..."
  - "Perform literature review on..."
  - "Run systematic literature review"
  - "Survey the state of the art on..."
  - "Write related work section..."
  - "Synthesize papers on..."
  - "Snowball citations from..."
  - "Screen papers for..."
---

# Literature Review Skill

Conduct systematic literature reviews with PRISMA 2020 methodology, citation snowballing, quality assessment, data extraction, and evidence synthesis.

## How It Works

1. **Planning**: Define research questions (PICO/PICo/PEO framework), develop protocol
2. **Searching**: Build and execute Boolean search queries across databases
3. **Screening**: Remove duplicates, perform title/abstract and full-text screening
4. **Extraction**: Extract structured data from included studies
5. **Quality Assessment**: Evaluate methodological quality using validated tools
6. **Synthesis**: Synthesize findings, generate PRISMA flow diagram

## Review Types

| Type | Description | When to Use |
|------|-------------|-------------|
| Systematic | Comprehensive with PRISMA compliance | Evidence synthesis, meta-analysis |
| Scoping | Map evidence without quality assessment | Broad questions, gap identification |
| Narrative | Thematic synthesis | Exploratory research |
| Rapid | Accelerated review | Time-constrained decisions |
| Meta-analysis | Quantitative synthesis | Combining similar studies |

## Screening Workflow

### Phase 1: Title/Abstract
- **[INCLUDE]** - Proceed to full-text
- **[EXCLUDE]** - Record reason
- **[UNCLEAR]** - Flag for full-text review

### Phase 2: Full-Text
- Apply same criteria to complete paper
- Record exclusion reasons for PRISMA

## Quality Assessment Tools

| Tool | Study Types |
|------|-------------|
| Cochrane ROB-2 | RCTs |
| ROBINS-I | Non-randomized |
| Newcastle-Ottawa | Cohort/Case-control |
| CASP | Various designs |
| GRADE | Evidence certainty |

## Citation Snowballing

```bash
# Forward snowball (papers citing this one)
/snowball-citations --paper-id 1706.03762 --direction forward --depth 1

# Backward snowball (papers this one cites)
/snowball-citations --paper-id 1706.03762 --direction backward --depth 1

# Bidirectional
/snowball-citations --paper-id 1706.03762 --direction both --depth 2
```

## Output Structure

```
literature-review-YYYY-MM-DD/
├── protocol.md
├── search-strategies/
├── screening/
├── extraction/
├── quality/
├── synthesis/
└── report/
    ├── systematic-review.md
    └── prisma-flow.md
```

## Dependencies

| Component | Integration |
|-----------|-------------|
| Paper Search | Feed search results (with web fallback when MCPs unavailable) |
| Citation Manager | Format citations for included studies |
| Paper Writing | Provide findings for drafting |
| Document Converter | Convert PDFs for extraction |

## Fallback Behavior

When MCP servers are unavailable, the literature review skill falls back to web search.
The `paper-search` skill handles fallback automatically — see its fallback documentation.

**Fallback sites:**
- arxiv.org, pubmed.ncbi.nlm.nih.gov, semanticscholar.org, ieeexplore.ieee.org
- dl.acm.org, openalex.org, doi.org, ssrn.com, dblp.org
- biorxiv.org, europepmc.org, scholar.google.com

**Fallback workflow:**
1. Detect MCP unavailability via probe
2. Switch to `websearch` + `webfetch` for each allowed site
3. Parse HTML results into structured format
4. Tag all results with `source: "web-fallback"`
