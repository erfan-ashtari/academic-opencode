---
name: explain-paper
description: Get step-by-step explanation of paper concepts for teaching and learning
arguments:
  - name: input
    description: Paper PDF path, DOI, or URL
    required: true
  - name: concept
    description: Specific concept to explain (optional, explains full paper if omitted)
    required: false
  - name: level
    description: Explanation level (beginner, intermediate, advanced)
    required: false
    default: intermediate
  - name: teach
    description: Enable step-by-step teaching mode
    required: false
    default: false
---

# Explain Paper Command

Get step-by-step explanations of paper concepts for teaching and learning.

## Usage

```bash
/explain-paper paper.pdf
/explain-paper paper.pdf --concept "attention mechanism"
/explain-paper paper.pdf --level beginner
/explain-paper paper.pdf --teach --step-by-step
```

## Explanation Levels

| Level | Audience |
|-------|----------|
| beginner | Undergraduate students |
| intermediate | Graduate students |
| advanced | Researchers, experts |

## Teaching Mode

When `--teach` is enabled:
1. Concept overview
2. Why it matters
3. How it works (step-by-step)
4. Building intuition with analogies
5. Concrete examples
6. Connections to other concepts
7. Practice exercises

## Output

Returns:
- Paper summary in plain language
- Key concepts explained
- Step-by-step breakdown
- Intuition-building analogies
- Further reading suggestions

## Skill Used

`paper-review`
