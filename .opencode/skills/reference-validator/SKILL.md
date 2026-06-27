---
name: reference-validator
description: Validate DOIs, check reference completeness, verify citation consistency, ensure bibliography accuracy, and detect fabricated or problematic citations. Combines format validation with integrity verification.
triggers:
  - "validate references"
  - "check doi"
  - "verify citations"
  - "reference validation"
  - "check bibliography"
  - "reference integrity"
---

# Reference Validator Skill

Comprehensive reference validation combining DOI format checks, existence verification, completeness assessment, and citation integrity verification.

## Features

- DOI format validation and existence verification
- Reference completeness checks (all required fields present)
- Citation-bibliography cross-validation
- Style consistency verification
- Missing field detection
- Fabricated citation detection (via integration with `anti-hallucination`)
- Claim-source verification
- Source reliability tiering

## Validation Checks

### Format Validation
| Check | Description | Severity |
|-------|-------------|----------|
| DOI Format | Proper DOI syntax (10.xxxx/xxxxx) | Error |
| DOI Exists | Verify DOI resolves to real paper | Error |
| Author Format | Authors properly formatted | Warning |
| Year Valid | Publication year is reasonable (1900-current) | Warning |
| Journal/Venue | Journal name is recognized | Warning |

### Completeness Validation
| Check | Description | Severity |
|-------|-------------|----------|
| Required Fields | All required fields present for style | Error |
| Style Consistency | All refs follow same style | Warning |
| Cross-Reference | Every citation has bibliography entry | Error |
| Orphan Entry | Every bibliography entry has at least one citation | Warning |

### Integrity Validation (via `anti-hallucination`)
| Check | Description | Severity |
|-------|-------------|----------|
| Fabricated Reference | Paper doesn't exist in any database | Critical |
| Misattributed Claim | Paper exists but doesn't support the claim | Critical |
| Outdated Information | Findings have been superseded | Warning |
| Predatory Venue | Published in non-peer-reviewed venue | Warning |

## Validation Levels

### Level 1: Format Only (Fast)
Quick check of DOI format and required fields:
- DOI syntax validation
- Required field presence
- Year range check
- Style consistency

### Level 2: Existence Check (Medium)
Verify references actually exist:
- DOI resolution check
- Semantic Scholar API lookup
- Title/author verification
- Metadata matching

### Level 3: Full Integrity (Thorough)
Complete verification including claim checking:
- All Level 1 + Level 2 checks
- Claim-source verification
- Fabricated citation detection
- Source reliability tiering
- Outdated information detection

## Validation Report Format

```markdown
## Reference Validation Report

**Document:** [filename]
**Date:** [validation date]
**References checked:** [count]
**Validation level:** [1/2/3]

### Summary
| Status | Count | Action |
|--------|-------|--------|
| ✓ Valid | [count] | None |
| ⚠ Warning | [count] | Review recommended |
| ✗ Error | [count] | Must fix |
| 🔴 Critical | [count] | Must fix before submission |

### Errors (Must Fix)
| # | Reference | Issue | Suggested Fix |
|---|-----------|-------|---------------|
| 1 | [reference] | [issue] | [fix] |

### Warnings (Review Recommended)
| # | Reference | Issue | Suggested Fix |
|---|-----------|-------|---------------|
| 1 | [reference] | [issue] | [fix] |

### Critical Issues (Integrity)
| # | Reference | Issue | Evidence | Action |
|---|-----------|-------|----------|--------|
| 1 | [reference] | [fabricated/not found] | [search results] | [remove or find alternative] |

### Validated References
| # | Reference | DOI | Status | Tier |
|---|-----------|-----|--------|------|
| 1 | [reference] | [link] | ✓ Verified | 1 |

### Completeness Check
- **Total citations in text:** [count]
- **Entries in bibliography:** [count]
- **Matched:** [count]
- **Orphan citations:** [list]
- **Orphan entries:** [list]

### Style Consistency
- **Expected style:** [APA/IEEE/etc.]
- **Consistent:** [Yes/No]
- **Inconsistencies:** [list specific issues]

### Overall Assessment
- **References status:** [Pass / Needs Revision / Fail]
- **Completeness:** [X%]
- **Integrity:** [X% verified]
- **Recommendation:** [what to do before submission]
```

## Usage

```bash
# Quick format check (Level 1)
/validate-references paper.md --level 1

# Existence check (Level 2)
/validate-references paper.md --level 2

# Full integrity check (Level 3)
/validate-references paper.md --level 3

# Validate specific DOI
/validate-doi 10.1234/5678

# Validate bibliography file
/validate-references references.bib --style apa

# Check specific paper for fabricated citations
/validate-references paper.md --integrity
```

## Integration with Other Skills

| Skill | Integration Point |
|-------|-------------------|
| `anti-hallucination` | Level 3 integrity checks — fabricated citation detection, claim verification |
| `citation-manager` | Format validated citations in the correct style |
| `paper-search` | Search for replacement sources when citations fail |
| `paper-writing` | Validate references during the drafting stage |
| `literature-review` | Ensure all reviewed papers are verified |

## Fallback Behavior

When MCP servers are unavailable for validation:
1. Use `webfetch` on `https://doi.org/{doi}` to check DOI resolution
2. Use `websearch` to search for exact paper title
3. Cross-check metadata against available web sources
4. Flag all web-verified results with `source: "web-fallback"`
5. Recommend human verification for uncertain results

**Limitations without MCP:**
- Only DOI-based lookups possible (no title search)
- BibTeX generation may be incomplete
- Cross-reference checking limited
- Claim verification not available (requires full paper access)

## Output

- Complete validation report with severity levels
- DOI format and existence verification
- Reference completeness assessment
- Style consistency check
- Integrity verification (Level 3)
- Actionable recommendations for fixes

## Present Results to User

```
## Reference Validation: [filename]

**References checked:** [count]
**Level:** [1/2/3]

### Results
✓ Valid: [count]
⚠ Warnings: [count]
✗ Errors: [count]
🔴 Critical: [count]

### Must Fix
1. [issue description with fix]

### Overall: [PASS / NEEDS REVISION / FAIL]

**Recommendation:** [what to do before submission]
```

## Troubleshooting

- **DOI doesn't resolve**: Check for typos, try `https://dx.doi.org/{doi}`, try Google Scholar
- **Paper behind paywall**: Verify metadata only (title, authors, year) via abstract
- **Very recent paper**: May not be indexed yet; flag for human review
- **Non-English paper**: Verify metadata, note language for the user
- **Multiple papers with same title**: Use DOI or author + year to disambiguate
