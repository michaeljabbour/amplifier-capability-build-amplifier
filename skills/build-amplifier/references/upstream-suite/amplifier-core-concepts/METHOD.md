> Preserved upstream topic, not a separate installation or current SDK guarantee. Read [current contracts](../../current-contracts.md) before using historical commands/code. The installed Build with Amplifier method governs scope and authority.

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
