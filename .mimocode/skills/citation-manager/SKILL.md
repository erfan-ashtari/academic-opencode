---
name: citation-manager
description: Format citations and references in APA, IEEE, Chicago, MLA, Harvard, and Vancouver styles. Generate BibTeX entries, validate DOIs, and manage bibliographies.
triggers:
  - "format citations"
  - "generate bibtex"
  - "citation style"
  - "reference format"
  - "bibliography management"
  - "validate doi"
---

# Citation Manager Skill

Format citations and references in multiple academic styles, generate BibTeX entries, validate DOIs, and manage bibliographies.

## Supported Styles

| Style | In-Text | Reference List |
|-------|---------|----------------|
| APA 7th | (Author, Year) | Alphabetical |
| IEEE | [Number] | Numbered |
| Chicago | Footnotes | Footnotes/Bib |
| MLA 9th | (Author Page) | Alphabetical |
| Harvard | (Author Year) | Alphabetical |
| Vancouver | Superscript | Numbered |

## Features

- In-text citation formatting
- Reference list generation
- BibTeX entry generation
- DOI validation
- Cross-reference checking
- Style conversion between formats

## Usage

```bash
# Format single reference
/format-citations "10.1234/5678" --style ieee

# Format from bibliography file
/format-citations references.bib --style apa

# Validate DOIs in paper
/validate-references paper.md
## Dependencies

| Component | Integration |
|-----------|-------------|
| Crossref MCP | DOI validation and metadata lookup |
| Semantic Scholar MCP | Citation formatting from metadata |
| Zotero MCP | Bibliography sync |

## Fallback Behavior

When MCP servers are unavailable, citation-manager falls back to web-based DOI resolution.

**Fallback sites:**
- doi.org (Crossref API)
- dx.doi.org (handle resolution)

**Fallback workflow:**
1. Attempt MCP-based DOI validation
2. If MCP unavailable, use `webfetch` on `https://doi.org/{doi}` to resolve metadata
3. Parse citation metadata from Crossref JSON response
4. Format citation in requested style
5. Tag output with `source: "web-fallback"`

**Limitations:**
- Only DOI-based lookups possible (no title search)
- BibTeX generation may be incomplete
- Cross-reference checking not available
