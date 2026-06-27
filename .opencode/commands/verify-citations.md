---
name: verify-citations
description: Verify all citations in a document for fabricated references, misattributed claims, and source integrity
arguments:
  - name: input
    description: File path or paste text containing citations
    required: true
  - name: level
    description: Verification level (format, existence, full)
    required: false
    default: full
  - name: output
    description: Output report path (optional)
    required: false
---

# Verify Citations Command

Verify all citations in a document for fabricated references, misattributed claims, and source integrity issues.

## Usage

```bash
/verify-citations paper.md
/verify-citations paper.md --level existence
/verify-citations paper.md --level full --output report.md
```

## Verification Levels

| Level | Description | Speed |
|-------|-------------|-------|
| `format` | DOI format and required fields only | Fast |
| `existence` | Verify papers exist via DOI/search | Medium |
| `full` | Existence + claim verification + hallucination detection | Thorough |

## What It Checks

### Level 1: Format
- DOI syntax validation (10.xxxx/xxxxx)
- Required field presence
- Year range check (1900-current)
- Style consistency

### Level 2: Existence
- DOI resolution to real paper
- Semantic Scholar API lookup
- Title/author verification
- Metadata matching

### Level 3: Full Integrity
- Fabricated reference detection
- Misattributed claim verification
- Outdated information detection
- Predatory venue flagging
- Source reliability tiering

## Hallucination Detection

| Type | Signal | Action |
|------|--------|--------|
| Fabricated Reference | Paper doesn't exist in any database | Remove or find alternative |
| Misattributed Claim | Paper exists but doesn't support the claim | Fix citation or claim |
| Outdated Information | Findings have been superseded | Update to newer source |
| Predatory Venue | Published in non-peer-reviewed venue | Flag for review |

## Output

```markdown
## Citation Verification Report

**Document:** [filename]
**Total citations:** X
**Verified:** Y ✓
**Issues found:** Z ⚠️

### Issues by Type
| Type | Count | Severity |
|------|-------|----------|
| Fabricated | N | Critical |
| Misattributed | N | Critical |
| Outdated | N | Warning |
| Low-quality | N | Warning |

### Issues Detail
| # | Citation | Issue | Suggested Fix |
|---|----------|-------|---------------|
| 1 | [Author, Year] | [issue] | [fix] |

### Overall Assessment
- **Reliability:** [High/Medium/Low]
- **Verified:** [X%]
- **Recommendation:** [what to fix before submission]
```

## Skill Used

`anti-hallucination` + `reference-validator`
