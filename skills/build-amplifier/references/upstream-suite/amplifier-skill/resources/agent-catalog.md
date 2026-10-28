# Expert-Agent Routing Guide

Two concerns live in this file:

1. **Expert agents** — authoritative sources for specific domains; route to these when details
   are volatile or you need an authoritative answer.
2. **Dynamic agent discovery** — do not rely on static catalogs; discover agents at runtime.

---

## Expert Agent Directory

| Agent | Domain | When to use |
|-------|--------|-------------|
| `amplifier:amplifier-expert` | Amplifier platform, CLI, module catalog, ecosystem governance | Platform questions, CLI behavior, which repo owns what |
| `core:core-expert` | `amplifier-core` kernel, module contracts, protocol spec | Kernel internals, module protocol compliance, contract questions |
| `foundation:foundation-expert` | `amplifier-foundation` library, bundles, session API, examples | Bundle composition, session lifecycle, Foundation API details |
| `foundation:ecosystem-expert` | Cross-repo architecture, dependency boundaries, release patterns | Questions spanning multiple repos, architectural decisions |

**Rule:** Embed stable mental models in skill content. Route volatile details — API signatures,
release-specific behavior, module resolution edge cases — to these experts rather than guessing.

---

## Dynamic Agent Discovery

Do not rely on static agent catalogs. Discover agents dynamically at runtime,
then fall back to cached bundle manifests.

### Preferred Discovery Flow

1. Runtime discovery:

```bash
amplifier agents list --bundle <bundle-name>
```

2. If runtime is blocked, use the fallback script:

```bash
./scripts/list_agents.sh --bundle <bundle-name>
```

3. For bundle composition context:

```bash
amplifier bundle show <bundle-name>
```

### Why Dynamic Discovery

Amplifier bundles and agent sets change frequently. Static copies drift and become misleading.
Prefer live runtime state. Use expert agents for authoritative guidance.

### Practical Commands

```bash
# List available bundles
amplifier bundle list

# Default/current context discovery
./scripts/list_agents.sh

# Target a specific bundle
./scripts/list_agents.sh --bundle foundation
./scripts/list_agents.sh --bundle recipes
```
