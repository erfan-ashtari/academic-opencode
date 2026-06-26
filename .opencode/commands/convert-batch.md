---
name: convert-batch
description: Batch convert multiple PDFs and Office documents to Markdown
---

# /convert-batch

Convert multiple PDFs and Office documents to Markdown format in parallel.

## Usage

```bash
/convert-batch <input_dir> [--output <output_dir>] [--pattern <glob>] [--concurrency <n>]
```

## Examples

```bash
# Convert all supported files in a directory
/convert-batch ./papers/

# Convert with custom output directory
/convert-batch ./papers/ --output ./markdown/

# Convert only PDF files
/convert-batch ./papers/ --pattern "*.pdf"

# Convert with limited concurrency
/convert-batch ./papers/ --concurrency 4
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--output` | Output directory | `./converted/` |
| `--pattern` | File glob pattern | `*` (all supported) |
| `--concurrency` | Max parallel conversions | 4 |
| `--recursive` | Recurse into subdirectories | false |

## Supported Formats

PDF, docx, doc, pptx, ppt, xlsx, xls, odt, odp, ods, rtf

## Output

```
./converted/
├── paper1.md
├── paper2.md
├── presentation.md
└── report.md
```

## Dependencies

- `pymupdf4llm` - PDF conversion
- `LibreOffice` - Office document conversion (optional)
- `markitdown` - Fallback converter (optional)
