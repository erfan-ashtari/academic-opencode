---
name: reference-validator
description: Validate DOIs, check reference completeness, verify citation consistency, and ensure bibliography accuracy.
triggers:
  - "validate references"
  - "check doi"
  - "verify citations"
  - "reference validation"
---

# Reference Validator Skill

Validate DOIs, check reference completeness, verify citation consistency, and ensure bibliography accuracy.

## Features

- DOI format validation
- DOI existence verification
- Reference completeness checks
- Citation-bibliography cross-validation
- Style consistency verification
- Missing field detection

## Validation Checks

| Check | Description |
|-------|-------------|
| DOI Format | Proper DOI syntax (10.xxxx/xxxxx) |
| DOI Exists | Verify DOI resolves to real paper |
| Required Fields | All required fields present |
| Style Consistency | All refs follow same style |
| Cross-Reference | Every citation has bibliography entry |
| Year Valid | Publication year is reasonable |

## Usage

```bash
# Validate all references in paper
/validate-references paper.md

# Validate specific bibliography
/validate-references references.bib

# Check DOI specifically
/validate-doi 10.1234/5678
```
