---
name: compose-email
description: Compose professional academic emails for various scenarios
arguments:
  - name: type
    description: Email type (inquiry, collaboration, submission, revision, thank-you, conference)
    required: true
  - name: to
    description: Recipient name and affiliation
    required: true
  - name: topic
    description: Email topic or purpose
    required: true
  - name: paper
    description: Related paper title (if applicable)
    required: false
  - name: venue
    description: Conference/journal name (if applicable)
    required: false
---

# Compose Email Command

Compose professional academic emails for inquiries, collaboration, submissions, and more.

## Usage

```bash
/compose-email inquiry --to "Prof. Smith" --topic "your recent paper on transformers"
/compose-email collaboration --to "Dr. Johnson" --topic "joint research on climate models"
/compose-email submission --paper "Our Paper" --venue "NeurIPS"
/compose-email revision --paper "Our Paper" --venue "Journal of ML"
/compose-email thank-you --to "Dr. Lee" --reason "PhD mentoring"
```

## Email Types

| Type | Purpose |
|------|---------|
| inquiry | Ask questions, request information |
| collaboration | Propose research partnership |
| submission | Submit paper/manuscript |
| revision | Respond to reviewer feedback |
| thank-you | Express gratitude |
| conference | Registration, inquiries |

## Output

Returns:
- Subject line
- Email body (professional, concise)
- Personalization suggestions
- Attachment checklist

## Skill Used

`email-composer`
