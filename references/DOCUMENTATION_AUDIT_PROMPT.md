# Documentation Audit Prompt

**Purpose:** Use this prompt with an adversarial AI to validate:
1. Documentation accuracy
2. Agent Skill readiness
3. **Foundation Pattern Alignment** - the most critical: whether code follows amplifier-foundation patterns (the source of truth)

**Reference:**
- Agent Skills specification at https://agentskills.io/specification
- **amplifier-foundation** - the source of truth for Amplifier patterns: https://github.com/microsoft/amplifier-foundation

---

## Audit Prompt

```
You are a skeptical technical auditor tasked with THREE objectives:

1. **Accuracy Audit**: Find errors, inconsistencies, and gaps in the documentation
2. **Agent Skill Readiness**: Evaluate if the documentation can be converted to a reliable, verifiable Agent Skill
3. **Foundation Alignment**: Verify the code and documentation teach/follow amplifier-foundation patterns (the source of truth), NOT amplifier-app-cli anti-patterns

CRITICAL: amplifier-foundation is the source of truth for how to build Amplifier applications. amplifier-app-cli is a reference implementation with app-layer policy, but its patterns should NOT be copied directly.

---

# PRE-FLIGHT (DO THIS FIRST)

Before you audit claims, capture enough environment context so another auditor can reproduce your findings.

1. **Identify the target**
   - Target repo absolute path and **git commit SHA** (or explain if not a git repo)
   - List the documents you will audit (e.g., `README.md`, `docs/`, `references/`, `SKILL.md`, `AGENTS.md`, `CLAUDE.md`)

2. **Record execution constraints**
   - Can you run shell commands? If not, do a static-only audit and mark runtime checks as “not verifiable”.
   - Is network access available? If not, do not attempt installs/clones; audit source only.
   - Are you sandboxed from `$HOME` (e.g., `~/.cache/uv`)? If yes, tests may fail for environmental reasons; report that explicitly.

3. **Pin the foundation “source of truth” you used**
   - Prefer auditing against a **local amplifier-foundation checkout** or the **exact version/commit pinned by the target repo**.
   - Always record:
     - Which amplifier-foundation you referenced (path/URL + commit/tag if available)
     - Which Python environment you used for import checks (`uv run python`, `python`, etc.)

4. **Foundation API sanity check (avoid version/API confusion)**
   - Verify the target repo’s `amplifier_foundation` imports using the same environment you’ll use for tests.
   - If you can execute commands, capture evidence like:
     - `python -c "import amplifier_foundation as af; print(af.__file__); print(getattr(af,'__version__','unknown'))"`
     - `python -c "import amplifier_foundation as af; print('BundleRegistry' in dir(af)); print('load_bundle' in dir(af))"`
   - If imports fail, treat it as a **Critical** alignment/packaging issue and continue with static analysis.

---

# PART 1: FOUNDATION ALIGNMENT AUDIT (HIGHEST PRIORITY)

This is the most important section. Code and documentation must align with amplifier-foundation patterns.

## Category 1: Core Workflow Alignment

The correct Amplifier workflow is:
```python
foundation = await load_bundle(...)
provider = await load_bundle(...)
composed = foundation.compose(provider)
prepared = await composed.prepare()
async with await prepared.create_session() as session:
    response = await session.execute(prompt)
```

### 1.1 Verify Code Follows This Pattern
- [ ] Does the code use `load_bundle()` → `compose()` → `prepare()` → `create_session()` → `execute()`?
- [ ] Are bundles composed using `bundle.compose(overlay)` (not custom merge logic)?
- [ ] Is `prepare()` called before session creation?
- [ ] Are sessions created with `prepared.create_session()`?
- [ ] If `async with` is used, does the session implement async context manager semantics? If not, is `cleanup()` called reliably?

### 1.2 Anti-Pattern Detection
Flag any code that:
- [ ] Treats app-specific persistence as “the mechanism” (persistence is policy; session lifecycle is mechanism)
- [ ] Custom session_spawner functions instead of using `prepared.spawn()`
- [ ] Custom bundle loading logic instead of `load_bundle()`
- [ ] Manual module mounting instead of bundle composition
- [ ] Re-implementing foundation functionality locally

### 1.3 Documentation Teaches Correct Patterns
- [ ] Does documentation show the load → compose → prepare → execute workflow?
- [ ] Does documentation use foundation code examples (not app-cli internals)?
- [ ] Does documentation warn against copying app-cli patterns directly?

## Category 2: Bundle System Alignment

### 2.1 Bundle Format Compliance
The correct bundle format is markdown with YAML frontmatter:
```markdown
---
bundle:
  name: my-bundle
  version: 1.0.0
session:
  orchestrator: {module: loop-streaming}
providers:
  - module: provider-anthropic
    source: git+...
---

System instruction here.
```

- [ ] Do bundle files use this format?
- [ ] Are bundle sections correct? (`bundle`, `session`, `providers`, `tools`, `hooks`, `agents`, `context`)
- [ ] Do `includes:` chains work correctly?

### 2.2 Composition Rules
Foundation merge rules:
| Section | Rule |
|---------|------|
| `session` | Deep merge |
| `providers` | Merge by module ID |
| `tools` | Merge by module ID |
| `hooks` | Merge by module ID |
| `instruction` | Replace (later wins) |

- [ ] Does code respect these merge rules?
- [ ] Is composition used (not manual merging)?

## Category 3: Application Architecture Alignment

### 3.1 AppConfig Pattern
The foundation blueprint uses:
```python
@dataclass
class AppConfig:
    provider_bundle: str
    api_key: str | None

    @classmethod
    def from_env(cls): ...

    def validate(self): ...
```

- [ ] Does the application use a configuration dataclass?
- [ ] Is configuration loaded from environment/files (not hardcoded)?
- [ ] Is there a validation method?

### 3.2 AmplifierApp Pattern
The foundation blueprint uses:
```python
class AmplifierApp:
    async def initialize(self): ...   # load → compose → prepare → session
    async def execute(self, prompt): ...
    async def shutdown(self): ...
    async def __aenter__(self): ...   # context manager
    async def __aexit__(self, *args): ...
```

- [ ] Is there a clear initialize/execute/shutdown lifecycle?
- [ ] Is the context manager pattern used (`async with`)?
- [ ] Is session cleanup handled properly?

### 3.3 Agent Delegation
The foundation uses:
```python
agent_bundle = await load_bundle("./agents/agent.md")
result = await prepared.spawn(child_bundle=agent_bundle, instruction=instruction)
```

- [ ] Is agent delegation done via `prepared.spawn()`?
- [ ] Are agents loaded as bundles?
- [ ] NOT: Custom spawn_sub_session/resume_sub_session functions

## Category 4: Anti-Pattern Inventory

### 4.1 amplifier-app-cli Patterns to AVOID Teaching

| Anti-Pattern | Why to Avoid | Correct Pattern |
|--------------|--------------|-----------------|
| `SessionStore` class | App-layer policy, not mechanism | Session lifecycle via `create_session()` |
| `session_spawner.py` functions | App-layer policy | `prepared.spawn()` |
| Custom bundle discovery | App-layer policy | `load_bundle()` from any path/URL |
| Three-scope config merging | App-layer policy | Bundle composition |
| Custom mention loading | App-layer policy | Foundation's `@namespace:path` |

- [ ] Does documentation avoid teaching these patterns?
- [ ] Does code avoid implementing these patterns?
- [ ] If used, are they clearly labeled as "app policy" not "the way to build"?

### 4.2 Foundation-First Mindset Check
Ask for each feature:
- [ ] "Could this use bundle composition instead of custom code?"
- [ ] "Could this use foundation's existing API instead of custom implementation?"
- [ ] "Is this mechanism (foundation) or policy (app-specific)?"

## Category 5: Documentation Source of Truth

### 5.1 Code Examples Source
For each code example in documentation:
- [ ] Does it come from foundation (correct)?
- [ ] Does it come from amplifier-app-cli (mark as "reference only")?
- [ ] Does it show the correct workflow?

### 5.2 Architecture Diagrams
For each architecture diagram:
- [ ] Does it show bundle composition as central?
- [ ] Does it avoid teaching app-cli internals?
- [ ] Does it align with foundation's concepts?

### 5.3 External Links
- [ ] Do external links point to foundation docs primarily?
- [ ] Is foundation's examples/08_cli_application.py referenced as blueprint?
- [ ] Is app-cli referenced as "reference implementation" not "how to build"?

---

# PART 2: ACCURACY AUDIT

## Category 6: File Path Verification
For every file path mentioned in the documentation:
- [ ] Verify the file actually exists at that path
- [ ] Check if the file has been renamed or moved
- [ ] Confirm directory structures match reality
- [ ] Separate **repo paths** (must exist in the repo) from **runtime paths** (e.g., `~/.amplifier/...`) and **syntax examples** (e.g., `@namespace:path`) which may not exist on disk

## Category 7: Function/Class Name Verification
For every function, class, or method mentioned:
- [ ] Verify it exists in the specified file
- [ ] Check the signature matches any documented parameters
- [ ] Confirm return types if mentioned

## Category 8: Import Statement Verification
The documentation claims specific imports from amplifier-foundation:
- [ ] `Bundle`, `load_bundle` - Verify these are used correctly
- [ ] `BundleRegistry` - Only if referenced by docs/code; verify it exists in the pinned foundation version
- [ ] `ContentDeduplicator`, `ContextFile` - Verify import locations
- [ ] `validate_bundle_or_raise` - Check this exists
- [ ] If any import fails, report the exact exception and the `amplifier_foundation.__file__` path to avoid “wrong version” confusion

## Category 9: Test Command Verification
Run the repo’s documented commands first (README/CONTRIBUTING/CLAUDE/AGENTS). If none exist, use best-effort defaults.

For Python repos using uv:
```bash
uv run pytest
```

Coverage is **optional** and only valid if `pytest-cov` is installed/configured:
```bash
uv run pytest --cov=<your_package_or_module>
```

Type checking is **optional** and only valid if `mypy` is installed/configured:
```bash
uv run mypy .
```

If commands fail due to environment restrictions (network/sandbox/home-dir access), capture the error output and mark tests as “not verifiable in this environment”.

## Category 10: Inconsistency Detection
Look for contradictions between documents:
- [ ] SKILL.md vs reference files - Any conflicting information?
- [ ] Code examples vs actual API - Mismatched?
- [ ] Diagrams (Mermaid/ASCII) vs real code paths - Boxes/files exist? Arrows/dependencies accurate? If “conceptual”, does it say so?

---

# PART 3: AGENT SKILL READINESS AUDIT

## Category 11: SKILL.md Metadata Readiness

### 11.1 Required Fields
- [ ] `name`: Valid skill name (lowercase, hyphens, 1-64 chars)?
- [ ] `description`: Clear what/when description (1-1024 chars)?

### 11.2 Content Quality
- [ ] Does SKILL.md teach foundation patterns first?
- [ ] Are amplifier-app-cli patterns clearly labeled as "reference only"?
- [ ] Are step-by-step instructions based on foundation workflow?

## Category 12: Instruction Content Readiness

### 12.1 Core Workflow Instructions
Must include:
- [ ] How to load and compose bundles
- [ ] How to prepare and create sessions
- [ ] How to execute prompts
- [ ] How to define agents as bundles
- [ ] How to spawn agent sub-sessions

### 12.2 Code Examples
Each example should:
- [ ] Use foundation APIs (`load_bundle`, `compose`, `prepare`, etc.)
- [ ] Show the complete workflow
- [ ] Be runnable (not pseudo-code)

## Category 13: Progressive Disclosure Structure

### 13.1 Tiered Information
- [ ] **Tier 1 (SKILL.md):** Core foundation patterns, quick start
- [ ] **Tier 2 (references/):** Detailed architecture, app-cli analysis
- [ ] Is the right content in the right tier?

## Category 14: Verifiability Requirements

### 14.1 Foundation Pattern Verification
Can an agent verify:
- [ ] Bundle loads correctly?
- [ ] Composition produces expected result?
- [ ] Session creation succeeds?
- [ ] Execution returns response?

### 14.2 Verification Commands
```bash
# Verify the pinned foundation API in the SAME environment used for tests
# (avoid accidentally using a different global/site-packages install).
python -c "import amplifier_foundation as af; print(af.__file__); print(getattr(af,'__version__','unknown'))"
python -c "from amplifier_foundation import load_bundle, Bundle"

# Optional: run foundation tests if you have a local checkout OR network access
# - If local checkout exists:
#   cd /path/to/amplifier-foundation && uv run pytest
# - If you must fetch it from the network, do so only if allowed in your environment.
```

- [ ] Are these documented?

---

# OUTPUT FORMAT

## Environment (REQUIRED)

Include this section at the top of your report:

```
## Environment

- Target repo: <absolute path or URL>
- Target commit: <git SHA or “not a git repo”>
- amplifier-foundation reference: <local path or pinned version/ref>
- Python: <version>
- Package manager: <uv/poetry/pip/other>
- Network access: <yes/no/unknown>
- Sandbox/home-dir limits: <yes/no/unknown>
- Commands run: <list>
- Not verifiable here: <list of checks blocked by environment>
```

## Part 1: Foundation Alignment Issues (CRITICAL)

For each foundation alignment issue:

```
## FOUNDATION ISSUE #[N]: [Brief Title]

**Severity:** Critical | High | Medium
**Type:** Anti-Pattern | Missing Pattern | Wrong Pattern | Documentation Mismatch
**Location:** [File and section]
**Problem:** [What's wrong]
**Foundation Pattern:** [What it should be]
**Current Code/Doc:** "[Quote]"
**Fix:** [How to align with foundation]
```

## Part 2: Accuracy Issues

```
## Issue #[N]: [Category] - [Brief Title]

**Severity:** Critical | High | Medium | Low
**Document:** [Which document]
**Location:** [Line number or section]
**Claim:** "[Quote]"
**Reality:** [What you found]
**Recommendation:** [How to fix]
```

## Part 3: Skill Readiness Report

```
## Agent Skill Readiness Assessment

### Foundation Alignment Score

| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|
| Uses load_bundle workflow | X | ... |
| Uses bundle composition | X | ... |
| Uses prepare → create_session | X | ... |
| Uses spawn for agents | X | ... |
| Avoids app-cli anti-patterns | X | ... |
| Documentation teaches foundation | X | ... |
| **Foundation Alignment Total** | **X** | ... |

### Skill Readiness Score

| Criterion | Score (1-10) | Notes |
|-----------|--------------|-------|
| Metadata completeness | X | ... |
| Foundation pattern coverage | X | ... |
| Example quality | X | ... |
| Verification support | X | ... |
| **Overall Readiness** | **X** | ... |

### Critical Action Items

1. **Foundation Alignment:** [Must fix first]
2. **Documentation:** [Required updates]
3. **Code:** [Required changes]
```

---

## Severity Definitions

### Foundation Issues
- **Critical**: Code/docs teach anti-patterns that would mislead developers
- **High**: Missing foundation patterns that would cause confusion
- **Medium**: Minor alignment issues

### Accuracy Issues
- **Critical**: Fundamentally wrong
- **High**: Important inaccuracy
- **Medium**: Minor inaccuracy
- **Low**: Cosmetic issue

---

## Key Foundation References

When auditing, verify against these foundation sources:

1. **Core Workflow**: `amplifier-foundation/README.md`
2. **Concepts**: `amplifier-foundation/docs/CONCEPTS.md`
3. **Patterns**: `amplifier-foundation/docs/PATTERNS.md`
4. **CLI Blueprint**: `amplifier-foundation/examples/08_cli_application.py`

---

## Final Checklist

After completing the audit:

1. **Foundation Alignment Summary**
   - Issues by severity
   - Anti-patterns detected
   - Missing patterns
   - Alignment score

2. **Top 5 Foundation Fixes**
   - Prioritized list of what must align first

3. **Accuracy Summary**
   - Issues by category
   - Documents ranked by accuracy

4. **Skill Readiness Summary**
   - Foundation alignment score
   - Overall readiness score
   - Critical action items

---

Begin your audit by reading foundation documentation first, then systematically verify that code and documentation align with foundation patterns. Anti-patterns from amplifier-app-cli should be flagged and corrected.
```

---

## Usage Instructions

1. **Copy the prompt above** into a conversation with an AI assistant
2. **Tell the AI your constraints up front:**
   - Whether it can run shell commands
   - Whether network access is allowed
   - Whether it can read/write outside the repo (e.g., `$HOME`, caches)
3. **Provide access to:**
   - The target repository to audit
   - amplifier-foundation repository (source of truth)
   - The agentskills specification (https://agentskills.io)
4. **Let it run the audit** with Part 1 (Foundation Alignment) as highest priority
5. **Review findings** - foundation alignment issues are most critical
6. **Fix foundation issues first** before addressing other concerns

## Expected Outcomes

### Foundation Alignment Audit (Most Important)
- Anti-patterns identified and flagged
- Missing foundation patterns documented
- Clear mapping of current → target patterns
- Foundation alignment score

### Accuracy Audit
- File paths verified
- Function names confirmed
- Stale references updated

### Skill Readiness
- SKILL.md teaches foundation patterns
- Examples use foundation APIs
- Verification commands documented

## Anti-Pattern Quick Reference

| If You See | Replace With |
|------------|--------------|
| Custom SessionStore | `prepared.create_session()` lifecycle |
| spawn_sub_session() | `prepared.spawn(child_bundle=...)` |
| Custom bundle loading | `await load_bundle(path_or_url)` |
| Manual config merging | `base.compose(overlay)` |
| Custom mention parsing | Foundation's `@namespace:path` |
| Class-heavy architecture | Bundle composition + simple app class |

## Maintenance Schedule

Run this audit:
- **After any code changes** - check foundation alignment
- **Before creating Agent Skills** - ensure teaching correct patterns
- **When updating documentation** - verify against foundation
- **Quarterly** - catch drift from foundation evolution
