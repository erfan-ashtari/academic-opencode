---
name: paper-review
description: Review academic papers as an expert. Provide structured feedback, identify strengths/weaknesses, suggest improvements. Use when reviewing a single paper, getting paper feedback, or teaching paper concepts step-by-step.
triggers:
  - "review paper"
  - "review this paper"
  - "paper feedback"
  - "critique paper"
  - "explain paper"
  - "teach me about"
  - "explain this concept"
  - "paper analysis"
  - "peer review"
---

# Paper Review Skill

Provide expert-level paper reviews and step-by-step concept explanations.

## How It Works

1. **Analyze Paper**: Read and understand the full paper
2. **Structured Review**: Evaluate across multiple dimensions
3. **Identify Issues**: Find methodological, writing, and presentation problems
4. **Generate Feedback**: Provide constructive, actionable suggestions
5. **Teach Concepts**: Explain complex ideas step-by-step when requested

## Review Dimensions

| Dimension | Weight | Evaluation Criteria |
|-----------|--------|---------------------|
| Originality | 15% | Novelty, innovation, contribution |
| Methodology | 25% | Soundness, reproducibility, rigor |
| Results | 20% | Significance, validity, analysis |
| Writing | 15% | Clarity, structure, grammar |
| Related Work | 10% | Coverage, positioning, comparison |
| Impact | 15% | Significance, applicability, future work |

## Usage Examples

### Full Paper Review
```bash
/review-paper paper.pdf
/review-paper "Attention Is All You Need" --style conference
```

### Quick Critique
```bash
/review-paper paper.pdf --quick
```

### Explain Paper to Student
```bash
/explain-paper paper.pdf --level beginner
/explain-paper paper.pdf --concept "attention mechanism"
```

### Step-by-Step Teaching
```bash
/explain-paper paper.pdf --teach --step-by-step
```

## Review Template

### Summary
[Brief summary of paper's main contribution]

### Strengths
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

### Weaknesses
1. [Weakness 1]
2. [Weakness 2]
3. [Weakness 3]

### Detailed Comments

#### Originality
[Assessment of novelty]

#### Methodology
[Assessment of methods]

#### Results
[Assessment of experiments]

#### Writing
[Assessment of presentation]

### Questions for Authors
1. [Question 1]
2. [Question 2]

### Minor Issues
- [Typo/suggestion 1]
- [Typo/suggestion 2]

### Recommendation
[Accept / Minor Revision / Major Revision / Reject]

### Overall Score
[1-10 scale]

## Teaching Mode

When `--teach` or `--explain` is used:

1. **Concept Overview**: What is this concept?
2. **Why It Matters**: Why is this important?
3. **How It Works**: Step-by-step explanation
4. **Intuition**: Building intuition with analogies
5. **Examples**: Concrete examples
6. **Connections**: How it relates to other concepts
7. **Practice**: Suggested exercises

## Score Interpretation

| Score | Meaning | Action |
|-------|---------|--------|
| 8-10 | Excellent | Minor suggestions only |
| 6-8 | Good | Moderate improvements needed |
| 4-6 | Average | Significant revisions required |
| 2-4 | Below Average | Major problems, likely reject |
| 1-2 | Poor | Fundamental issues |

## Dependencies

- `mcp_servers/document-converter` (read PDF papers)
- `skills/paper-search` (find related work)
- `skills/citation-manager` (reference checking)

## Output Format

```json
{
  "paper": "Paper Title",
  "review": {
    "summary": "...",
    "strengths": ["..."],
    "weaknesses": ["..."],
    "detailed_comments": {...},
    "questions": ["..."],
    "recommendation": "minor_revision",
    "score": 7
  },
  "teaching": {
    "concepts_explained": [...],
    "step_by_step": [...]
  }
}
```
