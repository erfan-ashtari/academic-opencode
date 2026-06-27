# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [0.3.1] - 2026-06-27

### Removed

- `ACADEMIC-AUDIT-PLAN.md` — development artifact
- `ACADEMIC-REFERENCE.md` — consolidated into AGENTS.md
- `CLAUDE.md` — consolidated into AGENTS.md
- `IMPLEMENTATION-COMPLETE.md` — development artifact
- `IMPLEMENTATION-PLAN.md` — development artifact

## [0.3.0] - 2026-06-27

### Added

#### Consolidated Documentation
- Single comprehensive `AGENTS.md` replacing:
  - `ACADEMIC-REFERENCE.md` (434 lines)
  - `CLAUDE.md` (98 lines)
  - `AGENTS.md` (193 lines)
- New 356-line reference covering all academic capabilities

### Changed

- Updated MCP server configurations (opencode.json, mimocode.json)
- Added `.gitignore` entries for Python `__pycache__` directories
- Removed tracked `.pyc` files from git

### Fixed

- Added missing `if __name__ == "__main__": mcp.run()` blocks to europepmc and google-scholar servers
- Fixed syntax error in google-scholar `__init__.py`
- Added `__init__.py` to scopus-mcp and acl-anthology-mcp directories

## [0.2.0] - 2026-06-27

### Added

#### New MCP Servers
- **Scopus MCP** - Elsevier Scopus database integration (27,000+ journals)
- **ACL Anthology MCP** - ACL/EMNLP/NAACL/COLING papers for NLP/CL

#### Documentation
- `mcp_servers/AGENTS.md` - MCP server development guidelines
- `templates/AGENTS.md` - Template usage guidelines
- `.opencode/skills/AGENTS.md` - Skill development guidelines
- `.opencode/agents/AGENTS.md` - Agent definition guidelines
- `CONTRIBUTING.md` - Contributor guide
- `CHANGELOG.md` - This file
- `mcp_servers/README.md` - MCP servers overview
- `templates/README.md` - Templates overview
- `.opencode/skills/.dev/README.md` - Development skills documentation

#### Configuration Enhancements
- Academic-specific categories in `oh-my-openagent.jsonc`:
  - `academic-research` - Low temperature, high reasoning
  - `academic-writing` - Medium temperature, medium reasoning
- Thinking configurations for key agents (sisyphus, oracle, research-agent, writing-agent)

#### Fallback Improvements
- Enhanced `fallback_utils.py` with Jina Reader API integration
- Real web search fallback instead of placeholder results
- Text extraction helpers (authors, DOI, year)

### Changed

- Updated `.mcp.json` with new server definitions
- Enhanced `oh-my-openagent.jsonc` with academic categories
- Improved `fallback_utils.py` with real web search capabilities

### Fixed

- Removed empty `templates/emails/` directory
- Added documentation for `.opencode/skills/.dev/` directory

## [0.1.0] - 2026-06-20

### Added

#### Core Features
- 14 MCP servers for academic database integration
- Automatic intent detection and agent routing
- Web search fallback system
- 15 specialized skills
- 15 agents with different capabilities
- 19 slash commands

#### MCP Servers
- arXiv - Physics, CS, Math
- Semantic Scholar - All fields
- PubMed - Biomedical
- IEEE Xplore - Engineering, CS
- ACM Digital Library - CS, Computing
- OpenAlex - Cross-discipline
- Crossref - DOI registry
- SSRN - Social Sciences
- DBLP - CS Bibliography
- bioRxiv - Biology
- Europe PMC - Biomedical
- Google Scholar - All fields
- Zotero - Reference management
- Document Converter - PDF/DOCX conversion

#### Skills
- paper-search - Multi-database paper search
- paper-writing - Section drafting with citations
- literature-review - PRISMA-compliant reviews
- citation-manager - Citation formatting (6 styles)
- paper-review - Expert paper critique
- anti-hallucination - Citation verification
- reference-validator - DOI validation
- email-composer - Academic correspondence
- document-converter - PDF/DOCX conversion
- latex-assistant - LaTeX support
- deep-research - Structured research
- academic-pipeline - 7-stage orchestration
- summarize-paper - Paper summaries
- teach-subject - Concept explanation
- zotero-integration - Reference management

#### Agents
- research-agent - Multi-source paper search
- writing-agent - Paper writing pipeline
- review-agent - Systematic literature review
- teacher - Academic tutoring
- summarizer - Paper summarization
- sisyphus - Main orchestrator
- oracle - Architecture consultant
- librarian - External docs search
- explore - Fast codebase grep
- multimodal-looker - Media analysis
- metis - Pre-planning consultant
- momus - Plan critic
- atlas - Code search
- hephaestus - Deep worker
- prometheus - Plan consultant

#### Commands
- /search-papers - Search academic databases
- /review-literature - Systematic literature review
- /write-paper - Draft paper sections
- /format-citations - Format references
- /compose-email - Academic emails
- /review-paper - Expert paper review
- /explain-paper - Plain-language explanation
- /convert-document - PDF/DOCX conversion
- /convert-batch - Batch document conversion
- /verify-citations - Citation verification
- /start-pipeline - Start academic pipeline
- /deep-research - Structured research
- /academic-mode - Check academic mode status

## [Unreleased]

### Planned

#### New MCP Servers
- Scopus MCP - Elsevier Scopus database
- ACL Anthology MCP - ACL/EMNLP/NAACL papers

#### New Skills
- plagiarism-check - Detect potential plagiarism
- citation-network - Visualize citation relationships
- research-gap - Identify research gaps
- methodology-advisor - Recommend research methods
- statistical-analysis - Help with statistical analysis
- figure-generator - Create publication-ready figures

#### Enhancements
- Model fallback chains for all agents
- Skill-embedded MCP configurations
- Enhanced thinking configurations
- Real web search fallback via Jina Reader API

#### Documentation
- CONTRIBUTING.md - Contributor guide
- CHANGELOG.md - Version history
- mcp_servers/README.md - MCP servers overview
- templates/README.md - Templates overview

---

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 0.2.0 | 2026-06-27 | Enhanced configuration, new MCP servers, documentation |
| 0.1.0 | 2026-06-20 | Initial release with 14 MCP servers, 15 skills, 15 agents |
