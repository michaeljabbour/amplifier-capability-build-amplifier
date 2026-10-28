# Contributing to amplifier-cli-skill

## What This Repository Is

This is an **Agent Skill** that teaches how to build CLI applications using amplifier-foundation patterns. It contains documentation and example bundles, not executable code.

## Repository Structure

- `SKILL.md` - Primary skill definition (YAML frontmatter + Markdown body)
- `references/` - All documentation and examples
  - `references/EXAMPLES.md` - Complete bundle examples (base, providers, agents)
  - `references/ARCHITECTURE*.md` - Architecture documentation
  - `references/BUILD_PATTERNS.md` - CLI build patterns
  - `references/HOOKS.md` - Hooks system documentation
  - `references/MEMORY.md` - Memory system guide
  - `references/CONTRIBUTING.md` - This file
- `scripts/` - Automation helpers (currently empty)

## Key Concept: Source of Truth

**amplifier-foundation is the source of truth**, not amplifier-app-cli. When documenting patterns:

```
CORRECT: load_bundle() → compose() → prepare() → create_session() → execute()
WRONG: Custom SessionStore, session_spawner, or other app-cli patterns
```

App-cli patterns should be labeled "reference only" - they are policy decisions, not the way to build.

## Validation Commands

```bash
# Verify references are correct
rg "references/" SKILL.md

# Validate SKILL.md structure
grep -A 5 "^---$" SKILL.md | head -20  # Check YAML frontmatter

# Test that examples in references/EXAMPLES.md are syntactically correct
# (Copy example to temporary file and load it)
```

## Coding Style & Naming Conventions

- **Markdown**: Use descriptive headings, fenced code blocks with language tags (e.g., ```python), and keep examples executable.
- **YAML/frontmatter**: 2-space indentation; keep frontmatter wrapped with `---` and include a trailing newline.
- **Naming**: Prefer kebab-case filenames (e.g., `bundles/dev.md`, `providers/anthropic.yaml`).

## Build, Test, and Development Commands

This repository is documentation + configuration examples; there is no build step.

- **Search/verify references**: `rg "references/" SKILL.md`
- **Check YAML frontmatter**: `grep -A 5 "^---$" SKILL.md | head -20`
- **Verify EXAMPLES.md**: Ensure all bundle examples are complete and syntactically correct

## When Editing

- Keep SKILL.md and references/EXAMPLES.md in sync - if you add/change an example, update EXAMPLES.md accordingly
- Bundle files use YAML frontmatter with `---` delimiters
- Provider files (`.yaml`) are pure YAML
- Agent/bundle files (`.md`) are Markdown with YAML frontmatter
- Use kebab-case for filenames (e.g., `bug-hunter.md`, `anthropic.yaml`)

## Testing Guidelines

- No automated test suite in this repo. Treat "tests" as validation:
  - Examples in `references/EXAMPLES.md` are syntactically correct.
  - Links and paths in `SKILL.md` resolve (especially under `references/`).

## Commit & Pull Request Guidelines

- This checkout may not include git history; default to Conventional Commits (`docs:`, `feat:`, `fix:`, `chore:`).
- **PRs**: Describe intent + affected files, keep changes scoped, and update `SKILL.md` and `references/EXAMPLES.md` together when examples change.

## Security & Configuration Tips

- Never commit API keys; use environment variables (e.g., `ANTHROPIC_API_KEY`) in examples.
- Prefer stable, pinned external references when practical; if using `@main`, call out why in the PR description.

## Foundation Alignment Checklist

When adding examples or documentation, verify:
- [ ] Shows `load_bundle → compose → prepare → create_session → execute` workflow
- [ ] Uses `base.compose(overlay)` for composition
- [ ] Uses `prepared.spawn()` for agent delegation (not custom spawners)
- [ ] Warns against copying amplifier-app-cli internals directly
