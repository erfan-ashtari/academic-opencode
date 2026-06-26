---
name: review-paper
description: Get expert-level review of a single academic paper
arguments:
  - name: input
    description: Paper PDF path, DOI, or URL
    required: true
  - name: style
    description: Review style (conference, journal, quick)
    required: false
    default: conference
  - name: focus
    description: Specific focus areas (methodology, writing, results)
    required: false
---

# Review Paper Command

Get expert-level review feedback on a single academic paper.

## Usage

```bash
/review-paper paper.pdf
/review-paper "10.1234/5678" --style journal
/review-paper paper.pdf --focus methodology,results
/review-paper paper.pdf --quick
```

## Review Dimensions

| Dimension | Weight |
|-----------|--------|
| Originality | 15% |
| Methodology | 25% |
| Results | 20% |
| Writing | 15% |
| Related Work | 10% |
| Impact | 15% |

## Output

Returns:
- Paper summary
- Strengths and weaknesses
- Detailed comments by section
- Questions for authors
- Recommendation (accept/revision/reject)
- Score (1-10)

## Skill Used

`paper-review`
