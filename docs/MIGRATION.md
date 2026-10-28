# Consolidation and compatibility map

Primary source: `amplifier-skill` at `81dc45815b65ec9c2dcef7c89750acba5fb72119`. Its Git history, native code and evaluation assets remain. Original personal working copies were not edited. The public repository has not been renamed or archived. Eventual publication should rename the primary owner repository to `amplifier-skill-build-amplifier`, preserving its history and redirects; this local name is not a live URL.

## Canonical portable entry

`skills/build-amplifier/SKILL.md` is the installable front door. Older topic entrypoints become preserved rich references; consumers should load the canonical entry and select the named mode/reference. This is a staged compatibility migration, not deletion of the source method. Native namespace/engine identities stay as originally registered.

| Original path | Current path | Role |
|---|---|---|
| `SKILL.md` | `skills/build-amplifier/references/delegation/METHOD.md` | Preserved source method; reached from canonical entry. |

Original examples/claims are retained as source evidence, not new benchmark claims. Distinct native methods and engines are not flattened into one generic checklist. Review all downstream consumers before retiring a secondary repository.

## Secondary source routes

- `amplifier-cli-skill` at `6904eca0980767cff8d3c70033839f6c1535dffc`: Secondary method/reference consolidation. Original source identity and history retained. Paths: `LICENSE`, `skills/amplifier-cli-skill/SKILL.md`, `skills/amplifier-cli-skill/references/ARCHITECTURE.md`, `skills/amplifier-cli-skill/references/ARCHITECTURE_FLOWS.md`, `skills/amplifier-cli-skill/references/BUILD_PATTERNS.md`, `skills/amplifier-cli-skill/references/CONTRIBUTING.md`, `skills/amplifier-cli-skill/references/CUSTOM_EXTENSIONS.md`, `skills/amplifier-cli-skill/references/EXAMPLES.md`, `skills/amplifier-cli-skill/references/HOOKS.md`, `skills/amplifier-cli-skill/references/MEMORY.md`, `skills/amplifier-cli-skill/references/README.md`, `skills/amplifier-cli-skill/references/REFERENCE_IMPLEMENTATION_HISTORY.md`, `skills/amplifier-cli-skill/references/TROUBLESHOOTING.md`.
- `amplifier-skill-codex` at `8559d311e635c3d2f85b51862ce43575a5014a61`: Secondary method/reference consolidation. Original source identity and history retained. Paths: `SKILL.md`.

Secondary ancestry is retained in merge commits using an ours strategy; selected procedures/contracts are imported deliberately, rather than overlaying unrelated engine trees. No original repository has been removed.

## Current public source reconciliation

The original local base lagged public main. Public commit `4beb46c0937ec9806960b5425be9ccd3ddc47533` is merged normally. Each of the six topic directories now lives under `skills/build-amplifier/references/upstream-suite/<original-topic>/`; its complete original `SKILL.md` body is generated as `METHOD.md` with an authority/version notice. Scripts/assets move with the router; nested helper paths forward to the repaired canonical helper implementation. `scripts/sync_upstream_suite.py --check` pins source/output bytes. Original source bodies and commits remain in Git history.

The upstream source README is retained with mapped local links in [UPSTREAM-SUITE.md](UPSTREAM-SUITE.md); original plan history and shell checks remain. The shell checks now exercise installed canonical helpers and use isolated `AMPLIFIER_HOME`, without overriding the user home. Current-contract notes identify the source examples’ historical Core/Foundation import, behavior composition and persistence assumptions; those examples are preserved, not asserted as current working APIs. No topic body, original asset content or source history was discarded. Only discoverable entry filenames and compatibility helper wrappers changed.
