---
name: start-pipeline
description: Start a multi-stage academic project with quality gates and progress tracking
arguments:
  - name: type
    description: Project type (paper, thesis, proposal)
    required: true
  - name: topic
    description: Project topic or title
    required: true
  - name: venue
    description: Target journal or conference (for papers)
    required: false
  - name: timeline
    description: Target completion date
    required: false
---

# Start Pipeline Command

Start a multi-stage academic project with quality gates between stages and artifact tracking.

## Usage

```bash
/start-pipeline paper "Attention Mechanisms for NLP" --venue NeurIPS
/start-pipeline thesis "Deep Learning in Medical Imaging" --timeline 2025-12
/start-pipeline proposal "Federated Learning for Healthcare" --venue NIH
```

## Pipeline Stages

| Stage | Description | Quality Gate |
|-------|-------------|--------------|
| 1. DEFINE | Scope, objectives, requirements | Scope clear, requirements documented |
| 2. RESEARCH | Literature review, source collection | Sources verified, gaps identified |
| 3. OUTLINE | Structure, arguments, citations | Structure approved, citation strategy defined |
| 4. DRAFT | Section-by-section writing | All sections complete, citations included |
| 5. REVIEW | Self-review, methodology check | Issues documented, revision plan created |
| 6. REVISE | Address issues, strengthen arguments | All issues addressed, quality standards met |
| 7. FINALIZE | Format, proofread, prepare submission | Formatting complete, submission ready |

## Project-Specific Workflows

### Paper Pipeline
- Target venue formatting
- Co-author coordination
- Cover letter preparation
- Supplementary materials

### Thesis Pipeline
- Committee checkpoints
- Proposal defense gate
- Chapter-by-chapter review
- University formatting

### Grant Proposal Pipeline
- Funder requirements research
- Budget justification
- Specific aims alignment
- Compliance checklist

## Project Passport

Tracks progress through the pipeline:
- Current stage and completion percentage
- Artifact inventory with locations
- Quality gate pass/fail status
- Decision log with rationale
- Next action recommendations

## Output

Returns:
- Pipeline status with stage progress
- Quality gate checklist
- Artifact inventory
- Next action recommendations
- Project passport for tracking

## Skill Used

`academic-pipeline`
