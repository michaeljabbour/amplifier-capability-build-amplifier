---
name: amplifier-cli-skill
description: Skill for building CLI applications on the Amplifier platform. Teaches amplifier-foundation patterns as the source of truth for composable AI application development. Use when building CLI tools, understanding bundle composition, implementing sessions, or extending the Amplifier ecosystem.
compatibility: Requires Python 3.10+, uv package manager. Works with amplifier-foundation, amplifier-core, and related ecosystem packages.
license: MIT
metadata:
  author: Microsoft
  version: "2.0"
  repository: https://github.com/microsoft/amplifier-foundation
---

# Building CLI Applications on Amplifier

This skill teaches how to build CLI applications using **amplifier-foundation** patterns - the source of truth for Amplifier application development.

## Core Workflow

Every Amplifier application follows this fundamental pattern:

```python
from amplifier_foundation import load_bundle

async def main():
    # 1. Load bundles
    foundation = await load_bundle("git+https://github.com/microsoft/amplifier-foundation@main")
    provider = await load_bundle("./providers/anthropic.yaml")

    # 2. Compose bundles (later overrides earlier)
    composed = foundation.compose(provider)

    # 3. Prepare (resolves and downloads modules)
    prepared = await composed.prepare()

    # 4. Create session and execute
    async with await prepared.create_session() as session:
        response = await session.execute("Hello!")
        print(response)
```

**This is the pattern.** Everything else builds on this foundation.

## Quick Start

```bash
# Install amplifier-foundation
pip install amplifier-foundation

# Or with uv
uv add amplifier-foundation
```

## Example Files

This skill includes working examples in the `assets/` directory:

```
assets/
├── providers/
│   └── anthropic.yaml      # Provider bundle example
├── bundles/
│   ├── base.md             # Base bundle with session and tools
│   ├── dev.md              # Development overlay (includes base)
│   └── prod.md             # Production overlay (includes base)
└── agents/
    └── bug-hunter.md       # Agent bundle example
```

Code examples in this document reference these files. Examine them to see real bundle structures.

## What is a Bundle?

A **Bundle** is a composable configuration unit that produces a **mount plan** for sessions.

```
Bundle → compose() → prepare() → create_session() → execute()
```

### Bundle Sections

| Section | Purpose |
|---------|---------|
| `bundle` | Metadata (name, version) |
| `session` | Orchestrator and context manager |
| `providers` | LLM backends |
| `tools` | Agent capabilities |
| `hooks` | Observability and control |
| `agents` | Named agent configurations |
| `context` | Context files to include |
| `instruction` | System instruction (markdown body) |

### Bundle Format

Bundles are markdown files with YAML frontmatter:

```markdown
---
bundle:
  name: my-app
  version: 1.0.0

session:
  orchestrator: {module: loop-streaming}
  context: {module: context-simple}

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-sonnet-4-5

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
---

You are a helpful assistant for software development.
```

## Composition Pattern

Bundles compose with later overriding earlier:

```python
result = base.compose(overlay)  # overlay wins on conflicts
```

### Merge Rules

| Section | Rule |
|---------|------|
| `session` | Deep merge (nested dicts merged) |
| `providers` | Merge by module ID |
| `tools` | Merge by module ID |
| `hooks` | Merge by module ID |
| `instruction` | Replace (later wins) |

### Common Composition Patterns

**Base + Environment:**
```python
base = await load_bundle("./bundles/base.md")
dev_overlay = await load_bundle("./bundles/dev.md")
prod_overlay = await load_bundle("./bundles/prod.md")

env = os.getenv("ENV", "dev")
overlay = dev_overlay if env == "dev" else prod_overlay
bundle = base.compose(overlay)
```

**Feature Bundles:**
```python
filesystem = Bundle(name="fs", tools=[{"module": "tool-filesystem", "source": "..."}])
web = Bundle(name="web", tools=[{"module": "tool-web", "source": "..."}])

# Compose what you need
full = base.compose(filesystem).compose(web)
```

**Includes Chain (Declarative):**
```yaml
# dev.md
bundle:
  name: dev
includes:
  - ./base.md
providers:
  - module: provider-anthropic
    config: {debug: true}
```

## CLI Application Architecture

Use this blueprint for building CLI applications:

```python
import asyncio
import logging
from dataclasses import dataclass
from pathlib import Path

from amplifier_foundation import Bundle, load_bundle


@dataclass
class AppConfig:
    """Application configuration."""
    provider_bundle: str = "anthropic-sonnet.yaml"
    api_key: str | None = None
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "AppConfig":
        return cls(
            provider_bundle=os.getenv("PROVIDER", "anthropic-sonnet.yaml"),
            api_key=os.getenv("ANTHROPIC_API_KEY"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )

    def validate(self) -> None:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")


class AmplifierApp:
    """Amplifier CLI application pattern."""

    def __init__(self, config: AppConfig):
        self.config = config
        self.session = None
        self.logger = logging.getLogger("amplifier_app")

    async def initialize(self) -> None:
        """Initialize: load bundles, compose, prepare, create session."""
        # Load foundation
        foundation = await load_bundle("git+https://github.com/microsoft/amplifier-foundation@main")

        # Load provider
        provider = await load_bundle(f"./providers/{self.config.provider_bundle}")

        # Add tools
        tools = Bundle(
            name="app-tools",
            tools=[
                {"module": "tool-filesystem", "source": "git+..."},
                {"module": "tool-bash", "source": "git+..."},
            ],
        )

        # Compose all bundles
        composed = foundation.compose(provider).compose(tools)

        # Prepare (downloads modules)
        prepared = await composed.prepare()

        # Create session
        self.session = await prepared.create_session()

    async def execute(self, prompt: str) -> str:
        """Execute a prompt."""
        if not self.session:
            raise RuntimeError("Session not initialized")
        return await self.session.execute(prompt)

    async def shutdown(self) -> None:
        """Graceful shutdown."""
        if self.session:
            await self.session.cleanup()

    async def __aenter__(self):
        await self.initialize()
        return self

    async def __aexit__(self, *args):
        await self.shutdown()


async def main():
    config = AppConfig.from_env()
    config.validate()

    async with AmplifierApp(config) as app:
        response = await app.execute("Hello!")
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
```

### Key Architectural Principles

1. **Configuration as Dataclass**: Use `@dataclass` for config, load from env/files
2. **Initialize/Execute/Shutdown Lifecycle**: Clean lifecycle management
3. **Context Manager Pattern**: Use `async with` for automatic cleanup
4. **Composition Over Inheritance**: Compose bundles, don't subclass

## Session Patterns

### Basic Session

```python
bundle = await load_bundle("/path/to/bundle.md")
prepared = await bundle.prepare()

async with await prepared.create_session() as session:
    response = await session.execute("Hello!")
```

### Multi-Turn Conversation

Session maintains context automatically:

```python
async with await prepared.create_session() as session:
    await session.execute("My name is Alice")
    response = await session.execute("What's my name?")
    # Response knows about Alice
```

### Resuming Sessions

```python
# First session
async with await prepared.create_session() as session:
    await session.execute("Remember: X=42")
    session_id = session.session_id

# Later: resume
async with await prepared.create_session(session_id=session_id) as session:
    response = await session.execute("What is X?")
    # Knows X=42
```

## Agent Delegation

### Defining Agents

In `agents/bug-hunter.md`:

```markdown
---
agent:
  name: bug-hunter
  description: Finds and fixes bugs

providers:
  - module: provider-anthropic
    config:
      default_model: claude-sonnet-4-5
      temperature: 0.3
---

You are an expert bug hunter. Find bugs systematically.
```

### Spawning Agents

```python
# Load agent as bundle
agent_bundle = await load_bundle("./agents/bug-hunter.md")

# Spawn sub-session
result = await prepared.spawn(
    child_bundle=agent_bundle,
    instruction="Find the bug in auth.py",
    compose=True,            # Compose with parent bundle
    parent_session=session,  # Inherit UX from parent
)

print(result["output"])
```

## @Mention System

Reference context files using `@namespace:path` syntax:

```markdown
See @foundation:context/guidelines.md for guidelines.
```

How it works:
1. During composition, each bundle's `base_path` is tracked by namespace
2. PreparedBundle resolves `@namespace:path` references
3. Content is loaded and included inline

## Philosophy

### Mechanism, Not Policy

**Foundation provides mechanism** for bundle composition. It doesn't decide which bundles to use - those are **policy decisions** for your application.

```
Foundation (mechanism):          App (policy):
- load_bundle()                  - Search path order
- compose()                      - Well-known bundles
- prepare()                      - @user:, @project: shortcuts
- create_session()               - Environment-specific config
```

### Text-First

- Bundles are markdown (human-readable)
- Configuration is YAML (diffable)
- No binary formats

### Composable

Small bundles compose into larger configurations. Prefer composition over complexity.

## Reference: amplifier-app-cli

The `amplifier-app-cli` repository is a reference implementation. Learn from it, but understand it implements **app-layer policy** on top of foundation mechanisms:

| App Policy (amplifier-app-cli) | Foundation Mechanism |
|--------------------------------|---------------------|
| SessionStore (persistence) | Session lifecycle |
| session_spawner (delegation) | spawn() API |
| paths.py (search paths) | load_bundle() |
| CLI commands | Direct API usage |

When building your own CLI, start from the foundation patterns above, not from copying amplifier-app-cli internals.

## Common Development Tasks

### Adding a New Provider

1. Create `providers/my-provider.yaml`:
   ```yaml
   bundle:
     name: my-provider
   providers:
     - module: provider-openai
       source: git+https://github.com/microsoft/amplifier-module-provider-openai@main
       config:
         default_model: gpt-4o
   ```

2. Load and compose:
   ```python
   provider = await load_bundle("./providers/my-provider.yaml")
   composed = foundation.compose(provider)
   ```

### Adding Tools

Compose a tools bundle:

```python
tools = Bundle(
    name="my-tools",
    tools=[
        {"module": "tool-filesystem", "source": "git+..."},
        {"module": "tool-bash", "source": "git+...", "config": {"allowed_commands": ["ls", "cat"]}},
    ],
)
composed = base.compose(tools)
```

### Testing with Mock Provider

```python
test_bundle = Bundle(
    name="test",
    providers=[{
        "module": "provider-mock",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-mock@main",
        "config": {"responses": ["Hello!", "How can I help?"]},
    }],
)
```

### Validation

```python
from amplifier_foundation import load_bundle, validate_bundle_or_raise

bundle = await load_bundle(path)
validate_bundle_or_raise(bundle)  # Raises if invalid
prepared = await bundle.prepare()
```

## Error Handling

```python
from amplifier_foundation import (
    load_bundle,
    BundleNotFoundError,
    BundleLoadError,
    BundleValidationError,
)

try:
    bundle = await load_bundle(path)
except BundleNotFoundError:
    print(f"Bundle not found: {path}")
except BundleLoadError as e:
    print(f"Failed to load: {e}")
except BundleValidationError as e:
    print(f"Invalid bundle: {e}")
```

## File Reference

See [references/ARCHITECTURE.md](references/ARCHITECTURE.md) for foundation architecture.

See [references/REFACTORING.md](references/REFACTORING.md) for amplifier-app-cli analysis (reference only).

## External Documentation

- **Foundation Concepts**: https://github.com/microsoft/amplifier-foundation/blob/main/docs/CONCEPTS.md
- **Common Patterns**: https://github.com/microsoft/amplifier-foundation/blob/main/docs/PATTERNS.md
- **CLI Blueprint**: https://github.com/microsoft/amplifier-foundation/blob/main/examples/08_cli_application.py
- **Profile Authoring**: https://github.com/microsoft/amplifier-profiles/blob/main/docs/PROFILE_AUTHORING.md
