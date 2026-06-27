---
name: anti-hallucination
description: Verify academic sources and detect fabricated citations. Use when checking if papers exist, if claims match cited sources, or before submitting any academic document. Detects 4 hallucination types and classifies source reliability.
triggers:
  - "verify citations"
  - "check for hallucinations"
  - "detect fabricated references"
  - "validate sources"
  - "citation integrity"
  - "source verification"
  - "check if paper exists"
  - "academic integrity check"
---

# Anti-Hallucination Verification

Detects fabricated citations, verifies academic source integrity, and classifies source reliability. This skill is the integrity layer that sits on top of citation formatting and DOI validation.

## When to Use

- Before submitting any academic document
- After writing sessions with many citations
- When uncertain about a source's existence or claims
- When reviewing someone else's draft for accuracy
- During quality assurance checks on manuscripts
- When a citation looks suspicious or too convenient

## How It Works

### Phase 1: Citation Extraction
1. Parse the document for all author-date pairs and numbered citations
2. Build a citation inventory with the claim each citation supports
3. Identify direct quotes vs. paraphrased claims

### Phase 2: Existence Verification
For each citation, verify in order:
1. **DOI Resolution** — Does the DOI resolve to a real paper?
2. **Semantic Scholar API** — Does the paper exist in the database?
3. **Google Scholar** — Can we find an exact title match?
4. **Crossref** — Does the metadata match?

### Phase 3: Accuracy Verification
For verified papers:
1. Check if the paper actually supports the cited claim
2. Verify page numbers for direct quotes
3. Confirm the context matches usage (not misattributed)
4. Check if findings have been superseded or contradicted

### Phase 4: Classification & Reporting
Classify each citation and generate a structured report.

## Hallucination Detection Patterns

### Type 1: Fabricated Reference
| Signal | Example |
|--------|---------|
| Author name is real, paper title is invented | "Smith (2023)" wrote a paper that doesn't exist |
| Year is plausible but incorrect | Citing 2023 for a 2019 paper |
| Journal name is real but paper not published there | Real journal, fake publication |
| DOI format is valid but non-resolving | 10.xxxx/xxxxx looks right but 404s |

### Type 2: Misattributed Claim
| Signal | Example |
|--------|---------|
| Paper exists but doesn't say what's claimed | Claim is from a different section or different paper |
| Claim is from a different paper entirely | Two papers confused due to similar topics |
| Claim is paraphrased incorrectly | Finding distorted to support a different argument |
| Page number is wrong for the quoted content | Correct paper, wrong location |

### Type 3: Outdated Information
| Signal | Example |
|--------|---------|
| Paper exists but findings have been superseded | Newer study contradicts the cited result |
| Methodology has been updated | Citing an old method when a better one exists |
| Results have been contradicted by replication | The original finding failed to replicate |

### Type 4: Predatory / Low-Quality Publication
| Signal | Example |
|--------|---------|
| Paper exists but in non-peer-reviewed venue | Preprint cited as peer-reviewed |
| Journal is on Beall's list or equivalent | Predatory publisher |
| Conference has no rigorous review process | Pay-to-publish venue |
| Conference proceedings not indexed | Not in DBLP, IEEE, or ACM |

## Source Reliability Tiers

### Tier 1: High Confidence
- Peer-reviewed journal articles ( SCI, SSCI, Scopus-indexed)
- Top-tier conference papers (NeurIPS, ICML, ACL, CVPR, etc.)
- Government and official institutional reports
- Systematic reviews and meta-analyses

### Tier 2: Medium Confidence
- Preprints from reputable servers (arXiv, bioRxiv, SSRN)
- Working papers from established research institutions
- Book chapters from academic publishers (Springer, Elsevier)
- Workshop papers at recognized venues

### Tier 3: Low Confidence
- Non-peer-reviewed blog posts and technical reports
- Industry reports without transparent methodology
- Wikipedia (as a primary source)
- Student theses (unless from top programs)
- News articles cited as academic evidence

### Tier 4: Unreliable
- Predatory journal publications
- Retracted papers
- Anonymous or unattributed sources
- Social media posts as academic evidence

## Verification Report Format

```markdown
## Citation Verification Report

**Document:** [filename or title]
**Date:** [verification date]
**Total citations checked:** X

### Summary
| Status | Count | Percentage |
|--------|-------|------------|
| VERIFIED | Y | % |
| MISMATCH | Z | % |
| NOT_FOUND | W | % |
| UNCERTAIN | V | % |
| OUTDATED | U | % |

### Issues Requiring Attention

#### Fabricated References
| # | Citation | Claim Supported | Problem | Suggested Fix |
|---|----------|-----------------|---------|---------------|
| 1 | [Author, Year] | "[claim]" | [issue] | [correction] |

#### Misattributed Claims
| # | Citation | Claim Supported | Problem | Suggested Fix |
|---|----------|-----------------|---------|---------------|
| 1 | [Author, Year] | "[claim]" | [issue] | [correction] |

#### Outdated Information
| # | Citation | Claim Supported | Current Status | Suggested Update |
|---|----------|-----------------|----------------|------------------|
| 1 | [Author, Year] | "[claim]" | [superseded by] | [newer source] |

#### Low-Quality Sources
| # | Citation | Venue | Concern | Recommendation |
|---|----------|-------|---------|----------------|
| 1 | [Author, Year] | [venue] | [issue] | [alternative] |

### Verified Citations
| # | Citation | Status | DOI | Tier |
|---|----------|--------|-----|------|
| 1 | [Author, Year] | ✓ Verified | [link] | 1 |

### Reliability Assessment
**Overall document reliability:** [High / Medium / Low]
**Percentage of verified citations:** [X%]
**Critical issues found:** [count]

### Recommendations
1. [Highest priority fix]
2. [Second priority fix]
3. [General improvement suggestion]
```

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `reference-validator` | Validates DOI format/existence; anti-hallucination goes deeper with claim verification |
| `citation-manager` | Formats verified citations; anti-hallucination flags which citations to keep |
| `paper-search` | Searches for replacement sources when citations fail verification |
| `literature-review` | Ensures all cited papers in the review are verified |

## Fallback Behavior

When MCP servers are unavailable for verification:
1. Use `webfetch` on `https://doi.org/{doi}` to check DOI resolution
2. Use `websearch` to search for exact paper title
3. Cross-check author names against known researcher profiles
4. Flag all web-verified results with `verification_source: "web-fallback"`
5. Recommend human verification for any uncertain results

## Output

- Complete verification report with issue classification
- Reliability tier for each source
- Suggested fixes for every issue found
- Overall document reliability score
- Actionable recommendations before submission

## Present Results to User

```
## Anti-Hallucination Check Complete

**Citations checked:** X
**Verified:** Y ✓
**Issues found:** Z ⚠️

### Critical Issues
1. **[Author, Year]** — Fabricated reference
   - Claim: "[quote]"
   - Problem: Paper not found in any database
   - Action: Remove citation or find alternative source

### Document Reliability: [HIGH / MEDIUM / LOW]

**Recommendation:** [What to fix before submission]
```

## Troubleshooting

- If Semantic Scholar API is unavailable: fall back to Google Scholar + DOI resolution
- If DOI doesn't resolve: check for typos, try `https://dx.doi.org/{doi}`
- If paper is behind paywall: verify metadata only (title, authors, year) via abstract
- If author name is ambiguous: search with co-authors or affiliation to disambiguate
- If paper is very recent: note that it may not be indexed yet; flag for human review
