"""CLI tests for the Kubernetes manifest security checker."""

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKER = ROOT / "scripts" / "security_manifest_checker.py"
EXAMPLES = ROOT / "examples" / "exercise-3"


def run_checker(*args):
    return subprocess.run(
        [sys.executable, str(CHECKER), *map(str, args)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


class ManifestCheckerTests(unittest.TestCase):
    def test_unsafe_manifest_fails_default_gate(self):
        result = run_checker(EXAMPLES / "unsafe-deployment.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("HOST_PATH", result.stdout)
        self.assertIn("PRIVILEGED_CONTAINER", result.stdout)
        self.assertIn("RUN_AS_ROOT", result.stdout)
        self.assertIn("Summary:", result.stdout)

    def test_hardened_manifest_passes(self):
        result = run_checker(EXAMPLES / "hardened-deployment.yaml")

        self.assertEqual(result.returncode, 0)
        self.assertIn("Summary: No findings", result.stdout)

    def test_invalid_yaml_fails_gracefully(self):
        result = run_checker(EXAMPLES / "invalid.yaml")

        self.assertEqual(result.returncode, 1)
        self.assertIn("INPUT_ERROR", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_file_fails_gracefully(self):
        missing_file = EXAMPLES / "does-not-exist.yaml"
        result = run_checker(missing_file)

        self.assertEqual(result.returncode, 1)
        self.assertIn("INPUT_ERROR", result.stdout)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
