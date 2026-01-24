# CLAUDE.md - AI Assistant Guidelines for Testy1-Santa

This file provides guidance for AI assistants (like Claude) working with this codebase.

## Project Overview

**Repository:** Testy1-Santa
**Status:** New project (initialized repository)
**Last Updated:** 2026-01-24

This repository is in its initial setup phase. As the project develops, this document should be updated to reflect the actual codebase structure, conventions, and workflows.

---

## Repository Structure

```
Testy1-Santa/
├── CLAUDE.md          # This file - AI assistant guidelines
└── .git/              # Git repository metadata
```

> **Note:** This is currently an empty repository. Update this section as the project grows.

---

## Development Workflow

### Git Branch Strategy

1. **Main Branch:** The primary stable branch (to be established)
2. **Feature Branches:** Use `claude/` prefix for AI-assisted development
   - Format: `claude/<description>-<session-id>`
   - Example: `claude/add-feature-XyZ123`

### Commit Guidelines

- Write clear, descriptive commit messages
- Use conventional commit format when applicable:
  - `feat:` for new features
  - `fix:` for bug fixes
  - `docs:` for documentation changes
  - `refactor:` for code refactoring
  - `test:` for adding/updating tests
  - `chore:` for maintenance tasks

### Pull Request Process

1. Create feature branch from main
2. Make changes with atomic commits
3. Push to remote with `git push -u origin <branch-name>`
4. Create PR with clear description of changes

---

## Code Conventions

### General Principles

1. **Readability:** Write clear, self-documenting code
2. **Simplicity:** Prefer simple solutions over complex ones
3. **Consistency:** Follow existing patterns in the codebase
4. **Testing:** Include tests for new functionality
5. **Security:** Never commit secrets, credentials, or sensitive data

### File Organization

- Keep related files together in logical directories
- Use descriptive file and directory names
- Maintain a flat structure where possible; nest only when necessary

---

## AI Assistant Guidelines

### Before Making Changes

1. **Read First:** Always read files before modifying them
2. **Understand Context:** Explore the codebase to understand existing patterns
3. **Plan:** Use TodoWrite to track multi-step tasks
4. **Ask:** If requirements are unclear, ask for clarification

### When Making Changes

1. **Minimal Changes:** Only modify what's necessary for the task
2. **Preserve Style:** Match existing code style and conventions
3. **No Over-Engineering:** Avoid adding unnecessary features or abstractions
4. **Security:** Check for vulnerabilities (injection, XSS, etc.)
5. **Test:** Verify changes work as expected

### After Making Changes

1. **Commit:** Create clear, descriptive commits
2. **Push:** Push to the designated feature branch
3. **Document:** Update documentation if needed

### Things to Avoid

- Creating unnecessary files (especially markdown/docs unless requested)
- Adding emojis unless explicitly requested
- Guessing at file contents - always read first
- Making changes beyond what was requested
- Committing without explicit permission

---

## Common Tasks

### Starting Development

```bash
# Clone the repository
git clone <repository-url>

# Create a feature branch
git checkout -b claude/<feature-name>-<session-id>

# Start development
```

### Making a Commit

```bash
# Stage changes
git add <files>

# Commit with descriptive message
git commit -m "feat: add new feature description"

# Push to remote
git push -u origin <branch-name>
```

---

## Project-Specific Notes

> Add project-specific information here as the codebase develops:
> - Build commands
> - Test commands
> - Environment setup
> - Dependencies
> - Configuration files

---

## Updating This Document

This CLAUDE.md should be updated when:

1. Project structure changes significantly
2. New development workflows are established
3. Coding conventions are defined or modified
4. Important dependencies or tools are added
5. Build/test/deploy processes are set up

---

*This document was auto-generated for a new repository. Update it as the project evolves.*
