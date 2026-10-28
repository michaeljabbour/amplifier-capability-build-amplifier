---
name: build-amplifier
description: Use when adding an Amplifier capability, composing a client, or debugging the boundary between Foundation and Core.
license: MIT
---

# Build with Amplifier

Build the extension in the right place, against the current contracts.

## Start with the seam

Inspect the actual host's manifests, source, extension protocol, and tests. Record versions or commit IDs. Ask what must change: app interaction, reusable composition, a callable operation, event observation/control, model access, context policy, or execution policy. Prefer the existing seam that owns that responsibility. A bundle wires capabilities; it does not replace Core. Foundation resolves/composes/prepares bundles; the host's Core protocol owns execution. Check this against the installed source, not a remembered catalog.

## Place → build → prove

1. State the user's observable outcome and one failure case. Locate the host's current contract and a neighboring implementation. Explain why config alone is sufficient or why code is needed.
2. Write a boundary table: inputs, output/result schema, failure semantics, lifecycle/cleanup, permissions, and owner. Keep credentials in the host's existing provider configuration.
3. Build one vertical slice in an isolated branch. Compose only needed modules; preserve the host's provider/session configuration. Avoid wrapping Foundation APIs solely to rename them.
4. Test mount/registration, a successful call, invalid input, cancellation, and cleanup using the host's actual test doubles or runtime. A fake-provider result proves integration plumbing only.
5. Run the host's normal checks. If live execution is warranted and already authorized, use one bounded test with explicit input/output limits. Record the exact command, source versions, result, and what remains untested.
6. Hand over a native install command and rollback. Do not claim persistence because a session ID was saved: distinguish metadata, current session state, and durable resumption.

## Choose the reference deliberately

[Current contract caveats](references/current-contracts.md) distinguish preserved source examples from verified installed APIs. The six substantial topics from the current public suite remain available behind this one entry:

| Need | Preserved topic |
|---|---|
| Classify repo, layer, intent and delegation | [Ecosystem router](references/upstream-suite/amplifier-skill/METHOD.md) |
| Kernel, module types, hooks and session concepts | [Core concepts](references/upstream-suite/amplifier-core-concepts/METHOD.md) |
| Author a module or compose a capability | [Module and bundle development](references/upstream-suite/amplifier-module-and-bundle-development/METHOD.md) |
| Navigate Foundation patterns and examples | [Foundation reference](references/upstream-suite/amplifier-foundation-reference/METHOD.md) |
| Embed runtime behind an application boundary | [Application integration](references/upstream-suite/amplifier-app-integration/METHOD.md) |
| Order changes and validate across repos | [Cross-repo workflows](references/upstream-suite/amplifier-cross-repo-workflows/METHOD.md) |

[CLI and Foundation patterns](references/cli/METHOD.md) retain the original substantial authoring guide and its architecture, hooks, build, and troubleshooting references. Those examples are historical patterns, not verified current SDK signatures. [Runtime delegation](references/delegation/METHOD.md) preserves the separate explicit-intent workflow. Optional helper scripts are installed in `scripts/`; use `sh scripts/list_agents.sh --help` or `sh scripts/session_context.sh --help` from the installed skill folder. Cached agent/session listings are dated evidence and can be stale. Do not print private transcripts or credentials.

For delegation, first inspect `amplifier --help` and provider/bundle state. Run only the task the user asked to delegate; report start/completion/error evidence separately. There is no requirement to delegate a local edit simply because this skill is installed.

## Completion

Return the seam decision, changed paths, inspected contracts, exact checks, live-versus-fake evidence, remaining blockers, and local install/rollback. Never count a copied API example or packaging check as a working extension.
