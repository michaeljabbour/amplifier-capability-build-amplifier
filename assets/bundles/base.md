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
