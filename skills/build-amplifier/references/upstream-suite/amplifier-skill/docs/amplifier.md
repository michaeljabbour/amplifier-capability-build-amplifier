# Amplifier Ecosystem Router — Quick Reference

Command cheatsheet and routing summary for the router skill.
For full routing logic, see [preserved router](../METHOD.md).

---

## Suite Routing Cheatsheet

| Task | Companion skill |
|------|----------------|
| App embedding / integration | `amplifier-app-integration` |
| Module authoring | `amplifier-module-and-bundle-development` |
| Bundle authoring | `amplifier-module-and-bundle-development` |
| Core concepts (kernel, hooks, sessions) | `amplifier-core-concepts` |
| Cross-repo workflows | `amplifier-cross-repo-workflows` |
| Foundation examples and docs | `amplifier-foundation-reference` |

---

## Install and Setup

```bash
uv tool install git+https://github.com/microsoft/amplifier
amplifier init
```

## Preflight

```bash
command -v amplifier
amplifier --help
amplifier provider current
amplifier bundle current
```

## Delegate Work

```bash
# Single-shot delegation
amplifier run "Review this codebase for security issues"

# Interactive delegation
amplifier
amplifier continue
amplifier session resume <session-id>

# Optional targeting (only when user asks)
amplifier run --bundle foundation "Analyze architecture tradeoffs"
amplifier run --provider provider-anthropic "Compare two designs"
```

## Sessions

```bash
amplifier session list -n 10
amplifier session list --project /abs/path/to/repo -n 10
amplifier session list --all-projects -n 10
amplifier session show <session-id>
```

## Agent and Bundle Discovery

```bash
amplifier bundle list
amplifier bundle show <bundle-name>
amplifier agents list --bundle <bundle-name>

# Fallback scripts (use when CLI is blocked)
./scripts/list_agents.sh --bundle foundation
./scripts/session_context.sh --project "$PWD" --limit 10
```

## Expert Agents

```bash
# Route to these for authoritative or volatile details
amplifier:amplifier-expert      # platform questions
core:core-expert                # kernel contracts
foundation:foundation-expert    # bundles, session API, foundation library
foundation:ecosystem-expert     # cross-repo architecture
```

## Troubleshooting

### `amplifier: command not found`
```bash
uv tool install git+https://github.com/microsoft/amplifier
which amplifier
```

### Provider not configured
```bash
amplifier init
```

### Runtime blocked (sandboxed environment)
```bash
./scripts/session_context.sh --all-projects --limit 10
./scripts/list_agents.sh
```

### Multiple binaries on PATH
```bash
which -a amplifier
```

---

## Canonical Sources

- [amplifier — MODULES.md](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md)
- [amplifier — MODULE_DEVELOPMENT.md](https://github.com/microsoft/amplifier/blob/main/docs/MODULE_DEVELOPMENT.md)
- [amplifier-foundation — BUNDLE_GUIDE.md](https://github.com/microsoft/amplifier-foundation/blob/main/docs/BUNDLE_GUIDE.md)
- [amplifier-foundation — APPLICATION_INTEGRATION_GUIDE.md](https://github.com/michaeljabbour/amplifier-foundation/blob/main/docs/APPLICATION_INTEGRATION_GUIDE.md)
- [amplifier-foundation — CONCEPTS.md](https://github.com/microsoft/amplifier-foundation/blob/main/docs/CONCEPTS.md)
- [amplifier-foundation — examples/](https://github.com/microsoft/amplifier-foundation/tree/main/examples)
