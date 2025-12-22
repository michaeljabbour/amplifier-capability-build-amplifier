# Memory System for Amplifier CLI Applications

**⚠️ IMPORTANT:** These are **custom extension modules** (community contributions), NOT part of the official amplifier-foundation ecosystem.

This document explains how to add persistent memory to your Amplifier CLI using custom memory modules.

## Status

### Working Modules ✅

**1. tool-memory**
- **Status**: ✅ Working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-tool-memory@main`
- **Pattern**: Uses `mount()` function (current standard)
- **Provides**: 16 memory tools
  - `add_memory`, `get_memory`, `update_memory`, `delete_memory`
  - `list_memories`, `search_memories`
  - `create_session`, `update_session`, `get_session`, `list_sessions`
  - `get_context_for_session`
  - `add_file_context`, `get_file_context`
  - `get_stats`, `compact`, `export_memories`

**2. context-memory**
- **Status**: ✅ Working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-context-memory@main`
- **Pattern**: Uses `mount()` function (current standard)
- **Provides**: Progressive memory context injection

**3. hooks-memory-capture**
- **Status**: ✅ Fixed and working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture@main`
- **Pattern**: Now uses `mount()` function (current standard)
- **Fixed**: Added mount() function in commit 47ddb46
- **Provides**:
  - Automatic memory capture from tool outputs
  - Session summaries on session end
  - Observation extraction without manual `add_memory` calls

## What Memory Provides

- **Persistent observations** across sessions (bugfix, feature, discovery, decision)
- **Session tracking** with structured summaries
- **Progressive disclosure** for cost-effective context injection
- **Automatic capture** of learnings from tool outputs
- **Full-text search** across all memory content

## The Three Core Memory Modules

### 1. tool-memory (Storage Layer)
**Repository**: https://github.com/michaeljabbour/amplifier-module-tool-memory

SQLite storage with FTS5 full-text search.

**Provides 16 tools**:
- `add_memory`, `get_memory`, `update_memory`, `delete_memory`
- `list_memories`, `search_memories`
- `create_session`, `update_session`, `get_session`, `list_sessions`
- `get_context_for_session`
- `add_file_context`, `get_file_context`
- `get_stats`, `compact`, `export_memories`

### 2. hooks-memory-capture (Automatic Capture)
**Repository**: https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture

Listens to `tool:post` events and automatically captures observations.

**Hook events**:
- `session:start` - Initialize session context
- `tool:post` - Analyze output, capture observations
- `session:end` - Create final summary

### 3. context-memory (Context Injection)
**Repository**: https://github.com/michaeljabbour/amplifier-module-context-memory

Injects relevant memories at session start using progressive disclosure.

**Progressive disclosure pattern**:
1. **Layer 1 (Index)**: ~20 tokens per observation (title, type, ID)
2. **Layer 2 (Full Details)**: On-demand via `get_memory(id)`

## Quick Setup

Add to your bundle configuration (e.g., `bundles/base.md`):

```yaml
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
  - module: hooks-memory-capture
    source: git+https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture@main
    config:
      min_content_length: 50
      auto_summarize_interval: 10
      priority: 150

tools:
  - module: tool-memory
    source: git+https://github.com/michaeljabbour/amplifier-module-tool-memory@main
    config:
      storage_path: ~/.amplifier/memories.db
      max_memories: 1000
      enable_fts: true
      enable_sessions: true
```

## Observation Types

| Type | When Used | Example |
|------|-----------|---------|
| `bugfix` | Fixed something broken | "Fixed null pointer in parser" |
| `feature` | Added new capability | "Implemented caching layer" |
| `refactor` | Restructured code, same behavior | "Extracted helper functions" |
| `change` | Generic modification | "Updated config file" |
| `discovery` | Learned about existing system | "Found config uses YAML frontmatter" |
| `decision` | Architectural choice | "Chose SQLite over Redis for simplicity" |

## Configuration Options

### tool-memory
```yaml
config:
  storage_path: ~/.amplifier/memories.db  # Where to store memories
  max_memories: 1000                       # Trigger compaction above this
  enable_fts: true                         # Full-text search
  enable_sessions: true                    # Session tracking
  compact_threshold: 0.9                   # Start compaction at 90% capacity
  min_importance_preserve: 7               # Never compact importance >= 7
```

### hooks-memory-capture
```yaml
config:
  min_content_length: 50         # Minimum chars to capture
  auto_summarize_interval: 10    # Create summary every N tool calls
  priority: 150                  # Hook priority (after event-broadcast)
```

### context-memory
```yaml
config:
  index_limit: 50               # Max observations in index
  lookback_days: 90             # How far back to look
  token_budget: 2000            # Max tokens for context injection
```

## How It Works

### Session Start
```
┌─────────────────────────────────────────┐
│  context-memory injects:                │
│  ├── Last session summary               │
│  └── Observation index                  │
└─────────────────────────────────────────┘
```

### During Session
```
┌─────────────────────────────────────────┐
│  hooks-memory-capture listens:          │
│  ├── tool:post events                   │
│  ├── Classifies observation type        │
│  ├── Extracts learnable content         │
│  └── Stores in tool-memory              │
└─────────────────────────────────────────┘
```

### Session End
```
┌─────────────────────────────────────────┐
│  hooks-memory-capture creates:          │
│  └── Final summary with next_steps      │
└─────────────────────────────────────────┘
```

## Example System Prompt

Tell the assistant about memory in your bundle instruction:

```markdown
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
```

## Safe Compaction

Memory automatically compacts when approaching capacity:

1. **Trigger**: At 90% of `max_memories` (configurable)
2. **Selection**: Old, low-importance memories selected first
3. **Preservation**: High-importance (≥7) and recent (<7 days) protected
4. **Sessions**: Session summaries preserved

## Pairs Well With

| Module | Why |
|--------|-----|
| **hooks-logging** | JSONL logs complement memory for debugging |
| **hooks-redaction** | Redact PII/secrets before memory capture |
| **tool-todo** | Track tasks alongside memory |
| **tool-search** | Combine with memory search for context |

## Testing Memory

```bash
# Run your CLI
python simple_cli.py

# In session:
You: What did we work on last time?
Assistant: [Retrieves memory context and summarizes previous session]

You: Add a memory that we fixed the authentication bug
Assistant: [Uses add_memory tool to store observation]
```

## Impact

**With full memory system (all 3 modules)**:
- ✅ Memory storage and retrieval works
- ✅ Memory context injection works
- ✅ Manual memory creation via `add_memory` works
- ✅ Automatic observation capture works
- ✅ Session summaries automatically created

## Module Count

**Total: 14 modules** (up from 13)
- Session: loop-streaming, context-simple, context-memory (3)
- Hooks: logging, redaction, streaming-ui, todo-reminder, memory-capture (5)
- Tools: filesystem, bash, web, search, todo, memory (6)

## What Changed

**hooks-memory-capture (commit 47ddb46)**:
- Added `mount()` function following amplifier-core patterns
- Hook registers via `coordinator.hooks.register()`
- Accesses memory store via `coordinator.get_capability("memory.store")`
- Backwards compatible - kept `create_hook()` for legacy support

**tool-memory (commit 53854f8)**:
- Exposes memory store via `coordinator.set_capability("memory.store", store)`
- Enables hooks-memory-capture to access store
- Required for auto-capture functionality
