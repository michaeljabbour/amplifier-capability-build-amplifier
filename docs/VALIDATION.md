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
