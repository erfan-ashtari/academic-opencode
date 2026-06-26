---
name: document-converter
description: Convert between PDF, Markdown, LaTeX, and other document formats with structure preservation.
triggers:
  - "convert document"
  - "pdf to markdown"
  - "markdown to latex"
  - "convert format"
---

# Document Converter Skill

Convert between PDF, Markdown, LaTeX, and other document formats with structure preservation.

## Supported Conversions

| From | To | Notes |
|------|-----|-------|
| PDF | Markdown | Extract text, tables, figures |
| Markdown | LaTeX | Apply formatting |
| LaTeX | Markdown | For review/collaboration |
| DOCX | Markdown | Structure preserved |
| Markdown | DOCX | For Word users |

## Features

- Structure preservation (headings, lists, tables)
- Math formula conversion (LaTeX ↔ Unicode)
- Figure extraction and referencing
- Citation format adaptation
- Table format conversion

## Usage

```bash
# Convert PDF to Markdown
/convert-document paper.pdf --to markdown

# Convert Markdown to LaTeX
/convert-document paper.md --to latex --venue ieee

# Batch convert
/convert-batch *.md --to latex
```
