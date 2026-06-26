---
name: convert-document
description: Convert PDFs and Office documents to Markdown for analysis
---

# /convert-document

Convert PDFs and Office documents (docx, pptx, xlsx) to Markdown format.

## Usage

```bash
# Convert single document
/convert-document <input_file> [output_file]

# Batch convert directory
/convert-batch <input_dir> [--output <output_dir>] [--pattern <glob>]
```

## Examples

### Single File Conversion

```bash
# Convert PDF to Markdown (output: paper.md)
/convert-document paper.pdf

# Convert with custom output path
/convert-document paper.pdf --output extracted-paper.md

# Convert Word document
/convert-document thesis.docx
```

### Batch Conversion

```bash
# Convert all documents in folder
/convert-batch ./papers/

# Convert with output directory
/convert-batch ./papers/ --output ./markdown/

# Convert only PDFs
/convert-batch ./papers/ --pattern "*.pdf"
```

## Supported Formats

| Format | Extensions |
|--------|------------|
| PDF | .pdf |
| Word | .docx, .doc |
| PowerPoint | .pptx, .ppt |
| Excel | .xlsx, .xls |
| OpenDocument | .odt, .odp, .ods |
| Rich Text | .rtf |

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output file/directory path | Same as input with .md extension |
| `--pattern` | File glob pattern for batch | `*` (all files) |
| `--no-fallback` | Disable markitdown fallback | false |

## Output

The command outputs:
- Converted Markdown content
- Output file path
- Content preview (first 500 characters)

## Use Cases in Research

1. **Paper Analysis**: Convert PDF papers to analyze with LLM
2. **Collaboration**: Convert collaborator's Word docs to readable format
3. **Literature Review**: Batch convert papers for systematic review
4. **Note Taking**: Extract text for annotation and summarization

## Dependencies

- `pymupdf4llm` - PDF conversion (required)
- `LibreOffice` - Office document conversion (optional, recommended)
- `markitdown` - Fallback converter (optional)
