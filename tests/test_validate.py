from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate  # noqa: E402


class RouteTests(unittest.TestCase):
    def test_hard_trigger_uses_reviewed_pipeline(self) -> None:
        self.assertEqual(validate.route(hard=1), "REVIEWED_PIPELINE")

    def test_exclusion_overrides_hard_trigger(self) -> None:
        self.assertEqual(validate.route(excluded=True, hard=1), "SINGLE_EXECUTOR")

    def test_two_soft_triggers_use_reviewed_pipeline(self) -> None:
        self.assertEqual(validate.route(soft=2), "REVIEWED_PIPELINE")


class PublicContentTests(unittest.TestCase):
    def test_safe_placeholders_pass(self) -> None:
        self.assertEqual(validate.scan_text(Path("safe.md"), "Root: ${PROJECT_ROOT}"), [])

    def test_windows_user_path_is_rejected(self) -> None:
        sample = "C:" + "\\Users\\example\\project"
        failures = validate.scan_text(Path("bad.md"), sample)
        self.assertTrue(failures)

    def test_fake_github_token_is_rejected(self) -> None:
        sample = "ghp" + "_abcdefghijklmnopqrstuvwxyz123456"
        failures = validate.scan_text(Path("bad.md"), sample)
        self.assertTrue(failures)

    def test_private_key_header_is_rejected(self) -> None:
        sample = "-----BEGIN " + "PRIVATE KEY-----"
        failures = validate.scan_text(Path("bad.md"), sample)
        self.assertTrue(failures)

    def test_missing_required_files_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            failures = validate.validate(Path(temp_dir))
        self.assertTrue(any("missing required file" in item for item in failures))


if __name__ == "__main__":
    unittest.main()
