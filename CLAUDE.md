# CLAUDE.md - AI Assistant Guidelines for Testy1-Santa

This file provides guidance for AI assistants (like Claude) working with this codebase.

## Project Overview

**Repository:** fitkidznj-commits/Testy1-Santa
**Status:** Initial setup — no application code yet
**Last Updated:** 2026-05-17

This repository is in its earliest phase. Only this CLAUDE.md exists as tracked content. Update this document as the project evolves.

---

## Repository Structure

```
Testy1-Santa/
├── CLAUDE.md          # This file - AI assistant guidelines
└── .git/              # Git repository metadata
```

---

## Environment

This project is developed via **Claude Code on the web** (remote execution environment). Sessions run in isolated, ephemeral containers. The repository is cloned fresh each session, so all changes must be committed and pushed before the session ends.

- Remote: `fitkidznj-commits/Testy1-Santa` (GitHub)
- Git operations go through a local proxy at session startup
- No persistent local filesystem between sessions

---

## Development Workflow

### Git Branch Strategy

- **AI-assisted branches** use the `claude/` prefix
  - Format: `claude/<description>-<session-id>`
  - Examples in use: `claude/add-claude-documentation-FHzF1`, `claude/add-claude-documentation-PzRnt`
- **Main branch:** to be established as the project grows
- Always push with `git push -u origin <branch-name>`

### Commit Guidelines

Use conventional commit format:

| Prefix | Purpose |
|--------|---------|
| `feat:` | new feature |
| `fix:` | bug fix |
| `docs:` | documentation only |
| `refactor:` | code restructuring, no behavior change |
| `test:` | adding or updating tests |
| `chore:` | maintenance, tooling, config |

Write commit messages that explain *why*, not just *what*.

### Pull Request Process

1. Create a `claude/` feature branch
2. Make atomic, well-described commits
3. Push with `git push -u origin <branch-name>`
4. Create a PR only when the user explicitly requests one

---

## Code Conventions

### General Principles

1. **Readability:** Write clear, self-documenting code
2. **Simplicity:** Prefer simple over clever; avoid premature abstractions
3. **Consistency:** Follow existing patterns — read before writing
4. **Security:** Never commit secrets, credentials, API keys, or `.env` files
5. **Testing:** Include tests for new functionality when a test framework exists

### File Organization

- Group related files in logical directories
- Use descriptive, lowercase names with hyphens for directories
- Prefer flat structure; nest only when necessary

### Comments

Write comments only when the **why** is non-obvious. Avoid restating what the code already says. Never write multi-line block comments for routine logic.

---

## AI Assistant Guidelines

### Before Making Changes

1. Read files before modifying — never guess at contents
2. Explore the codebase to understand existing patterns
3. Ask for clarification if the task is ambiguous
4. Prefer editing existing files over creating new ones

### When Making Changes

1. Change only what is necessary for the task
2. Match existing code style and conventions
3. Do not add features, refactors, or abstractions beyond the request
4. Check for security issues (injection, XSS, exposed secrets, etc.)
5. Do not add emojis unless explicitly requested

### After Making Changes

1. Commit with a clear, conventional message
2. Push to the designated feature branch
3. Update this CLAUDE.md if the project structure or conventions change

### Things to Avoid

- Creating documentation files unless explicitly requested
- Committing without the user's explicit permission
- Amending published commits — create a new commit instead
- Force-pushing without explicit user approval
- Skipping pre-commit hooks (`--no-verify`)
- Adding unnecessary error handling or validation for impossible cases

---

## Common Commands

```bash
# Create and switch to a feature branch
git checkout -b claude/<feature>-<session-id>

# Stage specific files (prefer over git add -A)
git add <file1> <file2>

# Commit
git commit -m "feat: short description of change"

# Push and set upstream
git push -u origin claude/<feature>-<session-id>
```

---

## Project-Specific Notes

> To be filled in as the project develops:
> - Build commands
> - Test runner and commands
> - Environment variables and setup
> - Key dependencies
> - CI/CD configuration

---

## Updating This Document

Update CLAUDE.md when:

1. Application code is added (update structure, commands, conventions)
2. A test framework or build tool is introduced
3. CI/CD pipelines are configured
4. Coding conventions are formalized
5. The main branch is established

---

*Last updated 2026-05-17. Reflects actual repository state at that date.*
