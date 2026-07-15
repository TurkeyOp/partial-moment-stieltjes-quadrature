#!/usr/bin/env python3
"""Independent high-precision audit of the complete n=2,3,4 hierarchy.

This module intentionally does not import the Round 43/44/50 solver code.
It reads only the frozen nodes/weights and alternation tables, then
re-evaluates geometry, moments, relative errors, stationarity, and a dense
continuum screening using separate mpmath/numpy formulas.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np

B_LEFT = mp.mpf("0.08")
B_RIGHT = mp.mpf("0.12")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"No rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def target(b: mp.mpf) -> mp.mpf:
    return 2 * mp.atan(1 / b) / b


def target_prime(b: mp.mpf) -> mp.mpf:
    return -2 / (b * (1 + b * b)) - 2 * mp.atan(1 / b) / (b * b)


def response(y: list[mp.mpf], w: list[mp.mpf], b: mp.mpf) -> mp.mpf:
    return 2 * mp.fsum(wj / (b * b + yj) for yj, wj in zip(y, w))


def response_prime(y: list[mp.mpf], w: list[mp.mpf], b: mp.mpf) -> mp.mpf:
    return -4 * b * mp.fsum(wj / (b * b + yj) ** 2 for yj, wj in zip(y, w))


def relative_error(y: list[mp.mpf], w: list[mp.mpf], b: mp.mpf) -> mp.mpf:
    return response(y, w, b) / target(b) - 1


def relative_error_prime(y: list[mp.mpf], w: list[mp.mpf], b: mp.mpf) -> mp.mpf:
    r = response(y, w, b)
    rp = response_prime(y, w, b)
    f = target(b)
    fp = target_prime(b)
    return (rp * f - r * fp) / (f * f)


def dense_error(y: list[mp.mpf], w: list[mp.mpf], size: int) -> float:
    grid = np.linspace(0.08, 0.12, size, dtype=float)
    yf = np.array([float(v) for v in y], dtype=float)
    wf = np.array([float(v) for v in w], dtype=float)
    f = 2.0 * np.arctan(1.0 / grid) / grid
    q = 2.0 * np.sum(wf[:, None] / (grid[None, :] ** 2 + yf[:, None]), axis=0)
    return float(np.max(np.abs(q / f - 1.0)))


def audit(nodes_path: Path, alternation_path: Path, summary_path: Path, output_dir: Path, grid_size: int) -> dict[str, Any]:
    mp.mp.dps = 100
    node_rows = read_csv(nodes_path)
    alt_rows = read_csv(alternation_path)
    summary_rows = read_csv(summary_path)

    nodes_by: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    alt_by: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    summary_by: dict[tuple[int, int], dict[str, str]] = {}
    for row in node_rows:
        nodes_by[(int(row["node_pairs_n"]), int(row["matched_moments_k"]))].append(row)
    for row in alt_rows:
        alt_by[(int(row["node_pairs_n"]), int(row["matched_moments_k"]))].append(row)
    for row in summary_rows:
        summary_by[(int(row["node_pairs_n"]), int(row["matched_moments_k"]))] = row

    expected_keys = {(n, k) for n in (2, 3, 4) for k in range(2 * n + 1)}
    if set(nodes_by) != expected_keys:
        missing = sorted(expected_keys - set(nodes_by))
        extra = sorted(set(nodes_by) - expected_keys)
        raise ValueError(f"Hierarchy key mismatch; missing={missing}, extra={extra}")

    audit_rows: list[dict[str, Any]] = []
    point_rows: list[dict[str, Any]] = []

    for n, k in sorted(expected_keys):
        nr = sorted(nodes_by[(n, k)], key=lambda row: int(row["node_index"]))
        ar = sorted(alt_by[(n, k)], key=lambda row: int(row["extremum_index"]))
        sr = summary_by[(n, k)]
        y = [mp.mpf(row["squared_node_y"]) for row in nr]
        x = [mp.mpf(row["positive_node_x"]) for row in nr]
        w = [mp.mpf(row["pair_weight"]) for row in nr]

        x_square_res = max(abs(xj * xj - yj) for xj, yj in zip(x, y))
        node_order_margin = min([y[0]] + [y[j + 1] - y[j] for j in range(n - 1)] + [1 - y[-1]])
        min_weight = min(w)
        moment_residuals = [
            abs(mp.fsum(wj * yj ** ell for yj, wj in zip(y, w)) - mp.mpf(1) / (2 * ell + 1))
            for ell in range(k)
        ]
        max_moment = max(moment_residuals, default=mp.mpf("0"))

        supplied_errors: list[mp.mpf] = []
        derivative_residuals: list[mp.mpf] = []
        signs: list[int] = []
        max_point_discrepancy = mp.mpf("0")
        for index, row in enumerate(ar):
            b = mp.mpf(row["b"])
            supplied = mp.mpf(row["relative_error"])
            computed = relative_error(y, w, b)
            discrepancy = abs(computed - supplied)
            max_point_discrepancy = max(max_point_discrepancy, discrepancy)
            supplied_errors.append(computed)
            signs.append(1 if computed > 0 else (-1 if computed < 0 else 0))
            derivative = relative_error_prime(y, w, b)
            is_internal = index not in (0, len(ar) - 1)
            if is_internal:
                derivative_residuals.append(abs(derivative))
            point_rows.append({
                "n": n,
                "k": k,
                "extremum_index": index,
                "b": mp.nstr(b, 30),
                "stored_relative_error": mp.nstr(supplied, 30),
                "recomputed_relative_error": mp.nstr(computed, 30),
                "absolute_discrepancy": mp.nstr(discrepancy, 12),
                "derivative_residual": mp.nstr(abs(derivative), 12),
                "internal": is_internal,
            })

        expected_alternation = 2 * n - k + 1 if k < 2 * n else None
        signs_alternate = all(signs[j + 1] == -signs[j] for j in range(len(signs) - 1))
        amplitude = [abs(value) for value in supplied_errors]
        amplitude_spread = max(amplitude) - min(amplitude) if amplitude else mp.mpf("0")
        max_derivative = max(derivative_residuals, default=mp.mpf("0"))
        extremal_max = max(amplitude)
        dense_max = dense_error(y, w, grid_size)
        published = mp.mpf(sr["worst_relative_error"])
        published_rel_diff = abs(extremal_max - published) / published if published else abs(extremal_max - published)

        endpoint = k == 2 * n
        alternation_count_pass = endpoint or len(ar) == expected_alternation
        alternation_sign_pass = endpoint or signs_alternate
        amplitude_pass = endpoint or amplitude_spread <= mp.mpf("1e-12")
        stationarity_pass = endpoint or max_derivative <= mp.mpf("5e-10")
        dense_screen_pass = dense_max <= float(extremal_max) * (1 + 2e-7) + 1e-15
        geometry_pass = node_order_margin > 0 and min_weight > 0 and x_square_res <= mp.mpf("5e-15")
        moments_pass = max_moment <= mp.mpf("2e-14")
        value_pass = max_point_discrepancy <= mp.mpf("5e-14")
        published_pass = published_rel_diff <= mp.mpf("5e-5")

        audit_rows.append({
            "n": n,
            "k": k,
            "source": nr[0]["source"],
            "rule_type": "gauss_endpoint" if endpoint else ("upper_half" if k > n else "lower_half"),
            "node_pairs": n,
            "moment_count": k,
            "polynomial_exactness_degree": 2 * k - 1,
            "observed_extrema": len(ar),
            "expected_alternation": "endpoint" if endpoint else expected_alternation,
            "minimum_node_order_margin": mp.nstr(node_order_margin, 16),
            "minimum_weight": mp.nstr(min_weight, 16),
            "maximum_x_squared_discrepancy": mp.nstr(x_square_res, 12),
            "maximum_moment_residual": mp.nstr(max_moment, 12),
            "maximum_extremum_value_discrepancy": mp.nstr(max_point_discrepancy, 12),
            "maximum_internal_derivative_residual": mp.nstr(max_derivative, 12),
            "alternation_amplitude_spread": mp.nstr(amplitude_spread, 12),
            "recomputed_extremal_error": mp.nstr(extremal_max, 18),
            "dense_grid_error": f"{dense_max:.18e}",
            "published_error": sr["worst_relative_error"],
            "published_relative_difference": mp.nstr(published_rel_diff, 12),
            "geometry_pass": geometry_pass,
            "moments_pass": moments_pass,
            "alternation_count_pass": alternation_count_pass,
            "alternation_sign_pass": alternation_sign_pass,
            "amplitude_pass": amplitude_pass,
            "stationarity_pass": stationarity_pass,
            "value_reproduction_pass": value_pass,
            "published_error_pass": published_pass,
            "dense_screen_pass": dense_screen_pass,
            "overall_pass": all([
                geometry_pass,
                moments_pass,
                alternation_count_pass,
                alternation_sign_pass,
                amplitude_pass,
                stationarity_pass,
                value_pass,
                published_pass,
                dense_screen_pass,
            ]),
        })

    write_csv(output_dir / "full_hierarchy_audit.csv", audit_rows)
    write_csv(output_dir / "alternation_point_reproduction.csv", point_rows)
    summary = {
        "method": "independent mpmath evaluation plus dense numpy screening",
        "mp_decimal_digits": mp.mp.dps,
        "dense_grid_size": grid_size,
        "rule_count": len(audit_rows),
        "expected_rule_count": 21,
        "all_rules_pass": all(bool(row["overall_pass"]) for row in audit_rows),
        "n2_levels": sum(row["n"] == 2 for row in audit_rows),
        "n3_levels": sum(row["n"] == 3 for row in audit_rows),
        "n4_levels": sum(row["n"] == 4 for row in audit_rows),
        "upper_half_rule_count": sum(row["rule_type"] == "upper_half" for row in audit_rows),
        "maximum_moment_residual": max(float(row["maximum_moment_residual"]) for row in audit_rows),
        "maximum_extremum_value_discrepancy": max(float(row["maximum_extremum_value_discrepancy"]) for row in audit_rows),
        "maximum_internal_derivative_residual": max(float(row["maximum_internal_derivative_residual"]) for row in audit_rows),
        "claim_scope": {
            "proved_by_this_script": [
                "arithmetic consistency of frozen rule data",
                "high-precision moment, geometry, alternation-point and stationarity reproduction",
            ],
            "numerical_only": [
                "dense-grid continuum screening",
            ],
            "not_proved": [
                "global minimax optimality from dense sampling alone",
                "existence of exact roots",
            ],
        },
    }
    (output_dir / "full_hierarchy_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nodes", type=Path, required=True)
    parser.add_argument("--alternation", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--grid-size", type=int, default=50001)
    args = parser.parse_args()
    result = audit(args.nodes, args.alternation, args.summary, args.output_dir, args.grid_size)
    print(json.dumps(result, indent=2))
    return 0 if result["all_rules_pass"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
