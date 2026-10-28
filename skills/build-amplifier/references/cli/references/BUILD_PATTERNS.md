# Build Patterns: Creating Amplifier CLI Applications

> **Note:** This document provides detailed build patterns and implementation details. For a high-level overview, see the "Building a Complete CLI Application" section in [SKILL.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/SKILL.md).

**Visual Documentation:** See [amplifier-simplecli's ARCHITECTURE_FLOWS.md](https://github.com/michaeljabbour/amplifier-simplecli/blob/main/docs/ARCHITECTURE_FLOWS.md) for comprehensive flow diagrams showing:
- Foundation (setup) → Core (runtime) separation
- Application startup sequence
- Execution loop with tool calls
- Module loading and activation
- Complete end-to-end data flow

This guide documents the complete pattern for building CLI applications with Amplifier, as demonstrated in `simple_cli.py`.

## One-Touch Build Checklist

Use this checklist to create a new Amplifier CLI from scratch:

### 1. Project Structure

```
your-cli/
├── simple_cli.py           # Main CLI application
├── requirements.txt         # Python dependencies
├── README.md               # User documentation
├── .gitignore              # Git ignores
├── bundles/
│   ├── base.md         # Base bundle configuration
│   ├── dev.md          # Development overlay (optional)
│   └── prod.md         # Production overlay (optional)
├── providers/
│   └── anthropic.yaml  # Provider configuration
└── agents/
    └── (custom agents) # Custom agent bundles (optional)
```

### 2. Core Dependencies

```txt
# requirements.txt
amplifier-foundation>=0.1.0
rich>=13.0.0
```

### 3. Base Bundle Template

```yaml
# bundles/base.md
---
bundle:
  name: base
  version: 1.0.0
  description: Base bundle with session orchestrator and core tools

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
---

You are a helpful assistant running in Amplifier, a composable AI application framework.

## Your Environment

You are running in an **Amplifier CLI session** built with amplifier-foundation. This means:
- Your capabilities are defined by composed bundles (base + provider)
- You have access to filesystem and bash tools
- Your responses are rendered as markdown in the terminal
- The user can see your session ID and model information

## Follow These Principles

- Be concise and direct
- Provide working code examples
- Explain your reasoning when asked
- When asked about your capabilities, explain that you're running in Amplifier with specific tools (filesystem, bash)
```

### 4. Provider Configuration Template

```yaml
# providers/anthropic.yaml
bundle:
  name: provider-anthropic
  version: 1.0.0
  description: Anthropic Claude provider configuration

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-opus-4-5
```

### 5. CLI Application Pattern

The CLI follows this structure:

```python
import argparse
import asyncio
from pathlib import Path
from amplifier_foundation import load_bundle
from rich.console import Console

# 1. Settings Management
SETTINGS_FILE = Path.home() / ".your-cli" / "settings.yaml"

def load_settings():
    """Load user preferences."""
    # Load from settings file or return defaults

def save_settings(settings):
    """Save user preferences."""
    # Write to settings file

# 2. Interactive Setup (--init)
def run_init():
    """Friendly setup wizard."""
    # Check API key
    # Let user choose model
    # Save preferences

# 3. Main CLI (default)
async def run_cli():
    """Run the REPL."""
    # Load settings
    # Load bundles
    # Compose
    # Prepare
    # Create session
    # Run REPL loop

# 4. Module Updates (--update)
async def run_update():
    """Check and update modules."""
    # Show modules in use
    # Check cache
    # Offer to clear and re-download
    # Trigger prepare() to download modules

# 5. Entry Point
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true")
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    if args.init:
        run_init()
    elif args.update:
        asyncio.run(run_update())
    else:
        asyncio.run(run_cli())
```

### 6. Key Implementation Details

#### Bundle Composition Workflow
```python
# Always follow this pattern:
base = await load_bundle("./bundles/base.md")
provider = await load_bundle("./providers/anthropic.yaml")
composed = base.compose(provider)
prepared = await composed.prepare()
session = await prepared.create_session()
```

See [EXAMPLES.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/EXAMPLES.md) for complete example bundles.

#### Dynamic Provider Configuration
```python
# Create provider bundle from settings at runtime:
provider_config = {
    "bundle": {"name": "provider", "version": "1.0.0"},
    "providers": [{
        "module": "provider-anthropic",
        "source": "git+https://github.com/microsoft/amplifier-module-provider-anthropic@main",
        "config": {"default_model": settings["model"]}
    }]
}

# Save temporarily and load
temp_provider = Path("temp_provider.yaml")
with open(temp_provider, "w") as f:
    yaml.dump(provider_config, f)

provider = await load_bundle(str(temp_provider))
# ... compose and use
temp_provider.unlink()  # Clean up
```

#### Module Cache Management
```python
# Amplifier caches modules in ~/.amplifier/
amplifier_home = Path.home() / ".amplifier"
modules_dir = amplifier_home / "modules"
cache_dir = amplifier_home / "cache"
module_cache_dir = amplifier_home / "module-cache"

# To force updates, clear cache and re-prepare:
shutil.rmtree(cache_dir)
shutil.rmtree(module_cache_dir)
await composed.prepare()  # Re-downloads all modules
```

#### Rich UI Components
```python
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

# Welcome panel
console.print(Panel(
    "[bold cyan]Welcome![/bold cyan]\n\n"
    "Getting started...",
    border_style="cyan"
))

# Markdown output
console.print(Markdown(response))

# Interactive prompts
choice = Prompt.ask("Choose model", choices=["1", "2", "3"])
proceed = Confirm.ask("Continue?", default=True)
```

## CLI Commands Pattern

### --init (Interactive Setup)
- Check for API key
- Present model choices
- Save preferences
- Friendly messaging with emojis

### --update (Module Management)
- Display modules in use
- Show cache size
- Offer to clear and re-download
- Confirm before destructive operations

### (default) (Run CLI)
- Load settings
- Check API key
- Load and compose bundles
- Display session info (model, session ID)
- Run REPL with markdown rendering
- Handle exit gracefully

## Testing Your CLI

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run setup
python your_cli.py --init

# 3. Set API key (if not set)
export ANTHROPIC_API_KEY=your-key

# 4. Run CLI
python your_cli.py

# 5. Update modules
python your_cli.py --update
```

## Distribution

### As a Python Package
```bash
# Create setup.py
# Build: python setup.py sdist bdist_wheel
# Install: pip install your-cli
```

### As a Standalone Script
```bash
# Make executable
chmod +x your_cli.py
# Add shebang: #!/usr/bin/env python3
# Run: ./your_cli.py
```

### As a Git Repository
```bash
# Users can clone and run:
git clone https://github.com/your-org/your-cli
cd your-cli
pip install -r requirements.txt
python your_cli.py --init
```

## Complete Example

See `simple_cli.py` in this repository for a complete, working implementation that includes:
- ✅ Interactive setup
- ✅ Settings persistence
- ✅ Model selection
- ✅ Module updates
- ✅ Markdown rendering
- ✅ Session info display
- ✅ Friendly UX

## Common Customizations

### Add Custom Tools
```yaml
# In bundles/base.md, add to tools section:
tools:
  - module: tool-web
    source: git+https://github.com/microsoft/amplifier-module-tool-web@main
```

### Add Custom Agents
```markdown
# Create agents/my-agent.md
---
bundle:
  name: my-agent
  version: 1.0.0

providers:
  - module: provider-anthropic
    config:
      default_model: claude-sonnet-4-5
      temperature: 0.7
---

You are a specialized agent for [specific task].
```

### Support Multiple Providers
```python
AVAILABLE_PROVIDERS = {
    "anthropic": "provider-anthropic",
    "openai": "provider-openai",
    "azure": "provider-azure-openai",
}

# Let user choose in --init
```

## Best Practices

1. **Settings Location**: Use `~/.your-cli/settings.yaml` for user settings
2. **Temp Files**: Always clean up temporary provider files
3. **Error Handling**: Show friendly error messages with instructions
4. **Git Ignore**: Add `temp_provider.yaml` to `.gitignore`
5. **API Keys**: Never hardcode, always use environment variables
6. **Rich UI**: Use panels, markdown, and colors for better UX
7. **Confirmation**: Ask before destructive operations (clear cache)
8. **Defaults**: Provide sensible defaults (Opus 4.5)
9. **Help Text**: Include `--help` with clear descriptions
10. **Documentation**: Include README with quick start guide
