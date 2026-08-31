#!/usr/bin/env python3

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from validate_review_yaml import validate_path


VALID_REVIEW = """\
verification_summary: ran tests
findings:
  - key: stable-key
    position: needs_fix
    severity: minor
    target: src/example.py
    reason: a concrete problem exists
    fix: correct the problem
  - key: accepted-risk
    position: no_fix
    severity: minor
    target: src/example.py
    reason: the behavior is intentional
    fix: no change is required
"""


class ReviewYamlValidatorTests(unittest.TestCase):
    def validate_source(self, source: str) -> list[str]:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "review.yaml"
            path.write_text(source, encoding="utf-8")
            return validate_path(path)

    def test_accepts_valid_review(self) -> None:
        self.assertEqual(self.validate_source(VALID_REVIEW), [])

    def test_accepts_empty_findings(self) -> None:
        source = "verification_summary: ran tests\nfindings: []\n"
        self.assertEqual(self.validate_source(source), [])

    def test_rejects_missing_fix_for_no_fix(self) -> None:
        source = VALID_REVIEW.replace("    fix: no change is required\n", "")
        errors = self.validate_source(source)
        self.assertTrue(any("missing keys: fix" in error for error in errors))

    def test_rejects_duplicate_yaml_keys(self) -> None:
        source = "verification_summary: one\nverification_summary: two\nfindings: []\n"
        errors = self.validate_source(source)
        self.assertTrue(any("duplicate key" in error for error in errors))

    def test_rejects_duplicate_finding_keys(self) -> None:
        source = VALID_REVIEW.replace("key: accepted-risk", "key: stable-key")
        errors = self.validate_source(source)
        self.assertTrue(any("duplicates 'stable-key'" in error for error in errors))

    def test_rejects_invalid_position_and_empty_value(self) -> None:
        source = VALID_REVIEW.replace("position: needs_fix", "position: maybe").replace(
            "severity: minor", "severity: ''", 1
        )
        errors = self.validate_source(source)
        self.assertTrue(any("position must be one of" in error for error in errors))
        self.assertTrue(any("severity must be a non-empty string" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
