# Hooks System Reference

## Overview

Hooks provide observability and control points in the amplifier-foundation execution pipeline. They are **pure observability** modules that do not modify core behavior, only observe and display information about the execution flow.

## Available Hooks Modules

### hooks-streaming-ui

**Purpose:** Terminal UI for streaming agentic behavior

**GitHub:** https://github.com/microsoft/amplifier-module-hooks-streaming-ui

**What it provides:**
- 🧠 **Thinking blocks** - Displays the agent's reasoning process
- 🔧 **Tool invocations** - Shows tool name and arguments
- ✅/❌ **Tool results** - Indicates success/failure with output preview
- 📊 **Token usage** - Displays input/output/total tokens after each turn

**Configuration:**

```yaml
hooks:
- module: hooks-streaming-ui
  source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  config:
    ui:
      show_thinking_stream: true    # Display thinking blocks (default: true)
      show_tool_lines: 20          # Max lines to show for tool I/O (default: 5)
      show_token_usage: true       # Display token usage after each turn (default: true)
```

**Configuration Options:**

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `show_thinking_stream` | boolean | `true` | Display thinking blocks with visual boundaries |
| `show_tool_lines` | integer | `5` | Maximum lines to display for tool input/output |
| `show_token_usage` | boolean | `true` | Show token statistics after each response |

**Key Characteristics:**
- Zero kernel changes - pure hooks implementation
- Pure observability - no behavior changes
- Uses standard `profile.ui` settings
- Displays formatted thinking blocks with visual boundaries
- Shows tool name and truncated arguments
- Indicates success/failure status for tool results
- Automatic truncation of long outputs

**Usage Example:**

See [EXAMPLES.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/EXAMPLES.md) for complete working examples with hooks configuration.

```yaml
---
bundle:
  name: base
  version: 1.0.0
hooks:
- module: hooks-streaming-ui
  source: git+https://github.com/microsoft/amplifier-module-hooks-streaming-ui@main
  config:
    ui:
      show_thinking_stream: true
      show_tool_lines: 20
      show_token_usage: true
---
```

### Other Available Hooks

#### Safety and Production Hooks

**hooks-approval**
- **Purpose:** Request user approval before executing dangerous operations
- **GitHub:** https://github.com/microsoft/amplifier-module-hooks-approval
- **Configuration:** Pattern matching for dangerous commands
- ⚠️ **Note:** Blocks execution waiting for approval - essential for production safety

```yaml
hooks:
- module: hooks-approval
  source: git+https://github.com/microsoft/amplifier-module-hooks-approval@main
  config:
    auto_approve: false
    dangerous_patterns:
      - "rm -rf"
      - "sudo"
      - "DELETE FROM"
      - "DROP TABLE"
      - "DROP DATABASE"
      - "chmod 777"
      - "chown"
```

**hooks-backup**
- **Purpose:** Automatic backup of files before modification
- **GitHub:** https://github.com/microsoft/amplifier-module-hooks-backup
- **Configuration:** Backup directory and max backup count
- **Use case:** Enables undo of file operations

```yaml
hooks:
- module: hooks-backup
  source: git+https://github.com/microsoft/amplifier-module-hooks-backup@main
  config:
    max_backups: 10
    backup_dir: ~/.amplifier-cli/backups
```

**hooks-status-context**
- **Purpose:** Inject git status and datetime into agent context
- **GitHub:** https://github.com/microsoft/amplifier-module-hooks-status-context
- **Configuration:** Control what context information is included
- **Use case:** Better contextual awareness for git operations

```yaml
hooks:
- module: hooks-status-context
  source: git+https://github.com/microsoft/amplifier-module-hooks-status-context@main
  config:
    include_datetime: true
    datetime_include_timezone: false
    include_git_status: true
```

#### Observability Hooks

**hooks-logging**
- **Purpose:** Log events to console or file
- **Configuration:** `log_level` (DEBUG, INFO, WARNING, ERROR)

**hooks-redaction**
- **Purpose:** Redact sensitive information from logs
- **Configuration:** Pattern-based redaction rules

**hooks-todo-reminder**
- **Purpose:** Remind about pending todos during execution

**hooks-memory-capture**
- **Purpose:** Capture and persist conversation context for memory systems
- **See:** [MEMORY_GUIDE.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/MEMORY_GUIDE.md)

## Creating Custom Hooks

**Status:** ⚠️ **Experimental - Not Recommended**

### Known Issues (December 2025)

Custom hook implementations face significant challenges:

1. **Response Handling Interference**
   - Custom hooks can cause empty API responses
   - Exact mechanism not fully understood
   - Symptom: `response.length = 0` from `session.execute()`

2. **Console Output Timing**
   - Hooks fire at specific lifecycle points
   - Console output must not interfere with response collection
   - Using `stderr` vs `stdout` affects behavior

3. **Module Loading**
   - Local file:// URIs work for loading
   - Requires absolute paths: `file:///absolute/path/to/hook.py`
   - Must implement proper `mount()` async function

### Hook Implementation Pattern

If you must create a custom hook, follow this pattern:

```python
"""Custom hook module."""

from typing import Any, Dict

async def mount(coordinator: Any, config: Dict[str, Any]) -> None:
    """Mount the hook by registering event handlers."""

    # Extract configuration
    ui_config = config.get("ui", {})

    # Create hook instance
    hooks = CustomHooks(
        show_something=ui_config.get("show_something", True)
    )

    # Register hooks for specific events
    coordinator.hooks.register("content_block:start", hooks.handle_block_start)
    coordinator.hooks.register("content_block:end", hooks.handle_block_end)
    coordinator.hooks.register("tool:pre", hooks.handle_tool_pre)
    coordinator.hooks.register("tool:post", hooks.handle_tool_post)


class CustomHooks:
    """Custom hook implementation."""

    def __init__(self, show_something: bool = True):
        self.show_something = show_something

    async def handle_block_start(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle content block start event."""
        # Your observability code here
        # WARNING: Do NOT modify data, only observe

        # MUST return continue action
        return {"action": "continue"}

    async def handle_block_end(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle content block end event."""
        return {"action": "continue"}

    async def handle_tool_pre(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool invocation event."""
        return {"action": "continue"}

    async def handle_tool_post(self, event: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool result event."""
        return {"action": "continue"}
```

### Critical Requirements

1. **Always return `{"action": "continue"}`** - Hooks must not block execution
2. **Pure observability** - Do not modify data or state
3. **Async handlers** - All handlers must be async functions
4. **Error handling** - Wrap output code in try/except to prevent crashes
5. **Console safety** - Consider using stderr instead of stdout

### Recommendation

**Use official hooks modules until custom hook patterns are better understood.**

The official `hooks-streaming-ui` module is:
- Well-tested and reliable
- Configurable for most needs
- Maintained by the amplifier team
- Does not cause API response issues

### Learnings from Failed Attempts

**What we tried (December 2025):**
1. Created custom hook with rich library for formatting
2. Used `Console(stderr=True)` to avoid stdout conflicts
3. Implemented intelligent JSON parsing
4. Added better visual formatting

**Why it failed:**
- Hook loaded successfully (no import errors)
- But caused empty API responses
- Response string had `length=0` after `session.execute()`
- Reverting to official module fixed the issue immediately

**Root cause hypothesis:**
- Custom hook interferes with response stream collection
- Possibly writes to wrong output stream at wrong time
- Or modifies event data inadvertently
- Exact mechanism remains unknown

## Hook Events Reference

**Available hook events:**
- `content_block:start` - Content block begins (thinking, text, etc.)
- `content_block:end` - Content block completes
- `tool:pre` - Before tool execution
- `tool:post` - After tool execution
- `llm:request` - Before LLM API call
- `llm:response` - After LLM API call

**Event data structure:**

```python
# content_block:start
{
    "block_type": "thinking" | "text" | "reasoning",
    "block_index": int
}

# content_block:end
{
    "block_index": int,
    "total_blocks": int,
    "block": {
        "type": "thinking",
        "thinking": str
    },
    "usage": {
        "input_tokens": int,
        "output_tokens": int,
        "total_tokens": int
    }
}

# tool:pre
{
    "tool_name": str,
    "tool_input": dict
}

# tool:post
{
    "tool_name": str,
    "tool_response": dict | str
}
```

## Best Practices

1. **Start with official modules** - Use `hooks-streaming-ui` for terminal UI
2. **Configure, don't customize** - Adjust settings before writing custom code
3. **Test incrementally** - If creating custom hooks, test each handler separately
4. **Use stderr for debug output** - Avoid interfering with response collection
5. **Keep handlers simple** - Minimal logic reduces chance of interference
6. **Return quickly** - Don't block the execution pipeline
7. **Handle errors gracefully** - Wrap all output code in try/except

## Troubleshooting

**Empty API responses:**
- Revert to official `hooks-streaming-ui`
- Check if custom hook is loaded
- Verify hook returns `{"action": "continue"}`

**No output displayed:**
- Check configuration: `show_thinking_stream`, `show_tool_lines`, `show_token_usage`
- Verify hook module is loaded in bundle
- Check console output isn't redirected

**Hooks not firing:**
- Verify hook registration in `mount()` function
- Check event names match exactly
- Ensure async handlers are used

## Future Work

- [ ] Understand exact mechanism of response interference
- [ ] Document safe console output patterns
- [ ] Create validated custom hook examples
- [ ] Test hook combinations and interactions
- [ ] Investigate rich library compatibility

## See Also

- [SKILL.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/SKILL.md) - Full CLI application patterns
- [ARCHITECTURE.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/ARCHITECTURE.md) - Foundation architecture reference
- [MEMORY.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/MEMORY.md) - Memory system integration
- [EXAMPLES.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/EXAMPLES.md) - Complete bundle examples
