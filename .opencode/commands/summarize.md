---
name: summarize
description: Summarize academic papers with key findings, methodology, and contribution assessment
arguments:
  - name: input
    description: Paper PDF path, DOI, title, or URL
    required: true
  - name: mode
    description: Summary mode (quick, standard, detailed)
    required: false
    default: standard
  - name: output
    description: Output format (text, markdown)
    required: false
    default: text
---

# Summarize Command

Create structured summaries of academic papers for quick understanding, screening, and reference.

## Usage

```bash
/summarize "Attention Is All You Need"
/summarize 10.48550/arXiv.1706.03762 --mode quick
/summarize paper.pdf --mode detailed
```

## Summary Modes

### Quick Mode
Fast 1-paragraph summary for screening:
- 1 sentence: What problem does this paper solve?
- 1 sentence: What method do they use?
- 1 sentence: What did they find?
- 1 sentence: Why does it matter?
- 1 sentence: Should you read it?

### Standard Mode (Default)
Structured summary with all key sections:
- Metadata (title, authors, year, venue, DOI)
- Research question
- Methodology (design, data, analysis)
- Key findings
- Contribution assessment (novelty, significance, reproducibility)
- Strengths and limitations
- Relevance to field
- APA citation

### Detailed Mode
Full analysis including everything from Standard Mode plus:
- Methodology critique (strengths, weaknesses, alternatives)
- Related work positioning (builds on, differs from, leads to)
- Reproducibility assessment (code, data, detail level)
- Questions for authors

## Output

Returns:
- **Quick**: 5-sentence screening summary with read recommendation
- **Standard**: Full structured summary with metadata and assessment
- **Detailed**: Complete analysis with methodology critique and positioning

## Skill Used

`summarize-paper`
