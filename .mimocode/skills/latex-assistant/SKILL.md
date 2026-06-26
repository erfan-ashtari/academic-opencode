---
name: latex-assistant
description: LaTeX compilation, template management, error fixing, and document formatting for academic papers.
triggers:
  - "compile latex"
  - "fix latex error"
  - "latex template"
  - "format latex document"
---

# LaTeX Assistant Skill

LaTeX compilation, template management, error fixing, and document formatting for academic papers.

## Features

- Document compilation (pdflatex, xelatex, lualatex)
- Template management (IEEE, ACM, Springer, etc.)
- Error diagnosis and fixing
- Bibliography compilation (bibtex, biber)
- Figure/table formatting
- Cross-reference resolution

## Supported Templates

| Template | Class |
|----------|-------|
| IEEE | IEEEtran.cls |
| ACM | acmart.cls |
| Springer | llncs.cls |
| Elsevier | elsarticle.cls |
| AAAI | aaai.sty |
| NeurIPS | neurips_2024.sty |

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Undefined `\mathbb` | Missing amsfonts | `\usepackage{amssymb}` |
| Missing `$` | Math mode | Add `$` delimiters |
| Overfull hbox | Line too long | Use `\allowbreak` |
| Citation undefined | Missing `\cite` | Run BibTeX/Biber |

## Usage

```bash
# Compile document
/compile-latex paper.tex

# Fix errors
/fix-latex paper.tex

# Apply template
/apply-template paper.tex --venue ieee
```
