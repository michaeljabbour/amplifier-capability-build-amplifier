> Preserved upstream topic, not a separate installation or current SDK guarantee. Read [current contracts](../../current-contracts.md) before using historical commands/code. The installed Build with Amplifier method governs scope and authority.

---
name: amplifier-module-and-bundle-development
description: Module and bundle authoring for the Amplifier ecosystem. Canonical home for MODULES.md, MODULE_DEVELOPMENT.md, and BUNDLE_GUIDE.md guidance. Covers module creation, bundle composition, the thin bundle pattern, and common authoring mistakes.
---

# Amplifier Module and Bundle Development

Use this skill when creating a new runtime module, authoring a bundle, or figuring out
the correct structure for either.

## What This Skill Is For

- Creating a new runtime module (tool, hook, orchestrator, context manager, provider)
- Authoring or updating a bundle
- Understanding module vs bundle vs agent distinctions
- Getting the thin bundle pattern right
- Avoiding the most common authoring mistakes

## Canonical Sources

- [`amplifier/docs/MODULES.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULES.md) — Full component catalog; current list of all modules, bundles, and applications
- [`amplifier/docs/MODULE_DEVELOPMENT.md`](https://github.com/microsoft/amplifier/blob/main/docs/MODULE_DEVELOPMENT.md) — Complete module development workflows and workspace patterns
- [`amplifier-foundation/docs/BUNDLE_GUIDE.md`](https://github.com/microsoft/amplifier-foundation/blob/main/docs/BUNDLE_GUIDE.md) — Authoritative bundle authoring guide with full examples

Also load the `creating-amplifier-modules` skill (available in this suite's skill tool)
for the mount() contract and protocol compliance validation specifics.

Expert agents:
- `amplifier:amplifier-expert` — module tooling, CLI behavior, module catalog questions
- `foundation:foundation-expert` — bundle composition, Foundation API details
- `core:core-expert` — module protocol compliance, kernel contracts

---

## Module vs Bundle vs Agent vs Behavior

| Concept | What it is | Where it lives |
|---------|-----------|---------------|
| **Module** | Python package implementing a kernel protocol (Tool, Hook, Orchestrator, Provider, ContextManager) | Its own git repo, e.g. `amplifier-module-tool-bash` |
| **Bundle** | Markdown+YAML configuration file that assembles modules, instructions, agents, and spawn policy into a composable unit | Its own git repo (no `pyproject.toml` required) or inline file |
| **Agent** | A named configuration within a bundle — specific instructions, provider, tools, and spawn policy for a sub-task | YAML section inside a bundle's frontmatter |
| **Behavior** | A lightweight bundle that provides only an instruction overlay — no tools, no orchestrator; composed on top of a base bundle | Usually a subdirectory inside a bundle repo |

**Key insight:** A bundle is configuration, not a Python package.
A module is a Python package. Do not confuse them.

---

## Module Taxonomy (from MODULES.md)

The Amplifier ecosystem has five architectural layers:

| Layer | What it contains |
|-------|-----------------|
| **Core infrastructure** | `amplifier-core` — the kernel |
| **Applications** | `amplifier`, `amplifier-app-cli`, `amplifier-app-log-viewer` |
| **Libraries** | `amplifier-foundation` — consumed by applications, not by modules |
| **Bundles** | Composable config packages — `recipes`, `foundation`, `shadow`, `superpowers`, etc. |
| **Runtime modules** | Orchestrators, providers, tools, context managers, hooks |

For the current catalog of all components, read `MODULES.md` directly or ask
`amplifier:amplifier-expert`. The catalog is volatile — components are added frequently.

---

## Creating a New Module

### Quick start

```bash
# Recommended: use the template generator
amplifier module dev create tool-myfeature

# Or manually
mkdir amplifier-module-tool-myfeature && cd amplifier-module-tool-myfeature
uv init --lib
```

### Required pyproject.toml structure

```toml
[project]
name = "amplifier-module-tool-myfeature"
requires-python = ">=3.11"
dependencies = ["amplifier-core"]       # ← only amplifier-core, never amplifier-foundation

[project.entry-points."amplifier.modules"]
tool-myfeature = "amplifier_module_tool_myfeature"   # ← module ID = entry point key

[tool.uv.sources.amplifier-core]
git = "https://github.com/microsoft/amplifier-core"
branch = "main"
```

**The module ID (entry point key) is what you use in bundle frontmatter.**
It must match exactly or module loading will fail silently.

### Implement the protocol

```python
# amplifier_module_tool_myfeature/__init__.py
from amplifier_core.protocols import Tool

class MyFeatureTool(Tool):
    def get_schema(self):
        return {
            "name": "my_feature",
            "description": "Does something useful",
            "input_schema": {
                "type": "object",
                "properties": {"param": {"type": "string"}},
                "required": ["param"]
            }
        }

    async def execute(self, **kwargs):
        return {"result": f"Processed: {kwargs['param']}"}
```

For the `mount()` contract and protocol compliance validation specifics, load the
`creating-amplifier-modules` skill — it covers the exact contracts and common pitfalls.

### Test locally

```bash
# Env var override (clears on terminal close)
export AMPLIFIER_MODULE_TOOL_MYFEATURE=$(pwd)
cd ~/test-project
amplifier run "test my feature"

# Or create a test bundle
cat > test-bundle.md << 'EOF'
---
bundle:
  name: test
  version: 1.0.0
includes:
  - bundle: foundation
tools:
  - module: tool-myfeature
    source: file:///path/to/amplifier-module-tool-myfeature
providers:
  - module: provider-mock
---
Test bundle for tool-myfeature.
EOF
amplifier run --bundle test-bundle.md "test my feature"
```

---

## Authoring a Bundle

### Bundle structure

Bundles are markdown files with YAML frontmatter. A bundle repo does NOT need a root `pyproject.toml`.

```markdown
---
bundle:
  name: my-bundle
  version: 1.0.0

includes:
  - bundle: foundation           # inherit foundation's tools, orchestrator, hooks

agents:
  my-agent:
    instructions: "..."
    providers:
      - module: provider-anthropic

context:
  - path: docs/
    description: "Project documentation"
---

# My Bundle

System instructions for the agent go here in the markdown body.
```

### The Thin Bundle Pattern (recommended)

Most bundles should be thin — inherit from foundation and add only their unique capabilities.

```markdown
---
# ✅ GOOD: thin bundle
bundle:
  name: my-bundle
  version: 1.0.0

includes:
  - bundle: foundation     # foundation provides: orchestrator, context, tools, hooks

agents:
  my-expert:
    instructions: "You are an expert in X..."
---

System prompt goes here.
```

**Do NOT redeclare what foundation already provides:**

```markdown
---
# ❌ BAD: fat bundle duplicating foundation
includes:
  - bundle: foundation

session:                    # ← foundation already defines this
  orchestrator:
    module: loop-streaming
    source: git+https://...

tools:                      # ← foundation already has these
  - module: tool-filesystem
    source: git+https://...
  - module: tool-bash
    source: git+https://...

hooks:                      # ← foundation already has these
  - module: hooks-streaming-ui
    source: git+https://...
---
```

Fat bundles create maintenance burden, version conflicts, and miss foundation updates
automatically. When in doubt: include foundation, then add only what is unique to your bundle.

### Bundle composition merge rules

| Section | Merge rule |
|---------|-----------|
| `session` | Deep merge — nested dicts are merged, not replaced |
| `providers` | Merge by module ID — same ID updates config, new ID adds to list |
| `tools` | Merge by module ID |
| `hooks` | Merge by module ID |
| `spawn` | Deep merge — later overrides earlier |
| `instruction` | Replace — later wins entirely |

---

## Module Development Workflows

### Quick fix (single module)

```bash
git clone https://github.com/microsoft/amplifier-module-tool-bash
cd amplifier-module-tool-bash
# ... make changes ...
export AMPLIFIER_MODULE_TOOL_BASH=$(pwd)
cd ~/test-project && amplifier run "test bash changes"
cd - && git commit -am "fix: ..." && git push
```

### Multi-module workspace

```bash
mkdir ~/amplifier-workspace && cd ~/amplifier-workspace
git clone https://github.com/microsoft/amplifier-module-tool-bash
git clone https://github.com/microsoft/amplifier-module-provider-anthropic
cat > .amplifier/settings.yaml << 'EOF'
sources:
  tool-bash: file://./amplifier-module-tool-bash
  provider-anthropic: file://./amplifier-module-provider-anthropic
EOF
```

### Module dev CLI

```bash
amplifier module dev init      # initialize workspace, create symlinks
amplifier module dev link <id> # link a specific module
amplifier module dev status    # show workspace state
amplifier module dev test <id> # run module's test suite
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding `amplifier-foundation` as a module dependency | Modules depend only on `amplifier-core` |
| Module ID in bundle doesn't match entry point key | Check pyproject.toml `[project.entry-points."amplifier.modules"]` |
| Creating a fat bundle that redeclares foundation's tools/orchestrator/hooks | Use the thin bundle pattern — include foundation, add only unique capabilities |
| Treating bundle as a Python package | Bundles are markdown+YAML config; no `pyproject.toml` needed |
| Pushing a bundle without testing thin composition | Test with `amplifier run --bundle your-bundle.md "test task"` |
| Using a static module catalog | Module catalog is volatile — query `MODULES.md` or `amplifier:amplifier-expert` |
