#!/usr/bin/env sh
# Compatibility path; the installed canonical helper owns the implementation.
set -eu
exec sh "$(CDPATH= cd -- "$(dirname -- "$0")/../../../.." && pwd)/scripts/session_context.sh" "$@"
