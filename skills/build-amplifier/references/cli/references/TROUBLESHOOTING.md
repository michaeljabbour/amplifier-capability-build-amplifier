# Troubleshooting Guide: Production Patterns & Bug Fixes

**Purpose:** Documents production patterns, common issues, race conditions, and bug fixes discovered while building Amplifier CLI applications.

**Last Updated:** 2025-12-21

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

- [Foundation alignment summary](#foundation-alignment-verification) (the separate historical `FOUNDATION_AUDIT.md` is not included).
- [CLI method](../METHOD.md#production-configuration-choices) (the vendored form of the historical `SKILL.md`).
- [HOOKS.md](HOOKS.md)
- Original planning note: not included in this public reference.

---

## Next Session Priorities

1. Test loop-streaming fix validates race condition is eliminated
2. Verify safety hooks work as expected (approval prompts, backups)
3. Measure token usage with hooks-streaming-ui
4. Consider adding cost tracking if needed (custom implementation)

---

## Skills as Passive Documentation (2025-12-21)

### The Discovery

Agent Skills are **teaching materials, not executable applications**. This fundamental insight reshaped the entire repository structure.

### What Changed

**Before (Misunderstanding):**
```
amplifier-cli-skill/
├── assets/
│   ├── bundles/base.md        # "Runnable" files
│   ├── providers/*.yaml        # Provider configs
│   └── agents/bug-hunter.md   # Example agents
├── README.md
├── CLAUDE.md
├── AGENTS.md
└── SKILL.md                    # Primary documentation
```

**After (Correct Understanding):**
```
amplifier-cli-skill/
├── SKILL.md                    # ONLY root file (per spec)
└── references/
    ├── EXAMPLES.md             # All code examples in one place
    ├── BUILD_PATTERNS.md       # How to build CLIs
    └── [other reference docs]
```

### Key Insights

1. **Skills Don't Execute Files**
   - SKILL.md code blocks are sufficient for teaching
   - Users create their own assets when building
   - No need to maintain "reference" files that aren't run
   - Validation overhead eliminated

2. **Teaching vs Providing**
   - **Teaching:** Show patterns in documentation
   - **Providing:** Give files to copy/run
   - Skills should teach, not provide
   - Users learn better by creating than copying

3. **Agent Skills Specification**
   - SKILL.md is the primary entry point (not README.md)
   - Optional assets/ directory for truly necessary files
   - Most skills don't need assets at all
   - Code examples in markdown are sufficient

4. **Progressive Disclosure**
   - SKILL.md: High-level teaching (8000+ lines)
   - references/: Deep dives and specialized topics
   - Single root file simplifies discovery
   - Clear information architecture

### Architectural Decisions Made

**Consolidated Documentation:**
- CLAUDE.md + AGENTS.md → references/CONTRIBUTING.md
- MEMORY_GUIDE.md + MEMORY_MODULE_STATUS.md → references/MEMORY.md
- BUILD_GUIDE.md → references/BUILD_PATTERNS.md
- SESSION_LEARNINGS.md → references/TROUBLESHOOTING.md
- CHANGELOG.md → references/REFERENCE_IMPLEMENTATION_HISTORY.md

**Removed Redundant Files:**
- README.md (SKILL.md is entry point)
- assets/ directory (examples in EXAMPLES.md)
- references/REFACTORING.md (obsolete)

**Result:**
- 8 root files → 1 root file (SKILL.md only)
- Cleaner repository structure
- Aligned with agentskills.io best practices
- Focus on teaching patterns over providing files

### When to Use assets/

Assets directory is appropriate when:
- **Binary files needed:** Images, PDFs, datasets
- **Complex configuration:** Multi-file setups too large for code blocks
- **Downloadable templates:** Starter projects users can clone

Assets directory is NOT needed for:
- Simple code examples (use code blocks)
- Single-file configurations (inline in SKILL.md)
- Teaching patterns (describe, don't provide)

### Impact on Validation

**Before:** Had to validate asset files work
```python
# Complex validation in CLAUDE.md
uv run python -c "import asyncio; from amplifier_foundation import load_bundle;
asyncio.run(load_bundle('./assets/bundles/base.md'))"
```

**After:** No validation needed
- Code examples are documentation only
- Users create their own working implementations
- Reference implementation (amplifier-simplecli) validates patterns work
- No maintenance burden for "example" files

---

## Repository Structure Evolution (2025-12-21)

### The Journey to "Stellar"

Goal: Create a professional, maintainable Agent Skills repository that exemplifies best practices.

### Phase 1: Initial Structure (Before)

```
amplifier-cli-skill/
├── README.md (redundant with SKILL.md)
├── AGENTS.md (coding guidelines)
├── CLAUDE.md (Claude Code instructions)
├── BUILD_GUIDE.md (build patterns)
├── MEMORY_GUIDE.md (memory system docs)
├── MEMORY_MODULE_STATUS.md (module status)
├── SKILL.md (primary skill)
├── assets/
│   ├── bundles/
│   ├── providers/
│   └── agents/
└── references/
    ├── REFACTORING.md
    └── [other docs]
```

**Problems:**
- 8 root-level files (confusing entry point)
- Redundant documentation (README vs SKILL.md)
- Split information (MEMORY_GUIDE + MEMORY_MODULE_STATUS)
- assets/ directory not serving purpose
- No clear information architecture

### Phase 2: Agent Skills Alignment

**Commit:** eada7dd "align repository structure with Agent Skills specification"

**Key Changes:**
1. Removed README.md (SKILL.md is spec-compliant entry point)
2. Merged related docs (CLAUDE+AGENTS→CONTRIBUTING, MEMORY docs→MEMORY.md)
3. Moved reference docs to references/
4. Created new comprehensive guides (HOOKS.md, CUSTOM_EXTENSIONS.md)
5. Removed obsolete docs (REFACTORING.md)

**Result:** 8 root files → 1 root file

### Phase 3: Assets Removal

**Commit:** a048e3f "remove assets/ directory and consolidate examples"

**Rationale:**
- Skills are passive documentation, not executable apps
- Code blocks in SKILL.md sufficient for teaching
- Users create their own implementations
- Simpler structure, less maintenance

**Key Changes:**
1. Created references/EXAMPLES.md with all code examples
2. Removed assets/bundles/, assets/providers/, assets/agents/
3. Updated all references in SKILL.md to use generic paths
4. No more validation overhead

### Phase 4: Final Polish

**Commit:** 241054f "reorganize references directory for clarity"

**Key Changes:**
1. SESSION_LEARNINGS.md → TROUBLESHOOTING.md (clearer name)
2. CHANGELOG.md → REFERENCE_IMPLEMENTATION_HISTORY.md (clarifies purpose)
3. DOCUMENTATION_AUDIT_PROMPT.md → .github/AUDIT_PROMPT.md (meta-document)
4. Updated cross-references everywhere

### Final Structure (Current)

```
amplifier-cli-skill/
├── SKILL.md                              # ONLY root file ✅
├── .github/
│   └── AUDIT_PROMPT.md                   # Maintainer tool
└── references/
    ├── ARCHITECTURE.md                   # Foundation architecture
    ├── ARCHITECTURE_FLOWS.md             # Detailed flows
    ├── BUILD_PATTERNS.md                 # Build guidance
    ├── CONTRIBUTING.md                   # Repository guidelines
    ├── CUSTOM_EXTENSIONS.md              # Community modules
    ├── EXAMPLES.md                       # All code examples
    ├── HOOKS.md                          # Hooks system
    ├── MEMORY.md                         # Memory system
    ├── README.md                         # Directory index
    ├── REFERENCE_IMPLEMENTATION_HISTORY.md  # simplecli evolution
    └── TROUBLESHOOTING.md                # This file
```

### Benefits Achieved

1. **Clear Entry Point**
   - SKILL.md is the only root file
   - Follows Agent Skills specification exactly
   - No confusion about where to start

2. **Progressive Disclosure**
   - High-level: SKILL.md (teaching patterns)
   - Deep dives: references/ (specialized topics)
   - Meta-tools: .github/ (maintainer utilities)

3. **Maintainability**
   - Single source of truth for each topic
   - No redundant documentation
   - Clear cross-references
   - Easy to find information

4. **Professional Polish**
   - Clean directory structure
   - Purpose-focused naming
   - Consistent documentation style
   - Comprehensive coverage

5. **Aligned with Specification**
   - Follows agentskills.io guidelines
   - SKILL.md as primary interface
   - Optional references/ for depth
   - No unnecessary files

### Lessons for Future Skills

1. **Start Simple**
   - Single SKILL.md file is often sufficient
   - Add references/ only when needed
   - Don't create assets/ unless truly necessary

2. **Think Teaching, Not Providing**
   - Code examples in markdown > separate files
   - Describe patterns > provide implementations
   - Users learn by building, not copying

3. **Follow the Spec**
   - agentskills.io defines best practices
   - SKILL.md is the entry point
   - Keep root directory clean
   - Use progressive disclosure

4. **Consolidate Ruthlessly**
   - Merge related documentation
   - Remove redundant files
   - Single source of truth per topic
   - Clear naming conventions

---

## Documentation Patterns Discovered (2025-12-21)

### Cross-Reference Architecture

**Pattern:** Every document should reference related documents explicitly.

**Example from SKILL.md:**
```markdown
For more details:
- [ARCHITECTURE.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/references/ARCHITECTURE.md) - Foundation architecture
- [HOOKS.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/references/HOOKS.md) - Complete hooks reference
- [EXAMPLES.md](https://github.com/michaeljabbour/amplifier-cli-skill/blob/6904eca0980767cff8d3c70033839f6c1535dffc/skills/amplifier-cli-skill/references/references/EXAMPLES.md) - Full code examples
```

**Benefits:**
- Users discover related content naturally
- Forms knowledge graph, not isolated docs
- Reduces duplicate information
- Guides learning journey

### Progressive Depth Pattern

**Pattern:** Start shallow, provide paths to depth.

**Implementation:**
1. **SKILL.md:** High-level patterns (what & why)
2. **references/:** Deep dives (how & when)
3. **EXAMPLES.md:** Complete working code
4. **TROUBLESHOOTING.md:** Production learnings

**Example Flow:**
```
User reads SKILL.md
  ↓ "Want to understand hooks?"
  → references/HOOKS.md
    ↓ "Want code examples?"
    → references/EXAMPLES.md
      ↓ "Hit production issues?"
      → references/TROUBLESHOOTING.md
```

### Single Source of Truth

**Pattern:** One authoritative document per topic.

**Before (Split):**
- MEMORY_GUIDE.md: How to use memory
- MEMORY_MODULE_STATUS.md: Module status
- SKILL.md: Basic memory info
- BUILD_GUIDE.md: More memory config

**After (Unified):**
- references/MEMORY.md: Complete memory documentation
- SKILL.md: Quick overview with link to MEMORY.md

**Benefits:**
- No conflicting information
- Clear update target
- Easier maintenance
- User knows where to look

### Meta-Document Separation

**Pattern:** Separate user docs from maintainer tools.

**Implementation:**
```
references/              # User-facing documentation
.github/                 # Maintainer tools
  └── AUDIT_PROMPT.md   # Documentation validation
```

**Why:**
- Users don't see maintenance tooling
- Clear separation of concerns
- Can expand .github/ without cluttering
- Professional repository hygiene

### Naming Conventions

**Pattern:** Names should reveal purpose immediately.

**Good Names:**
- TROUBLESHOOTING.md (not SESSION_LEARNINGS.md)
- REFERENCE_IMPLEMENTATION_HISTORY.md (not CHANGELOG.md)
- BUILD_PATTERNS.md (not BUILD_GUIDE.md)
- CONTRIBUTING.md (not AGENTS.md + CLAUDE.md)

**Why:**
- No guessing what file contains
- Search-friendly
- Self-documenting
- Industry standard conventions
