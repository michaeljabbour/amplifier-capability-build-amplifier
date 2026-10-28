> Preserved source method from `amplifier-skill` at `81dc45815b65ec9c2dcef7c89750acba5fb72119`. Original examples and runtime claims are historical; the canonical entry point defines current scope.

---
name: amplifier-skill
description: Delegate complex work to Microsoft Amplifier from coding assistants. Use when users explicitly ask to use Amplifier, delegate to Amplifier, inspect Amplifier history/context, or discover Amplifier agents and bundles. Prefer conservative delegation and use CLI-first discovery with filesystem fallbacks in restricted environments.
---

# Amplifier Skill

Delegate only on explicit Amplifier intent and keep simple local work local.

## Workflow

### 1. Run preflight checks

Verify Amplifier is available before delegating:

```bash
command -v amplifier
amplifier --help
amplifier provider current
```

If provider state is missing or invalid, instruct:

```bash
amplifier init
```

### 2. Decide whether to delegate

Delegate when the user is explicit about Amplifier, for example:
- "use Amplifier"
- "delegate to Amplifier"
- "show Amplifier context/history"
- "what agents does Amplifier have?"

Keep local when the task is a quick edit, simple shell command, obvious fix, or routine repo search.

When intent is ambiguous, ask one short clarification instead of auto-delegating.

### 3. Delegate tasks to Amplifier

Use single-shot delegation:

```bash
amplifier run "<task description>"
```

Use multi-turn delegation:

```bash
amplifier
amplifier continue
amplifier session resume <session-id>
```

Use optional targeting only when the user asks:

```bash
amplifier run --bundle <bundle-name> "<task description>"
amplifier run --provider <provider-name> "<task description>"
```

### 4. Query session context safely

Use the helper script first:

```bash
./scripts/session_context.sh --project "$PWD" --limit 10
./scripts/session_context.sh --all-projects --limit 10
```

The script uses `amplifier session list` first, then falls back to
`~/.amplifier/projects/**/metadata.json` parsing when runtime access is blocked.

### 5. Discover agents without hardcoding catalogs

Use the helper script first:

```bash
./scripts/list_agents.sh
./scripts/list_agents.sh --bundle foundation
```

The script tries runtime commands first, then parses cached manifests under
`~/.amplifier/cache/*/bundle.md`.

For bundle-level inspection:

```bash
amplifier bundle list
amplifier bundle current
amplifier bundle show <bundle-name>
```

### 6. Handle failure modes

If `amplifier` is missing, instruct installation:

```bash
uv tool install git+https://github.com/microsoft/amplifier
```

If runtime commands fail in sandboxed/restricted sessions, keep moving with the helper script fallbacks and summarize what data was available.

If no sessions or agents are found, return a clear empty-state response and next command to run.

## Guardrails

- Delegate conservatively: explicit intent only.
- Avoid stale hardcoded model, bundle, or agent lists.
- Prefer dynamic discovery over static documentation snapshots.
- Summarize Amplifier output and next steps after delegation completes.
