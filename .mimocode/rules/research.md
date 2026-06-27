---
paths:
  - "resources/**/*.md"
  - "resources/**/*.pdf"
  - "surveys/**/*.md"
  - "surveys/**/*.pdf"
---

# Research & Resource Finding Rules

## File Handling

**Convert downloaded papers (PDFs) to .md for analysis:**

```bash
/convert-document <paper.pdf>
```

Store in the same directory. This enables text search, summarization, and citation extraction.

## Search Strategy

### Database Priority

| Priority | Database | Coverage |
|----------|----------|----------|
| 1 | Semantic Scholar | Cross-discipline, citation network |
| 2 | Google Scholar | Broad coverage, citation tracking |
| 3 | arXiv | CS, Physics, Math, Stats, Bio, Econ |
| 4 | PubMed | Biomedical, life sciences |
| 5 | IEEE Xplore | Engineering, computer science |
| 6 | ACM Digital Library | Computing, information science |
| 7 | OpenAlex | Cross-discipline, open access |
| 8 | Crossref | DOI metadata, citation data |
| 9 | SSRN | Social sciences, humanities, legal |
| 10 | DBLP | CS bibliography |
| 11 | bioRxiv | Biology, biotech preprints |
| 12 | Europe PMC | Biomedical, life sciences |
| 13 | Scopus | Cross-discipline (if available) |

### Search Techniques
- Start broad, then narrow with filters
- Use Boolean operators: AND, OR, NOT
- Use quotes for exact phrases: "machine learning"
- Use wildcards: educat* (finds education, educational, educator)
- Check "Cited by" for newer related work
- Check references of key papers for foundational work
- Use `/search-papers` for parallel multi-database search

### Search Documentation
```markdown
## Search Documentation

### Query
[Exact search terms used]

### Databases
[List of databases searched]

### Filters
[Applied filters: year range, peer-review, language]

### Results
- Total found: X
- After screening: Y
- Included: Z
```

## Source Evaluation

### CRAAP Test
- **Currency** — When was it published? Is it still relevant?
- **Relevance** — Does it relate to your research question?
- **Authority** — Who are the authors? What are their credentials?
- **Accuracy** — Is it peer-reviewed? Are claims supported by evidence?
- **Purpose** — Is it objective? Any bias or conflict of interest?

### Source Reliability Tiers

| Tier | Types | Confidence |
|------|-------|------------|
| 1 — High | Peer-reviewed journals, top conferences, government reports, systematic reviews | High |
| 2 — Medium | Preprints (arXiv, bioRxiv, SSRN), working papers, book chapters | Medium |
| 3 — Low | Blog posts, industry reports, Wikipedia (as primary source) | Low |
| 4 — Unreliable | Predatory journals, retracted papers, anonymous sources | None |

### Red Flags
- No peer review process
- Anonymous authors
- No citations to other work
- Emotional language, not evidence-based
- Predatory journal (check Beall's list or DOAJ)
- Results too good to be true
- Small sample size without justification

## Organization
- Use a reference manager (Zotero, Mendeley, EndNote)
- Tag papers by theme/methodology/status
- Keep an annotated bibliography for key papers
- Track which papers support/contradict your argument
- Use `/summarize` for quick paper summaries

## Quality Checklist
- [ ] Search strategy is documented and reproducible
- [ ] Multiple databases were searched
- [ ] Inclusion/exclusion criteria are defined
- [ ] Sources are evaluated for reliability
- [ ] Key papers are verified with `/verify-citations`
- [ ] Annotated bibliography maintained
