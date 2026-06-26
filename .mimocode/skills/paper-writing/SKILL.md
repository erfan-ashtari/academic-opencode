---
name: paper-writing
description: Write academic paper sections (abstract, introduction, methods, results, discussion, conclusion). Manage citations, follow journal formatting, convert between LaTeX and Markdown.
triggers:
  - "write paper"
  - "draft introduction"
  - "write abstract"
  - "methods section"
  - "results section"
  - "discussion section"
  - "write conclusion"
  - "manuscript"
  - "academic writing"
  - "paper outline"
  - "related work"
  - "paper template"
  - "convert paper to latex"
  - "convert paper to markdown"
---

# Paper Writing Skill

Write structured academic papers with section templates, citation integration, and dual LaTeX/Markdown output.

## How It Works

1. **Analyze Requirements**: Determine paper type, target venue, formatting constraints
2. **Gather References**: Search for or import citations via citation-manager
3. **Select Template**: Choose section structure based on paper type
4. **Draft Sections**: Generate content following academic writing conventions
5. **Integrate Citations**: Insert references at appropriate points
6. **Review Consistency**: Ensure logical flow and terminology alignment
7. **Format Output**: Apply target venue formatting rules
8. **Export**: Produce final draft with complete bibliography

## Paper Sections

| Section | Purpose | Suggested Length |
|---------|---------|------------------|
| Title | Paper identity | 10-20 words |
| Abstract | Complete summary | 150-300 words |
| Introduction | Context and motivation | 5-10% of total |
| Related Work | Literature positioning | 10-15% of total |
| Methodology | Technical approach | 20-30% of total |
| Experiments | Empirical validation | 15-25% of total |
| Results | Quantitative findings | 10-15% of total |
| Discussion | Interpretation | 10-15% of total |
| Conclusion | Wrap-up | 5-10% of total |

## Citation Styles

| Style | Fields | In-Text Format |
|-------|--------|----------------|
| APA 7th | Psychology, Education | (Author, Year) |
| IEEE | Engineering, CS | [Number] |
| Chicago | History, Humanities | Footnotes |
| MLA | Literature, Arts | (Author Page) |
| Harvard | UK Universities | (Author Year) |
| Vancouver | Medicine | Superscript |

## Output Formats

### Markdown
- For drafting and review
- GitHub-Flavored Markdown + LaTeX math
- Inline citations: [[key]], [1], or (Author, Year)

### LaTeX
- For submission to venues
- pdflatex, xelatex, or lualatex
- Citations: \cite{key} or \parencite{key}

## Usage Examples

```bash
# Write abstract
/write-paper abstract --topic "attention mechanisms for NLP" --words 250

# Draft introduction
/write-paper introduction --contributions "novel architecture, 15% improvement"

# Write methods section
/write-paper methods --approach "transformer with linear attention"

# Generate full outline
/write-paper outline --type research --venue conference

# Convert to LaTeX
/write-paper convert paper.md --to latex --venue icml
```

## Dependencies

| Dependency | Purpose |
|-----------|---------|
| citation-manager | Format citations, generate BibTeX |
| latex-assistant | LaTeX compilation, template management |
| reference-validator | Validate DOI, check completeness |
| paper-search | Find reference papers |
| literature-review | Systematic review for related work |
