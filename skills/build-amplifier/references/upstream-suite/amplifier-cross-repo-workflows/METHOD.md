> Preserved upstream topic, not a separate installation or current SDK guarantee. Read [current contracts](../../current-contracts.md) before using historical commands/code. The installed Build with Amplifier method governs scope and authority.

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
