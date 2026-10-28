> Preserved upstream topic, not a separate installation or current SDK guarantee. Read [current contracts](../../current-contracts.md) before using historical commands/code. The installed Build with Amplifier method governs scope and authority.

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
