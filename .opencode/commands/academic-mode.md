---
description: Toggle academic mode on/off for automatic academic tool usage
---

# /academic-mode

Toggle academic mode to control whether academic tools are used automatically.

## Usage

```
/academic-mode on    # Enable academic mode
/academic-mode off   # Disable academic mode
/academic-mode       # Toggle current state
```

## Behavior

**When ON:**
- All research queries automatically use `/search-papers`
- Writing tasks default to `/write-paper`
- Citation formatting uses `/format-citations`
- PDFs are converted with `/convert-document`
- Emails use `/compose-email`

**When OFF:**
- Academic tools only used when explicitly requested
- Standard development workflow applies

## Configuration

Updates `academic_mode` in `opencode.json`:
```json
{
  "academic_mode": true
}
```
