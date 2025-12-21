# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is an **Agent Skill** that teaches how to build CLI applications using amplifier-foundation patterns. It contains documentation and example bundles, not executable code.

## Repository Structure

- `SKILL.md` - Primary skill definition (YAML frontmatter + Markdown body)
- `assets/` - Working example bundles referenced by SKILL.md
- `references/` - Architecture docs and audit prompts
- `AGENTS.md` - Repository guidelines (read this for coding style, naming conventions)

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

## When Editing

- Keep SKILL.md and assets/ in sync - if you add/change an example, update the corresponding asset file
- Bundle files use YAML frontmatter with `---` delimiters
- Provider files (`.yaml`) are pure YAML
- Agent/bundle files (`.md`) are Markdown with YAML frontmatter
- Use kebab-case for filenames (e.g., `bug-hunter.md`, `anthropic.yaml`)

## Foundation Alignment Checklist

When adding examples or documentation, verify:
- [ ] Shows `load_bundle → compose → prepare → create_session → execute` workflow
- [ ] Uses `base.compose(overlay)` for composition
- [ ] Uses `prepared.spawn()` for agent delegation (not custom spawners)
- [ ] Warns against copying amplifier-app-cli internals directly
