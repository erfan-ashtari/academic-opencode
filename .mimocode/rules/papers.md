---
paths:
  - "papers/**/*.md"
  - "papers/**/*.tex"
  - "papers/**/*.pdf"
  - "surveys/**/*.md"
  - "surveys/**/*.pdf"
---

# Paper Writing Rules

## File Handling

**Convert PDFs and Office files to .md before editing:**

```bash
/convert-document <input.pdf>
```

Store the `.md` file alongside the original. Work with the `.md` version.

## Structure

### Empirical Paper (Default: APA 7th)
1. **Title** — Concise, includes key variables (10-20 words)
2. **Abstract** — 150-300 words: purpose, methods, findings, implications
3. **Introduction** — Hook → Background → Problem → Purpose → Research Questions → Contributions
4. **Literature Review** — Thematic organization, not chronological
5. **Methods** — Participants, Materials, Procedure, Analysis Plan
6. **Results** — Statistical reporting, tables, figures
7. **Discussion** — Interpretation, limitations, future directions
8. **Conclusion** — Summary of contributions, broader impact
9. **References** — APA format, DOI when available

### Literature Review / Survey
1. **Title** — "A Review of..." or "Survey of..."
2. **Abstract**
3. **Introduction** — Scope, search strategy, inclusion criteria
4. **Thematic Sections** — Organized by theme, not by paper
5. **Synthesis** — Cross-cutting findings, gaps, future directions
6. **Conclusion**
7. **References**

### Conference Paper (IEEE/ACM Style)
1. **Title** — Concise, technical
2. **Abstract** — 150-250 words
3. **Introduction** — Problem, motivation, contributions
4. **Related Work** — Position relative to existing approaches
5. **Methodology/Approach** — Technical details, algorithms
6. **Experiments/Evaluation** — Setup, datasets, baselines, results
7. **Discussion** — Analysis of results, limitations
8. **Conclusion** — Summary, future work
9. **References** — IEEE or ACM format

## Citation Rules
- Every claim needs a citation (except common knowledge)
- Prefer primary sources over secondary
- Include page numbers for direct quotes
- Use "et al." for 3+ authors (APA 7th) or as per venue style
- Verify DOIs resolve correctly
- Cross-check with Semantic Scholar or Google Scholar

## Citation Styles

| Style | Fields | In-Text Format |
|-------|--------|----------------|
| APA 7th | Psychology, Education | (Author, Year) |
| IEEE | Engineering, CS | [Number] |
| Chicago | History, Humanities | Footnotes |
| MLA 9th | Literature, Arts | (Author Page) |
| Harvard | UK Universities | (Author Year) |
| Vancouver | Medicine | Superscript |

## Formatting
- Double-spaced, 12pt Times New Roman (or as specified by venue)
- 1-inch margins
- Running head if required
- Page numbers in header
- Headings follow APA levels (or venue-specific levels)

## Anti-Hallucination Protocol
- NEVER fabricate citations — if unsure, say "citation needed"
- Always verify: Author (Year), Title, Journal, Volume, Pages, DOI
- Cross-check with Semantic Scholar API or Google Scholar
- Flag any source you cannot verify
- Use `/verify-citations` before submission

## Quality Checklist
- [ ] All claims are cited
- [ ] Citations are verified (use `/verify-citations`)
- [ ] Arguments are logical and flow clearly
- [ ] Structure matches target venue guidelines
- [ ] Writing is clear and concise
- [ ] Formatting is correct per venue
- [ ] Grammar and spelling checked
- [ ] Abstract accurately reflects the paper
- [ ] References match in-text citations
