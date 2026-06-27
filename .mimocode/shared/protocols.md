# Academic Research Protocols

Standard operating procedures for academic work across all agents and skills.

## Search Protocol

### Database Selection
1. **Primary databases:** Semantic Scholar, Google Scholar (broad coverage)
2. **Discipline-specific:** PubMed (biomedical), IEEE (engineering), ACM (CS), bioRxiv (biology)
3. **Preprint servers:** arXiv, bioRxiv, SSRN
4. **Supplementary:** OpenAlex, Crossref, DBLP, Europe PMC

### Search Strategy
1. Start with broad keywords
2. Use Boolean operators (AND, OR, NOT)
3. Apply filters (date, peer-review, language)
4. Check "Cited by" for newer work
5. Check references for foundational work
6. Use `/search-papers` for parallel multi-database search

### Documentation Template
```markdown
## Search Documentation

### Query
[Exact search terms used]

### Databases
[List of databases searched]

### Filters
[Applied filters: year range, peer-review, language]

### Results
- Total found: X
- After screening: Y
- Included: Z

### Search Date
[Date of search]
```

## Citation Protocol

### When to Cite
- Every factual claim (unless common knowledge)
- Direct quotes (with page numbers)
- Paraphrased ideas
- Data and statistics
- Methodologies used
- Definitions of terms

### Verification Checklist
- [ ] Author name spelled correctly
- [ ] Year is accurate
- [ ] Title matches published version
- [ ] Journal/venue is correct
- [ ] DOI resolves to correct paper
- [ ] Page numbers are accurate (for quotes)
- [ ] Use `/verify-citations` before submission

## Writing Protocol

### Structure
1. Lead with main point
2. Support with evidence
3. Analyze implications
4. Connect to broader context

### Voice
- Active voice preferred
- First person for methods ("I collected...")
- Past tense for findings ("The results showed...")
- Present tense for established knowledge ("Research indicates...")

### Transitions
- Between paragraphs: topic sentence connection
- Between sections: explicit signposting ("In the next section...")
- Between ideas: logical connectors ("However," "Furthermore," "In contrast...")

## Review Protocol

### Self-Review Checklist
- [ ] All claims are cited
- [ ] Citations are verified
- [ ] Arguments are logical
- [ ] Structure is clear
- [ ] Writing is clear
- [ ] Formatting is correct
- [ ] Grammar and spelling checked
- [ ] Abstract matches paper content
- [ ] References match in-text citations

### Peer Review Response
1. Address every comment
2. Quote the original comment
3. Describe the change made
4. If no change, explain why
5. Be respectful and professional
6. Use `/review-paper` for self-assessment before responding

## Quality Standards

### For All Academic Work
- No fabricated citations (use `/verify-citations`)
- Consistent citation style throughout
- Clear, logical argument structure
- Proper attribution of all sources
- Adherence to target venue guidelines

### Before Submission
1. Run `/verify-citations` on the document
2. Check formatting against venue guidelines
3. Verify all figures and tables are referenced
4. Ensure abstract is within word limit
5. Proofread for grammar and spelling
6. Get feedback from colleagues/advisor
