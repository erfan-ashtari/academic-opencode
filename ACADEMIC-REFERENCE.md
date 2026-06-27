# ACADEMIC-REFERENCE.md — Comprehensive Academic Research Reference

> **Purpose**: Complete reference for all academic research capabilities, agent routing, workflows, and standards.
> **Read by**: All agents at session start. Primary reference for academic task execution.
> **Last updated**: 2026-06-27

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Agent Architecture](#agent-architecture)
3. [Skill Reference](#skill-reference)
4. [Command Reference](#command-reference)
5. [Routing Rules](#routing-rules)
6. [Database Coverage](#database-coverage)
7. [Writing Standards](#writing-standards)
8. [Citation Standards](#citation-standards)
9. [Quality Standards](#quality-standards)
10. [Workflows](#workflows)
11. [Protocols and Schemas](#protocols-and-schemas)
12. [File Conventions](#file-conventions)

---

## Project Overview

An academic research workspace powered by OpenCode + oh-my-openagent with 13+ MCP servers covering all major academic fields.

### Capabilities

| Category | Count | Examples |
|----------|-------|---------|
| Agents | 15 | Orchestrator, researcher, reviewer, writer, teacher, summarizer |
| Skills | 11 | Paper search, literature review, paper writing, citation management |
| Commands | 19 | `/search-papers`, `/write-paper`, `/review-literature` |
| Databases | 13 | arXiv, PubMed, Semantic Scholar, IEEE, ACM, OpenAlex |
| Rules | 5 | Papers, thesis, proposals, research, emails |
| Shared | 2 | Protocols, schemas |

---

## Agent Architecture

### Primary Agents

| Agent | Role | Model | Use When |
|-------|------|-------|----------|
| `sisyphus` | Main orchestrator | mimo-v2.5-free | Default — plans, delegates, executes |
| `atlas` | Todo-list orchestrator | mimo-v2.5-free | Task tracking, progress management |

### Academic Agents

| Agent | Role | Capabilities | Use When |
|-------|------|-------------|----------|
| `research-agent` | Multi-source paper search | Parallel search, dedup, ranking, citation network, 13 databases | "find papers", "search for research", "look up studies" |
| `review-agent` | Systematic literature review | PRISMA, screening, quality assessment, data extraction, synthesis | "review literature", "systematic review", "survey papers" |
| `writing-agent` | Paper writing pipeline | Section drafting, citation integration, LaTeX/Markdown, templates | "write paper", "draft section", "abstract", "introduction" |
| `teacher` | Academic tutor | Scaffolding, Feynman technique, level adaptation, practice questions | "teach me about", "explain concept", "prep for exam" |
| `summarizer` | Paper summarizer | Quick/Standard/Detailed modes, annotated bibliography, journal club prep | "summarize paper", "quick summary", "journal club prep" |

### General-Purpose Agents

| Agent | Role | Use When |
|-------|------|----------|
| `oracle` | Architecture consultant | Complex technical decisions |
| `prometheus` | Strategic planner | Planning, requirements analysis |
| `metis` | Pre-planning consultant | Plan review, risk identification |
| `momus` | Verification reviewer | Code review, correctness verification |
| `hephaestus` | Autonomous deep worker | Complex implementation, bug investigation |
| `explore` | Fast codebase grep | File discovery, code search |
| `librarian` | External docs search | Documentation, reference implementations |
| `multimodal-looker` | Vision specialist | Image/PDF analysis, UI review |

### Agent Delegation Pattern

```
User Query
    │
    ▼
┌─────────────────┐
│ Sisyphus        │
│ (Orchestrator)  │
└────────┬────────┘
         │
         ├──→ research-agent (paper search)
         ├──→ review-agent (literature review)
         ├──→ writing-agent (paper writing)
         ├──→ teacher (concept explanation)
         ├──→ summarizer (paper summary)
         └──→ [other agents as needed]
```

---

## Skill Reference

### Academic Skills

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `paper-search` | Search 13 databases with dedup and PDF tagging | "find papers", "search research" |
| `literature-review` | PRISMA systematic reviews with quality assessment | "review literature", "systematic review" |
| `paper-writing` | Section-by-section drafting with citation integration | "write paper", "draft introduction" |
| `paper-review` | Expert review with 6 dimensions and scoring | "review paper", "critique" |
| `citation-manager` | Format in 6 styles, BibTeX, DOI validation | "format citations", "generate bibtex" |
| `reference-validator` | DOI validation, completeness checks, integrity verification | "validate references", "check doi" |
| `anti-hallucination` | Detect fabricated citations, verify claim-source matching | "verify citations", "check for hallucinations" |
| `email-composer` | 6 email types with formality levels | "compose email", "write email" |
| `latex-assistant` | LaTeX compilation, template management, error fixing | "compile latex", "fix latex error" |
| `document-converter` | PDF/Office/Markdown/LaTeX conversion | "convert document", "pdf to markdown" |
| `zotero-integration` | Zotero reference management and sync | "zotero", "reference management" |
| `deep-research` | 3-phase: Outline → Investigation → Synthesis | "deep research on", "investigate topic" |
| `academic-pipeline` | 7-stage orchestration with quality gates | "academic pipeline", "thesis workflow" |
| `summarize-paper` | Quick/Standard/Detailed paper summaries | "summarize paper", "paper summary" |
| `teach-subject` | Concept explanation with scaffolding and analogies | "teach me about", "explain concept" |

### Skill Dependencies

| Skill | Depends On |
|-------|------------|
| `paper-search` | MCP servers (13) or web fallback |
| `literature-review` | `paper-search`, `citation-manager`, `document-converter` |
| `paper-writing` | `citation-manager`, `latex-assistant`, `reference-validator`, `paper-search` |
| `paper-review` | `document-converter`, `paper-search`, `citation-manager` |
| `anti-hallucination` | `reference-validator`, `paper-search` |
| `academic-pipeline` | All academic skills (orchestration layer) |

---

## Command Reference

### Academic Commands

| Command | Description | Arguments |
|---------|-------------|-----------|
| `/search-papers` | Search 13 databases | `query`, `--database`, `--year`, `--max-results`, `--sort` |
| `/review-literature` | PRISMA literature review | `topic`, `--type`, `--databases`, `--criteria`, `--format` |
| `/write-paper` | Write paper sections | `section`, `topic`, `--contributions`, `--format`, `--template` |
| `/review-paper` | Expert paper review | `input`, `--style`, `--focus` |
| `/explain-paper` | Paper concept explanation | `input`, `--concept`, `--level`, `--teach` |
| `/format-citations` | Format citations (7 styles) | `input`, `--style`, `--output` |
| `/verify-citations` | Verify citation integrity | `input`, `--level`, `--output` |
| `/compose-email` | Compose academic emails | `type`, `--to`, `--topic`, `--paper`, `--venue` |
| `/convert-document` | Convert PDF/Office to Markdown | `input`, `--output` |
| `/convert-batch` | Batch convert documents | `input_dir`, `--output`, `--pattern`, `--concurrency` |
| `/deep-research` | Structured deep research | `topic`, `--scope`, `--databases`, `--year` |
| `/start-pipeline` | Start multi-stage project | `type`, `topic`, `--venue`, `--timeline` |
| `/summarize` | Summarize papers | `input`, `--mode`, `--output` |
| `/academic-mode` | Check academic mode status | — |

### Utility Commands

| Command | Description |
|---------|-------------|
| `/handoff` | Hand off work to another agent |
| `/init-deep` | Generate AGENTS.md files |
| `/ralph-loop` | Persistent work loop |
| `/start-work` | Start work with planning interview |
| `/ulw-loop` | Multi-goal orchestration |

---

## Routing Rules

### Auto-Spawning Rules

When the query matches an academic intent, **automatically spawn the specialized subagent** with the appropriate skills loaded.

| Intent Pattern | Spawn Agent | Load Skills |
|----------------|-------------|-------------|
| "search for papers", "find research", "look up studies" | `research-agent` | `["paper-search"]` |
| "review literature", "systematic review", "survey papers" | `review-agent` | `["literature-review", "paper-search"]` |
| "write paper", "draft section", "abstract", "introduction" | `writing-agent` | `["paper-writing", "citation-manager"]` |
| "format citation", "bibliography", "reference list" | `sisyphus` | `["citation-manager"]` |
| "compose email", "send to professor", "submission email" | `sisyphus` | `["email-composer"]` |
| "review paper", "critique", "evaluate methodology" | `review-agent` | `["paper-review"]` |
| "explain paper", "summarize findings", "break down" | `summarizer` | `["summarize-paper"]` |
| "teach me about", "explain concept", "prep for exam" | `teacher` | `["teach-subject"]` |
| "convert PDF", "extract text", "parse document" | `sisyphus` | `["document-converter"]` |
| "find LaTeX template", "format paper" | `sisyphus` | `["latex-assistant"]` |
| "deep research on", "investigate topic" | `sisyphus` | `["deep-research"]` |
| "verify citations", "check for hallucinations" | `sisyphus` | `["anti-hallucination"]` |
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
| summarize, summary, quick overview | `summarize-paper` |
| teach, explain, concept, learn, exam | `teach-subject` |
| hallucination, fabricated, verify, integrity | `anti-hallucination` |
| deep research, investigate, complex topic | `deep-research` |
| pipeline, thesis, grant, multi-stage | `academic-pipeline` |

### When NOT to Use Academic Tools

Standard dev workflow (no academic routing):
- "fix this bug", "debug the error"
- "refactor this function"
- "write a test"
- "deploy to production"
- Pure code-related queries with no research intent

---

## Database Coverage

| Database | Coverage | MCP Server | Fallback |
|----------|----------|------------|----------|
| arXiv | Physics, CS, Math, Stats, Bio, Econ | `arxiv-mcp` | Web search |
| PubMed | Biomedical, life sciences | `pubmed-mcp` | Web search |
| Semantic Scholar | All fields | `semantic-scholar-mcp` | Web search |
| IEEE Xplore | Engineering, CS | `ieee-xplore-mcp` | Web search |
| ACM DL | CS, Computing | `acm-dl-mcp` | Web search |
| OpenAlex | Cross-discipline | `openalex-mcp` | Web search |
| Crossref | DOI registry | `crossref-mcp` | Web search |
| SSRN | Social Sciences | `ssrn-mcp` | Web search |
| DBLP | CS Bibliography | `dblp-mcp` | Web search |
| bioRxiv | Biology, Biotech | API fallback | Web search |
| Europe PMC | Biomedical | API fallback | Web search |
| Google Scholar | All fields | Web fallback | — |

### Fallback Behavior

When MCP servers are unavailable:
1. Use `websearch` tool with `site:` operator targeting the academic domain
2. Use `webfetch` to scrape the search results page
3. Parse titles, authors, abstracts, DOIs, and PDF links from HTML
4. Return results in the same JSON format as MCP results
5. Tag each result with `source: "web-fallback"` and `source_url` for provenance

---

## Writing Standards

### Voice and Tone
- **Formal academic** unless explicitly asked otherwise
- **Active voice** preferred ("I collected data" not "data was collected")
- **Past tense** for completed actions ("The results showed...")
- **Present tense** for established knowledge ("Research indicates...")
- **First person** for methods ("I conducted...")
- **No contractions** in formal writing

### Structure
- Lead with main point
- Support with evidence
- Analyze implications
- Connect to broader context
- Use topic sentences at paragraph starts
- Use transitions between paragraphs and sections

### Citations
- Every factual claim needs a citation (except common knowledge)
- Prefer primary sources over secondary
- Include page numbers for direct quotes
- Use "et al." for 3+ authors (APA 7th)
- Verify DOIs resolve correctly

### Common Pitfalls to Avoid
- Literature review that's a summary, not a synthesis
- Methods section that doesn't justify choices
- Discussion that simply restates results
- Missing limitations section
- Inconsistent citation formatting
- Too much background, not enough original contribution
- Figures/tables not referenced in text

---

## Citation Standards

### Supported Styles

| Style | Fields | In-Text Format |
|-------|--------|----------------|
| APA 7th | Psychology, Education | (Author, Year) |
| IEEE | Engineering, CS | [Number] |
| Chicago | History, Humanities | Footnotes |
| MLA 9th | Literature, Arts | (Author Page) |
| Harvard | UK Universities | (Author Year) |
| Vancouver | Medicine | Superscript |

### Verification Checklist
- [ ] Author name spelled correctly
- [ ] Year is accurate
- [ ] Title matches published version
- [ ] Journal/venue is correct
- [ ] DOI resolves to correct paper
- [ ] Page numbers are accurate (for quotes)

### Anti-Hallucination Protocol
- NEVER fabricate citations — if unsure, say "citation needed"
- Always verify: Author (Year), Title, Journal, Volume, Pages, DOI
- Cross-check with Semantic Scholar API or Google Scholar
- Flag any source you cannot verify
- Use `/verify-citations` before submission

---

## Quality Standards

### Source Reliability Tiers

| Tier | Types | Confidence |
|------|-------|------------|
| 1 — High | Peer-reviewed journals, top conferences, government reports, systematic reviews | High |
| 2 — Medium | Preprints (arXiv, bioRxiv, SSRN), working papers, book chapters | Medium |
| 3 — Low | Blog posts, industry reports, Wikipedia (as primary source) | Low |
| 4 — Unreliable | Predatory journals, retracted papers, anonymous sources, social media | None |

### Quality Checklist (All Academic Work)
- [ ] All claims are cited
- [ ] Citations are verified (use `/verify-citations`)
- [ ] Arguments are logical and flow clearly
- [ ] Structure is clear and organized
- [ ] Writing is clear, concise, and academic
- [ ] Formatting matches target venue guidelines
- [ ] Grammar and spelling checked
- [ ] Abstract accurately reflects the content
- [ ] References match in-text citations
- [ ] No fabricated or unverified sources

---

## Workflows

### Starting a New Research Project
1. Define research question
2. `/review-literature "topic"` — systematic search
3. `/search-papers "specific query" --year 2023-2025` — targeted search
4. `/format-citations` — organize references

### Writing a Paper
1. `/start-pipeline paper "title" --venue "target venue"` — start pipeline
2. `/write-paper introduction --contributions "..."` — draft sections
3. `/verify-citations paper.md` — verify all citations
4. `/compose-email submission --paper "title" --venue "venue"` — submission email

### Reviewing a Paper
1. `/review-paper "DOI or title"` — expert review
2. `/search-papers "related work"` — find related papers
3. `/explain-paper "complex paper"` — understand difficult concepts

### Conducting a Literature Review
1. `/start-pipeline research "topic"` — start research pipeline
2. `/deep-research "topic"` — structured investigation
3. `/review-literature "topic" --type systematic` — PRISMA review
4. `/summarize paper.pdf --mode detailed` — summarize key papers

### Preparing for Exams
1. `/teach-subject "concept"` — learn concept
2. `/explain-paper paper.pdf --teach --level beginner` — step-by-step teaching

---

## Protocols and Schemas

### Shared Resources
- **Protocols**: `.opencode/shared/protocols.md` — Search, citation, writing, review protocols
- **Schemas**: `.opencode/shared/schemas.md` — Data formats, reliability tiers, citation schema

### Rules
- **Papers**: `.opencode/rules/papers.md` — Paper structure, citations, formatting
- **Thesis**: `.opencode/rules/thesis.md` — Thesis structure, style, committee management
- **Proposals**: `.opencode/rules/proposals.md` — Grant proposal structure, budget
- **Research**: `.opencode/rules/research.md` — Search strategy, CRAAP test, source evaluation
- **Emails**: `.opencode/rules/emails.md` — Email structure, tone, templates

---

## File Conventions

### Directory Structure
```
project/
├── papers/              # Working papers
├── thesis/              # Thesis chapters
├── proposals/           # Grant proposals
├── resources/           # Collected sources
├── emails/              # Drafted emails
├── surveys/             # Literature surveys
├── .opencode/
│   ├── agents/          # Agent definitions
│   ├── commands/        # Slash commands
│   ├── rules/           # Context-specific rules
│   ├── shared/          # Protocols and schemas
│   └── skills/          # Skill definitions
└── ACADEMIC-REFERENCE.md # This file
```

### Naming Conventions
- Agent files: `agent-name.md` (lowercase, hyphenated)
- Skill directories: `skill-name/` (lowercase, hyphenated)
- Command files: `command-name.md` (lowercase, hyphenated)
- Rule files: `topic.md` (lowercase)

### File Handling
- Convert PDFs to `.md` before processing: `/convert-document paper.pdf`
- Store converted files alongside originals
- Work with `.md` versions for analysis

---

## Environment

- **Python**: Required for MCP servers
- **API Keys**: Set in `.env` (Zotero, etc.)
- **MCP Servers**: 13+ academic database servers
- **Fallback**: Web search when MCP servers unavailable

---

## Notes

- Google Scholar results need human review (rate-limited, less structured)
- MCP servers fall back to web search when unavailable
- All paper results include `pdf_available` and `pdf_url` tags
- Academic mode is auto-detected — no manual toggle needed

---

*This file is read by all agents at session start. It is the primary reference for academic task execution.*
