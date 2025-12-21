# Changelog - Simple Amplifier CLI

## Recent Updates (Last 4-6 Prompts)

### Memory System Complete (Latest)

**✅ Full Memory System Working**
- All 3 memory modules functional: `context-memory` + `tool-memory` + `hooks-memory-capture`
- All memory tools available: `add_memory`, `search_memories`, `list_memories`, etc.
- Automatic observation capture now working
- Session summaries automatically created
- Fresh database created at `~/.amplifier/memories.db` with correct schema

**✅ Fixed hooks-memory-capture**
- Updated module to use `mount()` function pattern (commit 47ddb46)
- Now compatible with current amplifier-core validation
- Accesses memory store via coordinator capabilities
- Pushed to GitHub: https://github.com/michaeljabbour/amplifier-module-hooks-memory-capture

**✅ Updated tool-memory**
- Exposes memory store via coordinator capabilities (commit 53854f8)
- Enables hooks-memory-capture to access store
- Pushed to GitHub: https://github.com/michaeljabbour/amplifier-module-tool-memory

**✅ Repository Cleanup**
- Removed unused composite bundles (opus.md, sonnet.md, haiku.md)
- Removed unused dev.md, prod.md, anthropic.yaml
- Clean bundle structure: base.md composes with provider yamls

**Final Module Count: 14**
- Session: loop-streaming, context-simple, context-memory (3)
- Hooks: logging, redaction, streaming-ui, todo-reminder, memory-capture (5)
- Tools: filesystem, bash, web, search, todo, memory (6)

### Bundle Composition Refactor

**✅ Implemented Bundle Includes Pattern**
- Created composite bundles: `opus.md`, `sonnet.md`, `haiku.md`
- Each bundle uses `includes:` to compose base + provider
- Simplified CLI code: single `load_bundle()` call instead of manual composition
- More declarative and maintainable

**Before:**
```python
base = await load_bundle("base.md")
provider = await load_bundle("opus.yaml")
composed = base.compose(provider)
```

**After:**
```python
bundle = await load_bundle("opus.md")  # Includes base + provider
```

### UX Improvements

**✅ Added Loading Spinners**
- Spinners during bundle loading and preparation
- Better visual feedback for long operations

**✅ Last Session Tracking**
- Shows "Last session: Xh ago" in welcome panel
- Helps users know when they last used the CLI

**✅ Better Prompts & Tips**
- Tips in welcome panel: "Type exit to quit | Use @ for memory search"
- Styled input prompt: `You:` in cyan
- "Thinking..." indicator during processing
- Better error messages with helpful tips

**✅ Improved Visual Design**
- Title emoji: 🚀 Ready
- Error emoji: ❌
- Consistent use of rich panels and formatting

### Memory System Integration

**✅ Added 14 Modules**
- Session: `loop-streaming`, `context-simple`, `context-memory`
- Hooks: `hooks-logging`, `hooks-redaction`, `hooks-streaming-ui`, `hooks-todo-reminder`, `hooks-memory-capture`
- Tools: `tool-filesystem`, `tool-bash`, `tool-web`, `tool-search`, `tool-todo`, `tool-memory`

**✅ Fixed Module Versions**
- Changed memory modules from `@v0.1.0` (didn't exist) to `@main`
- All modules now properly resolve and download

### Update Command Improvements

**✅ Comprehensive Update Checks**
- Checks `amplifier-foundation` package version
- Checks `rich` package version
- Checks CLI repository for git updates (local vs remote commits)
- Shows 14 modules in use with their types
- Displays cache size and module count

**✅ Smart Update Actions**
- Updates pip packages if needed (`pip install --upgrade`)
- Pulls latest CLI code if needed (`git pull`)
- Clears cache and re-downloads modules
- Shows update summary before proceeding

### Bundle Files Created

```
assets/
├── bundles/
│   ├── base.md          # Core modules (session, hooks, tools)
│   ├── opus.md          # Composite: base + opus provider (NEW)
│   ├── sonnet.md        # Composite: base + sonnet provider (NEW)
│   ├── haiku.md         # Composite: base + haiku provider (NEW)
│   ├── dev.md           # Development overlay
│   └── prod.md          # Production overlay
└── providers/
    ├── opus.yaml        # Opus 4.5 provider
    ├── sonnet.yaml      # Sonnet 4.5 provider
    └── haiku.yaml       # Haiku 4 provider
```

### Settings Management

**✅ Simplified Approach**
- Settings in `~/.amplifier-cli/settings.yaml`
- Model selection maps directly to composite bundle
- No temp file creation
- Clean version-controlled bundles

### Documentation Updates

**✅ Added Guides**
- `MEMORY_GUIDE.md` - Complete memory system documentation
- `BUILD_GUIDE.md` - One-touch build patterns
- `CHANGELOG.md` - This file!

**✅ Updated Skill Documentation**
- All patterns documented in amplifier-cli-skill repo
- Ready for future builds

## Architecture Summary

### Current Pattern (Clean & Simple)

1. **User runs CLI** → Loads settings from `~/.amplifier-cli/settings.yaml`
2. **Maps model to bundle** → `opus.md`, `sonnet.md`, or `haiku.md`
3. **Loads composite bundle** → Bundle uses `includes:` to compose base + provider
4. **Prepares session** → Downloads modules, creates session
5. **Runs REPL** → User chats with Claude, memory automatically captures learnings

### Key Benefits

- **Declarative**: Bundle composition via `includes:` is self-documenting
- **Maintainable**: All configs are version-controlled YAML/MD files
- **Extensible**: Add new models by creating new composite bundles
- **Standard**: Follows amplifier-foundation best practices

## What's Next

Potential improvements:
- Session save/resume with full context
- Token usage tracking
- Command history (arrow keys)
- Interactive model switching mid-session
- Export conversations to markdown
