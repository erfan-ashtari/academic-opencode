---
description: Generate hierarchical AGENTS.md files throughout the project
---

# /init-deep

Generate hierarchical AGENTS.md files at different project levels.

## Usage

```
/init-deep
```

## Output Structure

```
project/
├── AGENTS.md              ← Project-wide context
├── src/
│   ├── AGENTS.md          ← Source-specific context
│   └── components/
│       └── AGENTS.md      ← Component-specific context
```
