#!/usr/bin/env sh
# Retained repository helper path; canonical installed implementation owns behavior.
set -eu
exec sh "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)/skills/build-amplifier/scripts/session_context.sh" "$@"
