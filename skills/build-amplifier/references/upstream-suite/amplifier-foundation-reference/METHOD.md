> Preserved upstream topic, not a separate installation or current SDK guarantee. Read [current contracts](../../current-contracts.md) before using historical commands/code. The installed Build with Amplifier method governs scope and authority.

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
