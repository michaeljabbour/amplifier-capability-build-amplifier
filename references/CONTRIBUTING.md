# Contributing to amplifier-cli-skill

## What This Repository Is

This is an **Agent Skill** that teaches how to build CLI applications using amplifier-foundation patterns. It contains documentation and example bundles, not executable code.

## Repository Structure

- `SKILL.md` - Primary skill definition (YAML frontmatter + Markdown body)
- `assets/` - Working example bundles referenced by SKILL.md
  - `assets/providers/*.yaml` - Provider bundle examples (pure YAML)
  - `assets/bundles/*.md` - Bundle examples (Markdown with YAML frontmatter)
  - `assets/agents/*.md` - Agent bundle examples
- `references/` - Architecture docs, audit prompts, and deeper technical documentation
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
# Verify assets are referenced correctly
rg "assets/" SKILL.md

# Runtime validation (requires Python 3.10+, uv, network)
uv venv && uv pip install amplifier-foundation
uv run python -c "import asyncio; from amplifier_foundation import load_bundle; asyncio.run(load_bundle('./assets/bundles/base.md'))"
```

## Coding Style & Naming Conventions

- **Markdown**: Use descriptive headings, fenced code blocks with language tags (e.g., ```python), and keep examples executable.
- **YAML/frontmatter**: 2-space indentation; keep frontmatter wrapped with `---` and include a trailing newline.
- **Naming**: Prefer kebab-case filenames (e.g., `assets/bundles/dev.md`, `assets/providers/anthropic.yaml`).

## Build, Test, and Development Commands

This repository is documentation + configuration examples; there is no build step.

- **Search/verify references**: `rg "assets/" SKILL.md`
- **Optional runtime validation** (Python 3.10+, `uv`, network access for deps):
  - `uv venv && uv pip install amplifier-foundation`
  - `uv run python -c "import asyncio; from amplifier_foundation import load_bundle; asyncio.run(load_bundle('./assets/bundles/base.md'))"`

## When Editing

- Keep SKILL.md and assets/ in sync - if you add/change an example, update the corresponding asset file
- Bundle files use YAML frontmatter with `---` delimiters
- Provider files (`.yaml`) are pure YAML
- Agent/bundle files (`.md`) are Markdown with YAML frontmatter
- Use kebab-case for filenames (e.g., `bug-hunter.md`, `anthropic.yaml`)

## Testing Guidelines

- No automated test suite in this repo. Treat "tests" as validation:
  - Assets load without errors (see runtime validation above).
  - Links and paths in `SKILL.md` resolve (especially under `assets/` and `references/`).

## Commit & Pull Request Guidelines

- This checkout may not include git history; default to Conventional Commits (`docs:`, `feat:`, `fix:`, `chore:`).
- **PRs**: Describe intent + affected files, keep changes scoped, and update `SKILL.md` and `assets/` together when examples change.

## Security & Configuration Tips

- Never commit API keys; use environment variables (e.g., `ANTHROPIC_API_KEY`) in examples.
- Prefer stable, pinned external references when practical; if using `@main`, call out why in the PR description.

## Foundation Alignment Checklist

When adding examples or documentation, verify:
- [ ] Shows `load_bundle → compose → prepare → create_session → execute` workflow
- [ ] Uses `base.compose(overlay)` for composition
- [ ] Uses `prepared.spawn()` for agent delegation (not custom spawners)
- [ ] Warns against copying amplifier-app-cli internals directly
