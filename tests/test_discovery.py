"""Isolated cache/runtime discovery regressions; no personal state or providers."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
class Discovery(unittest.TestCase):
    def test_bundle_filter_does_not_silently_return_other_bundles(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp); root = tmp / "runtime"; (root / "cache/opaque-a").mkdir(parents=True)
            (root / "cache/opaque-b").mkdir()
            (root / "cache/opaque-a/bundle.md").write_text("---\nbundle:\n  name: chosen\nagents:\n  include: [chosen:expert]\n---\n")
            (root / "cache/opaque-b/bundle.md").write_text("---\nbundle:\n  name: other\nagents:\n  include: [other:expert]\n---\n")
            fake = tmp / "bin"; fake.mkdir(); (fake / "amplifier").write_text("#!/bin/sh\nexit 1\n");(fake / "amplifier").chmod(0o755)
            env = dict(os.environ, AMPLIFIER_HOME=str(root), PATH=str(fake)+":/usr/bin:/bin")
            chosen = subprocess.check_output(["sh", str(ROOT / "scripts/list_agents.sh"), "--bundle", "chosen"], env=env, text=True)
            self.assertIn("chosen:expert", chosen);self.assertNotIn("other:expert",chosen)
            absent = subprocess.check_output(["sh", str(ROOT / "scripts/list_agents.sh"), "--bundle", "missing"], env=env, text=True)
            self.assertIn("No agents discovered", absent);self.assertNotIn("other:expert",absent)
    def test_invalid_limit_fails_before_runtime_or_personal_state(self):
        result = subprocess.run(["sh",str(ROOT / "scripts/session_context.sh"),"--limit","oops"],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0);self.assertIn("non-negative",result.stderr)
if __name__ == "__main__":unittest.main()
