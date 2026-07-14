"""Audit the generated outputs against frozen reference data."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


class ReproductionTests(unittest.TestCase):
    def test_rule_geometry_and_alternation(self):
        rows = read_csv(ROOT / "results/hierarchy_reproduction.csv")
        self.assertEqual(len(rows), 5)

        for row in rows:
            self.assertEqual(row["all_nodes_inside"], "True")
            self.assertEqual(row["nodes_ordered"], "True")
            self.assertEqual(row["all_weights_positive"], "True")
            self.assertEqual(row["alternating_signs"], "True")
            self.assertEqual(
                int(row["expected_alternation_count"]),
                int(row["observed_alternation_count"]),
            )

    def test_centered_errors_match_frozen_values(self):
        generated = {
            int(row["matched_moments_k"]): float(row["worst_relative_error"])
            for row in read_csv(ROOT / "results/hierarchy_reproduction.csv")
        }
        reference = [
            row
            for row in read_csv(ROOT / "data/reference/hierarchy_summary.csv")
            if int(row["node_pairs_n"]) == 4
        ]

        for row in reference:
            k = int(row["matched_moments_k"])
            target = float(row["minimax_relative_error"])
            relative = abs(generated[k] - target) / target
            self.assertLess(relative, 2e-5)

    def test_structural_errors_inside_certified_intervals(self):
        generated = {
            int(row["matched_moments_k"]):
                float(row["structural_absolute_error"])
            for row in read_csv(ROOT / "results/structural_errors.csv")
        }

        for row in read_csv(ROOT / "data/reference/structural_enclosures.csv"):
            k = int(row["matched_moments_k"])
            lower = float(row["structural_lower"])
            upper = float(row["structural_upper"])
            self.assertGreaterEqual(generated[k], lower)
            self.assertLessEqual(generated[k], upper)

    def test_transfer_functions_match_frozen_values(self):
        generated = {
            (
                int(row["matched_moments_k"]),
                round(float(row["rho"]), 8),
            ): float(row["transfer_upper"])
            for row in read_csv(ROOT / "results/transfer_functions.csv")
        }

        for row in read_csv(ROOT / "data/reference/transfer_functions.csv"):
            rho = round(float(row["rho"]), 8)
            if rho not in {
                1.05, 1.10, 1.25, 1.50, 2.0, 3.0, 5.0
            }:
                continue
            key = (int(row["matched_moments_k"]), rho)
            target = float(row["transfer_upper"])
            relative = abs(generated[key] - target) / target
            tolerance = 5e-7 if rho == 1.05 else 5e-11
            self.assertLess(relative, tolerance)

    def test_selector_spots_match_certified_reference(self):
        generated = {
            (
                round(float(row["rho"]), 8),
                round(math.log10(float(row["tau"])), 8),
            ): int(row["selected_k"])
            for row in read_csv(ROOT / "results/selector_spots.csv")
        }

        scored = 0
        for row in read_csv(ROOT / "data/reference/selector_spots.csv"):
            if row["certified_reference_available"] != "True":
                continue
            key = (
                round(float(row["rho"]), 8),
                round(math.log10(float(row["tau"])), 8),
            )
            self.assertEqual(
                generated[key],
                int(float(row["certified_reference_k"])),
            )
            scored += 1
        self.assertGreaterEqual(scored, 20)

    def test_shifted_primary_box(self):
        generated = {
            row["method"]: float(row["worst_relative_error"])
            for row in read_csv(ROOT / "results/shifted_primary_box.csv")
        }
        reference_rows = [
            row
            for row in read_csv(ROOT / "data/reference/shifted_box_summary.csv")
            if row["box"] == "primary_shift"
        ]
        reference = {
            row["method"]: float(row["worst_relative_error"])
            for row in reference_rows
        }

        self.assertEqual(
            min(generated, key=generated.get),
            "PMC-k0",
        )
        relative = abs(
            generated["PMC-k0"] - reference["PMC-k0"]
        ) / reference["PMC-k0"]
        self.assertLess(relative, 5e-4)
        self.assertLess(
            generated["PMC-k0"],
            generated["Gauss-Legendre-8"],
        )
        self.assertLess(
            generated["PMC-k0"],
            generated["Composite-Simpson-9"],
        )

    def test_summary_file(self):
        payload = json.loads(
            (ROOT / "results/reproduction_summary.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(payload["all_geometry_checks_pass"])
        self.assertTrue(payload["all_alternation_counts_pass"])
        self.assertTrue(payload["all_alternating_signs_pass"])
        self.assertEqual(payload["best_shifted_primary_method"], "PMC-k0")


if __name__ == "__main__":
    unittest.main()
