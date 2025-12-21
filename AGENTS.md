# Repository Guidelines

## Project Structure & Module Organization

- `SKILL.md`: primary skill definition (YAML frontmatter + Markdown body).
- `assets/`: example bundles referenced by `SKILL.md`.
  - `assets/providers/*.yaml`: provider bundle examples (pure YAML).
  - `assets/bundles/*.md`: bundle examples (Markdown with YAML frontmatter).
  - `assets/agents/*.md`: agent bundle examples.
- `references/`: deeper architecture notes and audit prompts.
- `scripts/`: automation helpers (currently empty).

## Build, Test, and Development Commands

This repository is documentation + configuration examples; there is no build step.

- Search/verify references: `rg "assets/" SKILL.md`
- Optional runtime validation (Python 3.10+, `uv`, network access for deps):
  - `uv venv && uv pip install amplifier-foundation`
  - `uv run python -c "import asyncio; from amplifier_foundation import load_bundle; asyncio.run(load_bundle('./assets/bundles/base.md'))"`

## Coding Style & Naming Conventions

- Markdown: use descriptive headings, fenced code blocks with language tags (e.g., ```python), and keep examples executable.
- YAML/frontmatter: 2-space indentation; keep frontmatter wrapped with `---` and include a trailing newline.
- Naming: prefer kebab-case filenames (e.g., `assets/bundles/dev.md`, `assets/providers/anthropic.yaml`).

## Testing Guidelines

- No automated test suite in this repo. Treat “tests” as validation:
  - Assets load without errors (see runtime validation above).
  - Links and paths in `SKILL.md` resolve (especially under `assets/` and `references/`).

## Commit & Pull Request Guidelines

- This checkout may not include git history; default to Conventional Commits (`docs:`, `feat:`, `fix:`, `chore:`).
- PRs: describe intent + affected files, keep changes scoped, and update `SKILL.md` and `assets/` together when examples change.

## Security & Configuration Tips

- Never commit API keys; use environment variables (e.g., `ANTHROPIC_API_KEY`) in examples.
- Prefer stable, pinned external references when practical; if using `@main`, call out why in the PR description.
