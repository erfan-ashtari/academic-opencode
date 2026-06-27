---
name: deep-research
description: Conduct structured deep research with outline generation, parallel investigation, and synthesis. Use when researching complex topics that require systematic exploration across multiple sources.
triggers:
  - "deep research on"
  - "research topic thoroughly"
  - "investigate this topic"
  - "systematic investigation"
  - "research a complex topic"
  - "compare technologies academically"
  - "due diligence on research"
  - "explore this research area"
---

# Deep Research Skill

Two-phase research workflow: structured outline generation followed by parallel deep investigation with cross-referencing and synthesis.

## When to Use

- Complex research topics requiring multiple sources
- Literature reviews with broad scope
- Technology comparisons or evaluations
- Market or trend analysis in academic domains
- Due diligence on research claims
- Preparing research proposals or grant applications
- Understanding a new research area from scratch

## How It Works

### Phase 1: Outline Generation

1. **Analyze the research topic** — Understand scope, boundaries, and key dimensions
2. **Decompose into research items** — Break the topic into investigateable sub-questions
3. **Define information fields** — Specify what data to collect for each item
4. **Present outline for approval** — User reviews and adjusts before investigation begins
5. **Allow modifications** — Add/remove items, adjust scope, refine questions

### Phase 2: Deep Investigation

For each research item:
1. **Search multiple sources** — Use `paper-search` across relevant databases
2. **Collect structured data** — Gather findings for each defined field
3. **Cross-reference** — Compare findings across sources for consistency
4. **Flag conflicts** — Note contradictory evidence or methodologies
5. **Rate confidence** — Assess reliability of each finding (high/medium/low)

### Phase 3: Report Generation

1. **Synthesize findings** — Weave individual investigations into a coherent narrative
2. **Include comparisons** — Side-by-side analysis where applicable
3. **Highlight key insights** — The most important discoveries across all items
4. **Note limitations** — Gaps in evidence, areas of uncertainty
5. **Suggest future directions** — What should be investigated next

## Outline Format

```markdown
## Research Outline: [Topic]

### Research Questions
1. [Primary question]
2. [Secondary question]
3. [Tertiary question]

### Items to Investigate
1. **[Item 1]** — [brief description]
2. **[Item 2]** — [brief description]
3. **[Item 3]** — [brief description]

### Fields to Collect per Item
- **Core Finding**: [What was discovered]
- **Methodology**: [How it was studied]
- **Evidence Strength**: [high/medium/low]
- **Source Count**: [Number of independent sources]
- **Consensus Level**: [agree/mixed/conflicted]

### Scope Parameters
- **Date Range**: [e.g., 2020-2025]
- **Source Types**: [peer-reviewed, preprints, reports]
- **Disciplines**: [CS, Medicine, etc.]
- **Exclusions**: [what to skip and why]
```

## Investigation Format

```markdown
## Investigation: [Item Name]

### Sources Consulted
| # | Source | Year | Type | Reliability |
|---|--------|------|------|-------------|
| 1 | [Paper/Source] | [year] | [journal/conference/report] | [Tier 1/2/3] |

### Findings by Field

#### [Field 1]
- **Finding**: [what was discovered]
- **Confidence**: [high/medium/low]
- **Supporting Sources**: [count]
- **Source**: [citation]

#### [Field 2]
- **Finding**: [what was discovered]
- **Confidence**: [high/medium/low]
- **Supporting Sources**: [count]
- **Source**: [citation]

### Cross-Reference Analysis
- **Consistent findings**: [which sources agree]
- **Conflicting findings**: [which sources disagree and why]
- **Gaps**: [what couldn't be found]

### Synthesis
[2-3 paragraph synthesis of what this item tells us]
```

## Final Report Structure

```markdown
## Deep Research Report: [Topic]

**Research conducted:** [date]
**Items investigated:** [count]
**Sources consulted:** [count]
**Date range covered:** [range]

### Executive Summary
[3-5 sentence overview of the most important findings]

### Key Findings

#### 1. [Most Important Finding]
[Detailed explanation with evidence]

#### 2. [Second Finding]
[Detailed explanation with evidence]

#### 3. [Third Finding]
[Detailed explanation with evidence]

### Comparative Analysis
[If applicable: side-by-side comparison of approaches, technologies, etc.]

### Areas of Agreement
[What the literature consistently shows]

### Areas of Contention
[Where sources disagree, with analysis of why]

### Limitations and Gaps
[What we couldn't find, what needs more research]

### Future Research Directions
1. [Suggested direction 1]
2. [Suggested direction 2]
3. [Suggested direction 3]

### Source Inventory
[Complete list of all sources used, organized by reliability tier]
```

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `paper-search` | Primary search engine for finding sources across databases |
| `paper-summarizer` | Quick summaries of individual papers during investigation |
| `citation-manager` | Format all citations in the final report |
| `anti-hallucination` | Verify all sources before including in the report |
| `literature-review` | Can be triggered for any item requiring systematic review |

## Anti-Hallucination Protocol

- NEVER fabricate citations or findings
- Verify every source exists via DOI or search before citing
- Flag low-confidence findings explicitly
- Note when sources conflict rather than choosing one side
- Recommend verification for critical claims
- Use `anti-hallucination` skill to validate the final report

## Output

1. **Outline** — For user review and approval before investigation
2. **Investigation results** — Structured data per research item
3. **Final report** — Synthesized narrative with full citation support

## Present Results to User

```
## Deep Research: [Topic]

**Phase 1: Outline** ✓
[Link to outline]

**Phase 2: Investigation** ✓
[Count] items investigated across [count] sources

**Phase 3: Report** ✓
[Key findings summary]

### Top 3 Insights
1. [Most important finding]
2. [Second finding]
3. [Third finding]

**Full report:** [location]
**Recommendations:** [next steps]
```

## Troubleshooting

- **Topic too broad**: Suggest narrowing scope, split into sub-topics
- **Sources limited**: Note gaps explicitly, suggest alternative search strategies
- **Findings conflict**: Present both sides with evidence, note uncertainty
- **Recent topic**: Acknowledge that cutting-edge work may not be fully indexed
- **Cross-disciplinary**: Search discipline-specific databases in addition to general ones
