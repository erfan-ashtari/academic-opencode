---
name: academic-pipeline
description: Orchestrate multi-stage academic workflows with quality gates. Use for thesis chapters, grant proposals, paper submissions, or any complex multi-stage academic project.
triggers:
  - "academic pipeline"
  - "thesis chapter workflow"
  - "grant proposal workflow"
  - "paper submission pipeline"
  - "multi-stage academic project"
  - "academic project orchestration"
  - "research project workflow"
---

# Academic Pipeline

Orchestrates multi-stage academic work with quality gates between stages. Tracks project artifacts, enforces review checkpoints, and ensures nothing falls through the cracks.

## When to Use

- Writing thesis chapters (literature review, methodology, results, discussion)
- Preparing grant proposals (specific aims, research strategy, budget justification)
- Submitting papers to journals (drafting, revision, response to reviewers)
- Any multi-stage academic project requiring systematic progress

## Pipeline Stages

### Stage 1: DEFINE
- Clarify scope, objectives, and research questions
- Identify requirements (venue guidelines, word limits, formatting rules)
- Create project plan with milestones and deadlines
- Identify target audience and their expectations

### Stage 2: RESEARCH
- Conduct literature review using `literature-review` skill
- Gather sources and evidence using `paper-search` skill
- Document search strategy for reproducibility
- Identify research gaps and positioning

### Stage 3: OUTLINE
- Create detailed section structure
- Plan arguments and evidence flow
- Identify citation needs per section
- Map figures, tables, and supplementary materials

### Stage 4: DRAFT
- Write sections iteratively using `paper-writing` skill
- Include citations as you go using `citation-manager`
- Follow academic conventions for the target venue
- Maintain consistency in terminology and style

### Stage 5: REVIEW
- Self-review for quality and completeness
- Check methodology against research questions
- Verify all citations using `anti-hallucination` skill
- Run `paper-review` skill for structured feedback

### Stage 6: REVISE
- Address reviewer feedback systematically
- Strengthen weak arguments with additional evidence
- Fix issues identified in the review stage
- Re-verify citations after changes

### Stage 7: FINALIZE
- Format according to venue guidelines using `latex-assistant`
- Prepare submission materials (cover letter, highlights, graphical abstract)
- Final proofread using `proofreading` skill
- Generate submission package

## Quality Gates

### Gate 1: After DEFINE
- [ ] Research questions are clear and answerable
- [ ] Scope is well-defined (not too broad, not too narrow)
- [ ] Requirements documented (venue, word limit, formatting)
- [ ] Timeline established with realistic milestones
- [ ] Target audience identified

### Gate 2: After RESEARCH
- [ ] Literature review complete with systematic search strategy
- [ ] Key sources verified using `anti-hallucination`
- [ ] Research gaps identified and documented
- [ ] Positioning relative to existing work is clear
- [ ] Evidence base is sufficient for claims

### Gate 3: After OUTLINE
- [ ] Section structure approved
- [ ] Arguments and evidence flow logically
- [ ] Citation strategy defined per section
- [ ] Figures and tables planned
- [ ] Word count estimate is within limits

### Gate 4: After DRAFT
- [ ] All sections complete (no placeholders)
- [ ] Every claim has a citation
- [ ] Word count within limits (±10%)
- [ ] Terminology is consistent throughout
- [ ] Abstract accurately reflects the full paper

### Gate 5: After REVIEW
- [ ] All issues documented with severity levels
- [ ] Revision plan created with priorities
- [ ] Critical issues have proposed solutions
- [ ] Optional: External reviewer feedback incorporated

### Gate 6: After REVISE
- [ ] All critical issues addressed
- [ ] All major issues addressed
- [ ] Minor issues documented (acceptable for submission)
- [ ] Quality standards met for target venue
- [ ] Citations re-verified after revision

### Gate 7: After FINALIZE
- [ ] Formatting complete per venue guidelines
- [ ] All submission materials prepared
- [ ] Cover letter written
- [ ] Final proofread complete
- [ ] All co-authors have approved (if applicable)

## Project Passport

Track project artifacts and progress through the pipeline:

```markdown
## Project Passport: [Project Name]

### Status
- **Current Stage:** [stage name]
- **Started:** [date]
- **Last Updated:** [date]
- **Target Completion:** [date]
- **Next Action:** [specific next step]

### Stage Progress
| Stage | Status | Started | Completed | Gate Passed |
|-------|--------|---------|-----------|-------------|
| DEFINE | ✓ Done | [date] | [date] | ✓ |
| RESEARCH | ✓ Done | [date] | [date] | ✓ |
| OUTLINE | → In Progress | [date] | — | — |
| DRAFT | ⬚ Not Started | — | — | — |
| REVIEW | ⬚ Not Started | — | — | — |
| REVISE | ⬚ Not Started | — | — | — |
| FINALIZE | ⬚ Not Started | — | — | — |

### Artifacts
| Artifact | Location | Status | Last Modified |
|----------|----------|--------|---------------|
| Research Questions | [file] | ✓ Final | [date] |
| Literature Review | [file] | ✓ Final | [date] |
| Outline | [file] | → Draft | [date] |
| Draft v1 | [file] | ⬚ Not Started | — |
| Review Report | [file] | ⬚ Not Started | — |

### Quality Gates
| Gate | Stage | Status | Notes |
|------|-------|--------|-------|
| Gate 1 | After DEFINE | ✓ Passed | [date] |
| Gate 2 | After RESEARCH | ✓ Passed | [date] |
| Gate 3 | After OUTLINE | ⬚ Pending | — |
| Gate 4 | After DRAFT | ⬚ Pending | — |
| Gate 5 | After REVIEW | ⬚ Pending | — |
| Gate 6 | After REVISE | ⬚ Pending | — |
| Gate 7 | After FINALIZE | ⬚ Pending | — |

### Decision Log
| Date | Decision | Rationale |
|------|----------|-----------|
| [date] | [decision] | [why] |

### Notes
[Pipeline-specific notes, reminders, and context]
```

## Stage-Specific Workflows

### Thesis Chapter Pipeline
1. **DEFINE**: Chapter scope, research questions, advisor expectations
2. **RESEARCH**: Systematic literature review with PRISMA methodology
3. **OUTLINE**: Section structure with argument flow
4. **DRAFT**: Section-by-section writing with citations
5. **REVIEW**: Self-review + advisor feedback
6. **REVISE**: Address feedback, strengthen arguments
7. **FINALIZE**: Format per university guidelines, final proofread

### Grant Proposal Pipeline
1. **DEFINE**: Funding agency requirements, project scope, budget constraints
2. **RESEARCH**: Literature review, preliminary data analysis
3. **OUTLINE**: Specific aims, research strategy, budget justification
4. **DRAFT**: Write each section, prepare figures and budget
5. **REVIEW**: Internal review, mentor feedback
6. **REVISE**: Address feedback, strengthen significance/innovation
7. **FINALIZE**: Format per agency guidelines, prepare appendices

### Journal Paper Pipeline
1. **DEFINE**: Target journal, scope, contribution statement
2. **RESEARCH**: Literature review, position relative to state-of-the-art
3. **OUTLINE**: IMRAD structure, figure plan
4. **DRAFT**: Write sections, format citations
5. **REVIEW**: Co-author review, self-review, `paper-review` skill
6. **REVISE**: Address all feedback, re-verify citations
7. **FINALIZE**: Format per journal guidelines, prepare cover letter

## Integration with Other Skills

| Skill | Pipeline Stage |
|-------|----------------|
| `literature-review` | RESEARCH — Systematic search and synthesis |
| `paper-search` | RESEARCH — Finding sources |
| `paper-writing` | DRAFT — Section-by-section writing |
| `citation-manager` | DRAFT — Citation formatting |
| `anti-hallucination` | REVIEW — Citation verification |
| `paper-review` | REVIEW — Expert feedback |
| `reference-validator` | REVIEW — Reference integrity |
| `latex-assistant` | FINALIZE — Formatting and compilation |
| `document-converter` | FINALIZE — Format conversion |
| `email-composer` | FINALIZE — Submission correspondence |

## Output

- Stage-by-stage progress tracking with timestamps
- Quality gate checklists with pass/fail status
- Artifact inventory with locations and versions
- Decision log for tracking rationale
- Next action recommendations at each stage

## Present Results to User

```
## Pipeline Status: [Project Name]

**Current Stage:** [stage]
**Progress:** [X/7 stages complete] ([percentage])

### Completed Stages
✓ Stage 1: DEFINE — [date]
✓ Stage 2: RESEARCH — [date]
→ Stage 3: OUTLINE — in progress

### Next Steps
1. [Specific action to complete current stage]
2. [Upcoming action after that]

### Quality Gates
Gate 1: ✓ Passed
Gate 2: ✓ Passed
Gate 3: ⬚ Pending (next checkpoint)

### Artifacts
- [list of key files and their status]
```

## Troubleshooting

- **Stuck at a stage**: Review the quality gate checklist — identify which item is blocking progress
- **Scope creep**: Return to DEFINE stage, re-narrow scope, document decisions
- **Missing sources**: Trigger `paper-search` with expanded keywords or different databases
- **Quality gate failure**: Document specific issues, create targeted revision plan, don't proceed until resolved
- **Timeline pressure**: Prioritize critical sections, flag non-essential items for later
