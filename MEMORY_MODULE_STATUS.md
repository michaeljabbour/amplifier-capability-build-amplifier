# Memory Module Status

## Working Modules ✅

### 1. tool-memory
- **Status**: ✅ Working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-tool-memory@main`
- **Pattern**: Uses `mount()` function (current standard)
- **Provides**: 6 memory tools
  - `add_memory` - Store new memories
  - `search_memories` - Search by keyword
  - `list_memories` - List with filters
  - `get_memory` - Get by ID
  - `update_memory` - Update existing
  - `delete_memory` - Remove memory

### 2. context-memory
- **Status**: ✅ Working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-context-memory@main`
- **Pattern**: Uses `mount()` function (current standard)
- **Provides**: Progressive memory context injection

## Fixed Module ✅

### 3. hooks-memory-capture
- **Status**: ✅ Fixed and working
- **Location**: `git+https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture@main`
- **Pattern**: Now uses `mount()` function (current standard)
- **Fixed**: Added mount() function in commit 47ddb46

**What it provides**:
- Automatic memory capture from tool outputs
- Session summaries on session end
- Observation extraction without manual `add_memory` calls

**Fix needed**:
The module needs to be updated to use the `mount()` pattern like other hooks. Example:

```python
# Current pattern (OLD):
from .hook import MemoryCaptureHook, create_hook
__all__ = ["MemoryCaptureHook", "create_hook"]

# Needed pattern (NEW):
async def mount(coordinator: ModuleCoordinator, config: dict | None = None):
    # Hook registration logic here
    coordinator.hooks.register("tool:post", handler, priority=150)
    coordinator.hooks.register("session:end", summary_handler, priority=150)
```

Reference implementation: `amplifier-module-hooks-logging` (has correct mount() pattern)

## Current Setup in base.md

```yaml
session:
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
