from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PublicReleaseTests(unittest.TestCase):
    def test_current_manuscript(self):
        self.assertTrue((ROOT / "paper/current/main.tex").is_file())
        self.assertTrue((ROOT / "paper/current/MANUSCRIPT_VERSION_2_5.pdf").is_file())

    def test_hierarchy(self):
        data = json.loads((ROOT / "results/hierarchy/full_hierarchy_summary.json").read_text())
        self.assertEqual(data["rule_count"], 21)
        self.assertTrue(data["all_rules_pass"])

    def test_round49(self):
        data = json.loads((ROOT / "data/reference/round49/round49_interval_results.json").read_text())
        self.assertEqual(data["structural_rules_certified"], 9)
        self.assertEqual(data["certified_fraction"], "0.995956361293792724609375")

    def test_round50(self):
        data = json.loads((ROOT / "data/reference/round50/round50_certificate.json").read_text())
        self.assertTrue(data["all_six_certified"])
        self.assertEqual(len(data["problems"]), 6)

    def test_independent_verifier(self):
        data = json.loads((ROOT / "results/independent_round50_precision_fixed/independent_krawczyk_results.json").read_text())
        self.assertTrue(data["all_six_independently_certified"])
        self.assertTrue(data["does_not_import_round50_code"])

    def test_no_submission_directory(self):
        self.assertFalse((ROOT / "submission").exists())


if __name__ == "__main__":
    unittest.main()
