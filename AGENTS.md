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

## Academic Mode (Auto-Detected)

Academic tools are **automatically detected** based on query intent. No manual toggle needed.

### Auto-Spawning Rules

When the query matches an academic intent, **automatically spawn the specialized subagent** with the appropriate skills loaded.

| Intent Pattern | Spawn Agent | Load Skills |
|----------------|-------------|-------------|
| "search for papers", "find research", "look up studies" | `research-agent` | `["paper-search"]` |
| "review literature", "systematic review", "survey papers" | `review-agent` | `["literature-review", "paper-search"]` |
| "write paper", "draft section", "abstract", "introduction" | `writing-agent` | `["paper-writing", "citation-manager"]` |
| "format citation", "bibliography", "reference list" | `Sisyphus-Junior` | `["citation-manager"]` |
| "compose email", "send to professor", "submission email" | `Sisyphus-Junior` | `["email-composer"]` |
| "review paper", "critique", "evaluate methodology" | `review-agent` | `["paper-review"]` |
| "explain paper", "summarize findings", "break down" | `Sisyphus-Junior` | `["paper-review"]` |
| "convert PDF", "extract text", "parse document" | `Sisyphus-Junior` | `["document-converter"]` |
| "find LaTeX template", "format paper" | `Sisyphus-Junior` | `["latex-assistant"]` |
| Any query with DOI (10.xxxx/xxxxx) | `research-agent` | `["paper-search", "citation-manager"]` |
| Any query mentioning specific paper titles | `research-agent` | `["paper-search"]` |

### Auto-Skill Loading Rules

Even without spawning a new agent, **load relevant skills** when the query contains:

| Query Contains | Load Skill |
|----------------|------------|
| paper, research, study, publication | `paper-search` |
| citation, reference, bibliography, DOI | `citation-manager` |
| review, critique, methodology | `paper-review` |
| write, draft, abstract, introduction, conclusion | `paper-writing` |
| email, professor, submission, collaboration | `email-composer` |
| PDF, convert, extract, document | `document-converter` |
| LaTeX, template, journal, conference | `latex-assistant` |
| literature, survey, systematic, PRISMA | `literature-review` |

### When NOT to Use Academic Tools

Standard dev workflow (no academic routing):
- "fix this bug", "debug the error"
- "refactor this function"
- "write a test"
- "deploy to production"
- Pure code-related queries with no research intent

### Example Auto-Responses

**User:** "find recent papers on transformer attention"

**Agent should:**
1. Detect intent: paper search
2. Spawn: `research-agent`
3. Load skills: `["paper-search"]`
4. Execute: parallel search across arXiv, Semantic Scholar, IEEE

**User:** "write an introduction for my paper on face recognition"

**Agent should:**
1. Detect intent: paper writing
2. Spawn: `writing-agent`
3. Load skills: `["paper-writing", "citation-manager"]`
4. Execute: draft introduction with citations

**User:** "review this paper: 10.1234/5678"

**Agent should:**
1. Detect intent: paper review + DOI present
2. Spawn: `review-agent`
3. Load skills: `["paper-review", "paper-search"]`
4. Execute: fetch paper, provide structured review

## Environment

- Python: Required for MCP servers
- API Keys: Set in `.env` (Zotero, etc.)

## Notes

- Google Scholar results need human review (rate-limited, less structured)
- MCP servers fall back to web search when unavailable
- All paper results include `pdf_available` and `pdf_url` tags

---

*This file is read by OpenCode agents at the start of each session.*
