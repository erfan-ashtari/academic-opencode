---
name: summarize-paper
description: Summarize academic papers with key findings, methodology, and contribution assessment. Use for quick paper understanding, journal club preparation, screening papers for relevance, or building annotated bibliographies.
triggers:
  - "summarize paper"
  - "paper summary"
  - "quick summary of"
  - "paper overview"
  - "what is this paper about"
  - "journal club prep"
  - "screen paper"
  - "annotated bibliography"
  - "paper digest"
---

# Paper Summarizer

Creates structured summaries of academic papers for quick understanding, screening, and reference.

## When to Use

- Quickly understanding a paper's contributions
- Preparing for journal club or lab meetings
- Building an annotated bibliography
- Screening papers for relevance before deep reading
- Reviewing methodology before critique
- Creating reading lists with brief assessments
- Getting the gist of a paper before deciding to read fully

## How It Works

1. **Extract metadata** — Title, authors, year, journal/venue, DOI
2. **Identify key elements** — Research question, methods, findings, limitations
3. **Assess contribution** — What's new? What matters? How significant?
4. **Create summary** — Structured, concise, with citations
5. **Flag concerns** — Methodology issues, limitations, conflicting findings
6. **Suggest related work** — Papers that build on or complement this one

## Summary Modes

### Quick Mode (Default)
Fast 1-paragraph summary for screening:
- 1 sentence: What problem does this paper solve?
- 1 sentence: What method do they use?
- 1 sentence: What did they find?
- 1 sentence: Why does it matter?

### Standard Mode
Structured summary with all key sections (see template below).

### Detailed Mode
Full analysis including methodology critique, related work positioning, and limitations assessment.

## Summary Template

```markdown
## Paper Summary

**Title:** [full title]
**Authors:** [names]
**Year:** [year]
**Journal/Venue:** [name]
**DOI:** [link]
**Citations:** [count, if available]

### One-Line Summary
[Complete paper in one sentence]

### Research Question
[What problem does this paper address?]

### Methodology
[How did they study it? Design, participants/sample, analysis approach]
- **Design:** [experimental / observational / theoretical / review]
- **Data:** [dataset size, type, source]
- **Analysis:** [statistical methods, evaluation metrics]

### Key Findings
1. [Finding 1 — most important]
2. [Finding 2]
3. [Finding 3]

### Contribution Assessment
- **Novelty:** [What's new compared to existing work?]
- **Significance:** [How important is this finding?]
- **Reproducibility:** [Could you replicate this? Is code/data available?]

### Strengths
1. [Strength 1]
2. [Strength 2]

### Limitations
1. [Limitation 1]
2. [Limitation 2]

### Relevance
[How does this connect to other work in the field?]

### Suggested Citation
[APA format citation]
```

## Quick Mode Output

```markdown
## Quick Summary: [Paper Title] (Author et al., Year)

**Problem:** [1 sentence]
**Method:** [1 sentence]
**Finding:** [1 sentence]
**Why it matters:** [1 sentence]

**Read full paper?** [Yes — [reason] / Maybe — [condition] / Skip — [reason]]
```

## Detailed Mode Output

Includes everything from Standard Mode plus:

```markdown
### Methodology Critique
- **Strengths:** [What was done well methodologically]
- **Weaknesses:** [What could have been done better]
- **Alternatives:** [Other methods that could have been used]

### Related Work Positioning
- **Builds on:** [key prior work this extends]
- **Differs from:** [key competing approaches]
- **Leads to:** [subsequent work that cites this]

### Reproducibility Assessment
- **Code available:** [Yes/No — link if available]
- **Data available:** [Yes/No — link if available]
- **Sufficient detail:** [Could you reproduce from the paper alone?]
- **Compute requirements:** [GPU hours, dataset size, etc.]

### Questions for Authors
1. [Question about methodology]
2. [Question about results]
3. [Question about limitations]
```

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `paper-search` | Find papers to summarize |
| `document-converter` | Convert PDF papers to readable format for summarization |
| `anti-hallucination` | Verify claims in the paper before summarizing |
| `citation-manager` | Generate proper citation for the summary |
| `literature-review` | Summarize papers as part of a larger review |

## Output

- Structured summary following the selected mode template
- Key takeaways for quick reference
- Methodology assessment (Standard and Detailed modes)
- Suggested related papers
- Citation in requested format

## Present Results to User

```
## Summary: [Paper Title] (Author et al., Year)

**Quick take:** [1-sentence summary of the paper's main contribution]

### Research Question
[question]

### Key Findings
1. [finding]
2. [finding]

### Limitations
- [limitation]

### My Assessment
[Brief evaluation of methodology and contribution]

**Citation:** [APA format]

---
**Want more?** I can provide a detailed methodology critique, find related papers, or add this to an annotated bibliography.
```

## Troubleshooting

- **Paper not accessible**: Summarize from abstract and available metadata only
- **Methodology unclear**: Note this as a limitation, don't guess
- **Findings seem weak**: Provide balanced assessment, note sample size and statistical concerns
- **Very long paper**: Focus on abstract, conclusion, and key figures/tables
- **Non-English paper**: Summarize based on available English abstract if available
