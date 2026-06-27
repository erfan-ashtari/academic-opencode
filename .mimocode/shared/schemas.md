# Shared Contracts and Schemas

Common definitions used across all skills and agents for consistent inter-agent communication.

## Data Access Levels

Every skill declares its data access requirements:

| Level | Description | Examples |
|-------|-------------|----------|
| `raw` | Can access unprocessed user data | Email drafts, raw notes, unverified sources |
| `redacted` | Can access anonymized/aggregated data | Literature summaries, synthesis reports |
| `verified_only` | Can only access verified sources | Citation checks, reference validation |

## Task Types

Every skill declares its task type:

| Type | Description | Examples |
|------|-------------|----------|
| `open-ended` | No single correct answer | Writing, teaching, synthesis |
| `outcome-gradable` | Can be evaluated against criteria | Citation verification, quality assessment |

## Source Reliability Tiers

```yaml
reliability_tiers:
  high:
    - peer_reviewed_journal
    - conference_proceedings (top venues)
    - government_report
    - systematic_review
    - meta_analysis
  medium:
    - preprint (arXiv, bioRxiv, SSRN)
    - working_paper
    - book_chapter
    - workshop_paper
  low:
    - blog_post
    - industry_report
    - wikipedia (as primary source)
    - student_thesis
  unreliable:
    - predatory_journal
    - retracted_paper
    - anonymous_source
    - social_media
```

## Citation Schema

```yaml
citation:
  required:
    - authors
    - year
    - title
    - source
  optional:
    - doi
    - volume
    - issue
    - pages
    - url
    - access_date
    - arxiv_id
    - pmid
```

## Quality Gate Schema

```yaml
quality_gate:
  stage: string
  status: enum[pending, passed, failed]
  checklist: list[string]
  notes: string
  timestamp: datetime
```

## Material Passport Schema

```yaml
material_passport:
  project_name: string
  current_stage: string
  artifacts: list[artifact]
  quality_gates: list[quality_gate]
  notes: string

artifact:
  name: string
  location: string
  status: enum[draft, review, final]
  last_modified: datetime
```

## Paper Search Result Schema

```yaml
paper:
  title: string
  authors: list[string]
  year: integer
  abstract: string
  doi: string | null
  arxiv_id: string | null
  pmid: string | null
  venue: string
  citations: integer
  url: string
  pdf_url: string | null
  pdf_available: boolean
  source: string  # database name or "web-fallback"
  reliability_tier: enum[high, medium, low, unreliable]
```

## Review Report Schema

```yaml
review:
  paper_title: string
  summary: string
  strengths: list[string]
  weaknesses: list[string]
  detailed_comments: map[string, string]  # section -> comment
  questions: list[string]
  recommendation: enum[accept, minor_revision, major_revision, reject]
  score: integer  # 1-10
  reviewer_confidence: enum[high, medium, low]
```

## Email Schema

```yaml
email:
  type: enum[inquiry, collaboration, submission, revision, thank_you, follow_up, conference]
  recipient_name: string
  recipient_title: string  # Prof., Dr., Mr., Ms.
  recipient_affiliation: string
  subject: string
  body: string
  attachments: list[string] | null
  formality_level: enum[formal, semi_formal, informal]
```

## Pipeline Stage Schema

```yaml
pipeline_stage:
  name: enum[define, research, outline, draft, review, revise, finalize]
  status: enum[pending, in_progress, completed]
  started: datetime | null
  completed: datetime | null
  quality_gate_passed: boolean | null
  artifacts: list[string]
  notes: string
```
