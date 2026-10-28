# Local validation

Recorded 2026-10-28. These are actual packaging and native software/source checks, not comparative usefulness evidence.

## Isolated discovery regressions

Status: **passed**.

`python3 -m unittest discover -s tests -v`

2 tests; opaque cache-folder bundle filtering and invalid limit handling; stub runtime and dedicated AMPLIFIER_HOME. No personal state or provider used.

## Portable packaging and install

Status: **passed**.

`python3 scripts/capability.py build; python3 scripts/capability.py check; python3 scripts/capability.py doctor; python3 scripts/capability.py install --dest <temporary-parent> (twice)`

All operations passed. No runtime activation or effectiveness measured.

## Skill discovery metadata

Status: **passed**.

`<yaml-enabled-python> /path/to/skill-creator/scripts/quick_validate.py skills/build-amplifier`

Skill is valid. This is a structural check, not a behavioral benchmark.

The [dated machine-readable record](evaluations/2026-10-28/consolidation.json) retains source revisions, check scope, and limitations. Native runtime gates stay separate from installation. No public repository, current service, user installation, or personal source checkout was changed.

## Current public source reconciliation

Normal merge from public main `4beb46c…`, preserving all six complete source topic bodies and assets behind the canonical entry. `python3 scripts/sync_upstream_suite.py --check` and `sh scripts/validate_suite.sh` passed. Retained helper tests passed8 list-agent and11 session checks against isolated `AMPLIFIER_HOME`;2 discovery regressions passed. Portable build/check/doctor,31-file byte-identical clean install plus identical reinstall, and JavaScript syntax checks passed. The [dated merge record](evaluations/2026-10-28/upstream-merge.json) preserves source/output hashes, exact scope and adaptations. No guide body was lost; historical snippets remain accompanied by current-contract caveats. No provider or runtime was activated.
