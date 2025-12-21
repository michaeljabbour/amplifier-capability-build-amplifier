# Amplifier CLI

A lightweight, foundation-based CLI for composable AI applications.

**85% smaller than amplifier-app-cli** (~1,500 LOC vs ~10,000 LOC) by using amplifier-foundation directly.

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/amplifier-cli-skill
cd amplifier-cli-skill

# Install with uv (recommended)
uv pip install -e .

# Or with pip
pip install -e .
```

### Setup

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run a prompt
amplifier run "Hello, world!"

# Start interactive REPL
amplifier repl
```

## Features

### 🚀 Core Capabilities
- **Direct foundation workflow**: load_bundle → compose → prepare → create_session → execute
- **Bundle composition**: Configs ARE bundles, no custom merging
- **Agent delegation**: Spawn specialized agents with `prepared.spawn()`
- **Project isolation**: Automatic project detection and scoped sessions
- **Rich terminal UI**: Markdown rendering, progress indicators, color output

### 📦 Bundle Management
- Load bundles from local files or git URLs
- Compose multiple bundles for configuration
- Inspect bundle contents
- Update git-sourced bundles

### 🤖 Agent System
- Pre-built agents (bug-hunter, code-reviewer)
- Create custom agents
- Agent session resumption
- Multi-agent orchestration

### 💾 Memory System
- Persistent memory across sessions
- Automatic memory capture via hooks
- Search and recall past learnings
- Project-scoped memories

## Usage

### Basic Execution

```bash
# Execute a single prompt
amplifier run "What is 2+2?"

# With specific provider
amplifier run --provider ./providers/openai.yaml "prompt"

# Compose multiple bundles
amplifier run --bundle base.md --bundle dev.md "prompt"
```

### Interactive REPL

```bash
# Start REPL
amplifier repl

# REPL features:
# - Multi-line input (Ctrl-J)
# - Command history (↑↓)
# - History search (Ctrl-R)
# - Context preserved
# - Exit: 'exit', 'quit', or Ctrl-D
```

### Agent Delegation

```bash
# Run an agent
amplifier agent run bug-hunter "Find bugs in auth.py"

# Resume agent session
amplifier agent run bug-hunter "Continue analysis" --resume abc123...

# List available agents
amplifier agent list
```

### Session Management

```bash
# List recent sessions
amplifier session list

# Show session details
amplifier session show abc123...

# Delete old session
amplifier session delete abc123...
```

### Bundle Management

```bash
# List available bundles
amplifier bundle list

# Inspect bundle
amplifier bundle inspect ./bundles/base.md

# Update git bundles
amplifier bundle update --all
```

## Configuration

### Environment Variables

```bash
# Provider (default: ./providers/anthropic.yaml)
export AMPLIFIER_PROVIDER="./providers/openai.yaml"

# API keys
export ANTHROPIC_API_KEY="sk-..."
export OPENAI_API_KEY="sk-..."

# Logging
export LOG_LEVEL="INFO"
```

### Config Files

Config files ARE bundles! Create `.amplifier/config.yaml`:

```yaml
---
bundle:
  name: my-config
  version: 1.0.0

providers:
  - module: provider-anthropic
    config:
      default_model: claude-opus-4-5

tools:
  - module: tool-filesystem
  - module: tool-bash

hooks:
  - module: hooks-logging
    config:
      log_level: DEBUG
---

Custom instruction for this project...
```

### Project Structure

```
your-project/
├── .amplifier/
│   ├── config.yaml      # Project config (optional)
│   └── context/         # Context files for @project:
├── .git/                # Git root (auto-detected)
└── src/                 # Your code
```

## Architecture

### Foundation Pattern

```python
# Canonical workflow
async def main():
    # 1. Load bundles
    foundation = await load_bundle("git+https://github.com/microsoft/amplifier-foundation@main")
    provider = await load_bundle("./providers/anthropic.yaml")

    # 2. Compose (later wins)
    composed = foundation.compose(provider)

    # 3. Prepare (downloads modules)
    prepared = await composed.prepare()

    # 4. Create session
    session = await prepared.create_session()

    # 5. Execute
    response = await session.execute("Hello!")

    # 6. Cleanup
    await session.cleanup()
```

### What Foundation Provides
- Session management (context, history)
- Bundle loading (local files, git URLs)
- Module downloading and caching
- @namespace:path resolution
- W3C trace context propagation
- Streaming orchestration
- Hook system
- Tool system

### What App Layer Provides
- CLI commands (Typer framework)
- Config search paths (project detection)
- Session metadata storage (list past sessions)
- @mention shortcuts (@user:, @project:)
- Bundle composition order
- Error message formatting

## Bundles

### Providers

Available in `providers/`:
- `anthropic.yaml` - Claude (Opus, Sonnet, Haiku)
- `openai.yaml` - GPT models
- `azure-openai.yaml` - Azure OpenAI
- `ollama.yaml` - Local models (Llama, Mistral)

### Base Bundles

- `bundles/base.md` - Core tools and hooks
- `bundles/dev.md` - Development overlay with enhanced tools

### Agents

- `agents/bug-hunter.md` - Find and fix bugs
- `agents/code-reviewer.md` - Code quality reviews

## Advanced Features

### @Mention Shortcuts

```markdown
# In bundle instructions:
See @user:guidelines.md for project guidelines.
Reference @project:docs/arch.md for architecture.
Check @foundation:examples/pattern.py for patterns.
```

### Multi-Agent Orchestration

```python
# Parallel agents
results = await asyncio.gather(
    app.spawn_agent("bug-hunter", "Check auth.py"),
    app.spawn_agent("code-reviewer", "Review api.py"),
)
```

### Memory System

```bash
# Enable in bundles/base.md:
tools:
  - module: tool-memory
    config:
      storage_path: ~/.amplifier/memories.db

hooks:
  - module: hooks-memory-capture
    config:
      auto_summarize_interval: 10
```

## Development

### Project Structure

```
amplifier-cli/
├── amplifier_cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── app.py               # AmplifierApp class
│   ├── config.py            # Config dataclass
│   ├── session_manager.py   # Session metadata
│   ├── project.py           # Project detection
│   └── commands/            # CLI commands
├── providers/               # Provider bundles
├── bundles/                 # Base bundles
├── agents/                  # Agent bundles
└── pyproject.toml          # Dependencies
```

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest

# Type checking
mypy amplifier_cli

# Linting
ruff check amplifier_cli
```

## Comparison with app-cli

| Component | app-cli | amplifier-cli | Reduction |
|-----------|---------|---------------|-----------|
| Session management | 834 lines | 50 lines | 94% |
| Bundle loading | 700+ lines | 0 (foundation) | 100% |
| Mention loading | 466 lines | 30 lines | 93% |
| Config system | 704 lines | 100 lines | 86% |
| Commands | 6,120 lines | 800 lines | 87% |
| **Total** | **~10,000** | **~1,500** | **85%** |

### Why This is Better

1. **Massive code reduction** - 85% fewer lines to maintain
2. **Simpler architecture** - 2 layers vs 3 (no policy layer)
3. **Better composability** - Bundle composition vs custom config merging
4. **Cleaner delegation** - Direct `spawn()` vs custom spawner wrapper
5. **Native features** - Foundation built-ins (mentions, caching, traces, memory)
6. **Easier testing** - Only test thin app layer, foundation already tested
7. **Future-proof** - Direct dependency on foundation, breaking changes are immediate

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and type checking
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Links

- [Foundation Documentation](https://github.com/microsoft/amplifier)
- [Module Catalog](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md)
- [Issue Tracker](https://github.com/yourusername/amplifier-cli-skill/issues)
