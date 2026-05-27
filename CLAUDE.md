# CLAUDE.md - AI Assistant Guidelines for Testy1-Santa

This file provides guidance for AI assistants (like Claude) working with this codebase.

## Project Overview

**Repository:** fitkidznj-commits/Testy1-Santa
**Status:** Early-stage repository (bootstrapping phase)
**Last Updated:** 2026-05-27

This repository is in its initial setup phase. It contains only this CLAUDE.md file so far. As the project develops, this document should be updated to reflect the actual codebase structure, conventions, and workflows.

---

## Repository Structure

```
Testy1-Santa/
├── CLAUDE.md          # This file - AI assistant guidelines
└── .git/              # Git repository metadata
```

Only one file has been committed so far. Update this section as the project grows.

---

## Current Git State

- **Commits:** 1 (initial CLAUDE.md)
- **Active branch:** `claude/claude-md-docs-YkSLj`
- **Known branches:**
  - `claude/add-claude-documentation-PzRnt` — first session that created CLAUDE.md
  - `claude/claude-md-docs-YkSLj` — current documentation update session
- **Remote:** `fitkidznj-commits/Testy1-Santa` (via GitHub MCP proxy)

No `main` or `master` branch exists yet. The first stable branch should be created once the project has meaningful content.

---

## Execution Environment

This repository is used with **Claude Code on the web** (remote execution mode). Each session runs in an isolated, ephemeral container. Key implications:

- The container is wiped after the session ends — commit and push everything worth keeping.
- Use `git push -u origin <branch-name>` to persist changes.
- The `gh` CLI is not available; use the GitHub MCP tools (`mcp__github__*`) for GitHub interactions.
- Network access is governed by the environment's network policy.

---

## Development Workflow

### Git Branch Strategy

- **Feature branches:** Use the `claude/` prefix for AI-assisted development.
  - Format: `claude/<description>-<session-id>`
  - Example: `claude/add-feature-XyZ123`
- **Stable branch:** Establish `main` once meaningful content lands.
- Each Claude Code session should target the branch specified in its system instructions.

### Commit Guidelines

- Write clear, descriptive commit messages.
- Use conventional commit prefixes when applicable:
  - `feat:` — new features
  - `fix:` — bug fixes
  - `docs:` — documentation changes
  - `refactor:` — code refactoring
  - `test:` — adding/updating tests
  - `chore:` — maintenance tasks
- Do not commit secrets, credentials, `.env` files, or large binaries.

### Push Protocol

Always push with:

```bash
git push -u origin <branch-name>
```

On network failure, retry up to 4 times with exponential backoff (2 s, 4 s, 8 s, 16 s).

### Pull Request Process

1. Create feature branch from the base branch.
2. Make atomic commits with descriptive messages.
3. Push to remote.
4. Create PR only when the user explicitly requests it — do not create PRs automatically.

---

## Code Conventions

### General Principles

1. **Readability:** Write clear, self-documenting code.
2. **Simplicity:** Prefer simple solutions over complex ones.
3. **Consistency:** Follow existing patterns in the codebase.
4. **Testing:** Include tests for new functionality.
5. **Security:** Never commit secrets, credentials, or sensitive data.
6. **No over-engineering:** Don't add abstractions or features beyond what the task requires.

### Comments

- Default to writing no comments.
- Only add a comment when the *why* is non-obvious (hidden constraint, subtle invariant, workaround for a specific bug).
- Never write multi-paragraph docstrings or multi-line comment blocks.

### File Organization

- Keep related files together in logical directories.
- Use descriptive file and directory names.
- Maintain a flat structure where possible; nest only when necessary.

---

## AI Assistant Guidelines

### Before Making Changes

1. **Read first:** Always read files before modifying them.
2. **Understand context:** Explore the codebase to understand existing patterns.
3. **Ask:** If requirements are unclear, ask for clarification.

### When Making Changes

1. **Minimal changes:** Only modify what's necessary for the task.
2. **Preserve style:** Match existing code style and conventions.
3. **No over-engineering:** Avoid adding unnecessary features or abstractions.
4. **Security:** Check for injection, XSS, and other OWASP top-10 vulnerabilities.
5. **Test:** Verify changes work as expected before reporting completion.

### After Making Changes

1. **Commit:** Create clear, descriptive commits (only when explicitly asked).
2. **Push:** Push to the designated feature branch.
3. **Document:** Update this file if the project structure changes.

### Things to Avoid

- Creating unnecessary files (markdown/docs) unless explicitly requested.
- Adding emojis unless explicitly requested.
- Guessing at file contents — always read first.
- Making changes beyond what was requested.
- Committing without explicit permission.
- Pushing to a branch other than the one specified in session instructions.
- Creating pull requests unless the user explicitly asks.

---

## Common Tasks

### Starting Development

```bash
# Check current branch
git branch

# Create a feature branch (if needed)
git checkout -b claude/<feature-name>-<session-id>
```

### Making a Commit

```bash
# Stage specific files (avoid git add -A to prevent accidental secret commits)
git add <files>

# Commit with descriptive message
git commit -m "feat: add new feature description"

# Push to remote
git push -u origin <branch-name>
```

### GitHub Interactions

Since `gh` CLI is unavailable in this environment, use MCP tools:

- View/create PRs: `mcp__github__pull_request_read`, `mcp__github__create_pull_request`
- Add comments: `mcp__github__add_issue_comment`
- Check CI / reviews: `mcp__github__pull_request_read`

Only interact with the `fitkidznj-commits/Testy1-Santa` repository. Calls targeting other repositories will be denied.

---

## Project-Specific Notes

> Add project-specific information here as the codebase develops:
> - Build commands
> - Test commands
> - Environment setup
> - Dependencies
> - Configuration files
> - Linting / formatting tools

---

## Updating This Document

Update this CLAUDE.md when:

1. Project structure changes significantly.
2. New development workflows are established.
3. Coding conventions are defined or modified.
4. Important dependencies or tools are added.
5. Build/test/deploy processes are set up.
6. The git branch topology changes (new stable branch, etc.).
