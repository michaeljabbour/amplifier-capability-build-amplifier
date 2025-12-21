---
bundle:
  name: dev
  version: 1.0.0
  description: Development overlay with enhanced tools and debugging

# This is an overlay bundle - compose it with base.md for development
# Example: amplifier run --bundle base.md --bundle dev.md "prompt"

tools:
  # Additional dev tools
  - module: tool-task
    source: git+https://github.com/microsoft/amplifier-module-tool-task@main

  # Enhanced filesystem with more permissions
  - module: tool-filesystem
    source: git+https://github.com/microsoft/amplifier-module-tool-filesystem@main
    config:
      allowed_paths:
        - "."
        - "~/.amplifier"

  # Bash with common dev commands
  - module: tool-bash
    source: git+https://github.com/microsoft/amplifier-module-tool-bash@main
    config:
      allowed_commands:
        - "ls"
        - "cat"
        - "grep"
        - "find"
        - "git"
        - "npm"
        - "python"
        - "pytest"
        - "mypy"

hooks:
  # Verbose logging for debugging
  - module: hooks-logging
    source: git+https://github.com/microsoft/amplifier-module-hooks-logging@main
    config:
      log_level: DEBUG
      log_path: ~/.amplifier/logs/dev.log
---

You are a development assistant with enhanced capabilities for coding tasks.

## Development Environment

You're running in **development mode** with:
- Full filesystem access (within project)
- Git commands enabled
- Task delegation capabilities
- Debug logging enabled
- All common dev tools available

## Focus Areas

- Writing and reviewing code
- Running tests and debugging
- Git operations
- Project refactoring
- Documentation

## Commands You Can Use

- `git status`, `git diff`, `git log`
- `pytest` for Python tests
- `npm test` for Node.js tests
- `mypy` for Python type checking
- `grep`, `find` for code search

Be proactive in using these tools to help the developer!
