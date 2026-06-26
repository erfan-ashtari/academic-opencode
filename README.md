<div align="center">

# 🎓 Academic OpenCode

**AI-powered academic research assistant with 14 MCP servers, automatic intent detection, and intelligent agent routing.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-green.svg)](https://github.com/anthropics/opencode)
[![MCP Servers](https://img.shields.io/badge/MCP%20Servers-14-orange.svg)](#-mcp-servers)
[![Release](https://img.shields.io/badge/Release-v0.1-purple.svg)](https://github.com/erfan-ashtari/academic-opencode/releases)

---

<img src="https://raw.githubusercontent.com/erfan-ashtari/academic-opencode/main/assets/hero.png" alt="Academic OpenCode Hero" width="800" />

---

**Academic OpenCode** transforms your coding assistant into a full-featured research powerhouse. Search 14 academic databases, manage citations, write papers, conduct literature reviews, and compose professional emails — all through natural language queries that automatically route to specialized agents.

</div>

---

## ✨ Features

### 🧠 Automatic Intent Detection

No manual toggles needed. Just ask naturally:

```
You:  "find recent papers on transformer attention"
      → Auto-spawns research-agent with paper-search skill

You:  "write an introduction for my paper on face recognition"
      → Auto-spawns writing-agent with paper-writing + citation-manager skills

You:  "review this paper: 10.1234/5678"
      → Auto-spawns review-agent with paper-review + paper-search skills
```

### 🔄 Per-MCP Web Search Fallback

Every MCP server has its own fallback. When an API fails (rate limit, timeout, no key), results automatically come from web search instead. Every result includes metadata:

```json
{
  "title": "Attention Is All You Need",
  "authors": ["Vaswani et al."],
  "_metadata": {
    "mcp_name": "arxiv",
    "method": "api",
    "weblink": "https://arxiv.org/abs/1706.03762"
  }
}
```

### 📚 14 Academic MCP Servers

Search across every major database from a single interface:

| Database | Coverage | Key Required |
|----------|----------|:------------:|
| **arXiv** | Physics, CS, Math | ❌ |
| **PubMed** | Biomedical | Optional |
| **Semantic Scholar** | All fields | Optional |
| **IEEE Xplore** | Engineering, CS | ✅ |
| **ACM DL** | CS, Computing | ❌ |
| **OpenAlex** | Cross-discipline | Optional |
| **Crossref** | DOI registry | Optional |
| **SSRN** | Social Sciences | ❌ |
| **DBLP** | CS Bibliography | ❌ |
| **bioRxiv** | Biology | ❌ |
| **Europe PMC** | Biomedical | ❌ |
| **Google Scholar** | All fields | ❌ |
| **Zotero** | Reference management | ✅ |
| **Document Converter** | PDF/DOCX → Markdown | ❌ |

### 🛠️ Built-in Skills

| Skill | Purpose |
|-------|---------|
| `paper-search` | Multi-database paper search with deduplication |
| `paper-writing` | Draft abstracts, introductions, methods, results, conclusions |
| `literature-review` | Systematic reviews with PRISMA 2020 methodology |
| `citation-manager` | Format citations in APA, IEEE, Chicago, MLA, Harvard, Vancouver |
| `paper-review` | Expert-level paper critique and feedback |
| `email-composer` | Draft academic emails (inquiry, collaboration, submission) |
| `document-converter` | PDF/DOCX → Markdown with structure preservation |
| `latex-assistant` | LaTeX templates, compilation, error fixing |
| `reference-validator` | DOI validation, reference completeness checking |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Query                                │
│   "search for papers on quantum computing and write a review"    │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Intent Detection Engine                        │
│  • Analyzes query keywords and patterns                          │
│  • Determines: research / writing / review / citations           │
│  • Selects appropriate agent + skills                            │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Research     │ │ Writing      │ │ Review       │
│ Agent        │ │ Agent        │ │ Agent        │
├──────────────┤ ├──────────────┤ ├──────────────┤
│ paper-search │ │ paper-writing│ │ paper-review │
│              │ │ citation-mgr │ │ paper-search │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MCP Server Layer                             │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐     │
│  │arXiv│ │IEEE │ │PubMed│ │S2   │ │OAlex│ │Cross│ │SSRN │ ... │
│  └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘ └──┬──┘     │
│     │       │       │       │       │       │       │          │
│     └───────┴───────┴───────┴───────┴───────┴───────┘          │
│                          │                                       │
│                    Fallback Layer                                │
│              (web search on API failure)                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for OpenCode)
- **OpenCode CLI** — [Install here](https://github.com/anthropics/opencode)

### Installation

```bash
# Clone the repository
git clone https://github.com/erfan-ashtari/academic-opencode.git
cd academic-opencode

# Install Python dependencies for MCP servers
pip install httpx fastmcp scholarly

# Copy environment template
cp .env.example .env

# Edit .env with your API keys (most work without keys)
nano .env
```

### Configuration

Edit `.env` to add your API keys (most servers work without them):

```bash
# Required only for IEEE Xplore and Zotero
IEEE_API_KEY=your_key_here
ZOTERO_API_KEY=your_key_here
ZOTERO_USER_ID=your_id_here

# Optional — improves rate limits and reliability
SEMANTIC_SCHOLAR_API_KEY=your_key_here
NCBI_API_KEY=your_key_here
OPENALEX_EMAIL=your@email.com
CROSSREF_MAILTO=your@email.com
```

### Start Using

```bash
# Launch OpenCode with the academic project
opencode

# Or use slash commands directly
/search-papers "transformer attention mechanisms"
/review-literature "face recognition in low light"
/write-paper "quantum computing applications" --style ieee
/format-citations "10.1234/5678" --style apa
```

---

## 📖 Usage Examples

### Search Papers

```bash
# Basic search
> search for papers on "BERT pre-training"

# Filtered search
> find recent papers on reinforcement learning from 2023-2025

# Specific database
> search arxiv for "large language model agents"
```

### Literature Review

```bash
# Systematic review
> conduct a systematic review on "federated learning privacy"

# With PRISMA methodology
> review-literature "transformer efficiency" --methodology prisma
```

### Write Paper

```bash
# Draft abstract
> write an abstract for my paper on "CNN-based image segmentation"

# Draft introduction with citations
> write an introduction about "reinforcement learning in robotics" with citations

# Full section drafting
> write-paper "topic" --section methodology --style ieee --format latex
```

### Citation Management

```bash
# Format a DOI
> format-citations "10.1038/nature12373" --style ieee

# Generate BibTeX
> generate bibtex for these 5 papers

# Validate references
> check if these DOIs are valid
```

### Paper Review

```bash
# Expert review
> review-paper "Attention Is All You Need"

# By DOI
> review this paper: 10.48550/arXiv.1706.03762
```

### Email Composition

```bash
# Collaboration email
> compose-email --type collaboration --to prof@university.edu

# Submission email
> draft a submission email for my paper to IEEE TPAMI
```

---

## 🗂️ Project Structure

```
academic-opencode/
├── .opencode/
│   ├── academic-mode.json          # Auto-detection config
│   └── commands/
│       ├── academic-mode.md        # Auto-spawning documentation
│       ├── search-papers.md        # /search-papers command
│       ├── review-literature.md    # /review-literature command
│       ├── write-paper.md          # /write-paper command
│       ├── format-citations.md     # /format-citations command
│       ├── compose-email.md        # /compose-email command
│       ├── review-paper.md         # /review-paper command
│       ├── explain-paper.md        # /explain-paper command
│       ├── convert-document.md     # /convert-document command
│       └── convert-batch.md        # /convert-batch command
├── mcp_servers/
│   ├── fallback_utils.py           # Shared fallback utilities
│   ├── arxiv-mcp/                  # arXiv integration
│   ├── ieee-xplore-mcp/            # IEEE Xplore integration
│   ├── semantic-scholar-mcp/       # Semantic Scholar integration
│   ├── openalex-mcp/               # OpenAlex integration
│   ├── pubmed-mcp/                 # PubMed integration
│   ├── crossref-mcp/               # Crossref integration
│   ├── ssrn-mcp/                   # SSRN integration
│   ├── acm-dl-mcp/                 # ACM Digital Library
│   ├── dblp-mcp/                   # DBLP bibliography
│   ├── biorxiv-mcp/                # bioRxiv preprints
│   ├── europepmc-mcp/              # Europe PMC
│   ├── google-scholar-mcp/         # Google Scholar
│   ├── zotero-mcp/                 # Zotero references
│   └── document-converter/         # PDF/DOCX conversion
├── AGENTS.md                       # Agent auto-detection rules
├── .env                            # Environment variables
├── .mcp.json                       # MCP server definitions
└── .gitignore
```

---

## 🔧 Configuration Reference

### Auto-Detection Rules

The system automatically routes queries based on keywords:

| Query Pattern | Agent Spawned | Skills Loaded |
|---------------|---------------|---------------|
| "search for papers", "find research" | `research-agent` | `paper-search` |
| "review literature", "systematic review" | `review-agent` | `literature-review`, `paper-search` |
| "write paper", "draft section" | `writing-agent` | `paper-writing`, `citation-manager` |
| "format citation", "bibliography" | `Sisyphus-Junior` | `citation-manager` |
| "compose email", "submission email" | `Sisyphus-Junior` | `email-composer` |
| "review paper", "critique methodology" | `review-agent` | `paper-review` |
| "explain paper", "summarize findings" | `Sisyphus-Junior` | `paper-review` |
| "convert PDF", "extract text" | `Sisyphus-Junior` | `document-converter` |
| "find LaTeX template" | `Sisyphus-Junior` | `latex-assistant` |
| Any DOI (10.xxxx/xxxxx) | `research-agent` | `paper-search`, `citation-manager` |

### Fallback Behavior

When an MCP API fails, each server falls back to web search:

```
API Request → Success? → Return API results with method="api"
                ↓ (failure)
         Web Search → Return results with method="websearch"
```

Every result includes `_metadata`:
```json
{
  "_metadata": {
    "mcp_name": "ieee-xplore",
    "method": "api",
    "weblink": "https://ieeexplore.ieee.org/document/1234567"
  }
}
```

---

## 🛡️ API Keys Guide

### Required Keys

| Service | How to Get | Free Tier |
|---------|------------|-----------|
| **IEEE Xplore** | [developer.ieee.org](https://developer.ieee.org/) | 200 req/day |
| **Zotero** | [zotero.org/settings/keys](https://www.zotero.org/settings/keys) | Unlimited |

### Optional Keys (Improve Reliability)

| Service | How to Get | Benefit |
|---------|------------|---------|
| **Semantic Scholar** | [semanticscholar.org/product/api](https://www.semanticscholar.org/product/api) | Higher rate limits |
| **NCBI/PubMed** | [ncbi.nlm.nih.gov/labs/account](https://www.ncbi.nlm.nih.gov/labs/account/) | 10 req/sec → 3 req/sec without |
| **OpenAlex** | Just add your email | Polite pool (faster responses) |
| **Crossref** | Just add your email | Polite pool (faster responses) |

### Free-First Design

10 of 14 MCP servers require **zero API keys**. The system is designed to work out of the box:

- ✅ arXiv, ACM DL, SSRN, DBLP, bioRxiv, Europe PMC, Google Scholar — **always free**
- ✅ OpenAlex, Crossref — **free with email** (polite pool)
- ✅ PubMed — **free with optional key** (better rate limits)
- 🔑 IEEE Xplore, Zotero — **require keys**

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Adding a New MCP Server

```bash
# 1. Create server directory
mkdir mcp_servers/my-new-mcp

# 2. Create server.py with FastMCP
# 3. Add fallback logic using fallback_utils.py
# 4. Add to .mcp.json
# 5. Update AGENTS.md if needed
```

---

## 📋 Roadmap

- [ ] Zotero library synchronization
- [ ] BibTeX auto-generation from search results
- [ ] Figure/table extraction from PDFs
- [ ] Multi-language paper support
- [ ] Citation network visualization
- [ ] Automated related work generation
- [ ] Journal/conference recommendation engine

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [OpenCode](https://github.com/anthropics/opencode) — AI coding assistant framework
- [oh-my-openagent](https://github.com/anthropics/oh-my-openagent) — Agent orchestration
- [FastMCP](https://github.com/jlowin/fastmcp) — MCP server framework
- [Semantic Scholar](https://www.semanticscholar.org/) — Academic paper API
- [arXiv](https://arxiv.org/) — Open access preprints
- [PubMed](https://pubmed.ncbi.nlm.nih.gov/) — Biomedical literature
- [OpenAlex](https://openalex.org/) — Open catalog of scholarly works

---

<div align="center">

**Built with ❤️ for researchers, by researchers.**

[⭐ Star this repo](https://github.com/erfan-ashtari/academic-opencode) • [🐛 Report Bug](https://github.com/erfan-ashtari/academic-opencode/issues) • [💡 Request Feature](https://github.com/erfan-ashtari/academic-opencode/issues)

</div>
