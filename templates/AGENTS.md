# AGENTS.md — Templates

## Purpose
Document templates for academic communications and papers.

## File Structure

```
templates/
├── email/              # Email templates (6 templates)
│   ├── inquiry.md
│   ├── collaboration.md
│   ├── submission.md
│   ├── revision.md
│   ├── thank_you.md
│   └── follow_up.md
├── latex/              # LaTeX templates
│   ├── article.md
│   ├── conference.md
│   ├── thesis.md
│   ├── elsevier/
│   └── ieee/
└── markdown/           # Markdown templates
    ├── paper.md
    ├── proposal.md
    └── review.md
```

## Usage

Templates are used by:
- `email-composer` skill → `email/` templates
- `paper-writing` skill → `latex/` and `markdown/` templates
- `latex-assistant` skill → `latex/` templates

## Adding Templates

### Email Templates

1. Create `.md` file in `email/`
2. Use placeholder variables:
   - `{TITLE}` — Subject/paper title
   - `{AUTHOR}` — Author name(s)
   - `{DATE}` — Date
   - `{PROFESSOR}` — Recipient name
   - `{UNIVERSITY}` — Institution name
   - `{DEPARTMENT}` — Department name

### LaTeX Templates

1. Create directory in `latex/` for venue-specific templates
2. Include `.tex` and `.bib` files
3. Add `README.md` with usage instructions

### Markdown Templates

1. Create `.md` file in `markdown/`
2. Use YAML frontmatter for metadata
3. Include section placeholders

## Template Format

```markdown
---
name: template-name
type: email|latex|markdown
venue: journal/conference name (if applicable)
style: citation style (if applicable)
---

# Template Content

Dear {PROFESSOR},

[Template body with {PLACEHOLDERS}]

Best regards,
{AUTHOR}
```

## Dependencies

- Used by: email-composer, paper-writing, latex-assistant skills
- Depends on: Nothing (standalone resources)
