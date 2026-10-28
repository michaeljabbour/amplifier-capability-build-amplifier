#!/usr/bin/env sh
# Tests for amplifier-skill/scripts/list_agents.sh
# Runs without amplifier installed; exercises argument handling and fallback paths.
set -eu

SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/skills/build-amplifier/scripts/list_agents.sh"
task_root="$(mktemp -d)"
trap 'rm -rf "$task_root"' EXIT HUP INT TERM
export AMPLIFIER_HOME="$task_root"
PASS=0
FAIL=0

pass() { printf 'PASS: %s\n' "$1"; PASS=$((PASS + 1)); }
fail() { printf 'FAIL: %s\n' "$1"; FAIL=$((FAIL + 1)); }

# ── Test: script is executable ──────────────────────────────────────────────────
if [ -x "$SCRIPT" ]; then
  pass "script is executable"
else
  fail "script is not executable: $SCRIPT"
fi

# ── Test: --help exits 0 and prints usage ────────────────────────────────────────
output="$(sh "$SCRIPT" --help 2>&1)"
status=$?
if [ "$status" -eq 0 ] && printf '%s' "$output" | grep -q "Usage:"; then
  pass "--help exits 0 and prints Usage"
else
  fail "--help: exit=$status output='$output'"
fi

# ── Test: unknown option exits non-zero ──────────────────────────────────────────
sh "$SCRIPT" --unknown-option >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "unknown option exits non-zero"
else
  fail "unknown option should exit non-zero but exited 0"
fi

# ── Test: --bundle requires an argument ──────────────────────────────────────────
sh "$SCRIPT" --bundle >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--bundle without argument exits non-zero"
else
  fail "--bundle without argument should exit non-zero"
fi

# ── Test: no amplifier → falls back gracefully (exits 0, prints message) ────────
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

# ── Test: --bundle flag accepted without error ───────────────────────────────────
output="$(PATH=/usr/bin:/bin sh "$SCRIPT" --bundle foundation 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "--bundle foundation: exits 0"
else
  fail "--bundle foundation: expected exit 0, got $status"
fi

# ── Test: AMPLIFIER_RUNTIME_OUTPUT env triggers extraction path ───────────────────
# Inject a fake runtime output containing an agent ref
output="$(AMPLIFIER_RUNTIME_OUTPUT='foundation:some-agent other text' PATH=/usr/bin:/bin sh "$SCRIPT" 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "AMPLIFIER_RUNTIME_OUTPUT injection: exits 0"
else
  fail "AMPLIFIER_RUNTIME_OUTPUT injection: expected exit 0, got $status"
fi

# ── Summary ──────────────────────────────────────────────────────────────────────
printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
