# AGENTS.md - Academic Research Project

This file provides context and instructions for AI coding agents working in this academic research project.

## Project Overview

This is an academic research workspace powered by OpenCode + oh-my-openagent with 14 MCP servers covering all major academic fields.

## Available Research Tools

### Paper Search (14 databases)
| Database | Coverage | Command |
|----------|----------|---------|
| arXiv | Physics, CS, Math | `/search-papers "query" --sources arxiv` |
| PubMed | Biomedical | `/search-papers "query" --sources pubmed` |
| Semantic Scholar | All fields | `/search-papers "query" --sources semantic-scholar` |
| IEEE Xplore | Engineering, CS | `/search-papers "query" --sources ieee-xplore` |
| ACM DL | CS, Computing | `/search-papers "query" --sources acm-dl` |
| OpenAlex | Cross-discipline | `/search-papers "query" --sources openalex` |
| Crossref | DOI registry | `/search-papers "query" --sources crossref` |
| SSRN | Social Sciences | `/search-papers "query" --sources ssrn` |
| DBLP | CS Bibliography | `/search-papers "query" --sources dblp` |
| bioRxiv | Biology | `/search-papers "query" --sources biorxiv` |
| Europe PMC | Biomedical | `/search-papers "query" --sources europepmc` |
| Google Scholar | All fields | `/search-papers "query" --sources google-scholar` |

### Citation Management
- Format: APA, IEEE, Chicago, MLA, Harvard, Vancouver
- Generate BibTeX entries
- Validate DOIs
- Command: `/format-citations "10.1234/5678" --style ieee`

### Literature Review
- Systematic reviews with PRISMA 2020 methodology
- Citation snowballing (forward/backward)
- Quality assessment (Cochrane ROB-2, Newcastle-Ottawa, CASP)
- Command: `/review-literature "topic"`

### Paper Writing
- Section-by-section drafting (intro, methodology, experiments, conclusion)
- Citation integration
- LaTeX and Markdown output
- Command: `/write-paper "topic" --style ieee --format latex`

### Document Conversion
- PDF → Markdown (preserves math, tables, figures)
- DOCX → Markdown
- Batch conversion supported
- Command: `/convert-document paper.pdf`

### Academic Email Composition
- Inquiry, collaboration, submission, revision, thank-you, conference emails
- Command: `/compose-email --type inquiry --to professor@university.edu`

### Paper Review
- Expert analysis of individual papers
- Methodology critique, reproducibility assessment
- Command: `/review-paper "paper title or DOI"`

### Explain Paper
- Plain-language explanation of complex papers
- Key concepts, methodology, findings breakdown
- Command: `/explain-paper "paper title"`

### LaTeX Assistant
- Find templates for journals/conferences
- Fix LaTeX bugs
- Command: `/find-latex-template --venue "NeurIPS"`

## Recommended Workflows

### Starting a New Research Project
1. Define research question
2. `/review-literature "topic"` — systematic search
3. `/search-papers "specific query" --year 2023-2025` — targeted search
4. `/format-citations` — organize references

### Writing a Paper
1. `/find-latex-template --venue "target venue"` — get template
2. `/write-paper "topic" --style ieee --format latex` — draft sections
3. `/compose-email --type submission` — submission email

### Reviewing a Paper
1. `/review-paper "DOI or title"` — expert review
2. `/search-papers "related work"` — find related papers
3. `/explain-paper "complex paper"` — understand difficult concepts

## Available Slash Commands

| Command | Purpose |
|---------|---------|
| `/search-papers` | Search academic databases |
| `/review-literature` | Systematic literature review |
| `/write-paper` | Draft paper sections |
| `/format-citations` | Format references |
| `/compose-email` | Academic emails |
| `/review-paper` | Expert paper review |
| `/explain-paper` | Plain-language explanation |
| `/convert-document` | PDF/DOCX → Markdown |
| `/convert-batch` | Batch document conversion |

## Communication Style

- Be concise and academic in tone
- Include citations with DOIs when referencing papers
- Distinguish between established facts and speculation
- Note when results need human verification (especially Google Scholar)

## Academic Mode

Toggle automatic academic tool usage:

```bash
/academic-mode on    # Enable (default for research tasks)
/academic-mode off   # Disable (standard dev workflow)
```

When ON: all research/writing/citation tasks auto-route to academic tools.
When OFF: academic tools only used when explicitly requested.

## Environment

- Python: Required for MCP servers
- API Keys: Set in `.env` (Zotero, etc.)

## Notes

- Google Scholar results need human review (rate-limited, less structured)
- MCP servers fall back to web search when unavailable
- All paper results include `pdf_available` and `pdf_url` tags

---

*This file is read by OpenCode agents at the start of each session.*
