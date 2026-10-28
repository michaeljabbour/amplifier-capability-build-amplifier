# Amplifier Ecosystem Skill Suite Rehab — Phase 1: Router Rehab & Repo Layout

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Convert `amplifier-skill/SKILL.md` from a single delegation skill into the ecosystem router, fix README/install-path drift, and create the companion skill directory stubs that Phase 2 will fill.

**Architecture:** Keep `amplifier-skill/` as the entry-point skill directory. The existing `SKILL.md` becomes the ecosystem router. Five empty companion skill directories are created as stubs. The README is rewritten to accurately describe the suite and provide correct install paths.

**Tech Stack:** Markdown skill files, POSIX shell scripts, git.

---

## Prerequisites

All commands run from the repo root: `/Users/michaeljabbour/dev/amplifier-skill`

```bash
cd /Users/michaeljabbour/dev/amplifier-skill
```

---

### Task 1: Fix README.md

**Files:**
- Modify: `README.md`

**Step 1: Read the current README to understand what needs to change**

```bash
cat -n README.md
```

The README currently references `SKILL.md` at the repo root (not the subdirectory) and describes a single delegation skill. Both are wrong after the rehab.

**Step 2: Verify the install path drift**

```bash
# The README says:
#   claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/SKILL.md
# But SKILL.md now lives at:
#   amplifier-skill/SKILL.md
ls amplifier-skill/SKILL.md
```

Expected: file exists at `amplifier-skill/SKILL.md`, not repo root.

**Step 3: Write the new README.md**

Replace the entire file with:

```markdown
# Amplifier Ecosystem Skill Suite

A router-first skill suite for the [Microsoft Amplifier](https://github.com/microsoft/amplifier) ecosystem.
Start at the router skill. It classifies your task and routes you to the right companion skill,
canonical docs, and expert agent.

## Skill Suite

| Skill | Purpose |
|-------|---------|
| [`amplifier-skill`](amplifier-skill/SKILL.md) | **Entry point.** Routes by repo, layer, and intent. |
| [`amplifier-cross-repo-workflows`](amplifier-cross-repo-workflows/SKILL.md) | Dependency hierarchy, change order, testing ladder, local override, shadow, app-cli validation. |
| [`amplifier-core-concepts`](amplifier-core-concepts/SKILL.md) | Kernel, five module types, orchestrators, session lifecycle, hooks, tool-vs-hook. |
| [`amplifier-module-and-bundle-development`](amplifier-module-and-bundle-development/SKILL.md) | Module and bundle authoring: `MODULES.md`, `MODULE_DEVELOPMENT.md`, `BUNDLE_GUIDE.md`. |
| [`amplifier-foundation-reference`](amplifier-foundation-reference/SKILL.md) | Foundation docs, examples, and `APPLICATION_INTEGRATION_GUIDE.md` distilled. |
| [`amplifier-app-integration`](amplifier-app-integration/SKILL.md) | Building apps on Amplifier. Protocol boundary, session lifecycle, app-cli as proof surface. |

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

- [Quick Reference](amplifier-skill/docs/amplifier.md)
- [Expert-Agent Routing Guide](amplifier-skill/resources/agent-catalog.md)
```

**Step 4: Verify the README was written correctly**

```bash
grep -c "amplifier-skill/SKILL.md" README.md
```

Expected: `1` (the install path now points to the subdirectory).

```bash
grep "SKILL.md" README.md | head -5
```

Expected: all `SKILL.md` references include the `amplifier-skill/` prefix or a companion skill directory prefix.

**Step 5: Commit**

```bash
git add README.md
git commit -m "docs: fix README install-path drift and describe suite architecture"
```

---

### Task 2: Convert `amplifier-skill/SKILL.md` to Ecosystem Router

**Files:**
- Modify: `amplifier-skill/SKILL.md`

**Step 1: Read the current SKILL.md**

```bash
cat -n amplifier-skill/SKILL.md
```

Note: the current skill is focused on delegation mechanics only. The router must also classify tasks by repo/layer/intent and route to companions and expert agents.

**Step 2: Write the new router SKILL.md**

Replace the entire file with:

```markdown
---
name: amplifier-ecosystem-router
description: Front door for the Amplifier ecosystem skill suite. Routes tasks by repo, layer, and intent to the right companion skill, docs, and expert agent. Use this first for any Amplifier ecosystem question.
---

# Amplifier Ecosystem Router

Start here. Answer three questions, then follow the routing table.

1. **Which repo is involved?**
2. **Which layer is this?**
3. **What kind of task is this?**

---

## Quick Routing Table

| Task type | Go here |
|-----------|---------|
| Delegating work to Amplifier from a coding assistant | Stay here — see Delegation Workflow below |
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

---

## Delegation Workflow

Use when the user explicitly asks to delegate to Amplifier, inspect Amplifier history, or discover agents.

**Rule:** Delegate on explicit intent only. Keep quick edits, simple shell commands, and obvious fixes local.

### 1. Preflight

```bash
command -v amplifier
amplifier --help
amplifier provider current
```

If provider state is missing: `amplifier init`

### 2. Delegate

```bash
# Single-shot
amplifier run "<task description>"

# Interactive
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

### 5. Install if missing

```bash
uv tool install git+https://github.com/microsoft/amplifier
```

---

## Guardrails

- Delegate on explicit intent only. When intent is ambiguous, ask one short clarification.
- Never hardcode bundle or agent lists — use runtime discovery.
- When details are volatile or authoritative clarification is needed, route to docs or an expert agent; do not guess.
- After delegation completes, summarize Amplifier output and recommend next steps.
```

**Step 3: Verify the file was written correctly**

```bash
grep -c "amplifier-app-integration\|amplifier-cross-repo\|amplifier-core-concepts\|amplifier-module-and-bundle\|amplifier-foundation-reference" amplifier-skill/SKILL.md
```

Expected: `5` (one match per companion skill reference).

```bash
grep "ecosystem-router" amplifier-skill/SKILL.md | head -3
```

Expected: shows the YAML frontmatter `name: amplifier-ecosystem-router`.

**Step 4: Commit**

```bash
git add amplifier-skill/SKILL.md
git commit -m "feat: convert amplifier-skill SKILL.md to ecosystem router"
```

---

### Task 3: Update Router Quick Reference

**Files:**
- Modify: `amplifier-skill/docs/amplifier.md`

**Step 1: Read the current file**

```bash
cat -n amplifier-skill/docs/amplifier.md
```

The current file is a delegation command cheatsheet. It needs to become the router's quick reference: suite overview + routing cheatsheet + delegation commands.

**Step 2: Write the updated quick reference**

Replace the entire file with:

```markdown
# Amplifier Ecosystem Router — Quick Reference

Command cheatsheet and routing summary for the router skill.
For full routing logic, see [SKILL.md](../SKILL.md).

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
```

**Step 3: Verify**

```bash
grep "amplifier-app-integration\|amplifier-cross-repo\|amplifier-core-concepts" amplifier-skill/docs/amplifier.md
```

Expected: three lines, one for each companion skill routing entry.

**Step 4: Commit**

```bash
git add amplifier-skill/docs/amplifier.md
git commit -m "docs: update router quick reference with suite routing cheatsheet"
```

---

### Task 4: Update Expert-Agent Routing Guide

**Files:**
- Modify: `amplifier-skill/resources/agent-catalog.md`

**Step 1: Read the current file**

```bash
cat -n amplifier-skill/resources/agent-catalog.md
```

The current file explains dynamic discovery. It needs to also document the expert agent routing pattern — which agents exist, what each covers, when to route to each.

**Step 2: Write the updated expert-agent guide**

Replace the entire file with:

```markdown
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
```

**Step 3: Verify**

```bash
grep "amplifier-expert\|core-expert\|foundation-expert\|ecosystem-expert" amplifier-skill/resources/agent-catalog.md | wc -l
```

Expected: `4` (one per expert agent entry in the table).

**Step 4: Commit**

```bash
git add amplifier-skill/resources/agent-catalog.md
git commit -m "docs: update agent-catalog with expert-agent routing directory"
```

---

### Task 5: Create Companion Skill Directory Stubs

**Files:**
- Create: `amplifier-cross-repo-workflows/SKILL.md` (stub)
- Create: `amplifier-core-concepts/SKILL.md` (stub)
- Create: `amplifier-module-and-bundle-development/SKILL.md` (stub)
- Create: `amplifier-foundation-reference/SKILL.md` (stub)
- Create: `amplifier-app-integration/SKILL.md` (stub)

**Step 1: Confirm companion directories do not exist yet**

```bash
ls -d amplifier-cross-repo-workflows amplifier-core-concepts \
       amplifier-module-and-bundle-development amplifier-foundation-reference \
       amplifier-app-integration 2>&1
```

Expected: `No such file or directory` for each — they don't exist yet.

**Step 2: Create the stubs**

```bash
mkdir -p amplifier-cross-repo-workflows \
         amplifier-core-concepts \
         amplifier-module-and-bundle-development \
         amplifier-foundation-reference \
         amplifier-app-integration
```

Create `amplifier-cross-repo-workflows/SKILL.md`:

```markdown
---
name: amplifier-cross-repo-workflows
description: "STUB — Phase 2 will fill this. Cross-repo execution workflows for the Amplifier ecosystem: dependency hierarchy, change order, testing ladder, local override, shadow environments, and why amplifier-app-cli is the real end-to-end validation surface."
---

# amplifier-cross-repo-workflows

> **This skill is a stub.** Full content arrives in Phase 2 of the rehab.

See the router skill (`amplifier-skill`) for current routing guidance.
```

Create `amplifier-core-concepts/SKILL.md`:

```markdown
---
name: amplifier-core-concepts
description: "STUB — Phase 2 will fill this. Core Amplifier concepts: kernel architecture, five module types, orchestrators as the main engine, session lifecycle, hooks and events, tool-vs-hook distinction."
---

# amplifier-core-concepts

> **This skill is a stub.** Full content arrives in Phase 2 of the rehab.

See the router skill (`amplifier-skill`) for current routing guidance.
```

Create `amplifier-module-and-bundle-development/SKILL.md`:

```markdown
---
name: amplifier-module-and-bundle-development
description: "STUB — Phase 2 will fill this. Module and bundle authoring for the Amplifier ecosystem. Canonical home for MODULES.md, MODULE_DEVELOPMENT.md, and BUNDLE_GUIDE.md guidance."
---

# amplifier-module-and-bundle-development

> **This skill is a stub.** Full content arrives in Phase 2 of the rehab.

See the router skill (`amplifier-skill`) for current routing guidance.
```

Create `amplifier-foundation-reference/SKILL.md`:

```markdown
---
name: amplifier-foundation-reference
description: "STUB — Phase 2 will fill this. Heavier reference companion for amplifier-foundation: docs, examples, and APPLICATION_INTEGRATION_GUIDE.md distilled."
---

# amplifier-foundation-reference

> **This skill is a stub.** Full content arrives in Phase 2 of the rehab.

See the router skill (`amplifier-skill`) for current routing guidance.
```

Create `amplifier-app-integration/SKILL.md`:

```markdown
---
name: amplifier-app-integration
description: "STUB — Phase 2 will fill this. How to build applications on top of Amplifier: protocol boundary principle, session lifecycle patterns, and amplifier-app-cli as the validation surface."
---

# amplifier-app-integration

> **This skill is a stub.** Full content arrives in Phase 2 of the rehab.

See the router skill (`amplifier-skill`) for current routing guidance.
```

**Step 3: Verify all five stubs exist**

```bash
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  echo -n "$dir/SKILL.md: "
  [ -f "$dir/SKILL.md" ] && echo "OK" || echo "MISSING"
done
```

Expected:
```
amplifier-cross-repo-workflows/SKILL.md: OK
amplifier-core-concepts/SKILL.md: OK
amplifier-module-and-bundle-development/SKILL.md: OK
amplifier-foundation-reference/SKILL.md: OK
amplifier-app-integration/SKILL.md: OK
```

**Step 4: Verify each stub has valid YAML frontmatter**

```bash
for dir in amplifier-cross-repo-workflows amplifier-core-concepts \
           amplifier-module-and-bundle-development amplifier-foundation-reference \
           amplifier-app-integration; do
  echo -n "$dir: "
  head -1 "$dir/SKILL.md" | grep -q "^---$" && echo "frontmatter OK" || echo "MISSING frontmatter"
done
```

Expected: `frontmatter OK` for all five.

**Step 5: Commit**

```bash
git add amplifier-cross-repo-workflows/ amplifier-core-concepts/ \
        amplifier-module-and-bundle-development/ amplifier-foundation-reference/ \
        amplifier-app-integration/
git commit -m "feat: add companion skill directory stubs for Phase 2"
```

---

### Task 6: Create scripts/ and tests/ directories for Phase 3

**Files:**
- Create: `scripts/.gitkeep`
- Create: `tests/.gitkeep`

**Step 1: Confirm they don't exist at the repo root yet**

```bash
ls -d scripts tests 2>&1
```

Expected: `No such file or directory` (the `scripts/` directory inside `amplifier-skill/` is separate).

**Step 2: Create the directories**

```bash
mkdir -p scripts tests
touch scripts/.gitkeep tests/.gitkeep
```

**Step 3: Verify**

```bash
ls -la scripts/ tests/
```

Expected: both directories exist with `.gitkeep` files.

**Step 4: Commit**

```bash
git add scripts/ tests/
git commit -m "chore: add scripts/ and tests/ directories for Phase 3"
```

---

### Task 7: Verify Phase 1 Completeness

**Step 1: Check repo layout matches the README**

```bash
echo "=== Router skill ===" && ls amplifier-skill/
echo "=== Companion stubs ===" && ls -d amplifier-*/
echo "=== Scripts dir ===" && ls scripts/
echo "=== Tests dir ===" && ls tests/
```

Expected output (approximately):
```
=== Router skill ===
SKILL.md  agents  docs  resources  scripts
=== Companion stubs ===
amplifier-app-integration/  amplifier-core-concepts/  amplifier-cross-repo-workflows/
amplifier-foundation-reference/  amplifier-module-and-bundle-development/  amplifier-skill/
=== Scripts dir ===
.gitkeep
=== Tests dir ===
.gitkeep
```

**Step 2: Verify the router SKILL.md has the correct name in frontmatter**

```bash
head -3 amplifier-skill/SKILL.md
```

Expected:
```
---
name: amplifier-ecosystem-router
description: Front door for the Amplifier ecosystem skill suite. ...
```

**Step 3: Verify no broken references in README**

```bash
# Every SKILL.md path referenced in README should exist on disk
grep "SKILL.md" README.md | grep -oE '[a-z-]+/SKILL\.md' | while read path; do
  echo -n "$path: "
  [ -f "$path" ] && echo "exists" || echo "MISSING"
done
```

Expected: `exists` for all paths found.

**Step 4: Final Phase 1 commit (if anything was left unstaged)**

```bash
git status
# If clean:
echo "Phase 1 complete — working directory clean"
```

Expected: `nothing to commit, working tree clean`

---

## Phase 1 Acceptance Checklist

- [ ] `README.md` references `amplifier-skill/SKILL.md` (not a root `SKILL.md`)
- [ ] `README.md` documents all six skills in the suite table
- [ ] `amplifier-skill/SKILL.md` has `name: amplifier-ecosystem-router` in frontmatter
- [ ] Router skill routes to all five companion skills by name
- [ ] Router skill includes an expert agent directory
- [ ] `amplifier-skill/docs/amplifier.md` has a suite routing cheatsheet
- [ ] `amplifier-skill/resources/agent-catalog.md` documents the four expert agents
- [ ] Five companion skill stubs exist with valid frontmatter
- [ ] `scripts/` and `tests/` directories exist at repo root
- [ ] Working directory is clean with all commits made

**Next:** Phase 2 — fill the five companion skill stubs with content.
