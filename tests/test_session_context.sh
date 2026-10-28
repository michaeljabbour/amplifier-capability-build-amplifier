#!/usr/bin/env sh
# Tests for amplifier-skill/scripts/session_context.sh
# Runs without amplifier installed; exercises argument handling and fallback paths.
set -eu

SCRIPT="$(cd "$(dirname "$0")/.." && pwd)/skills/build-amplifier/scripts/session_context.sh"
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

# ── Test: --help exits 0 and prints Usage ────────────────────────────────────────
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
  fail "unknown option should exit non-zero"
fi

# ── Test: --limit requires a number ──────────────────────────────────────────────
sh "$SCRIPT" --limit abc >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--limit abc exits non-zero"
else
  fail "--limit abc should exit non-zero"
fi

# ── Test: --limit without value exits non-zero ───────────────────────────────────
sh "$SCRIPT" --limit >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--limit without value exits non-zero"
else
  fail "--limit without value should exit non-zero"
fi

# ── Test: --project without value exits non-zero ─────────────────────────────────
sh "$SCRIPT" --project >/dev/null 2>&1 && status=0 || status=$?
if [ "$status" -ne 0 ]; then
  pass "--project without value exits non-zero"
else
  fail "--project without value should exit non-zero"
fi

# ── Test: no amplifier, no projects dir → graceful empty output ──────────────────
# Use a fake HOME that has no .amplifier directory
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT HUP INT TERM
output="$(AMPLIFIER_HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --all-projects 2>&1)"
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

# ── Test: --project with a valid path exits 0 ────────────────────────────────────
output="$(AMPLIFIER_HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --project "$tmpdir" --limit 5 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "--project with valid path: exits 0"
else
  fail "--project with valid path: expected exit 0, got $status"
fi

# ── Test: filesystem fallback reads metadata.json files ──────────────────────────
# Create a fake projects directory with a metadata.json
fake_session_dir="$tmpdir/projects/my-project-dir/sessions/session-abc"
mkdir -p "$fake_session_dir"
cat > "$fake_session_dir/metadata.json" << 'METAEOF'
{"session_id": "test-session-123", "name": "test session", "created": "2024-01-01T00:00:00Z", "turn_count": 5}
METAEOF
output="$(AMPLIFIER_HOME="$tmpdir" PATH=/usr/bin:/bin sh "$SCRIPT" --all-projects --limit 10 2>&1)"
status=$?
if [ "$status" -eq 0 ]; then
  pass "filesystem fallback: exits 0 with metadata.json present"
else
  fail "filesystem fallback: expected exit 0, got $status"
fi
if printf '%s' "$output" | grep -q "test-session-123"; then
  pass "filesystem fallback: actual session identifier returned"
else
  fail "filesystem fallback: session identifier missing"
fi

# ── Summary ──────────────────────────────────────────────────────────────────────
printf '\n%d passed, %d failed\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
