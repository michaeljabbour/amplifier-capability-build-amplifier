---
name: amplifier-ecosystem-router-codex
description: Front door for the Amplifier ecosystem skill suite. Routes tasks by repo, layer, and intent to the right companion skill, docs, and expert agent. Use this first for any Amplifier ecosystem question.
---

# Amplifier Ecosystem Router (Codex)

Start here. Answer three questions, then follow the routing table.

1. **Which repo is involved?**
2. **Which layer is this?**
3. **What kind of task is this?**

---

## Quick Routing Table

| Task type | Go here |
|-----------|---------|
| Delegating work to Amplifier from an AI agent (Manus, Claude Code, Cursor, Copilot) | Stay here — see Delegation Workflow below |
| Building an app on Amplifier (web, CLI, Slack, voice) | `amplifier-app-integration` skill + `APPLICATION_INTEGRATION_GUIDE.md` |
| Creating or modifying a runtime module | `amplifier-module-and-bundle-development` skill + `MODULES.md` + `MODULE_DEVELOPMENT.md` |
| Authoring or updating a bundle | `amplifier-module-and-bundle-development` skill + `BUNDLE_GUIDE.md` |
| Understanding kernel, sessions, hooks, module types | `amplifier-core-concepts` skill + `CONCEPTS.md` |
| Working across multiple repos safely | `amplifier-cross-repo-workflows` skill |
| Learning from Foundation examples | `amplifier-foundation-reference` skill + `amplifier-foundation/examples/` |
| Foundation docs (patterns, API, concepts) | `amplifier-foundation-reference` skill + `amplifier-foundation/docs/` |

---

## Repo and Layer Classification

**Which repo are you in?**

| Repo | What it owns | Expert agent |
|------|-------------|--------------|
| `amplifier` | Entry point, CLI wrapper, docs, module catalog | `amplifier:amplifier-expert` |
| `amplifier-core` | Ultra-thin kernel, module contracts, protocol definitions | `core:core-expert` |
| `amplifier-foundation` | Library layer: bundles, app integration, session API, examples | `foundation:foundation-expert` |
| `amplifier-app-cli` | Reference CLI app — the real end-to-end validation surface | `foundation:ecosystem-expert` |
| `amplifier-desktop` | Desktop app bundle surface (uses `superpowers` app bundle) | `foundation:ecosystem-expert` |

**Architectural boundary rule:** Runtime modules depend only on `amplifier-core`. They never import from `amplifier-foundation`. Libraries (`amplifier-foundation`) are consumed by applications (`amplifier-app-cli`), not by modules.

---

## Expert Agent Directory

Route to these when details are volatile, authoritative, or cross-repo:

| Need | Agent |
|------|-------|
| Authoritative Amplifier platform guidance | `amplifier:amplifier-expert` |
| Kernel contracts, module protocol spec | `core:core-expert` |
| Foundation library, bundles, session API | `foundation:foundation-expert` |
| Cross-ecosystem architecture and governance | `foundation:ecosystem-expert` |
| TDD, plan writing, design validation | `superpowers:implementer`, `superpowers:spec-reviewer` |
| Memory, context retrieval, knowledge graphs | `mempalace:archivist`, `mempalace:curator` |

---

## Delegation Workflow

Use when the user explicitly asks to delegate to Amplifier, inspect Amplifier history, or discover agents.

**Rule:** Delegate on explicit intent only. Keep quick edits, simple shell commands, and obvious fixes local.

### 1. Preflight & Setup

Ensure Amplifier is installed in the environment (e.g., `~/.local/bin` for `uv` installs).

```bash
export PATH="$HOME/.local/bin:$PATH"
command -v amplifier
amplifier provider current
```

If missing, install:
```bash
uv tool install git+https://github.com/microsoft/amplifier
```

If provider state is missing: `amplifier init` (or manually configure `~/.amplifier/settings.yaml` in non-interactive sandboxes like Manus).

### 2. Delegate

```bash
# Single-shot (Best for Manus/Autonomous Agents)
amplifier run "<task description>"

# Interactive (Best for Claude Code/Terminal)
amplifier
amplifier continue
amplifier session resume <session-id>

# Optional targeting (only when user asks)
amplifier run --bundle <bundle-name> "<task>"
amplifier run --provider <provider-name> "<task>"
```

### 3. Query session context safely

```bash
./scripts/session_context.sh --project "$PWD" --limit 10
./scripts/session_context.sh --all-projects --limit 10
```

Falls back to `~/.amplifier/projects/**/metadata.json` when CLI is blocked.

### 4. Discover agents without hardcoding

```bash
./scripts/list_agents.sh
./scripts/list_agents.sh --bundle foundation
```

Falls back to `~/.amplifier/cache/*/bundle.md` manifests when CLI is blocked.

### 5. Memory & Context Awareness

If the user asks to use the memory bundle or maintain long-term context:
```bash
amplifier run --bundle memory "<task>"
```
This enables the `mempalace` integration (`hooks-mempalace-briefing`, `hooks-project-context`, etc.) for persistent state.

---

## Guardrails

- Delegate on explicit intent only. When intent is ambiguous, ask one short clarification.
- Never hardcode bundle or agent lists — use runtime discovery.
- When details are volatile or authoritative clarification is needed, route to docs or an expert agent; do not guess.
- After delegation completes, summarize Amplifier output and recommend next steps.
