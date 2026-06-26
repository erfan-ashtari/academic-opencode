# AGENTS.md - Project Instructions for OpenCode

This file provides context and instructions for AI coding agents working in this repository.

## Repository Overview

This is an academic research project managed with OpenCode and the oh-my-openagent plugin, enhanced with the academic-research-assistant plugin for paper search, citation management, and literature review.

## Development Guidelines

### Code Style
- Follow consistent coding conventions
- Write clean, readable, and maintainable code
- Use meaningful variable and function names
- Add comments only when necessary for complex logic

### Git Workflow
- Use descriptive commit messages
- Follow conventional commits format when possible
- Keep commits focused on single changes
- Review changes before committing

### Testing
- Write tests for new functionality
- Ensure existing tests pass before submitting changes
- Aim for meaningful test coverage

### Documentation
- Update documentation when changing public APIs
- Keep README.md current with setup instructions
- Document any configuration changes

## Agent Instructions

### Primary Agent (Sisyphus)
- You are the main orchestrator
- Plan before executing complex tasks
- Delegate to specialized agents when appropriate
- Drive tasks to completion

### Working with Code
- Read existing code before making changes
- Understand the codebase structure
- Follow existing patterns and conventions
- Test changes thoroughly

### Communication
- Be concise in responses
- Provide clear explanations when needed
- Ask for clarification when requirements are ambiguous

## Tools Available

### Code Editing
- Use edit tool for file modifications
- Prefer targeted edits over full file rewrites
- Verify changes after editing

### File Operations
- Use read tool to examine files
- Use grep to search code
- Use glob to find files by pattern

### Bash Commands
- Use bash for git operations
- Run tests and build scripts
- Check system status

### Web Operations
- Use webfetch to retrieve documentation
- Use websearch to find solutions

## Academic Research Tools

### Paper Search
- Search 13+ academic databases simultaneously
- Deduplicate results by DOI/title
- Tag PDF availability

### Citation Management
- Format citations in APA, IEEE, Chicago, MLA, Harvard, Vancouver
- Generate BibTeX entries
- Validate DOIs

### Literature Review
- Conduct systematic reviews with PRISMA methodology
- Citation snowballing
- Quality assessment

## Environment

- Platform: Windows
- Shell: PowerShell
- Working Directory: E:\project\academic-research-assistant\first_academic_project

## Security Notes

- Never commit secrets or API keys
- Use environment variables for sensitive data
- Review code for security vulnerabilities

## Performance

- Optimize for readability first
- Consider performance implications
- Profile when necessary

---

*This file is read by OpenCode agents at the start of each session.*
