> Source README retained from upstream 4beb46c0937ec9806960b5425be9ccd3ddc47533. Its install/CLI commands are historical examples; use the current root install guide and installed host contracts. Local links were mapped to the consolidated references.

# Amplifier Ecosystem Skill Suite

A router-first skill suite for the [Microsoft Amplifier](https://github.com/microsoft/amplifier) ecosystem.
Works with **Manus**, **Claude Code**, **Cursor**, **GitHub Copilot**, **Windsurf**, and any AI coding assistant that supports skills or system prompts.
Start at the router skill. It classifies your task and routes you to the right companion skill,
canonical docs, and expert agent.

## Skill Suite

| Skill | Purpose |
|-------|---------| 
| [`amplifier-skill`](../skills/build-amplifier/references/upstream-suite/amplifier-skill/METHOD.md) | **Entry point.** Routes by repo, layer, and intent. |
| [`amplifier-cross-repo-workflows`](../skills/build-amplifier/references/upstream-suite/amplifier-cross-repo-workflows/METHOD.md) | Dependency hierarchy, change order, testing ladder, local override, shadow, app-cli validation. |
| [`amplifier-core-concepts`](../skills/build-amplifier/references/upstream-suite/amplifier-core-concepts/METHOD.md) | Kernel, five module types, orchestrators, session lifecycle, hooks, tool-vs-hook. |
| [`amplifier-module-and-bundle-development`](../skills/build-amplifier/references/upstream-suite/amplifier-module-and-bundle-development/METHOD.md) | Module and bundle authoring: `MODULES.md`, `MODULE_DEVELOPMENT.md`, `BUNDLE_GUIDE.md`. |
| [`amplifier-foundation-reference`](../skills/build-amplifier/references/upstream-suite/amplifier-foundation-reference/METHOD.md) | Foundation docs, examples, and `APPLICATION_INTEGRATION_GUIDE.md` distilled. |
| [`amplifier-app-integration`](../skills/build-amplifier/references/upstream-suite/amplifier-app-integration/METHOD.md) | Building apps on Amplifier. Protocol boundary, session lifecycle, app-cli as proof surface. |

## Install

### 1. Install Amplifier

```bash
uv tool install git+https://github.com/microsoft/amplifier
amplifier init
```

### 2. Install the Router Skill

**Claude Code:**

```bash
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-skill/SKILL.md
```

**Manus (Autonomous Agents):**

Copy the skill file into the Manus skills directory:
```bash
mkdir -p ~/skills/amplifier-ecosystem-router
curl -o ~/skills/amplifier-ecosystem-router/SKILL.md \
  https://raw.githubusercontent.com/michaeljabbour/amplifier-skill/main/amplifier-skill/SKILL.md
```

**Cursor / Windsurf:**

Add to `.cursorrules` or `.windsurfrules` in your project root:
```bash
curl -o .cursorrules https://raw.githubusercontent.com/michaeljabbour/amplifier-skill/main/amplifier-skill/SKILL.md
```

**Manual install (Warp or other tools):**

```bash
mkdir -p ~/.claude/skills/amplifier-ecosystem-router
curl -o ~/.claude/skills/amplifier-ecosystem-router/SKILL.md \
  https://raw.githubusercontent.com/michaeljabbour/amplifier-skill/main/amplifier-skill/SKILL.md
```

**Other tools:** copy `amplifier-skill/SKILL.md` into the tool's skills directory.

### 3. Install Companion Skills (optional)

Each companion skill is self-contained in its own directory. Install the ones you need:

```bash
# Cross-repo workflows
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-cross-repo-workflows/SKILL.md

# Core concepts
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-core-concepts/SKILL.md

# Module and bundle development
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-module-and-bundle-development/SKILL.md

# Foundation reference
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-foundation-reference/SKILL.md

# App integration
claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-app-integration/SKILL.md
```

## Helper Scripts

These live in `amplifier-skill/scripts/` and are used by the router skill.

### Session context lookup

```bash
./amplifier-skill/scripts/session_context.sh --project "$PWD" --limit 10
./amplifier-skill/scripts/session_context.sh --all-projects --limit 10
```

### Agent discovery

```bash
./amplifier-skill/scripts/list_agents.sh
./amplifier-skill/scripts/list_agents.sh --bundle foundation
```

## Validation

Run suite validation:

```bash
bash scripts/validate_suite.sh
```

## Repository Layout

```text
.
├── README.md
├── amplifier-skill/                        ← Router skill (entry point)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── docs/
│   │   └── amplifier.md                    ← Router quick reference
│   ├── resources/
│   │   └── agent-catalog.md                ← Expert-agent routing guide
│   └── scripts/
│       ├── list_agents.sh
│       └── session_context.sh
├── amplifier-cross-repo-workflows/         ← Companion skill
│   └── SKILL.md
├── amplifier-core-concepts/                ← Companion skill
│   └── SKILL.md
├── amplifier-module-and-bundle-development/ ← Companion skill
│   └── SKILL.md
├── amplifier-foundation-reference/         ← Companion skill
│   └── SKILL.md
├── amplifier-app-integration/              ← Companion skill
│   └── SKILL.md
├── scripts/
│   └── validate_suite.sh
└── tests/
    ├── test_list_agents.sh
    └── test_session_context.sh
```

## Canonical Sources

This suite distills and routes around these authoritative sources:

- [`amplifier/docs/MODULES.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) — Component catalog and module taxonomy
- [`amplifier/docs/MODULE_DEVELOPMENT.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULE_DEVELOPMENT.md) — Module development workflows
- [`amplifier-foundation/docs/BUNDLE_GUIDE.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/BUNDLE_GUIDE.md) — Bundle authoring guide
- [`amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/APPLICATION_INTEGRATION_GUIDE.md) — App embedding guide
- [`amplifier-foundation/examples/`](https://github.com/microsoft/amplifier-foundation/tree/main/examples) — Reference examples

## Documentation

- [Quick Reference](../skills/build-amplifier/references/upstream-suite/amplifier-skill/docs/amplifier.md)
- [Expert-Agent Routing Guide](../skills/build-amplifier/references/upstream-suite/amplifier-skill/resources/agent-catalog.md)
