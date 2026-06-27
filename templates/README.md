# Templates

Document templates for academic communications and papers.

## Overview

Templates provide standardized formats for academic documents. They are used by various skills to generate consistent, professional outputs.

## Directory Structure

```
templates/
├── email/              # Email templates
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

## Email Templates

| Template | Purpose | Used By |
|----------|---------|---------|
| `inquiry.md` | Initial inquiry to professors | email-composer |
| `collaboration.md` | Research collaboration request | email-composer |
| `submission.md` | Paper submission notification | email-composer |
| `revision.md` | Revision submission | email-composer |
| `thank_you.md` | Thank you notes | email-composer |
| `follow_up.md` | Follow-up emails | email-composer |

### Placeholder Variables

- `{TITLE}` — Subject/paper title
- `{AUTHOR}` — Author name(s)
- `{DATE}` — Date
- `{PROFESSOR}` — Recipient name
- `{UNIVERSITY}` — Institution name
- `{DEPARTMENT}` — Department name
- `{DOI}` — DOI identifier
- `{VENUE}` — Journal/conference name

## LaTeX Templates

| Template | Purpose | Used By |
|----------|---------|---------|
| `article.md` | Standard article format | latex-assistant, paper-writing |
| `conference.md` | Conference paper format | latex-assistant, paper-writing |
| `thesis.md` | Thesis/dissertation format | latex-assistant, paper-writing |
| `elsevier/` | Elsevier journal templates | latex-assistant |
| `ieee/` | IEEE conference templates | latex-assistant |

## Markdown Templates

| Template | Purpose | Used By |
|----------|---------|---------|
| `paper.md` | Paper draft template | paper-writing |
| `proposal.md` | Research proposal template | paper-writing |
| `review.md` | Paper review template | paper-review |

## Usage

### With Skills

Templates are automatically used by skills:

```bash
# Email composition
/compose-email --type collaboration --to prof@university.edu

# Paper writing
/write-paper "quantum computing applications" --style ieee

# LaTeX assistance
/find-latex-template --venue "NeurIPS"
```

### Manual Usage

You can also use templates directly:

1. Find the appropriate template
2. Replace placeholder variables
3. Customize as needed

## Adding Templates

### Email Templates

1. Create `.md` file in `email/`
2. Use placeholder variables
3. Include subject line and body
4. Update `templates/README.md`

### LaTeX Templates

1. Create directory in `latex/` for venue-specific templates
2. Include `.tex` and `.bib` files
3. Add `README.md` with usage instructions
4. Update `templates/README.md`

### Markdown Templates

1. Create `.md` file in `markdown/`
2. Use YAML frontmatter for metadata
3. Include section placeholders
4. Update `templates/README.md`

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
