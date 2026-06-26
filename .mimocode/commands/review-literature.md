---
name: review-literature
description: Conduct systematic literature review with PRISMA compliance
arguments:
  - name: topic
    description: Research topic or question for the review
    required: true
  - name: type
    description: Review type (systematic, scoping, narrative, rapid)
    required: false
    default: systematic
  - name: databases
    description: Databases to search (comma-separated)
    required: false
    default: all
  - name: criteria
    description: Path to inclusion/exclusion criteria file
    required: false
  - name: format
    description: Output format (report, prisma, summary)
    required: false
    default: report
---

# Review Literature Command

Conduct systematic literature reviews following PRISMA guidelines.

## Usage

```bash
/review-literature "effect of exercise on depression" --type systematic
/review-literature "AI in healthcare" --databases pubmed,ieee-xplore
/review-literature --screen results.csv --criteria criteria.md
/review-literature --extract papers/ --template extraction.md
/review-literature --report --format prisma
```

## Review Types

| Type | Description |
|------|-------------|
| systematic | Comprehensive, reproducible protocol |
| scoping | Map available evidence |
| narrative | Thematic synthesis |
| rapid | Accelerated review |

## Workflow

1. Define scope and criteria
2. Execute multi-database searches
3. Screen title/abstract, then full-text
4. Extract data from included studies
5. Assess quality with validated tools
6. Synthesize findings
7. Generate PRISMA-compliant report

## Output

Returns:
- PRISMA flow diagram data
- Included/excluded studies with reasons
- Quality assessment scores
- Evidence tables
- Synthesized findings

## Skill Used

`literature-review`
