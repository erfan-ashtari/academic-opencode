---
name: write-paper
description: Write academic paper sections with proper structure and citations
arguments:
  - name: section
    description: Section to write (abstract, introduction, methods, results, discussion, conclusion, outline)
    required: true
  - name: topic
    description: Paper topic or title
    required: true
  - name: contributions
    description: Key contributions (comma-separated)
    required: false
  - name: format
    description: Output format (latex, markdown)
    required: false
    default: markdown
  - name: template
    description: Template to use (article, conference, thesis)
    required: false
    default: article
  - name: words
    description: Target word count (for abstract)
    required: false
---

# Write Paper Command

Write structured academic paper sections with proper citations and formatting.

## Usage

```bash
/write-paper abstract --topic "attention mechanisms for NLP" --words 250
/write-paper introduction --contributions "novel architecture, 15% improvement"
/write-paper methods --approach "transformer with linear attention"
/write-paper outline --type research --venue conference
```

## Sections

| Section | Purpose |
|---------|---------|
| abstract | Summary (150-300 words) |
| introduction | Context, problem, contributions |
| methods | Technical approach, implementation |
| results | Findings, experiments, metrics |
| discussion | Interpretation, limitations |
| conclusion | Summary, future work |
| outline | Full paper structure |

## Output

Returns:
- Generated section content
- Suggested citations to include
- Formatting applied
- Word count

## Skill Used

`paper-writing`
