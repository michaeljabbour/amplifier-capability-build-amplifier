#!/usr/bin/env sh
set -eu

usage() {
  cat <<'EOF'
Usage: session_context.sh [--project <path> | --all-projects] [--limit <n>]

List Amplifier sessions using CLI commands first, then fall back to scanning
~/.amplifier/projects/**/metadata.json.

Options:
  --project <path>  Project path to query (defaults to current directory)
  --all-projects    Query sessions across all projects
  --limit <n>       Maximum rows to return (default: 10)
  --help            Show this help
EOF
}

die() {
  printf 'Error: %s\n' "$*" >&2
  exit 1
}

is_integer() {
  case "$1" in
    ''|*[!0-9]*) return 1 ;;
    *) return 0 ;;
  esac
}

normalize_path() {
  path="$1"
  if [ -d "$path" ]; then
    (cd "$path" 2>/dev/null && pwd -P) || printf '%s' "$path"
  else
    printf '%s' "$path"
  fi
}

project_key_from_path() {
  printf '%s' "$1" | sed 's#/#-#g; s#^-##'
}

mtime_epoch() {
  target="$1"
  if stat -f '%m' "$target" >/dev/null 2>&1; then
    stat -f '%m' "$target"
    return 0
  fi
  if stat -c '%Y' "$target" >/dev/null 2>&1; then
    stat -c '%Y' "$target"
    return 0
  fi
  printf '0'
}

sanitize_field() {
  printf '%s' "$1" | tr '\r\n\t' '   ' | sed 's/  */ /g; s/^ //; s/ $//'
}

json_string_field() {
  field="$1"
  file="$2"
  sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\"\\([^\"]*\\)\".*/\\1/p" "$file" | head -n 1
}

json_number_field() {
  field="$1"
  file="$2"
  sed -n "s/.*\"$field\"[[:space:]]*:[[:space:]]*\\([0-9][0-9]*\\).*/\\1/p" "$file" | head -n 1
}

print_row_from_file() {
  file="$1"
  project_slug="$(basename "$(dirname "$(dirname "$(dirname "$file")")")")"

  if command -v jq >/dev/null 2>&1; then
    created="$(jq -r '.created // ""' "$file" 2>/dev/null || true)"
    session_id="$(jq -r '.session_id // ""' "$file" 2>/dev/null || true)"
    name="$(jq -r '.name // "unnamed"' "$file" 2>/dev/null || true)"
    description="$(jq -r '.description // ""' "$file" 2>/dev/null || true)"
    turns="$(jq -r '.turn_count // .messages // "?"' "$file" 2>/dev/null || true)"
  else
    created="$(json_string_field created "$file")"
    session_id="$(json_string_field session_id "$file")"
    name="$(json_string_field name "$file")"
    description="$(json_string_field description "$file")"
    turns="$(json_number_field turn_count "$file")"
    [ -n "$name" ] || name='unnamed'
    [ -n "$turns" ] || turns='?'
  fi

  created="$(sanitize_field "$created")"
  session_id="$(sanitize_field "$session_id")"
  name="$(sanitize_field "$name")"
  description="$(sanitize_field "$description")"

  printf 'filesystem-fallback\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "$project_slug" "$session_id" "$created" "$turns" "$name" "$description"
}

try_amplifier_cli() {
  if ! command -v amplifier >/dev/null 2>&1; then
    return 1
  fi

  if [ "$mode" = 'all' ]; then
    amplifier session list --all-projects -n "$limit" 2>/dev/null && return 0
    return 1
  fi

  amplifier session list --project "$project" -n "$limit" 2>/dev/null && return 0
  return 1
}

collect_fallback_candidates() {
  projects_root="${AMPLIFIER_HOME:-${HOME}/.amplifier}/projects"
  [ -d "$projects_root" ] || return 0

  if [ "$mode" = 'all' ]; then
    find "$projects_root" -type f -name metadata.json 2>/dev/null || true
    return 0
  fi

  project_key="$(project_key_from_path "$project")"
  find "$projects_root" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | \
    while IFS= read -r project_dir; do
      base="$(basename "$project_dir")"
      case "$base" in
        *"$project_key"*)
          find "$project_dir" -type f -name metadata.json 2>/dev/null || true
          ;;
      esac
    done
}

mode='project'
project=''
limit='10'

while [ $# -gt 0 ]; do
  case "$1" in
    --project)
      [ $# -ge 2 ] || die "--project requires a path"
      mode='project'
      project="$2"
      shift 2
      ;;
    --all-projects)
      mode='all'
      shift
      ;;
    --limit)
      [ $# -ge 2 ] || die "--limit requires a number"
      limit="$2"
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

is_integer "$limit" || die "--limit must be a non-negative integer"

if [ "$mode" = 'project' ]; then
  if [ -z "$project" ]; then
    project="$(pwd -P)"
  else
    project="$(normalize_path "$project")"
  fi
fi

if try_amplifier_cli; then
  exit 0
fi

tmp_candidates="$(mktemp)"
tmp_sorted="$(mktemp)"
trap 'rm -f "$tmp_candidates" "$tmp_sorted"' EXIT HUP INT TERM

collect_fallback_candidates >"$tmp_candidates"

if [ ! -s "$tmp_candidates" ]; then
  if [ "$mode" = 'all' ]; then
    printf 'No sessions found in ~/.amplifier/projects\n'
  else
    printf 'No sessions found for project: %s\n' "$project"
  fi
  exit 0
fi

while IFS= read -r file; do
  [ -f "$file" ] || continue
  printf '%s\t%s\n' "$(mtime_epoch "$file")" "$file"
done <"$tmp_candidates" | sort -rn | awk -F '\t' '{print $2}' | head -n "$limit" >"$tmp_sorted"

printf 'SOURCE\tPROJECT\tSESSION_ID\tCREATED\tTURNS\tNAME\tDESCRIPTION\n'
while IFS= read -r file; do
  [ -f "$file" ] || continue
  print_row_from_file "$file"
done <"$tmp_sorted"
