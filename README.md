# Amplifier CLI Skill

An Agent Skill that teaches Claude Code how to build CLI applications using [Amplifier](https://github.com/microsoft/amplifier) patterns.

## What This Is

This is **not executable code** - it's a **skill definition** that provides:
- Amplifier architecture patterns and best practices
- Working example bundles in `assets/`
- Memory system integration guide
- Build documentation for one-touch CLI creation

## About Amplifier

[Amplifier](https://github.com/microsoft/amplifier) is Microsoft's composable AI agent framework that enables:
- **Bundle composition** - Mix session, hooks, tools, and providers
- **Module ecosystem** - 36+ modules available ([Module Catalog](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md))
- **Provider flexibility** - Claude, GPT, Gemini, local models
- **Production-ready** - Logging, observability, and hooks built-in

This skill teaches the **amplifier-foundation** patterns (source of truth), not amplifier-app-cli implementation details.

## Contents

```
amplifier-cli-skill/
├── SKILL.md              # Primary skill definition
├── CLAUDE.md             # Repository guidelines
├── assets/
│   ├── bundles/
│   │   └── base.md      # Example bundle with 14 modules
│   └── providers/
│       ├── opus.yaml    # Claude Opus 4.5
│       ├── sonnet.yaml  # Claude Sonnet 4.5
│       └── haiku.yaml   # Claude Haiku 4
├── BUILD_GUIDE.md        # One-touch build patterns
├── MEMORY_GUIDE.md       # Memory system documentation
├── MEMORY_MODULE_STATUS.md  # Module compatibility status
└── CHANGELOG.md          # Recent updates and patterns
```

## Key Concepts

### Bundle Composition

```python
# Source of truth pattern
base = await load_bundle("base.md")
provider = await load_bundle("opus.yaml")
bundle = base.compose(provider)
prepared = await bundle.prepare()
session = await prepared.create_session()
```

### Module Structure

**base.md** (YAML frontmatter + Markdown):
```yaml
---
bundle:
  name: base
  version: 1.0.0

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main

hooks:
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
---

System prompt and instructions...
```

### Memory System

Complete memory integration with 3 modules:
- `context-memory` - Progressive disclosure context injection
- `tool-memory` - 6 memory tools (add, search, list, etc.)
- `hooks-memory-capture` - Automatic observation capture

See [MEMORY_GUIDE.md](MEMORY_GUIDE.md) for details.

## Example Implementation

See [amplifier-simplecli](https://github.com/michaeljabbour/amplifier-simplecli) for a working reference implementation with:
- 14 pre-configured modules
- Interactive setup (`--init`)
- Update management (`--update`)
- Rich terminal UI
- Full memory system

## Foundation Alignment Checklist

When building with Amplifier:
- ✅ Use `load_bundle → compose → prepare → create_session` workflow
- ✅ Use `base.compose(overlay)` for composition
- ✅ Modules loaded via git sources: `git+https://github.com/...@main`
- ✅ Configuration via YAML frontmatter
- ✅ System prompts in Markdown body
- ❌ Don't copy amplifier-app-cli internals (reference only)

## Validation

```bash
# Verify bundles load correctly
uv venv && uv pip install amplifier-foundation
uv run python -c "
import asyncio
from amplifier_foundation import load_bundle
asyncio.run(load_bundle('./assets/bundles/base.md'))
"
```

## Module Catalog

For available modules, see [Amplifier Module Catalog](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md).

**Categories:**
- **Orchestrators** (3) - loop-basic, loop-streaming, loop-events
- **Providers** (7) - anthropic, openai, azure-openai, gemini, vllm, ollama, mock
- **Tools** (7) - filesystem, bash, web, search, task, todo, skills
- **Context** (2) - simple, persistent
- **Hooks** (9) - logging, redaction, approval, backup, streaming-ui, status-context, todo-reminder, scheduler-cost-aware, scheduler-heuristic

## Resources

- [Amplifier](https://github.com/microsoft/amplifier) - Main framework repository
- [amplifier-core](https://github.com/microsoft/amplifier-core) - Foundation library
- [Module Catalog](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) - All available modules
- [amplifier-simplecli](https://github.com/michaeljabbour/amplifier-simplecli) - Reference implementation

## Contributing

This skill documents amplifier-foundation patterns. Keep it aligned with:
- amplifier-foundation as source of truth
- Working example bundles in `assets/`
- Documentation synchronized with code

## License

MIT
