#!/usr/bin/env sh
# Validate the one-entry suite and exact preservation of all six upstream topics.
set -eu
cd "$(dirname "$0")/.."
python3 scripts/sync_upstream_suite.py --check
python3 - <<'CHECK'
from pathlib import Path
import json
root=Path('.')
entry=root/'skills/build-amplifier/SKILL.md'
manifest=json.loads((root/'docs/upstream-suite-manifest.json').read_text())
assert len(manifest)==6
for item in manifest:
    topic=root/item['destination']
    assert topic.exists() and len(topic.read_text().splitlines())>=80
    link=str(topic.relative_to(entry.parent))
    assert link in entry.read_text(), link
assert len([p for p in root.rglob('SKILL.md') if '_site' not in p.parts and '.git' not in p.parts])==1
for name in ['list_agents.sh','session_context.sh']:
    assert (entry.parent/'scripts'/name).exists()
assert 'skills/build-amplifier' in (root/'README.md').read_text()
print('Six topic routes, complete source bodies, canonical entry/helpers and README agree.')
CHECK
