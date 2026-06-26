---
name: format-citations
description: Format citations in various academic styles (APA, IEEE, Chicago, MLA, Harvard, Vancouver)
arguments:
  - name: input
    description: DOI, BibTeX, or file path to references
    required: true
  - name: style
    description: Citation style (apa, ieee, chicago, mla, harvard, vancouver, bibtex)
    required: true
  - name: output
    description: Output file path (optional)
    required: false
---

# Format Citations Command

Format citations in various academic styles and generate BibTeX entries.

## Usage

```bash
/format-citations "10.1234/5678" --style apa
/format-citations "10.1234/5678" --style ieee
/format-citations references.bib --style chicago
/format-citations paper.md --style bibtex
```

## Citation Styles

| Style | Common Use | Example |
|-------|-----------|---------|
| APA 7th | Psychology, Education | (Author, Year) |
| IEEE | Engineering, CS | [1] |
| Chicago | History, Humanities | Footnotes |
| MLA | Literature, Arts | (Author Page) |
| Harvard | UK Universities | (Author Year) |
| Vancouver | Medicine | Superscript |
| BibTeX | LaTeX | @article{...} |

## Output

Returns:
- Formatted citation(s)
- BibTeX entry (if requested)
- Validation status

## Skill Used

`citation-manager`
