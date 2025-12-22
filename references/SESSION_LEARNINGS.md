# Session Learnings: Foundation Alignment & Production Readiness

**Date:** 2025-12-21
**Session Focus:** Fixing write_file bug, achieving 100% foundation alignment, production safety

---

## Critical Bug Fix: Race Condition in Tool Execution

### The Problem
Model repeatedly called `write_file` with only `file_path` parameter (no content), resulting in:
- 0 bytes written each time
- Infinite loops lasting 40+ minutes to 2 hours
- Hundreds of failed attempts

### Root Cause
**loop-events orchestrator** had a race condition:
```python
# Sequential execution (BROKEN)
for tool_call in tool_calls:
    result = await tool.execute(tool_call.arguments)  # Async starts
    await context.add_message({...})  # Added BEFORE execution completes
    # Race condition: Next iteration sees incomplete result
```

### Solution
**loop-streaming orchestrator** uses parallel execution:
```python
# Parallel with gather (FIXED)
tool_tasks = [self._execute_tool_only(tc, ...) for tc in tool_calls]
tool_results = await asyncio.gather(*tool_tasks)  # WAIT for ALL to complete

# THEN add results (all executions finished)
for tool_call_id, content in tool_results:
    await context.add_message({...})
```

**Key Insight:** `asyncio.gather()` ensures all tool executions complete before ANY result is added to context, eliminating the race condition.

---

## Production Safety Layers Added

### 1. Orchestrator Configuration
```yaml
session:
  orchestrator:
    module: loop-streaming
    config:
      extended_thinking: true
      max_iterations: 25  # Hard limit prevents infinite loops
```

### 2. Request Timeout Protection
```python
response = await asyncio.wait_for(
    session.execute(user_input),
    timeout=300.0  # 5 minute max per request
)
```

### 3. Safety Hooks from Foundation
- **hooks-approval:** Validates dangerous operations before execution
- **hooks-backup:** Automatic file backups before modification
- **hooks-status-context:** Git and datetime awareness

### 4. Enhanced System Prompt
Added explicit safety guidelines:
- "Never write empty files"
- "Never loop indefinitely"
- "Always verify success"
- Maximum 25 tool iterations

---

## Foundation Alignment Verification

### Code Pattern: 100% Match
```python
# Foundation canonical pattern
base = await load_bundle(...)
provider = await load_bundle(...)
bundle = base.compose(provider)
prepared = await bundle.prepare()
session = await prepared.create_session()
response = await session.execute(...)
```

### Dependencies: Foundation Only
```
amplifier-foundation>=0.1.0  ✅
rich>=13.0.0                 (UI library)
```

### Modules: 19/19 from Foundation
All modules sourced from: `git+https://github.com/microsoft/amplifier-module-*@main`

### Anti-Patterns: Zero Found
- No SessionStore (app-cli persistence)
- No session_spawner (app-cli delegation)
- No paths.py (app-cli search)
- No app-cli imports anywhere

---

## Documentation Improvements

### New Section: Production Configuration Choices
Added to SKILL.md (lines 408-495):
- Why loop-streaming: Parallel execution prevents race conditions
- Why context-simple: In-memory for stateless CLI sessions
- Safety hooks: From foundation ecosystem
- Validation: app-cli uses same foundation modules

### Clarified App-CLI Role
Explicit warning in SKILL.md:
> "When building your own CLI, start from the foundation patterns above, not from copying amplifier-app-cli internals."

### References Documentation
- HOOKS.md: Comprehensive hooks system reference
- ARCHITECTURE.md: Foundation architecture patterns
- CUSTOM_EXTENSIONS.md: Clear separation of custom vs foundation modules

---

## Key Architectural Decisions

### 1. Orchestrator: loop-streaming
**Rationale:**
- Parallel tool execution via asyncio.gather()
- Prevents race conditions in tool result handling
- Production-tested in amplifier-app-cli

**Foundation provides:**
- loop-basic: Sequential execution
- loop-events: Event-driven (vulnerable to race conditions)
- loop-streaming: Parallel with determinism ✅ CHOSEN

### 2. Context: context-simple
**Rationale:**
- In-memory context management (fast startup)
- Automatic compaction at 80% of token limit
- Perfect for stateless CLI sessions

**Foundation provides:**
- context-simple: In-memory ✅ CHOSEN
- context-persistent: File-based memory loading
- context-memory: Advanced memory patterns

### 3. Safety Hooks
**Chosen based on production needs:**
- hooks-approval: Dangerous operation validation
- hooks-backup: File modification protection
- hooks-status-context: Git/datetime awareness

**NOT included (doesn't exist):**
- hooks-scheduler-cost-aware: Module doesn't exist in foundation

---

## Lessons Learned

### 1. Foundation is Source of Truth
- Don't base implementation on app-cli patterns
- Use foundation's canonical workflow directly
- Reference app-cli only for validation that modules work

### 2. Orchestrator Choice Matters
- loop-events has race conditions in tool execution
- loop-streaming's parallel pattern is production-ready
- The choice directly impacts reliability

### 3. Multiple Safety Layers Needed
No single safeguard is sufficient:
- Max iterations (prevents infinite loops)
- Request timeout (prevents multi-hour hangs)
- System prompt guidance (helps model behavior)
- Debug hooks (visibility into tool calls)
- Safety hooks (dangerous operation validation)

### 4. Documentation Must Be Explicit
- Warn against anti-patterns explicitly
- Show code patterns side-by-side
- Provide rationale for architectural choices
- Separate custom extensions from foundation clearly

---

## Testing Outcomes

### Before Fix (loop-events)
```
🔧 Using tool: write_file
   Arguments: {'file_path': 'index.html'}
✅ Tool result: {'bytes': 0}

[Repeats hundreds of times for 40+ minutes...]
```

### After Fix (loop-streaming)
- **Expected:** Tool receives content parameter
- **Expected:** Bytes written > 0
- **Expected:** No infinite loops
- **Status:** Awaiting user testing with debug hooks enabled

---

## Implementation Checklist

Completed Steps:
- ✅ Switched to loop-streaming orchestrator
- ✅ Added max_iterations: 25
- ✅ Added 5-minute request timeout
- ✅ Improved system prompt with safety rules
- ✅ Added safety hooks (approval, backup, status-context)
- ✅ Created debug hooks for monitoring
- ✅ Documented production configuration choices
- ✅ Verified 100% foundation alignment
- ✅ Removed non-existent hooks-scheduler-cost-aware
- ✅ Clarified custom vs foundation modules
- ✅ Created FOUNDATION_AUDIT.md proof

Pending Steps:
- ⏳ Test loop-streaming fix with debug hooks
- ⏳ Verify safety features work (approval, backup, status)

---

## File Changes Summary

### amplifier-cli-skill
- ✅ SKILL.md: Added Production Configuration Choices section
- ✅ references/HOOKS.md: Documented safety hooks
- ✅ references/CUSTOM_EXTENSIONS.md: Separated custom modules
- ✅ MEMORY_GUIDE.md: Labeled as custom extensions
- ✅ MEMORY_MODULE_STATUS.md: Labeled as custom
- ✅ Removed references/REFACTORING.md (not relevant)

### amplifier-simplecli
- ✅ assets/bundles/base.md: Added 3 safety hooks, updated system prompt
- ✅ assets/providers/*.yaml: Added max_iterations and timeout
- ✅ hooks/hooks_debug/__init__.py: Created debug logging
- ✅ simple_cli.py: Added 5-minute timeout
- ✅ FOUNDATION_AUDIT.md: Comprehensive proof document

---

## References

- [FOUNDATION_AUDIT.md](/Users/michaeljabbour/dev/amplifier-simplecli/FOUNDATION_AUDIT.md)
- [SKILL.md](/Users/michaeljabbour/dev/amplifier-cli-skill/SKILL.md)
- [HOOKS.md](/Users/michaeljabbour/dev/amplifier-cli-skill/references/HOOKS.md)
- [Plan File](/Users/michaeljabbour/.claude/plans/luminous-whistling-grove.md)

---

## Next Session Priorities

1. Test loop-streaming fix validates race condition is eliminated
2. Verify safety hooks work as expected (approval prompts, backups)
3. Measure token usage with hooks-streaming-ui
4. Consider adding cost tracking if needed (custom implementation)
