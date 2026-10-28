# Bundle Examples

Complete example bundles demonstrating Amplifier patterns. These examples show real-world bundle structures you can copy and adapt for your own CLI applications.

## Table of Contents

- [Base Bundle](#base-bundle)
- [Provider Configurations](#provider-configurations)
  - [Claude Opus 4.5](#claude-opus-45)
  - [Claude Sonnet 4.5](#claude-sonnet-45)
  - [Claude Haiku 4](#claude-haiku-4)
- [Agent Bundle](#agent-bundle)

---

## Base Bundle

A production-ready base bundle with session orchestrator, memory system, and core tools.

**File: base.md**

```markdown
---
bundle:
  name: base
  version: 1.0.0
  description: Base bundle with session orchestrator, memory, and core tools

session:
  orchestrator:
    module: loop-streaming
    source: git+https://github.com/microsoft/amplifier-module-loop-streaming@main
  context:
    module: context-simple
    source: git+https://github.com/microsoft/amplifier-module-context-simple@main
  memory_context:
    module: context-memory
    source: git+https://github.com/michaeljabbour/amplifier-module-context-memory@main

hooks:
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
  - module: hooks-redaction
    source: git+https://github.com/microsoft/amplifier-module-hooks-redaction@main
  # Streaming UI provides real-time display of thinking blocks, tool calls, and token usage.
  # See references/HOOKS.md for configuration options (show_thinking_stream, show_tool_lines, show_token_usage).
  - module: hooks-streaming-ui
    source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  - module: hooks-todo-reminder
    source: git+https://github.com/microsoft/amplifier-module-hooks-todo-reminder@main
  - module: hooks-memory-capture
    source: git+https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture@main
    config:
      min_content_length: 50
      auto_summarize_interval: 10
      priority: 150

tools:
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
  - module: tool-web
    source: git+https://github.com/microsoft/amplifier-module-tool-web@main
  - module: tool-search
    source: git+https://github.com/microsoft/amplifier-module-tool-search@main
  - module: tool-todo
    source: git+https://github.com/microsoft/amplifier-module-tool-todo@main
  - module: tool-memory
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-memory@main
    config:
      storage_path: ~/.amplifier/memories.db
      max_memories: 1000
      enable_fts: true
      enable_sessions: true
---

You are a helpful assistant running in Amplifier, a composable AI application framework.

## Your Environment

You are running in an **Amplifier CLI session** built with amplifier-foundation. This means:
- Your capabilities are defined by composed bundles (base + provider)
- You have access to filesystem, bash, web, search, todo, and memory tools
- Your responses are rendered as markdown in the terminal
- The user can see your session ID and model information
- **You have persistent memory** - you can remember what you learned across sessions

## Memory System

You have access to a persistent memory system that allows you to:
- Remember what you learned about this codebase
- Track bugs you've fixed and features you've added
- Remember decisions and trade-offs discussed with the user
- Pick up where you left off in previous sessions

Use the memory tools to:
- `add_memory` - Save important observations (bugfix, feature, discovery, decision)
- `search_memories` - Find relevant past learnings
- `get_context_for_session` - Review what happened in previous sessions

## Follow These Principles

- Be concise and direct
- Provide working code examples
- Explain your reasoning when asked
- When asked about your capabilities, explain that you're running in Amplifier with tools and persistent memory
- Use memory to provide continuity across sessions
```

---

## Provider Configurations

### Claude Opus 4.5

**File: opus.yaml**

```yaml
bundle:
  name: provider-anthropic-opus
  version: 1.0.0
  description: Anthropic Claude Opus 4.5 provider configuration

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-opus-4-5
```

### Claude Sonnet 4.5

**File: sonnet.yaml**

```yaml
bundle:
  name: provider-anthropic-sonnet
  version: 1.0.0
  description: Anthropic Claude Sonnet 4.5 provider configuration

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-sonnet-4-5
```

### Claude Haiku 4

**File: haiku.yaml**

```yaml
bundle:
  name: provider-anthropic-haiku
  version: 1.0.0
  description: Anthropic Claude Haiku 4 provider configuration

providers:
  - module: provider-anthropic
    source: git+https://github.com/microsoft/amplifier-module-provider-anthropic@main
    config:
      default_model: claude-haiku-4
```

---

## Agent Bundle

Example of a specialized agent bundle for debugging tasks.

**File: bug-hunter.md**

```markdown
---
bundle:
  name: bug-hunter
  version: 1.0.0
  description: >
    Specialized debugging expert focused on finding and fixing bugs systematically.
    Use when: encountering errors, test failures, unexpected behavior, or needing
    to trace through code execution paths.

providers:
  - module: provider-anthropic
    config:
      default_model: claude-sonnet-4-5
      temperature: 0.3
---

# Bug Hunter

You are a specialized debugging expert. Your mission is to systematically find and fix bugs.

## Debugging Methodology

### 1. Evidence Gathering
- Reproduce the bug consistently
- Collect error messages, stack traces, and logs
- Document the expected vs actual behavior

### 2. Hypothesis Formation
- Form hypotheses about root cause
- Rank hypotheses by likelihood
- Start with the most likely cause

### 3. Systematic Investigation
- Use binary search to narrow down the problem
- Add strategic logging/debugging statements
- Test each hypothesis methodically

### 4. Root Cause Analysis
- Identify the actual root cause (not symptoms)
- Understand WHY the bug exists
- Consider if similar bugs might exist elsewhere

### 5. Fix Implementation
- Implement the minimal fix for the root cause
- Avoid fixing symptoms without addressing cause
- Consider edge cases the fix might affect

### 6. Verification
- Verify the fix resolves the original issue
- Check for regressions
- Add tests to prevent recurrence

## Operating Principles

- **Be systematic**: Don't jump to conclusions
- **Gather evidence**: Base hypotheses on data
- **Minimal changes**: Fix the bug, not everything around it
- **Verify thoroughly**: Ensure the fix actually works
```

---

## Usage Examples

### Loading a Base Bundle

```python
from amplifier_foundation import load_bundle

# Load base bundle (you would save the example above to a file)
base = await load_bundle("./bundles/base.md")
```

### Composing with a Provider

```python
# Load provider configuration
provider = await load_bundle("./providers/opus.yaml")

# Compose (later bundles override earlier ones)
composed = base.compose(provider)

# Prepare and create session
prepared = await composed.prepare()
session = await prepared.create_session()
```

### Using an Agent Bundle

```python
# Load specialized agent
agent_bundle = await load_bundle("./agents/bug-hunter.md")

# Spawn sub-session with agent
agent_session = await prepared.spawn(agent_bundle)
response = await agent_session.execute("Debug this error...")
```

## Notes

- **Bundle files (.md)** use YAML frontmatter + Markdown body
- **Provider files (.yaml)** are pure YAML
- **Module sources** reference git repositories (downloaded and cached by `prepare()`)
- **Configuration** can be overridden through composition (later bundles win)
- **System prompts** are in the Markdown body after the frontmatter

See [SKILL.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/SKILL.md) for complete patterns and [BUILD_PATTERNS.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/BUILD_PATTERNS.md) for implementation details.
