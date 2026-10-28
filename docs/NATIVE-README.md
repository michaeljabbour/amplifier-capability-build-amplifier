> Original native guide, preserved at source commit `81dc45815b65ec9c2dcef7c89750acba5fb72119`. Install locations, model names, service availability, and claims below are historical and must be verified before use. Current portable installation is in INSTALL.md.

# Amplifier Skill

Delegate complex work to [Microsoft Amplifier](https://github.com/microsoft/amplifier)
from coding assistants while keeping local/simple tasks local.

## What Changed in V2

- Explicit-intent delegation policy: delegate only when users explicitly ask for Amplifier.
- Runtime-first discovery: avoid hardcoded bundle/agent lists.
- Sandbox-safe behavior: filesystem fallbacks for sessions and agent discovery.
- Skill metadata support: `agents/openai.yaml` included for product UIs.

## Quick Start

### 1. Install Amplifier

```bash
uv tool install git+https://github.com/microsoft/amplifier
amplifier init
```

### 2. Install This Skill

**Claude Code:**

```bash
claude skill add https://github.com/michaeljabbour/amplifier-skill-codex/blob/main/SKILL.md
```

**Warp (or manual install):**

```bash
mkdir -p ~/.claude/skills/amplifier
curl -o ~/.claude/skills/amplifier/SKILL.md \
  https://raw.githubusercontent.com/michaeljabbour/amplifier-skill-codex/main/SKILL.md
```

**Other tools:** copy `SKILL.md` into the tool's skills/commands directory.

## Core Behavior

- Delegate only when users explicitly request Amplifier usage.
- Prefer local execution for quick edits, simple shell operations, and obvious fixes.
- Query Amplifier history/context via script or runtime commands.
- Discover agents dynamically at runtime or from local cache fallback.

## Helper Scripts

### Session context lookup

```bash
./scripts/session_context.sh --project "$PWD" --limit 10
./scripts/session_context.sh --all-projects --limit 10
```

### Agent discovery

```bash
./scripts/list_agents.sh
./scripts/list_agents.sh --bundle foundation
```

## Validation

Run the skill validator:

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py .
```

## Documentation

- [Quick Reference](https://github.com/michaeljabbour/amplifier-skill/blob/81dc45815b65ec9c2dcef7c89750acba5fb72119/docs/amplifier.md)
- [Agent Discovery Guide](https://github.com/michaeljabbour/amplifier-skill/blob/81dc45815b65ec9c2dcef7c89750acba5fb72119/resources/agent-catalog.md)
- [Official Amplifier Docs](https://github.com/microsoft/amplifier)

## Repository Layout

```text
.
├── SKILL.md
├── README.md
├── agents/
│   └── openai.yaml
├── docs/
│   └── amplifier.md
├── resources/
│   └── agent-catalog.md
└── scripts/
    ├── list_agents.sh
    └── session_context.sh
```
