# User Stories - Simple List

## Phase 1: MVP (Weeks 1-2) - 7 stories

### Core Execution
- **US-1.1: Basic Prompt Execution** - Execute prompts against configured model from CLI
- **US-1.2: Multi-Turn Conversations** - Multi-turn conversations with preserved context

### Bundle Management
- **US-2.1: Load Provider Bundles** - Load providers from local files and git URLs

### Configuration
- **US-3.1: Environment-Based Configuration** - Configure via environment variables

### Agent Delegation
- **US-4.1: Spawn Agent Sub-Sessions** - Delegate tasks to specialized agents

### Context & Memory
- **US-5.1: @Mention File References** - Reference files using @namespace:path syntax

### Developer Experience
- **US-8.1: Clear Error Messages** - Helpful, actionable error messages

---

## Phase 2: Power User (Weeks 3-4) - 12 stories

### Core Execution
- **US-1.3: Interactive REPL Mode** - Interactive REPL session with history
- **US-1.4: Session Persistence & Resumption** - Save and resume sessions across invocations

### Bundle Management
- **US-2.2: Bundle Composition CLI** - Compose multiple bundles from CLI
- **US-2.3: Bundle Inspection** - Inspect bundle contents (metadata, providers, tools)

### Configuration
- **US-3.2: Config File Support** - Use config files (which are bundles)
- **US-3.3: Project-Scoped Configuration** - Project-specific config with directory search

### Agent Delegation
- **US-4.2: Resume Agent Sessions** - Resume previous agent sessions

### Context & Memory
- **US-5.2: Custom @Mention Shortcuts** - Shortcuts like @user:, @project:, @~/

### Tools & Capabilities
- **US-6.1: Tool Discovery & Management** - Discover and enable tools via bundles

### Observability
- **US-7.1: Hook System for Observability** - Observe and control behavior with hooks

### Developer Experience
- **US-8.2: Shell Completion** - Shell completion for commands
- **US-8.3: Rich Terminal UI** - Beautiful terminal with markdown rendering

### Multi-Project Support
- **US-9.1: Project Isolation** - Project-isolated sessions and config

---

## Phase 3: Advanced (Weeks 5+) - 9 stories

### Bundle Management
- **US-2.4: Bundle Update & Refresh** - Update git-sourced bundles

### Agent Delegation
- **US-4.3: Agent Library Management** - Install and manage agent collections
- **US-4.4: Multi-Agent Orchestration** - Coordinate multiple agents working together

### Context & Memory
- **US-5.3: Persistent Memory** - AI remembers across sessions with memory system

### Tools & Capabilities
- **US-6.2: Custom Tool Development** - Create custom tools for domain-specific needs

### Observability
- **US-7.2: Trace Collection & Analysis** - Collect execution traces for analysis

### Performance
- **US-10.1: Smart Caching** - Efficient caching of bundles and modules
- **US-10.2: Parallel Bundle Loading** - Load bundles concurrently for fast startup

---

## Total: 28 User Stories

**Phase 1 (MVP):** 7 stories - ~500 LOC
**Phase 2 (Power User):** 12 stories - ~1,200 LOC total
**Phase 3 (Advanced):** 9 stories - ~2,000 LOC total

**Expected Outcome:** Full-featured CLI in ~1,500-2,000 LOC vs app-cli's ~10,000 LOC (85% reduction)

---

## Implementation Priority

### Must-Have (Week 1)
1. US-1.1: Basic Prompt Execution
2. US-1.2: Multi-Turn Conversations
3. US-3.1: Environment-Based Configuration

### Should-Have (Week 2)
4. US-2.1: Load Provider Bundles
5. US-4.1: Spawn Agent Sub-Sessions
6. US-5.1: @Mention File References
7. US-1.3: Interactive REPL Mode

### Nice-to-Have (Week 3+)
8. US-1.4: Session Persistence & Resumption
9. US-3.2: Config File Support
10. US-3.3: Project-Scoped Configuration
11. Everything else...

---

## Quick Reference: User Story Format

**As a** [user type]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria:**
- [Specific, testable requirements]

**Foundation Pattern:**
```[language]
[Code example showing foundation-based implementation]
```

**Surpasses app-cli:**
- [How this is better/simpler than app-cli]

---

See `USER_STORIES.md` for complete details, acceptance criteria, and implementation patterns.
