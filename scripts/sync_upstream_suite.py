#!/usr/bin/env python3
"""Generate rich portable references from the preserved public source commit."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "4beb46c0937ec9806960b5425be9ccd3ddc47533"
TOPICS = (
    "amplifier-skill", "amplifier-core-concepts",
    "amplifier-module-and-bundle-development", "amplifier-foundation-reference",
    "amplifier-app-integration", "amplifier-cross-repo-workflows",
)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    records = []
    for topic in TOPICS:
        source_path = topic + "/SKILL.md"
        original = subprocess.check_output(["git", "show", SOURCE + ":" + source_path], cwd=ROOT)
        header = (
            "> Preserved upstream topic, not a separate installation or current SDK guarantee. "
            "Read [current contracts](../../current-contracts.md) before using historical commands/code. "
            "The installed Build with Amplifier method governs scope and authority.\n\n"
        ).encode()
        output = header + original
        destination = ROOT / "skills/build-amplifier/references/upstream-suite" / topic / "METHOD.md"
        if args.check:
            if destination.read_bytes() != output:
                raise SystemExit("Upstream reference drift: " + topic)
        else:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(output)
        records.append(dict(source_commit=SOURCE, source_path=source_path,
                            destination=str(destination.relative_to(ROOT)),
                            source_sha256=hashlib.sha256(original).hexdigest(),
                            output_sha256=hashlib.sha256(output).hexdigest(),
                            preservation="Entire original topic body preserved byte-for-byte after a generated authority/version notice."))
    manifest = ROOT / "docs/upstream-suite-manifest.json"
    content = (json.dumps(records, indent=2) + "\n").encode()
    if args.check:
        if manifest.read_bytes() != content:
            raise SystemExit("Upstream source/output manifest drift")
    else:
        manifest.write_bytes(content)
    print("Six upstream topics and source/output hashes match." if args.check else "Generated six preserved upstream topics.")


if __name__ == "__main__":
    main()
