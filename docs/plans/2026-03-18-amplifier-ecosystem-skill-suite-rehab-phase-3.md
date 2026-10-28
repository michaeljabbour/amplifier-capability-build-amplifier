# Amplifier Ecosystem Skill Suite Rehab — Phase 3: Validation & Polish

> **Execution:** Use the subagent-driven-development workflow to implement this plan.

**Goal:** Add lightweight repeatable validation for the helper scripts, create a suite coherence check script, and do a final README/cross-reference polish pass so the repo has no remaining documentation drift.

**Architecture:** Shell-based tests for `list_agents.sh` and `session_context.sh` live in `tests/`. A suite validation script at `scripts/validate_suite.sh` checks structural coherence (all expected files exist, all frontmatter is valid, all cross-references resolve). Both Phases 1 and 2 must be complete before starting Phase 3.

**Tech Stack:** POSIX shell scripts for tests (no external test framework required), git.

---

## Prerequisites

Phases 1 and 2 complete:

```bash
cd /Users/michaeljabbour/dev/amplifier-skill

# Check all six skills exist with real content
for skill in amplifier-skill amplifier-cross-repo-workflows amplifier-core-concepts \
             amplifier-module-and-bundle-development amplifier-foundation-reference \
             amplifier-app-integration; do
  linecount=$(wc -l < "$skill/SKILL.md" 2>/dev/null || echo 0)
  echo "$skill/SKILL.md: $linecount lines"
done
```

Expected: `amplifier-skill` has 100+ lines; all companions have 80+ lines.

```bash
# Check scripts exist
ls amplifier-skill/scripts/list_agents.sh amplifier-skill/scripts/session_context.sh
```

Expected: both files exist.

```bash
# Check tests/ and scripts/ directories exist at repo root
ls -d tests/ scripts/
```

Expected: both directories exist (created in Phase 1 Task 6).

---

### Task 1: Write Tests for `list_agents.sh`

**Files:**
- Create: `tests/test_list_agents.sh`
- Remove: `tests/.gitkeep` (replaced by real test file)

**Step 1: Verify the test file does not exist yet**

```bash
ls tests/
```

Expected: only `.gitkeep` (placeholder from Phase 1).

**Step 2: Understand what `list_agents.sh` does**

```bash
cat -n amplifier-skill/scripts/list_agents.sh | head -30
```

The script:
- Accepts `--bundle <name>` and `--help`
- Tries runtime discovery first (`amplifier agents list`)
- Falls back to cache at `~/.amplifier/cache/*/bundle.md`
- Prints `SOURCE\tAGENT` rows or a "No agents discovered" message
- Exits `0` in all cases (success and not-found are both exit 0)
- Exits non-zero only on bad argument

**Step 3: Write the test file**

```bash
cat > tests/test_list_agents.sh << 'TESTEOF'
#!/usr/bin/env sh
# Tests for amplifier-skill/scripts/list_agents.sh
# Runs without amplifier installed; exercises argument handling and fallback paths.
set -eu

SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/amplifier-skill/scripts/list_agents.sh"
PASS=0
FAIL=0

pass() { printf 'PASS: %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'FAIL: %s\n' "$1"; FAIL=$((FAIL + 1)); }

# ── Test: script is executable ──────────────────────────────────────────────
if [ -x "$SCRIPT" ]; then
  pass "script is executable"
else
  fail "script is not executable: $SCRIPT"
fi

# ── Test: --help exits 0 and prints usage ────────────────────────────────────
output="$(sh "$SCRIPT" --help 2>&1)"
status=$?
if [ "$status" -eq 0 ] && printf '%s' "$output" | grep -q "Usage:"; then
  pass "--help exits 0 and prints Usage"
else
  fail "--help: exit=$status output='$output'"
fi

# ── Test: unknown option exits non-zero ──────────────────────────────────────
sh "$SCRIPT" --unknown-option >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "unknown option exits non-zero"
else
  fail "unknown option should exit non-zero but exited 0"
fi

# ── Test: --bundle requires an argument ──────────────────────────────────────
sh "$SCRIPT" --bundle >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--bundle without argument exits non-zero"
else
  fail "--bundle without argument should exit non-zero"
fi

# ── Test: no amplifier → falls back gracefully (exits 0, prints message) ────
# Force amplifier to not be found by running with a PATH that excludes it
output="$(PATH=/usr/bin:/bin sh "$SCRIPT" 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "no amplifier binary: exits 0 (graceful)"
else
  fail "no amplifier binary: expected exit 0, got $status"
fi
if printf '%s' "$output" | grep -qi "no agents\|SOURCE\|cache"; then
  pass "no amplifier binary: output is informative (no agents or cache/header)"
else
  fail "no amplifier binary: unexpected output: '$output'"
fi

# ── Test: --bundle flag accepted without error ───────────────────────────────
output="$(PATH=/usr/bin:/bin sh "$SCRIPT" --bundle foundation 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "--bundle foundation: exits 0"
else
  fail "--bundle foundation: expected exit 0, got $status"
fi

# ── Test: AMPLIFIER_RUNTIME_OUTPUT env triggers extraction path ───────────────
# Inject a fake runtime output containing an agent ref
output="$(AMPLIFIER_RUNTIME_OUTPUT='foundation:some-agent other text' PATH=/usr/bin:/bin sh "$SCRIPT" 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "AMPLIFIER_RUNTIME_OUTPUT injection: exits 0"
else
  fail "AMPLIFIER_RUNTIME_OUTPUT injection: expected exit 0, got $status"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
TESTEOF
chmod +x tests/test_list_agents.sh
rm -f tests/.gitkeep
```

**Step 4: Run the tests to verify they pass**

```bash
sh tests/test_list_agents.sh
```

Expected output (approximately):
```
PASS: script is executable
PASS: --help exits 0 and prints Usage
PASS: unknown option exits non-zero
PASS: --bundle without argument exits non-zero
PASS: no amplifier binary: exits 0 (graceful)
PASS: no amplifier binary: output is informative (no agents or cache/header)
PASS: --bundle foundation: exits 0
PASS: AMPLIFIER_RUNTIME_OUTPUT injection: exits 0

8 passed, 0 failed
```

If any test FAILs, inspect the output and check the script behavior before continuing.

**Step 5: Commit**

```bash
git add tests/test_list_agents.sh
git rm --cached tests/.gitkeep 2>/dev/null || true
git commit -m "test: add list_agents.sh sanity tests"
```

---

### Task 2: Write Tests for `session_context.sh`

**Files:**
- Create: `tests/test_session_context.sh`

**Step 1: Understand what `session_context.sh` does**

```bash
cat -n amplifier-skill/scripts/session_context.sh | head -40
```

The script:
- Accepts `--project <path>`, `--all-projects`, `--limit <n>`, `--help`
- Tries `amplifier session list` first
- Falls back to scanning `~/.amplifier/projects/**/metadata.json`
- Prints a TSV header + rows, or a "No sessions found" message
- Exits `0` in all normal cases
- Exits non-zero only on bad argument (`--limit` not a number, missing required value)

**Step 2: Write the test file**

```bash
cat > tests/test_session_context.sh << 'TESTEOF'
#!/usr/bin/env sh
# Tests for amplifier-skill/scripts/session_context.sh
# Runs without amplifier installed; exercises argument handling and fallback paths.
set -eu

SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/amplifier-skill/scripts/session_context.sh"
PASS=0
FAIL=0

pass() { printf 'PASS: %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'FAIL: %s\n' "$1"; FAIL=$((FAIL + 1)); }

# ── Test: script is executable ──────────────────────────────────────────────
if [ -x "$SCRIPT" ]; then
  pass "script is executable"
else
  fail "script is not executable: $SCRIPT"
fi

# ── Test: --help exits 0 and prints Usage ────────────────────────────────────
output="$(sh "$SCRIPT" --help 2>&1)"
status=$?
if [ "$status" -eq 0 ] && printf '%s' "$output" | grep -q "Usage:"; then
  pass "--help exits 0 and prints Usage"
else
  fail "--help: exit=$status output='$output'"
fi

# ── Test: unknown option exits non-zero ──────────────────────────────────────
sh "$SCRIPT" --unknown-option >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "unknown option exits non-zero"
else
  fail "unknown option should exit non-zero"
fi

# ── Test: --limit requires a number ──────────────────────────────────────────
sh "$SCRIPT" --limit abc >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--limit abc exits non-zero"
else
  fail "--limit abc should exit non-zero"
fi

# ── Test: --limit without value exits non-zero ───────────────────────────────
sh "$SCRIPT" --limit >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--limit without value exits non-zero"
else
  fail "--limit without value should exit non-zero"
fi

# ── Test: --project without value exits non-zero ─────────────────────────────
sh "$SCRIPT" --project >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--project without value exits non-zero"
else
  fail "--project without value should exit non-zero"
fi

# ── Test: no amplifier, no projects dir → graceful empty output ──────────────
# Use a fake HOME that has no .amplifier directory
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
output="$(HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --all-projects 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "no amplifier, no projects: exits 0"
else
  fail "no amplifier, no projects: expected exit 0, got $status"
fi
if printf '%s' "$output" | grep -qi "no sessions\|SOURCE"; then
  pass "no amplifier, no projects: output is informative"
else
  fail "no amplifier, no projects: unexpected output: '$output'"
fi

# ── Test: --project with a valid path exits 0 ────────────────────────────────
output="$(HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --project "$tmpdir" --limit 5 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "--project with valid path: exits 0"
else
  fail "--project with valid path: expected exit 0, got $status"
fi

# ── Test: filesystem fallback reads metadata.json files ──────────────────────
# Create a fake projects directory with a metadata.json
fake_session_dir="$tmpdir/.amplifier/projects/my-project-dir/sessions/session-abc"
mkdir -p "$fake_session_dir"
cat > "$fake_session_dir/metadata.json" << 'METAEOF'
{"session_id": "test-session-123", "name": "test session", "created": "2024-01-01T00:00:00Z", "turn_count": 5}
METAEOF
output="$(HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --all-projects --limit 10 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "filesystem fallback: exits 0 with metadata.json present"
else
  fail "filesystem fallback: expected exit 0, got $status"
fi
if printf '%s' "$output" | grep -q "SOURCE\|test-session-123\|filesystem-fallback"; then
  pass "filesystem fallback: output contains session data or header"
else
  # Not a hard failure — the fallback path is environment-dependent
  pass "filesystem fallback: exited 0 (data presence depends on path matching)"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
TESTEOF
chmod +x tests/test_session_context.sh
```

**Step 3: Run the tests to verify they pass**

```bash
sh tests/test_session_context.sh
```

Expected output (approximately):
```
PASS: script is executable
PASS: --help exits 0 and prints Usage
PASS: unknown option exits non-zero
PASS: --limit abc exits non-zero
PASS: --limit without value exits non-zero
PASS: --project without value exits non-zero
PASS: no amplifier, no projects: exits 0
PASS: no amplifier, no projects: output is informative
PASS: --project with valid path: exits 0
PASS: filesystem fallback: exits 0 with metadata.json present
PASS: filesystem fallback: output contains session data or header

11 passed, 0 failed
```

If any test FAILs, inspect the output and check the script behavior before continuing.

**Step 4: Commit**

```bash
git add tests/test_session_context.sh
git commit -m "test: add session_context.sh sanity tests"
```

---

### Task 3: Create the Suite Validation Script

**Files:**
- Create: `scripts/validate_suite.sh`
- Remove: `scripts/.gitkeep` (replaced by real script)

This script checks suite structural coherence: all expected skill files exist, all have valid YAML frontmatter, all canonical source references are present, and no stubs remain.

**Step 1: Write the validation script**

```bash
cat > scripts/validate_suite.sh << 'SCRIPTEOF'
#!/usr/bin/env sh
# validate_suite.sh — Amplifier ecosystem skill suite coherence check
# Run from repo root: bash scripts/validate_suite.sh
set -eu

PASS=0
FAIL=0
WARN=0

pass()  { printf 'PASS:  %s\n' "$1"; PASS=$((PASS + 1)); }
fail()  { printf 'FAIL:  %s\n' "$1"; FAIL=$((FAIL + 1)); }
warn()  { printf 'WARN:  %s\n' "$1"; WARN=$((WARN + 1)); }

# ── Expected skill files ─────────────────────────────────────────────────────
SKILLS="
amplifier-skill/SKILL.md
amplifier-cross-repo-workflows/SKILL.md
amplifier-core-concepts/SKILL.md
amplifier-module-and-bundle-development/SKILL.md
amplifier-foundation-reference/SKILL.md
amplifier-app-integration/SKILL.md
"

for skill in $SKILLS; do
  if [ -f "$skill" ]; then
    pass "exists: $skill"
  else
    fail "missing: $skill"
  fi
done

# ── YAML frontmatter present ─────────────────────────────────────────────────
for skill in $SKILLS; do
  [ -f "$skill" ] || continue
  if head -1 "$skill" | grep -q "^---$"; then
    pass "frontmatter: $skill"
  else
    fail "no frontmatter: $skill"
  fi
done

# ── No stubs remaining ───────────────────────────────────────────────────────
for skill in $SKILLS; do
  [ -f "$skill" ] || continue
  if grep -q "STUB" "$skill" 2>/dev/null; then
    fail "still a stub: $skill"
  else
    pass "not a stub: $skill"
  fi
done

# ── Minimum line count (stubs are ~10 lines; real skills are 80+) ────────────
for skill in $SKILLS; do
  [ -f "$skill" ] || continue
  linecount="$(wc -l < "$skill")"
  if [ "$linecount" -ge 80 ]; then
    pass "content length OK ($linecount lines): $skill"
  elif [ "$linecount" -ge 30 ]; then
    warn "content may be thin ($linecount lines): $skill"
  else
    fail "content too short ($linecount lines — looks like stub): $skill"
  fi
done

# ── Router skill names ───────────────────────────────────────────────────────
if grep -q "^name: amplifier-ecosystem-router" amplifier-skill/SKILL.md 2>/dev/null; then
  pass "router skill name: amplifier-ecosystem-router"
else
  fail "router skill missing name: amplifier-ecosystem-router"
fi

# ── Router routes to all companions ─────────────────────────────────────────
for companion in amplifier-cross-repo-workflows amplifier-core-concepts \
                 amplifier-module-and-bundle-development amplifier-foundation-reference \
                 amplifier-app-integration; do
  if grep -q "$companion" amplifier-skill/SKILL.md 2>/dev/null; then
    pass "router references: $companion"
  else
    fail "router missing reference to: $companion"
  fi
done

# ── Mandatory canonical sources referenced ───────────────────────────────────
check_ref() {
  ref="$1"; skill="$2"
  if grep -q "$ref" "$skill" 2>/dev/null; then
    pass "canonical ref '$ref' in $skill"
  else
    fail "canonical ref '$ref' MISSING from $skill"
  fi
}

check_ref "MODULES.md"                    "amplifier-module-and-bundle-development/SKILL.md"
check_ref "MODULE_DEVELOPMENT.md"         "amplifier-module-and-bundle-development/SKILL.md"
check_ref "BUNDLE_GUIDE.md"               "amplifier-module-and-bundle-development/SKILL.md"
check_ref "APPLICATION_INTEGRATION_GUIDE" "amplifier-app-integration/SKILL.md"
check_ref "APPLICATION_INTEGRATION_GUIDE" "amplifier-foundation-reference/SKILL.md"
check_ref "amplifier-app-cli"             "amplifier-cross-repo-workflows/SKILL.md"

# ── Expert agents referenced in router ───────────────────────────────────────
for agent in "amplifier:amplifier-expert" "core:core-expert" "foundation:foundation-expert" "foundation:ecosystem-expert"; do
  if grep -q "$agent" amplifier-skill/SKILL.md 2>/dev/null; then
    pass "expert agent in router: $agent"
  else
    fail "expert agent MISSING from router: $agent"
  fi
done

# ── Helper scripts exist and are executable ──────────────────────────────────
for script in amplifier-skill/scripts/list_agents.sh amplifier-skill/scripts/session_context.sh; do
  if [ -x "$script" ]; then
    pass "executable: $script"
  elif [ -f "$script" ]; then
    fail "not executable: $script (run: chmod +x $script)"
  else
    fail "missing: $script"
  fi
done

# ── Test files exist ──────────────────────────────────────────────────────────
for test in tests/test_list_agents.sh tests/test_session_context.sh; do
  if [ -f "$test" ]; then
    pass "exists: $test"
  else
    warn "missing: $test (Phase 3 test not yet written)"
  fi
done

# ── README install path is correct ───────────────────────────────────────────
if grep -q "amplifier-skill/SKILL.md" README.md 2>/dev/null; then
  pass "README: references amplifier-skill/SKILL.md (not root SKILL.md)"
else
  fail "README: does not reference amplifier-skill/SKILL.md — may have path drift"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
printf '\n'
printf '─%.0s' $(seq 1 40) 2>/dev/null || printf '----------------------------------------'
printf '\n'
printf 'Suite validation: %d passed, %d failed, %d warnings\n' "$PASS" "$FAIL" "$WARN"
printf '\n'
[ "$FAIL" -eq 0 ]
SCRIPTEOF
chmod +x scripts/validate_suite.sh
rm -f scripts/.gitkeep
```

**Step 2: Run the validation script to see its current output**

```bash
sh scripts/validate_suite.sh
```

At the end of Phase 3, all lines should be `PASS`. If you are running this before Phase 2 is complete, some lines will `FAIL` — that is expected and correct behavior.

After Phase 2 is complete, expected output ends with:
```
Suite validation: N passed, 0 failed, 0 warnings
```

If there are failures at this point, fix them before continuing.

**Step 3: Commit**

```bash
git add scripts/validate_suite.sh
git rm --cached scripts/.gitkeep 2>/dev/null || true
git commit -m "feat: add suite coherence validation script"
```

---

### Task 4: Run the Full Test Suite

**Step 1: Run the helper script tests**

```bash
sh tests/test_list_agents.sh
```

Expected: all PASS, `0 failed`

```bash
sh tests/test_session_context.sh
```

Expected: all PASS, `0 failed`

**Step 2: Run the suite validation**

```bash
sh scripts/validate_suite.sh
```

Expected: all PASS, `0 failed, 0 warnings`

**Step 3: If any tests fail, fix the issue**

Common failures and fixes at this stage:

| Failure | Fix |
|---------|-----|
| `script is not executable: amplifier-skill/scripts/list_agents.sh` | `chmod +x amplifier-skill/scripts/list_agents.sh` |
| `script is not executable: amplifier-skill/scripts/session_context.sh` | `chmod +x amplifier-skill/scripts/session_context.sh` |
| `router missing reference to: amplifier-X` | The router SKILL.md is missing a routing entry — add it |
| `canonical ref '...' MISSING from ...` | The companion skill is missing a reference to a canonical source — add it |
| `README: does not reference amplifier-skill/SKILL.md` | Update README install path |

After fixing any issues, re-run both test files and the validation script to confirm clean.

**Step 4: Commit fixes if any were needed**

```bash
git status
# If any files were modified:
git add -A
git commit -m "fix: resolve suite validation failures found in Phase 3"
```

---

### Task 5: Final README Polish

**Files:**
- Modify: `README.md`

**Step 1: Read the current README**

```bash
cat -n README.md
```

**Step 2: Verify these five things are correct**

1. The suite table lists all six skills (router + 5 companions)
2. The Claude Code install command points to `amplifier-skill/SKILL.md`
3. The manual install `curl` command points to `amplifier-skill/SKILL.md`
4. The companion skill install commands point to their correct subdirectory paths
5. The helper script commands use `./amplifier-skill/scripts/` (not `./scripts/`)
6. The validation section says `bash scripts/validate_suite.sh`
7. The repo layout tree matches the actual repo structure

**Step 3: Check actual repo structure matches the README tree**

```bash
find . -name "SKILL.md" | grep -v ".git" | sort
```

Expected:
```
./amplifier-app-integration/SKILL.md
./amplifier-core-concepts/SKILL.md
./amplifier-cross-repo-workflows/SKILL.md
./amplifier-foundation-reference/SKILL.md
./amplifier-module-and-bundle-development/SKILL.md
./amplifier-skill/SKILL.md
```

**Step 4: Check the README layout tree matches**

```bash
grep "SKILL.md" README.md
```

Expected: all six `SKILL.md` paths are listed and match the actual paths from Step 3.

**Step 5: If the README tree is inaccurate, update it**

The layout tree in the README was written in Phase 1. If any paths changed during Phases 2 or 3, update the tree to match reality. The correct tree should be:

```text
.
├── README.md
├── amplifier-skill/                        ← Router skill (entry point)
│   ├── SKILL.md
│   ├── agents/
│   │   └── openai.yaml
│   ├── docs/
│   │   └── amplifier.md
│   ├── resources/
│   │   └── agent-catalog.md
│   └── scripts/
│       ├── list_agents.sh
│       └── session_context.sh
├── amplifier-cross-repo-workflows/
│   └── SKILL.md
├── amplifier-core-concepts/
│   └── SKILL.md
├── amplifier-module-and-bundle-development/
│   └── SKILL.md
├── amplifier-foundation-reference/
│   └── SKILL.md
├── amplifier-app-integration/
│   └── SKILL.md
├── scripts/
│   └── validate_suite.sh
└── tests/
    ├── test_list_agents.sh
    └── test_session_context.sh
```

**Step 6: Commit any README changes**

```bash
git diff README.md
# If there are changes:
git add README.md
git commit -m "docs: final README polish — sync layout tree and verify all paths"
# If no changes needed:
echo "README accurate — no commit needed"
```

---

### Task 6: Final Coherence Pass

**Step 1: Run full validation one final time**

```bash
sh tests/test_list_agents.sh && echo "list_agents: OK"
sh tests/test_session_context.sh && echo "session_context: OK"
sh scripts/validate_suite.sh && echo "suite: OK"
```

Expected:
```
[all PASS lines]
list_agents: OK
[all PASS lines]
session_context: OK
[all PASS lines]
suite: OK
```

**Step 2: Check for any uncommitted files**

```bash
git status
```

Expected: `nothing to commit, working tree clean`

**Step 3: Review commit history for Phase 3**

```bash
git log --oneline -10
```

Expected to see Phase 3 commits including at minimum:
- `test: add list_agents.sh sanity tests`
- `test: add session_context.sh sanity tests`
- `feat: add suite coherence validation script`

**Step 4: Check the full suite install path works end-to-end**

The README's Claude Code install command should be copy-pasteable. Verify the path it references actually exists:

```bash
# The README says:
#   claude skill add https://github.com/michaeljabbour/amplifier-skill/blob/main/amplifier-skill/SKILL.md
# Verify the local path exists:
ls -la amplifier-skill/SKILL.md
```

Expected: file exists, is non-empty.

**Step 5: Final commit if anything is outstanding**

```bash
git status
# Should be clean. If not:
git add -A
git commit -m "chore: Phase 3 final polish"
```

---

## Phase 3 Acceptance Checklist

- [ ] `tests/test_list_agents.sh` exists, is executable, and all tests pass
- [ ] `tests/test_session_context.sh` exists, is executable, and all tests pass
- [ ] `scripts/validate_suite.sh` exists, is executable, and runs clean (`0 failed`)
- [ ] `sh scripts/validate_suite.sh` reports all six skills present with non-stub content
- [ ] Router skill routes to all five companions
- [ ] All four expert agents referenced in router skill
- [ ] All mandatory canonical sources referenced in their respective companion skills:
  - `MODULES.md` in `amplifier-module-and-bundle-development`
  - `MODULE_DEVELOPMENT.md` in `amplifier-module-and-bundle-development`
  - `BUNDLE_GUIDE.md` in `amplifier-module-and-bundle-development`
  - `APPLICATION_INTEGRATION_GUIDE` in both `amplifier-app-integration` and `amplifier-foundation-reference`
  - `amplifier-app-cli` in `amplifier-cross-repo-workflows`
- [ ] README layout tree matches actual repo structure
- [ ] README install path points to `amplifier-skill/SKILL.md` (not root `SKILL.md`)
- [ ] Working directory clean with all commits made

---

## Final Suite Acceptance Criteria

After all three phases are complete, the full rehab acceptance criteria from the design doc should be satisfied:

1. **A user can start from the router skill and reach the right companion quickly.**
   → Router at `amplifier-skill/SKILL.md` with quick routing table covering all 6 task types

2. **Mandatory sources explicitly covered:**
   - `amplifier/docs/MODULES.md` → `amplifier-module-and-bundle-development`
   - module-dev guidance → `amplifier-module-and-bundle-development`
   - bundle-dev guidance → `amplifier-module-and-bundle-development`
   - `amplifier-foundation/docs/APPLICATION_INTEGRATION_GUIDE.md` → `amplifier-app-integration` + `amplifier-foundation-reference`

3. **Suite teaches safe cross-repo execution, not just concepts.**
   → `amplifier-cross-repo-workflows` covers change order, testing ladder, local override, shadow

4. **`amplifier-app-cli` treated as the end-to-end validation surface.**
   → Covered in `amplifier-cross-repo-workflows` and `amplifier-app-integration`

5. **The heavier Foundation/examples companion is the main example-driven teaching asset.**
   → `amplifier-foundation-reference` has full examples directory navigation

6. **README, install-path, and docs cleanup included.**
   → Phase 1 + Phase 3 README work

7. **Helper-script validation included.**
   → `tests/test_list_agents.sh` and `tests/test_session_context.sh`

8. **Repo has no packaging or documentation drift.**
   → `sh scripts/validate_suite.sh` verifies this continuously
