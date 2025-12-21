# Simple Amplifier CLI 🚀

The simplest working terminal UI CLI for Amplifier, demonstrating the core `load_bundle → compose → prepare → create_session → execute` workflow.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the interactive setup:**
   ```bash
   python simple_cli.py --init
   ```

   This will:
   - Check for your API key
   - Let you choose your preferred model (Opus, Sonnet, or Haiku)
   - Save your settings to `~/.amplifier-cli/settings.yaml`

3. **Set your API key** (if not already set):
   ```bash
   export ANTHROPIC_API_KEY=your_key_here
   ```

4. **Start chatting:**
   ```bash
   python simple_cli.py
   ```

## Features

✨ **Interactive Setup** - Friendly `--init` wizard to configure your preferences
🎨 **Beautiful Output** - Markdown rendering with syntax highlighting
🤖 **Model Selection** - Choose between Opus, Sonnet, or Haiku
📊 **Session Info** - See your model and session ID at startup
💾 **Persistent Settings** - Your preferences are saved automatically
🔄 **Module Updates** - Check and update Amplifier modules with `--update`

## Usage

```bash
# Run the CLI with your saved settings
python simple_cli.py

# Re-run setup to change settings
python simple_cli.py --init

# Check for and install module updates
python simple_cli.py --update

# Get help
python simple_cli.py --help
```

## What It Does

- Loads the base bundle (`assets/bundles/base.md`) with session orchestrator and tools
- Creates a provider configuration based on your settings
- Composes them together following amplifier-foundation patterns
- Starts a simple REPL where you can chat with Claude
- Maintains conversation context across turns
- Renders responses as formatted markdown

## Example Session

```
$ python simple_cli.py
Loading bundles...
Preparing session...

╭──────────────────────────────────────╮
│ Amplifier CLI                        │
│ Model: claude-opus-4-5               │
│ Session ID: abc123...                │
│                                      │
│ Type exit, quit, or q to exit       │
╰──────────────────────────────────────╯

You: Hello! What's under your hood?