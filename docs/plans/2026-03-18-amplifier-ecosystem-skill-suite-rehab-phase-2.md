# Amplifier Ecosystem Skill Suite Rehab — Phase 2: Companion Skills

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Replace the five companion skill stubs created in Phase 1 with complete, substantive SKILL.md files covering their respective canonical sources.

**Architecture:** Each companion skill embeds stable mental models and routes volatile details to authoritative docs and expert agents. All five skills follow the same structural pattern: what it's for → when to use it → canonical sources → workflow/checklist → common mistakes to avoid. Phase 1 must be complete before starting Phase 2.

**Tech Stack:** Markdown skill files, git.

---

## Prerequisites

Phase 1 complete. All five stub directories exist:

```bash
cd /Users/michaeljabbour/dev/amplifier-skill
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  [ -f "$dir/SKILL.md" ] && echo "$dir: OK" || echo "$dir: MISSING — run Phase 1 first"
done
```

Expected: all five show `OK`.

---

### Task 1: Write `amplifier-cross-repo-workflows` Skill

**Files:**
- Modify: `amplifier-cross-repo-workflows/SKILL.md`

**Step 1: Read the current stub**

```bash
cat -n amplifier-cross-repo-workflows/SKILL.md
```

Expected: stub content with "STUB — Phase 2 will fill this."

**Step 2: Write the full skill content**

Replace the entire file with:

```markdown
---
name: amplifier-cross-repo-workflows
description: Safe execution workflows for the Amplifier ecosystem spanning multiple repos. Covers dependency hierarchy, change order, testing ladder, local override, shadow environments, and why amplifier-app-cli is the real end-to-end validation surface.
---

# Amplifier Cross-Repo Workflows

Use this skill when your work touches more than one Amplifier repo, or when you need to
understand how the repos fit together before making a change.

## What This Skill Is For

- Knowing which repo to change first when a fix spans multiple repos
- Understanding the testing ladder (when is library-level testing not enough?)
- Setting up local module overrides without modifying installed packages
- Using shadow environments for safe local ecosystem testing
- Knowing when `amplifier-app-cli` must be part of your validation

## Canonical Sources

- [`amplifier/docs/MODULE_DEVELOPMENT.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULE_DEVELOPMENT.md) — Authoritative module development workflows, workspace patterns, env var overrides
- [`amplifier/docs/MODULES.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) — Component catalog and repo roles

Expert agents for volatile details:
- `amplifier:amplifier-expert` — CLI and module tooling behavior
- `foundation:ecosystem-expert` — Cross-repo architecture questions

---

## Repo Dependency Hierarchy

```
amplifier-core              ← ultra-thin kernel; defines protocols/contracts only
    ↑
amplifier-foundation        ← library layer; builds on core; used by applications
    ↑
amplifier-app-cli           ← reference CLI app; the real end-to-end surface
    ↑
amplifier                   ← entry-point wrapper; installs amplifier-app-cli
```

**Architectural boundary:** Runtime modules depend only on `amplifier-core`. They never
import `amplifier-foundation`. The foundation library is for application-layer code only.

---

## Change and Push Order

When a change spans multiple repos, make changes bottom-up, validate bottom-up, push bottom-up.

```
1. amplifier-core        ← change the contract first
2. amplifier-foundation  ← update library to satisfy new contract
3. amplifier-app-cli     ← validate end-to-end in the real app
4. amplifier             ← update entry-point / docs if needed
5. affected modules      ← update runtime modules to satisfy new contracts
```

**Never push a foundation or app-cli change before the core change it depends on is merged.**

---

## Testing Ladder

| Level | Command | When it is enough |
|-------|---------|------------------|
| Module unit tests | `uv run pytest` in the module repo | Isolated logic changes |
| Bundle integration | `amplifier run --bundle test-bundle.md "test"` | Bundle composition, tool interactions |
| App-CLI end-to-end | `amplifier run "<real task>"` in a project | Cross-module behavior, hook interactions, session flow |
| Shadow environment | `amplifier bundle use shadow` + `amplifier run` | Risky changes, OS-level isolation |

**Rule:** Stop at the lowest level that actually exercises the change. But if the change
touches session lifecycle, hook integration, context flow, or provider routing — go to app-cli.

---

## Local Module Override

Override a module without touching installed packages. The override clears when the terminal closes.

### Single-module override (env var)

```bash
# Clone the module you are working on
git clone https://github.com/microsoft/amplifier-module-tool-bash
cd amplifier-module-tool-bash

# Point Amplifier at your local version
export AMPLIFIER_MODULE_TOOL_BASH=$(pwd)

# Test in your project
cd ~/my-project
amplifier run "test bash tool changes"
```

The env var name is always `AMPLIFIER_MODULE_<MODULE_ID_UPPERCASE_UNDERSCORED>`.

### Multi-module workspace (settings.yaml)

```bash
mkdir ~/amplifier-workspace && cd ~/amplifier-workspace
git clone https://github.com/microsoft/amplifier-module-tool-bash
git clone https://github.com/microsoft/amplifier-module-provider-anthropic

cat > .amplifier/settings.yaml << 'EOF'
sources:
  tool-bash: file://./amplifier-module-tool-bash
  provider-anthropic: file://./amplifier-module-provider-anthropic
EOF

# Changes to either module are used automatically
amplifier run "test multi-module changes"
```

### Workspace convention (auto-discovery)

```bash
mkdir amplifier-workspace && cd amplifier-workspace
git clone https://github.com/microsoft/amplifier-module-tool-bash
# ... clone others as needed

amplifier module dev init
# Creates .amplifier/modules/ symlinks automatically
amplifier module dev status
```

---

## Shadow Environments

The `shadow` bundle creates an OS-level sandbox for testing ecosystem changes safely.
Use it when you need to test changes that touch the installed amplifier binary, module
resolution cache, or provider state without polluting your real environment.

```bash
amplifier bundle use shadow
amplifier run "test risky changes in sandbox"
```

Consult `foundation:ecosystem-expert` or the
[amplifier-bundle-shadow repo](https://github.com/microsoft/amplifier-bundle-shadow)
for the current shadow API — its configuration surface changes.

---

## Why amplifier-app-cli Is the Real Validation Surface

`amplifier-app-cli` is the reference application that exercises the full stack:
- session lifecycle (prepare → create → execute → close)
- tool dispatch and result handling
- hook integration (logging, approval, streaming UI)
- context management across turns
- provider routing and error handling

Library-level tests (unit tests in `amplifier-core` or `amplifier-foundation`) prove
contracts work in isolation. Only `amplifier-app-cli` proves the full integration works
end-to-end with real modules, real hooks, and real provider calls.

**Practical rule:** If you are unsure whether your change is validated, run it through
`amplifier-app-cli` with a real task before pushing.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Pushing foundation changes before core changes are merged | Follow the bottom-up push order |
| Stopping at unit tests for cross-module changes | Go to app-cli end-to-end validation |
| Hardcoding module source URLs instead of using overrides | Use env var overrides or workspace convention |
| Modifying the installed amplifier binary directly | Use shadow environments or local workspace |
| Forgetting that library code (amplifier-foundation) must not be imported by runtime modules | Check your module's pyproject.toml — only `amplifier-core` as a dependency |
```

**Step 3: Verify the file was written correctly**

```bash
grep -c "amplifier-app-cli\|amplifier-core\|amplifier-foundation" amplifier-cross-repo-workflows/SKILL.md
```

Expected: at least `5` matches (multiple references to each repo).

```bash
grep "^name:" amplifier-cross-repo-workflows/SKILL.md
```

Expected: `name: amplifier-cross-repo-workflows`

**Step 4: Commit**

```bash
git add amplifier-cross-repo-workflows/SKILL.md
git commit -m "feat: write amplifier-cross-repo-workflows companion skill"
```

---

### Task 2: Write `amplifier-core-concepts` Skill

**Files:**
- Modify: `amplifier-core-concepts/SKILL.md`

**Step 1: Read the current stub**

```bash
cat -n amplifier-core-concepts/SKILL.md
```

**Step 2: Write the full skill content**

Replace the entire file with:

```markdown
---
name: amplifier-core-concepts
description: Core Amplifier concepts — kernel architecture, five module types, orchestrators as the main engine, session lifecycle, hooks and events, tool-vs-hook distinction, and kernel-vs-module philosophy.
---

# Amplifier Core Concepts

Use this skill when you need to understand how Amplifier is structured before making a change,
implementing a module, or debugging unexpected session behavior.

## What This Skill Is For

- Understanding the kernel's role vs a module's role
- Knowing the five module types and when to use each
- Understanding the session execution lifecycle
- Knowing the difference between a tool and a hook
- Understanding what amplifier-core defines vs what modules implement

## Canonical Sources

- [`amplifier-foundation/docs/CONCEPTS.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/CONCEPTS.md) — Bundle model, mount plan, session lifecycle
- [`amplifier/docs/MODULES.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) — Full module taxonomy with current catalog
- [`amplifier-module-resolution — SPECIFICATION.md`](https://github.com/microsoft/amplifier-module-resolution/blob/main/docs/SPECIFICATION.md) — Module protocol contracts

Expert agents for volatile details:
- `core:core-expert` — Kernel contracts, module protocol compliance
- `foundation:foundation-expert` — Bundle model, session API, Foundation library

---

## The Kernel Philosophy

`amplifier-core` is an ultra-thin kernel. Its entire job is to define **contracts** — the
interfaces that modules must implement. It has almost no implementation of its own.

**What the kernel defines:**
- Module protocol interfaces (Tool, Hook, Orchestrator, Provider, ContextManager)
- Session lifecycle contract (prepare → execute → teardown)
- Module resolution protocol (how modules are found and loaded)
- Coordination contracts (how modules communicate during a session)

**What the kernel does NOT do:**
- Implement any tool behavior
- Connect to any AI provider
- Manage any session state
- Define any bundle composition logic

Everything else is in modules or in `amplifier-foundation` (the library layer for apps).

---

## The Five Module Types

Modules implement the kernel's contracts. There are exactly five types:

| Type | What it does | Key examples |
|------|-------------|--------------|
| **Orchestrator** | Controls the agent execution loop — when to call the model, how to handle tool calls, when to stop | `loop-basic`, `loop-streaming`, `loop-events` |
| **Provider** | Connects to an AI model backend — translates the kernel's messages protocol to a specific API | `provider-anthropic`, `provider-openai`, `provider-gemini`, `provider-mock` |
| **Tool** | Gives the agent a capability it can invoke — the agent calls tools by name with parameters | `tool-filesystem`, `tool-bash`, `tool-web`, `tool-task` |
| **Context Manager** | Manages conversation history — compaction strategy, persistence, retrieval | `context-simple`, `context-persistent` |
| **Hook** | Observes and intercepts session lifecycle events — logging, redaction, approval gates, streaming UI | `hooks-logging`, `hooks-approval`, `hooks-streaming-ui` |

---

## Orchestrators: The Main Engine

The orchestrator is the most important module. It is the execution loop that drives everything else.

An orchestrator's responsibilities:
1. Receive the user prompt
2. Build the message payload for the provider
3. Call the provider to get the model's response
4. Parse the response for tool calls
5. Dispatch tool calls to the registered tools
6. Feed tool results back to the provider
7. Repeat until the model signals completion
8. Return the final response

Orchestrators fire hooks at key lifecycle events. This is what enables streaming UIs,
logging, approval gates, and cost-aware scheduling — the orchestrator doesn't implement
any of that, it just fires events that hooks handle.

**Rule:** If session behavior is unexpected, start by understanding which orchestrator
is loaded and what events it fires.

---

## Session Lifecycle

```
PREPARE  →  load bundle → resolve modules → download from git URLs → return PreparedBundle
CREATE   →  PreparedBundle.create_session(...) → activates modules → returns AmplifierSession
EXECUTE  →  session.execute(prompt) → orchestrator loop → tool dispatch → response
CLOSE    →  session.close() → teardown hooks → release resources
```

**PreparedBundle is the expensive singleton.** `prepare()` downloads modules from git URLs.
Do it once at application startup. `create_session()` is cheap — do it per-request.

**Session ID is persistent identity.** Reusing a session ID across close/recreate lets
context-persistent modules restore history while the configuration changes.

---

## Tool vs Hook

These are often confused. They are fundamentally different:

| | Tool | Hook |
|--|------|------|
| **Who calls it** | The AI model (agent) | The orchestrator (lifecycle events) |
| **When** | When the model decides to use a capability | At fixed lifecycle events (before call, after call, on error, etc.) |
| **Purpose** | Give the agent something it can do | Observe, modify, or intercept the execution flow |
| **Examples** | Read a file, run bash, search the web | Log events, redact secrets, show streaming UI, ask for approval |
| **Return value** | Tool result returned to the model | Hook return can modify or intercept the event |

**Mental model:** Tools are what the agent does. Hooks are what happens around the agent.

---

## Module Resolution

Modules are loaded by the kernel from source URIs at `prepare()` time.

Source types:
- `git+https://github.com/...@main` — Git URL (standard production pattern)
- `file:///path/to/module` — Local path (workspace/settings.yaml pattern)
- `AMPLIFIER_MODULE_<ID>` env var — Development override (clears on terminal close)

Module ID must match the `[project.entry-points."amplifier.modules"]` key in the module's
`pyproject.toml`. If they don't match, the module fails to load.

For module resolution internals and edge cases, consult `core:core-expert` or the
[amplifier-module-resolution SPECIFICATION.md](https://github.com/microsoft/amplifier-module-resolution/blob/main/docs/SPECIFICATION.md).

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Importing `amplifier-foundation` in a runtime module | Modules depend only on `amplifier-core` |
| Confusing tools and hooks | Tools are agent capabilities; hooks observe lifecycle events |
| Putting implementation logic in the kernel | The kernel only defines contracts; implementation belongs in modules |
| Treating orchestrators as interchangeable | Different orchestrators fire different events and have different streaming behavior |
| Calling `prepare()` per request | `prepare()` is expensive — call it once at startup |
```

**Step 3: Verify**

```bash
grep "^name:" amplifier-core-concepts/SKILL.md
```

Expected: `name: amplifier-core-concepts`

```bash
grep "Orchestrator\|Provider\|Tool\|Context Manager\|Hook" amplifier-core-concepts/SKILL.md | grep "|" | wc -l
```

Expected: at least `5` lines (the five module types table rows).

**Step 4: Commit**

```bash
git add amplifier-core-concepts/SKILL.md
git commit -m "feat: write amplifier-core-concepts companion skill"
```

---

### Task 3: Write `amplifier-module-and-bundle-development` Skill

**Files:**
- Modify: `amplifier-module-and-bundle-development/SKILL.md`

**Step 1: Read the current stub**

```bash
cat -n amplifier-module-and-bundle-development/SKILL.md
```

**Step 2: Write the full skill content**

Replace the entire file with:

```markdown
---
name: amplifier-module-and-bundle-development
description: Module and bundle authoring for the Amplifier ecosystem. Canonical home for MODULES.md, MODULE_DEVELOPMENT.md, and BUNDLE_GUIDE.md guidance. Covers module creation, bundle composition, the thin bundle pattern, and common authoring mistakes.
---

# Amplifier Module and Bundle Development

Use this skill when creating a new runtime module, authoring a bundle, or figuring out
the correct structure for either.

## What This Skill Is For

- Creating a new runtime module (tool, hook, orchestrator, context manager, provider)
- Authoring or updating a bundle
- Understanding module vs bundle vs agent distinctions
- Getting the thin bundle pattern right
- Avoiding the most common authoring mistakes

## Canonical Sources

- [`amplifier/docs/MODULES.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) — Full component catalog; current list of all modules, bundles, and applications
- [`amplifier/docs/MODULE_DEVELOPMENT.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULE_DEVELOPMENT.md) — Complete module development workflows and workspace patterns
- [`amplifier-foundation/docs/BUNDLE_GUIDE.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/BUNDLE_GUIDE.md) — Authoritative bundle authoring guide with full examples

Also load the `creating-amplifier-modules` skill (available in this suite's skill tool)
for the mount() contract and protocol compliance validation specifics.

Expert agents:
- `amplifier:amplifier-expert` — module tooling, CLI behavior, module catalog questions
- `foundation:foundation-expert` — bundle composition, Foundation API details
- `core:core-expert` — module protocol compliance, kernel contracts

---

## Module vs Bundle vs Agent vs Behavior

| Concept | What it is | Where it lives |
|---------|-----------|---------------|
| **Module** | Python package implementing a kernel protocol (Tool, Hook, Orchestrator, Provider, ContextManager) | Its own git repo, e.g. `amplifier-module-tool-bash` |
| **Bundle** | Markdown+YAML configuration file that assembles modules, instructions, agents, and spawn policy into a composable unit | Its own git repo (no `pyproject.toml` required) or inline file |
| **Agent** | A named configuration within a bundle — specific instructions, provider, tools, and spawn policy for a sub-task | YAML section inside a bundle's frontmatter |
| **Behavior** | A lightweight bundle that provides only an instruction overlay — no tools, no orchestrator; composed on top of a base bundle | Usually a subdirectory inside a bundle repo |

**Key insight:** A bundle is configuration, not a Python package.
A module is a Python package. Do not confuse them.

---

## Module Taxonomy (from MODULES.md)

The Amplifier ecosystem has five architectural layers:

| Layer | What it contains |
|-------|-----------------|
| **Core infrastructure** | `amplifier-core` — the kernel |
| **Applications** | `amplifier`, `amplifier-app-cli`, `amplifier-app-log-viewer` |
| **Libraries** | `amplifier-foundation` — consumed by applications, not by modules |
| **Bundles** | Composable config packages — `recipes`, `foundation`, `shadow`, `superpowers`, etc. |
| **Runtime modules** | Orchestrators, providers, tools, context managers, hooks |

For the current catalog of all components, read `MODULES.md` directly or ask
`amplifier:amplifier-expert`. The catalog is volatile — components are added frequently.

---

## Creating a New Module

### Quick start

```bash
# Recommended: use the template generator
amplifier module dev create tool-myfeature

# Or manually
mkdir amplifier-module-tool-myfeature && cd amplifier-module-tool-myfeature
uv init --lib
```

### Required pyproject.toml structure

```toml
[project]
name = "amplifier-module-tool-myfeature"
requires-python = ">=3.11"
dependencies = ["amplifier-core"]       # ← only amplifier-core, never amplifier-foundation

[project.entry-points."amplifier.modules"]
tool-myfeature = "amplifier_module_tool_myfeature"   # ← module ID = entry point key

[tool.uv.sources.amplifier-core]
git = "https://github.com/microsoft/amplifier-core"
branch = "main"
```

**The module ID (entry point key) is what you use in bundle frontmatter.**
It must match exactly or module loading will fail silently.

### Implement the protocol

```python
# amplifier_module_tool_myfeature/__init__.py
from amplifier_core.protocols import Tool

class MyFeatureTool(Tool):
    def get_schema(self):
        return {
            "name": "my_feature",
            "description": "Does something useful",
            "input_schema": {
                "type": "object",
                "properties": {"param": {"type": "string"}},
                "required": ["param"]
            }
        }

    async def execute(self, **kwargs):
        return {"result": f"Processed: {kwargs['param']}"}
```

For the `mount()` contract and protocol compliance validation specifics, load the
`creating-amplifier-modules` skill — it covers the exact contracts and common pitfalls.

### Test locally

```bash
# Env var override (clears on terminal close)
export AMPLIFIER_MODULE_TOOL_MYFEATURE=$(pwd)
cd ~/test-project
amplifier run "test my feature"

# Or create a test bundle
cat > test-bundle.md << 'EOF'
---
bundle:
  name: test
  version: 1.0.0
includes:
  - bundle: foundation
tools:
  - module: tool-myfeature
    source: file:///path/to/amplifier-module-tool-myfeature
providers:
  - module: provider-mock
---
Test bundle for tool-myfeature.
EOF
amplifier run --bundle test-bundle.md "test my feature"
```

---

## Authoring a Bundle

### Bundle structure

Bundles are markdown files with YAML frontmatter. A bundle repo does NOT need a root `pyproject.toml`.

```markdown
---
bundle:
  name: my-bundle
  version: 1.0.0

includes:
  - bundle: foundation           # inherit foundation's tools, orchestrator, hooks

agents:
  my-agent:
    instructions: "..."
    providers:
      - module: provider-anthropic

context:
  - path: docs/
    description: "Project documentation"
---

# My Bundle

System instructions for the agent go here in the markdown body.
```

### The Thin Bundle Pattern (recommended)

Most bundles should be thin — inherit from foundation and add only their unique capabilities.

```markdown
---
# ✅ GOOD: thin bundle
bundle:
  name: my-bundle
  version: 1.0.0

includes:
  - bundle: foundation     # foundation provides: orchestrator, context, tools, hooks

agents:
  my-expert:
    instructions: "You are an expert in X..."
---

System prompt goes here.
```

**Do NOT redeclare what foundation already provides:**

```markdown
---
# ❌ BAD: fat bundle duplicating foundation
includes:
  - bundle: foundation

session:                    # ← foundation already defines this
  orchestrator:
    module: loop-streaming
    source: git+https://...

tools:                      # ← foundation already has these
  - module: tool-filesystem
    source: git+https://...
  - module: tool-bash
    source: git+https://...

hooks:                      # ← foundation already has these
  - module: hooks-streaming-ui
    source: git+https://...
---
```

Fat bundles create maintenance burden, version conflicts, and miss foundation updates
automatically. When in doubt: include foundation, then add only what is unique to your bundle.

### Bundle composition merge rules

| Section | Merge rule |
|---------|-----------|
| `session` | Deep merge — nested dicts are merged, not replaced |
| `providers` | Merge by module ID — same ID updates config, new ID adds to list |
| `tools` | Merge by module ID |
| `hooks` | Merge by module ID |
| `spawn` | Deep merge — later overrides earlier |
| `instruction` | Replace — later wins entirely |

---

## Module Development Workflows

### Quick fix (single module)

```bash
git clone https://github.com/microsoft/amplifier-module-tool-bash
cd amplifier-module-tool-bash
# ... make changes ...
export AMPLIFIER_MODULE_TOOL_BASH=$(pwd)
cd ~/test-project && amplifier run "test bash changes"
cd - && git commit -am "fix: ..." && git push
```

### Multi-module workspace

```bash
mkdir ~/amplifier-workspace && cd ~/amplifier-workspace
git clone https://github.com/microsoft/amplifier-module-tool-bash
git clone https://github.com/microsoft/amplifier-module-provider-anthropic
cat > .amplifier/settings.yaml << 'EOF'
sources:
  tool-bash: file://./amplifier-module-tool-bash
  provider-anthropic: file://./amplifier-module-provider-anthropic
EOF
```

### Module dev CLI

```bash
amplifier module dev init      # initialize workspace, create symlinks
amplifier module dev link <id> # link a specific module
amplifier module dev status    # show workspace state
amplifier module dev test <id> # run module's test suite
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding `amplifier-foundation` as a module dependency | Modules depend only on `amplifier-core` |
| Module ID in bundle doesn't match entry point key | Check pyproject.toml `[project.entry-points."amplifier.modules"]` |
| Creating a fat bundle that redeclares foundation's tools/orchestrator/hooks | Use the thin bundle pattern — include foundation, add only unique capabilities |
| Treating bundle as a Python package | Bundles are markdown+YAML config; no `pyproject.toml` needed |
| Pushing a bundle without testing thin composition | Test with `amplifier run --bundle your-bundle.md "test task"` |
| Using a static module catalog | Module catalog is volatile — query `MODULES.md` or `amplifier:amplifier-expert` |
```

**Step 3: Verify**

```bash
grep "^name:" amplifier-module-and-bundle-development/SKILL.md
```

Expected: `name: amplifier-module-and-bundle-development`

```bash
grep "MODULES.md\|MODULE_DEVELOPMENT.md\|BUNDLE_GUIDE.md" amplifier-module-and-bundle-development/SKILL.md | wc -l
```

Expected: at least `3` (all three canonical sources referenced).

**Step 4: Commit**

```bash
git add amplifier-module-and-bundle-development/SKILL.md
git commit -m "feat: write amplifier-module-and-bundle-development companion skill"
```

---

### Task 4: Write `amplifier-foundation-reference` Skill

**Files:**
- Modify: `amplifier-foundation-reference/SKILL.md`

**Step 1: Read the current stub**

```bash
cat -n amplifier-foundation-reference/SKILL.md
```

**Step 2: Write the full skill content**

Replace the entire file with:

```markdown
---
name: amplifier-foundation-reference
description: Heavier reference companion for amplifier-foundation. Distills CONCEPTS.md, PATTERNS.md, APPLICATION_INTEGRATION_GUIDE.md, and the examples directory. The main example-driven teaching asset in the suite.
---

# Amplifier Foundation Reference

Use this skill when you need stable mental models from `amplifier-foundation`: the bundle
model, session API, composition patterns, and the application integration guide. Also use
it to navigate the examples directory.

## What This Skill Is For

- Understanding the Bundle → MountPlan → AmplifierSession lifecycle
- Learning bundle composition patterns and namespace resolution
- Getting oriented in the `amplifier-foundation/examples/` directory
- Understanding `APPLICATION_INTEGRATION_GUIDE.md` before building an app on Amplifier
- Finding the right example for your use case

## Canonical Sources

These are the primary references. Read them for authoritative and up-to-date details:

- [`amplifier-foundation/docs/CONCEPTS.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/CONCEPTS.md) — Bundle model, mount plan, PreparedBundle, @mention resolution, namespace model
- [`amplifier-foundation/docs/PATTERNS.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/PATTERNS.md) — Code patterns with full examples
- [`amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`](https://github.com/michaeljabbour/amplifier-foundation/blob/main/docs/APPLICATION_INTEGRATION_GUIDE.md) — Protocol boundary, session lifecycle, app embedding patterns
- [`amplifier-foundation/examples/`](https://github.com/microsoft/amplifier-foundation/tree/main/examples) — Numbered, runnable examples from hello world to multi-agent systems
- [`amplifier-foundation/docs/BUNDLE_GUIDE.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/BUNDLE_GUIDE.md) — Bundle authoring (see `amplifier-module-and-bundle-development` skill for distilled version)

Expert agents:
- `foundation:foundation-expert` — Foundation library API, bundle model questions
- `foundation:ecosystem-expert` — Cross-repo architecture questions

---

## What amplifier-foundation Is (and Is Not)

`amplifier-foundation` is the **library layer** for applications. It builds on `amplifier-core`
and provides:
- The `Bundle` class and composition engine
- The `PreparedBundle` and `AmplifierSession` wrappers
- Module resolution and download infrastructure
- Reference implementations of common modules (context-simple, context-persistent, etc.)
- The `load_bundle()` and related API functions
- Application integration patterns and examples

**It is NOT for runtime modules.** Runtime modules depend only on `amplifier-core`.
`amplifier-foundation` is consumed by application code (like `amplifier-app-cli`), not by modules.

---

## The Core Lifecycle Model

```
Bundle.to_mount_plan()  →  MountPlan  →  AmplifierSession
```

In practice:

```python
from amplifier_core import load_bundle

# Once at startup — expensive, downloads modules from git
bundle = await load_bundle("./bundle.md")
prepared = await bundle.prepare()

# Per request — cheap
async with prepared.create_session(session_id="session-001") as session:
    response = await session.execute("Hello!")
```

**PreparedBundle is your singleton.** `prepare()` downloads and activates modules.
**Sessions are ephemeral.** `create_session()` is cheap; do it per-request or per-user.

---

## Bundle Composition Rules

Bundles can be composed to layer configuration. The general rule: **later overrides earlier**.

```python
result = base.compose(overlay)  # overlay's values win on conflict
```

| Section | Merge rule |
|---------|-----------|
| `session` | Deep merge |
| `providers` | Merge by module ID |
| `tools` | Merge by module ID |
| `hooks` | Merge by module ID |
| `spawn` | Deep merge |
| `instruction` | Replace — overlay wins entirely |

### Three composition strategies

| Strategy | When to use |
|----------|-------------|
| Declarative (YAML `includes` chain) | Stable configurations that rarely change at runtime |
| Programmatic (Python `compose()`) | Runtime overlays — different config per user, per mode, per environment |
| Hybrid | Base in YAML, runtime adjustments in Python |

---

## @Mention Resolution

Instructions can reference files from composed bundles using `@namespace:path` syntax:

```markdown
See @foundation:context/guidelines.md for guidelines.
```

How it works:
1. When a bundle loads, its `bundle.name` becomes a namespace
2. `PreparedBundle` resolves `@namespace:path` references against the original bundle's path
3. Content is loaded inline

This allows instructions to reference files from any included bundle without knowing
absolute paths. The namespace comes from `bundle.name`, not from the repo URL or directory name.

---

## Examples Directory Navigation

The `amplifier-foundation/examples/` directory has 20+ numbered, runnable examples.
Here is the map — read the example that matches your use case:

| Example | What it demonstrates |
|---------|---------------------|
| `01_hello_world.py` | Minimal AmplifierSession — load, prepare, create, execute |
| `02_custom_configuration.py` | Overriding bundle config at load time |
| `03_custom_tool.py` | Adding a custom tool to an existing bundle |
| `04_load_and_inspect.py` | Inspecting what a bundle contains before running |
| `05_composition.py` | Bundle composition — base + overlay pattern |
| `06_sources_and_registry.py` | Module sources, registry, resolution |
| `07_full_workflow.py` | Complete session lifecycle end-to-end |
| `08_cli_application.py` | CLI app built on Amplifier — how amplifier-app-cli works |
| `09_multi_agent_system.py` | Multi-agent delegation with tool-task |
| `10_meeting_notes_to_actions.py` | Real-world pipeline — document to structured output |
| `11_provider_comparison.py` | Same task across multiple providers |
| `12_approval_gates.py` | hooks-approval for human-in-the-loop confirmation |
| `13_event_debugging.py` | Hooking into events for debugging |
| `14_session_persistence.py` | context-persistent — session history across restarts |
| `17_multi_model_ensemble.py` | Multi-model ensemble via custom routing |
| `18_custom_hooks.py` | Writing a custom hook from scratch |
| `19_github_actions_ci.py` | Running Amplifier in CI with provider-mock |
| `20_calendar_assistant.py` | Full assistant app with approval and streaming |
| `21_bundle_updates.py` | Handling bundle updates and version management |
| `22_custom_orchestrator_routing.py` | Custom orchestrator with model routing |

**If you are building a new application:** start with `08_cli_application.py` and
`07_full_workflow.py`. Then read `APPLICATION_INTEGRATION_GUIDE.md`.

**If you need a custom tool or hook:** start with `03_custom_tool.py` or `18_custom_hooks.py`.

**If you need multi-agent:** start with `09_multi_agent_system.py`.

---

## Key Opinions from the Foundation Docs

These are stable architectural principles worth internalizing:

1. **PreparedBundle is the singleton; sessions are ephemeral.** Never call `prepare()` per-request.
2. **`session_cwd` is critical for non-CLI apps.** Without it, filesystem tools see the server's working directory.
3. **Composition replaces configuration.** Different behavior for different users/modes? Compose a different overlay, don't toggle flags.
4. **Module ID = entry point key.** These must match exactly in `pyproject.toml`.
5. **Bundles are config, not packages.** Bundle repos do not need a `pyproject.toml`.
6. **Foundation is for apps; modules only use core.** Never import amplifier-foundation in a runtime module.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Calling `prepare()` per request | Call it once at startup; it downloads modules |
| Not setting `session_cwd` in web/API apps | Always pass it explicitly |
| Importing amplifier-foundation in a runtime module | Only `amplifier-core` is allowed |
| Namespace confusion (repo name ≠ bundle name) | Namespace comes from `bundle.name` in the YAML frontmatter |
| Reading examples out of order | Start with 01-08 for foundations, then jump to the example matching your use case |
```

**Step 3: Verify**

```bash
grep "^name:" amplifier-foundation-reference/SKILL.md
```

Expected: `name: amplifier-foundation-reference`

```bash
grep "01_hello_world\|08_cli_application\|09_multi_agent" amplifier-foundation-reference/SKILL.md | wc -l
```

Expected: at least `3` (three examples referenced in the navigation table).

**Step 4: Commit**

```bash
git add amplifier-foundation-reference/SKILL.md
git commit -m "feat: write amplifier-foundation-reference companion skill"
```

---

### Task 5: Write `amplifier-app-integration` Skill

**Files:**
- Modify: `amplifier-app-integration/SKILL.md`

**Step 1: Read the current stub**

```bash
cat -n amplifier-app-integration/SKILL.md
```

**Step 2: Write the full skill content**

Replace the entire file with:

```markdown
---
name: amplifier-app-integration
description: How to build applications on top of Amplifier — web apps, CLI tools, voice assistants, Slack bots, background services. Covers the protocol boundary principle, four protocol points, session lifecycle, bundle composition strategies, and why amplifier-app-cli is the validation surface.
---

# Amplifier App Integration

Use this skill when building an application that embeds Amplifier — a web app, Slack bot,
CLI tool, voice assistant, background service, or any other host that runs Amplifier sessions.

## What This Skill Is For

- Understanding the protocol boundary between your app and Amplifier
- Implementing the four protocol points correctly
- Getting the session lifecycle right (prepare vs create vs execute)
- Choosing a bundle composition strategy
- Validating your app through `amplifier-app-cli`

## Canonical Sources

- [`amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`](https://github.com/michaeljabbour/amplifier-foundation/blob/main/docs/APPLICATION_INTEGRATION_GUIDE.md) — The authoritative guide; covers all ten sections in depth
- [`amplifier-foundation/examples/08_cli_application.py`](https://github.com/microsoft/amplifier-foundation/blob/main/examples/08_cli_application.py) — Reference CLI app implementation
- [`amplifier-foundation/examples/07_full_workflow.py`](https://github.com/microsoft/amplifier-foundation/blob/main/examples/07_full_workflow.py) — Complete lifecycle example
- [`amplifier-foundation/examples/12_approval_gates.py`](https://github.com/microsoft/amplifier-foundation/blob/main/examples/12_approval_gates.py) — Human-in-loop approval pattern
- [`amplifier-foundation/examples/20_calendar_assistant.py`](https://github.com/microsoft/amplifier-foundation/blob/main/examples/20_calendar_assistant.py) — Full assistant app with approval and streaming

Expert agents:
- `foundation:foundation-expert` — Foundation library API, session lifecycle questions
- `foundation:ecosystem-expert` — Architecture questions, app-cli as validation surface

---

## The Protocol Boundary Principle

**This is the single most important concept for app integration.**

Your application has its own concerns: HTTP routing, WebSocket management, audio streaming,
Slack events, UI rendering. Amplifier has its concerns: session lifecycle, tool dispatch,
provider management, hooks, context.

These two domains must meet at a **clean boundary** — a thin bridge layer where:
- Application-specific events become Amplifier operations
- Amplifier events become application-specific outputs

Everything on the application side should know nothing about bundles, coordinators, or
tool protocols. Everything on the Amplifier side should know nothing about HTTP, WebSockets,
or Slack.

**Why this matters:**

Applications that ignore this boundary get none of the benefits (hooks, observability,
tool dispatch, session continuity) while paying the complexity cost. Applications that
respect it get:
- **Testability** — mock either side independently
- **Portability** — same Amplifier session behind web, voice, CLI, or Slack
- **Clarity** — know which side to debug when something breaks
- **Evolvability** — swap your web framework without touching Amplifier; swap your orchestrator without touching your web framework

---

## The Four Protocol Points

The boundary is implemented through four protocol points:

| Protocol | Direction | What Your App Provides | Amplifier Invokes It When |
|----------|-----------|------------------------|--------------------------|
| **ApprovalSystem** | Amplifier → App | Implementation of the approval contract | A tool or hook requests human confirmation |
| **DisplaySystem** | Amplifier → App | Implementation of the display contract | An agent wants to show output to the user |
| **StreamingHook** | Amplifier → App | A hook handler forwarding real-time events (content deltas, tool status, errors) | Any session event fires during execution |
| **SpawnCapability** | Amplifier → App | A capability function registered on the coordinator | Any component needs to create a new Amplifier session |

**On SpawnCapability:** This is the general mechanism for creating new sessions from within
existing ones. Agent delegation is one common use, but sessions are also spawned by
orchestrators managing sub-tasks, recipe steps, observer patterns, and any module needing
an isolated execution context.

---

## The Universal Session Lifecycle

Every Amplifier application follows this pattern regardless of app type:

```
1. LOAD     → load_bundle(source)
2. COMPOSE  → bundle.compose(overlays)          # optional
3. PREPARE  → await bundle.prepare()            # expensive — do once at startup
4. CREATE   → await prepared.create_session(...)
5. MOUNT    → coordinator.mount("tools", tool)  # optional, post-creation
6. HOOK     → coordinator.hooks.register(...)   # optional, post-creation
7. EXECUTE  → await session.execute(prompt)
```

### Minimal example

```python
from amplifier_core import load_bundle

# Steps 1-3: Once at startup
bundle = await load_bundle("./bundle.md")
prepared = await bundle.prepare()

# Steps 4-7: Per interaction
session = await prepared.create_session(
    session_id="user-session-001",
    session_cwd="/path/to/user/project",    # ← critical for non-CLI apps
    approval_system=my_approval_impl,
    display_system=my_display_impl,
)
response = await session.execute("Hello, what can you help with?")
```

### What is required vs optional

| Step | Required? | Notes |
|------|-----------|-------|
| Load | Yes | File path, bundle name, or git URI |
| Compose | No | Only for runtime overlays on the base bundle |
| Prepare | Yes | Downloads modules — do once, not per-request |
| Create | Yes | Produces the AmplifierSession |
| Mount | No | For tools not declared in the bundle |
| Hook | No | For app-specific event handling |
| Execute | Yes | Runs the agent loop |

---

## Bundle Composition Strategies

| Strategy | Pattern | When to use |
|----------|---------|-------------|
| **Declarative** | YAML `includes` chain in bundle.md | Stable configs that rarely change at runtime |
| **Programmatic** | Python `bundle.compose(overlay)` | Runtime overlays — different config per user, mode, or environment |
| **Hybrid** | Base in YAML, runtime adjustments in Python | Most production apps |

```python
# Programmatic composition example
base_bundle = await load_bundle("./base-bundle.md")
user_overlay = await load_bundle(f"./bundles/{user.tier}.md")
composed = base_bundle.compose(user_overlay)
prepared = await composed.prepare()
```

---

## Session ID Reuse Pattern

Reuse a session ID across close/recreate cycles to evolve configuration while preserving
context continuity:

```python
# Initial session
session = await prepared.create_session(session_id="user-42")

# Later: tear down, reconfigure, recreate with same ID
await session.close()
session = await prepared_v2.create_session(session_id="user-42")
# Context-persistent module restores history; configuration has changed
```

Useful for: upgrading providers, adding tools mid-conversation, A/B testing orchestrators
without losing user context.

---

## amplifier-app-cli as the Validation Surface

`amplifier-app-cli` is the reference CLI application. It exercises the full integration
stack: session lifecycle, tool dispatch, hook integration, context management, provider
routing.

**Use it to validate your integration when:**
- Your app's behavior differs from what library-level tests predict
- You have unexpected session lifecycle behavior
- Hooks are not firing as expected
- Context is not persisting correctly

```bash
# Run a task through the full stack
amplifier run "test task that exercises your integration concern"

# Run with a specific bundle to isolate a composition issue
amplifier run --bundle ./your-bundle.md "test task"

# Inspect session after the run
amplifier session show <session-id>
```

---

## Common Anti-Patterns

| Anti-pattern | Why it's a problem | Fix |
|-------------|-------------------|-----|
| Calling `prepare()` per request | Downloads modules every time — extremely slow | Call `prepare()` once at startup |
| Not setting `session_cwd` | Filesystem tools see the server's working directory | Always pass `session_cwd` explicitly for web/API apps |
| Bypassing the protocol boundary (direct API calls wrapped in Amplifier labels) | None of the benefits; all of the complexity | Implement the four protocol points properly |
| Toggling flags instead of composing bundles | Configuration drift, harder testing | Use `compose()` for different behaviors |
| Stopping validation at library-level tests | Cross-module integration issues not caught | Validate through `amplifier-app-cli` |
| Treating all orchestrators as equivalent | Different orchestrators fire different events and stream differently | Know which orchestrator your bundle uses and what events it fires |

---

## Where to Go Next

- **Full integration guide (all 10 sections):** Read `APPLICATION_INTEGRATION_GUIDE.md`
- **Working app example:** `amplifier-foundation/examples/08_cli_application.py`
- **Streaming and approval patterns:** `examples/12_approval_gates.py`, `examples/20_calendar_assistant.py`
- **Session persistence:** `examples/14_session_persistence.py`
- **Multi-agent from an app:** `examples/09_multi_agent_system.py`
- **Authoritative architecture guidance:** `foundation:foundation-expert`
```

**Step 3: Verify**

```bash
grep "^name:" amplifier-app-integration/SKILL.md
```

Expected: `name: amplifier-app-integration`

```bash
grep "APPLICATION_INTEGRATION_GUIDE\|protocol boundary\|four protocol" amplifier-app-integration/SKILL.md | wc -l
```

Expected: at least `3`.

**Step 4: Commit**

```bash
git add amplifier-app-integration/SKILL.md
git commit -m "feat: write amplifier-app-integration companion skill"
```

---

### Task 6: Update README Companion Skill Table

**Files:**
- Modify: `README.md`

The README was written in Phase 1 with the correct companion skill table. After Phase 2
the stubs are now real skills — verify that the README table still accurately describes
what each skill does.

**Step 1: Read the current README skill table**

```bash
grep -A 10 "## Skill Suite" README.md
```

**Step 2: Verify the table descriptions match the skill names in frontmatter**

```bash
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  echo "=== $dir ==="
  head -3 "$dir/SKILL.md"
done
```

Expected: each skill has a `name:` that matches its directory name (with hyphens).

**Step 3: Update the README table description for amplifier-foundation-reference**

The Phase 1 README described `amplifier-foundation-reference` as "Foundation docs, examples, and APPLICATION_INTEGRATION_GUIDE.md distilled." Verify this still accurately reflects the skill. If the description looks accurate, no change is needed.

```bash
grep "amplifier-foundation-reference" README.md
```

Expected: one line describing the skill with examples and APPLICATION_INTEGRATION_GUIDE.md mentioned.

**Step 4: Commit if any README changes were needed**

```bash
git status README.md
# If modified:
git add README.md
git commit -m "docs: sync README companion skill descriptions after Phase 2"
# If no changes:
echo "README is accurate — no commit needed"
```

---

### Task 7: Verify Phase 2 Completeness

**Step 1: Check all five skills have real content (not stubs)**

```bash
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  linecount=$(wc -l < "$dir/SKILL.md")
  echo "$dir: $linecount lines"
done
```

Expected: every skill has at least `80` lines (stubs were ~10 lines).

**Step 2: Check all skills have non-stub descriptions in frontmatter**

```bash
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  echo -n "$dir: "
  grep "STUB" "$dir/SKILL.md" && echo "STILL A STUB" || echo "OK"
done
```

Expected: `OK` for all five (no STUB text remaining).

**Step 3: Check all mandatory canonical sources are explicitly referenced**

```bash
echo "=== MODULES.md references ===" 
grep -rl "MODULES.md" amplifier-*/SKILL.md

echo "=== MODULE_DEVELOPMENT.md references ==="
grep -rl "MODULE_DEVELOPMENT.md" amplifier-*/SKILL.md

echo "=== BUNDLE_GUIDE.md references ==="
grep -rl "BUNDLE_GUIDE.md" amplifier-*/SKILL.md

echo "=== APPLICATION_INTEGRATION_GUIDE.md references ==="
grep -rl "APPLICATION_INTEGRATION_GUIDE.md" amplifier-*/SKILL.md
```

Expected:
- `MODULES.md` — referenced in at least `amplifier-module-and-bundle-development` and `amplifier-cross-repo-workflows`
- `MODULE_DEVELOPMENT.md` — referenced in at least `amplifier-module-and-bundle-development`
- `BUNDLE_GUIDE.md` — referenced in at least `amplifier-module-and-bundle-development`
- `APPLICATION_INTEGRATION_GUIDE.md` — referenced in at least `amplifier-app-integration` and `amplifier-foundation-reference`

**Step 4: Check the router skill routes to all five companions by name**

```bash
grep "amplifier-cross-repo-workflows\|amplifier-core-concepts\|amplifier-module-and-bundle\|amplifier-foundation-reference\|amplifier-app-integration" amplifier-skill/SKILL.md | wc -l
```

Expected: at least `5` (one routing entry per companion skill).

**Step 5: Final Phase 2 commit check**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

---

## Phase 2 Acceptance Checklist

- [ ] `amplifier-cross-repo-workflows/SKILL.md` — complete, covers dependency hierarchy, change order, testing ladder, local override, shadow, app-cli validation
- [ ] `amplifier-core-concepts/SKILL.md` — complete, covers kernel, five module types, orchestrators, session lifecycle, tool-vs-hook, module resolution
- [ ] `amplifier-module-and-bundle-development/SKILL.md` — complete, covers MODULES.md, MODULE_DEVELOPMENT.md, BUNDLE_GUIDE.md, thin bundle pattern, common mistakes
- [ ] `amplifier-foundation-reference/SKILL.md` — complete, covers CONCEPTS.md, examples directory navigation, APPLICATION_INTEGRATION_GUIDE overview, key opinions
- [ ] `amplifier-app-integration/SKILL.md` — complete, covers protocol boundary, four protocol points, session lifecycle, composition strategies, app-cli validation
- [ ] All mandatory canonical sources explicitly referenced in appropriate skills
- [ ] No skill still contains "STUB" in its content
- [ ] Working directory clean with all commits made

**Next:** Phase 3 — helper-script validation and final polish.
