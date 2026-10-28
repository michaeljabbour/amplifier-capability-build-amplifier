#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage: list_agents.sh [--bundle <name>]

List Amplifier agents using runtime commands first, then fall back to cached
bundle manifests under ~/.amplifier/cache/*/bundle.md.

Options:
  --bundle <name>  Target a specific bundle
  --help           Show this help
EOF
}

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

extract_agent_refs() {
  awk '
    {
      line = $0
      while (match(line, /[a-z0-9][a-z0-9-]*:[a-z0-9][a-z0-9-]*/)) {
        token = substr(line, RSTART, RLENGTH)
        next_char = substr(line, RSTART + RLENGTH, 1)
        if (next_char != "/") {
          print token
        }
        line = substr(line, RSTART + RLENGTH)
      }
    }
  ' |
    grep -v '^bundle:' |
    sort -u
}

extract_frontmatter() {
  awk '
    NR == 1 && $0 == "---" {in_frontmatter = 1; next}
    in_frontmatter && $0 == "---" {exit}
    in_frontmatter {print}
  '
}

print_refs() {
  source_name="$1"
  refs="$2"
  [ -n "$refs" ] || return 1

  printf 'SOURCE\tAGENT\n'
  printf '%s\n' "$refs" | while IFS= read -r ref; do
    [ -n "$ref" ] || continue
    printf '%s\t%s\n' "$source_name" "$ref"
  done
  return 0
}

runtime_refs() {
  [ -n "${AMPLIFIER_RUNTIME_OUTPUT:-}" ] || return 1
  refs="$(printf '%s\n' "$AMPLIFIER_RUNTIME_OUTPUT" | extract_agent_refs || true)"
  [ -n "$refs" ] || return 1
  printf '%s\n' "$refs"
}

run_runtime_discovery() {
  if ! command -v amplifier >/dev/null 2>&1; then
    return 1
  fi

  if [ -n "$bundle" ]; then
    AMPLIFIER_RUNTIME_OUTPUT="$(amplifier agents list --bundle "$bundle" 2>/dev/null || true)"
    if refs="$(runtime_refs)"; then
      printf '%s\n' "$refs"
      return 0
    fi

    AMPLIFIER_RUNTIME_OUTPUT="$(amplifier bundle show "$bundle" 2>/dev/null || true)"
    if refs="$(runtime_refs)"; then
      printf '%s\n' "$refs"
      return 0
    fi
    return 1
  fi

  AMPLIFIER_RUNTIME_OUTPUT="$(amplifier agents list 2>/dev/null || true)"
  if refs="$(runtime_refs)"; then
    printf '%s\n' "$refs"
    return 0
  fi

  current_bundle="$(amplifier bundle current 2>/dev/null | sed -nE 's/.*\(([a-z0-9-]+)\).*/\1/p' | head -n 1)"
  if [ -n "$current_bundle" ]; then
    AMPLIFIER_RUNTIME_OUTPUT="$(amplifier bundle show "$current_bundle" 2>/dev/null || true)"
    if refs="$(runtime_refs)"; then
      printf '%s\n' "$refs"
      return 0
    fi
  fi

  return 1
}

run_cache_discovery() {
  cache_root="${AMPLIFIER_HOME:-${HOME}/.amplifier}/cache"
  [ -d "$cache_root" ] || return 1

  tmp_files="$(mktemp)"
  trap 'rm -f "$tmp_files"' EXIT HUP INT TERM

  target_lower="$(printf '%s' "$bundle" | tr '[:upper:]' '[:lower:]')"
  for file in "$cache_root"/*/bundle.md; do
    [ -f "$file" ] || continue
    if [ -n "$bundle" ]; then
      dir_lower="$(basename "$(dirname "$file")" | tr '[:upper:]' '[:lower:]')"
      manifest_name="$(extract_frontmatter <"$file" | awk '/^[[:space:]]*name:/ {sub(/^[[:space:]]*name:[[:space:]]*/, ""); gsub(/[\047\042]/, ""); print; exit}' | tr '[:upper:]' '[:lower:]')"
      case "$dir_lower" in
        *"$target_lower"*) ;;
        *) [ "$manifest_name" = "$target_lower" ] || continue ;;
      esac
    fi
    printf '%s\n' "$file" >>"$tmp_files"
  done

  [ -s "$tmp_files" ] || return 1

  refs="$(
    while IFS= read -r file; do
      extract_frontmatter <"$file" | extract_agent_refs || true
    done <"$tmp_files" | sort -u
  )"
  [ -n "$refs" ] || return 1
  printf '%s\n' "$refs"
}

bundle=''

while [ $# -gt 0 ]; do
  case "$1" in
    --bundle)
      [ $# -ge 2 ] || die "--bundle requires a name"
      bundle="$2"
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "unknown option: $1"
      ;;
  esac
done

if refs="$(run_runtime_discovery)"; then
  print_refs 'runtime' "$refs"
  exit 0
fi

if refs="$(run_cache_discovery)"; then
  print_refs 'cache-fallback' "$refs"
  exit 0
fi

if [ -n "$bundle" ]; then
  printf 'No agents discovered for bundle: %s\n' "$bundle"
else
  printf 'No agents discovered\n'
fi
