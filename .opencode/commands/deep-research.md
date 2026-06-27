---
name: deep-research
description: Conduct structured deep research with outline generation, parallel investigation, and synthesis report
arguments:
  - name: topic
    description: Research topic or question to investigate
    required: true
  - name: scope
    description: Scope (narrow, broad) or specific aspect to focus on
    required: false
    default: broad
  - name: databases
    description: Databases to search (comma-separated, or 'all')
    required: false
    default: all
  - name: year
    description: Year range filter (e.g., '2020-2025')
    required: false
---

# Deep Research Command

Conduct structured deep research on complex topics with outline generation, parallel investigation, and synthesis.

## Usage

```bash
/deep-research "transformer attention mechanisms"
/deep-research "CRISPR gene editing" --scope narrow --year 2022-2025
/deep-research "AI in healthcare" --databases pubmed,arxiv
```

## Workflow

### Phase 1: Outline Generation
1. Analyze the research topic
2. Decompose into research items/questions
3. Define information fields to collect for each item
4. Present outline for user approval
5. Allow additions/removals before proceeding

### Phase 2: Deep Investigation
1. For each item, search multiple sources
2. Collect structured data for each field
3. Cross-reference findings across sources
4. Flag conflicts and uncertainties
5. Compile results into structured format

### Phase 3: Report Generation
1. Synthesize findings into narrative
2. Include tables and comparisons
3. Highlight key insights
4. Note limitations and gaps
5. Suggest future research directions

## Output

Returns:
- **Outline**: For user review and approval
- **Investigation results**: Structured data per research item
- **Final report**: Synthesized narrative with full citation support

## Report Structure

```markdown
## Deep Research Report: [Topic]

### Executive Summary
[3-5 sentence overview]

### Key Findings
1. [Most important finding]
2. [Second finding]
3. [Third finding]

### Comparative Analysis
[Side-by-side comparison if applicable]

### Areas of Agreement
[What literature consistently shows]

### Areas of Contention
[Where sources disagree]

### Limitations and Gaps
[What needs more research]

### Future Research Directions
1. [Suggested direction]

### Source Inventory
[Complete list of sources by reliability tier]
```

## Skill Used

`deep-research` + `paper-search`
