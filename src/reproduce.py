"""Generate the main numerical tables and figures."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize

from .core import (
    B_MIN,
    B_MAX,
    S_MIN,
    S_MAX,
    absolute_error,
    chebyshev_defects,
    exact_shifted_integral,
    hierarchy_shifted_value,
    load_rules,
    relative_extrema,
    structural_extrema,
    transfer_value,
)


TRANSFER_RHOS = [1.05, 1.10, 1.25, 1.50, 2.0, 3.0, 5.0]
SELECTOR_SPOTS = [
    (1.10, 1e-2), (1.10, 1e2), (1.10, 1e5), (1.10, 1e7),
    (1.25, 1e-1), (1.25, 1e2), (1.25, 1e5), (1.25, 1e7),
    (1.50, 1e-1), (1.50, 1e2), (1.50, 1e4), (1.50, 1e7),
    (2.00, 1e-2), (2.00, 1e1), (2.00, 1e4), (2.00, 1e7),
    (3.00, 1e-2), (3.00, 1e1), (3.00, 1e3), (3.00, 1e6),
    (5.00, 1e-2), (5.00, 1e0), (5.00, 1e3), (5.00, 1e6),
]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def gauss_legendre_8(a, b):
    nodes, weights = leggauss(8)
    result = np.zeros(np.broadcast(a, b).shape, dtype=float)
    for node, weight in zip(nodes, weights):
        result += weight / ((node - a) ** 2 + b**2)
    return result


def composite_simpson_9(a, b):
    nodes = np.linspace(-1.0, 1.0, 9)
    coefficients = np.array(
        [1, 4, 2, 4, 2, 4, 2, 4, 1],
        dtype=float,
    ) * ((2.0 / 8.0) / 3.0)
    result = np.zeros(np.broadcast(a, b).shape, dtype=float)
    for node, coefficient in zip(nodes, coefficients):
        result += coefficient / ((node - a) ** 2 + b**2)
    return result


def reproduce(root: Path) -> dict:
    rules = load_rules(root / "rules/published_n4_rules.json")
    results_dir = root / "results"
    figures_dir = root / "figures"
    results_dir.mkdir(exist_ok=True)
    figures_dir.mkdir(exist_ok=True)

    moment_rows: list[dict] = []
    hierarchy_rows: list[dict] = []
    alternation_rows: list[dict] = []
    structural_rows: list[dict] = []
    transfer_rows: list[dict] = []
    transfer_cache: dict[tuple[int, float], float] = {}
    structural_cache: dict[int, float] = {}

    for k in sorted(rules):
        rule = rules[k]

        for ell in range(9):
            approximate = float(
                np.sum(
                    np.asarray(rule["weights"], dtype=float)
                    * np.asarray(rule["squared_nodes"], dtype=float) ** ell
                )
            )
            target_moment = 1.0 / (2 * ell + 1)
            moment_rows.append({
                "matched_moments_k": k,
                "moment_degree_y": ell,
                "nominally_constrained": bool(ell < k),
                "approximate_moment": approximate,
                "target_moment": target_moment,
                "absolute_residual": abs(approximate - target_moment),
            })

        relative_points, relative_values = relative_extrema(rule)
        signs = np.sign(relative_values)
        magnitudes = np.abs(relative_values)

        hierarchy_rows.append({
            "matched_moments_k": k,
            "all_nodes_inside": bool(
                np.all(np.asarray(rule["nodes"]) > 0.0)
                and np.all(np.asarray(rule["nodes"]) < 1.0)
            ),
            "nodes_ordered": bool(
                np.all(np.diff(np.asarray(rule["nodes"])) > 0.0)
            ),
            "all_weights_positive": bool(
                np.all(np.asarray(rule["weights"]) > 0.0)
            ),
            "expected_alternation_count": 2 * 4 - k + 1,
            "observed_alternation_count": len(relative_points),
            "alternating_signs": bool(
                np.all(signs[:-1] * signs[1:] < 0.0)
            ),
            "worst_relative_error": float(np.max(magnitudes)),
            "relative_magnitude_spread": float(
                (np.max(magnitudes) - np.min(magnitudes))
                / max(np.max(magnitudes), 1e-300)
            ),
        })

        for index, (s_value, error_value) in enumerate(
            zip(relative_points, relative_values)
        ):
            alternation_rows.append({
                "matched_moments_k": k,
                "extremum_index": index,
                "s": float(s_value),
                "b": math.sqrt(float(s_value)),
                "relative_error": float(error_value),
            })

        structural_points, structural_values = structural_extrema(rule)
        worst_index = int(np.argmax(np.abs(structural_values)))
        structural_error = abs(float(structural_values[worst_index]))
        structural_cache[k] = structural_error
        structural_rows.append({
            "matched_moments_k": k,
            "structural_absolute_error": structural_error,
            "worst_b": math.sqrt(float(structural_points[worst_index])),
            "signed_error_at_worst": float(structural_values[worst_index]),
        })

        defects = chebyshev_defects(rule)
        for rho in TRANSFER_RHOS:
            lower, upper = transfer_value(rule, defects, rho)
            transfer_cache[(k, rho)] = upper
            transfer_rows.append({
                "matched_moments_k": k,
                "rho": rho,
                "transfer_lower": lower,
                "transfer_upper": upper,
                "tail_width": upper - lower,
            })

    selector_rows: list[dict] = []
    for rho, tau in SELECTOR_SPOTS:
        risks = np.array([
            transfer_cache[(k, rho)] + tau * structural_cache[k]
            for k in sorted(rules)
        ])
        order = np.argsort(risks)
        selector_rows.append({
            "rho": rho,
            "tau": tau,
            "selected_k": int(order[0]),
            "runner_up_k": int(order[1]),
            "selected_risk": float(risks[order[0]]),
            "runner_up_risk": float(risks[order[1]]),
            "risk_margin": float(risks[order[1]] - risks[order[0]]),
        })

    # Primary shifted-family stress test.
    a_grid = np.linspace(0.0, 0.03, 601)
    b_grid = np.linspace(B_MIN, B_MAX, 241)
    a_mesh, b_mesh = np.meshgrid(a_grid, b_grid, indexing="ij")
    exact = exact_shifted_integral(a_mesh, b_mesh)

    methods = {
        **{f"PMC-k{k}": rules[k] for k in sorted(rules)},
        "Gauss-Legendre-8": None,
        "Composite-Simpson-9": None,
    }
    shift_rows: list[dict] = []

    def method_value(name: str, a, b):
        if name.startswith("PMC-k"):
            return hierarchy_shifted_value(
                rules[int(name.split("k")[1])], a, b
            )
        if name == "Gauss-Legendre-8":
            return gauss_legendre_8(a, b)
        return composite_simpson_9(a, b)

    for name in methods:
        approximation = method_value(name, a_mesh, b_mesh)
        error = np.abs(approximation / exact - 1.0)
        grid_index = np.unravel_index(int(np.argmax(error)), error.shape)
        initial = np.array([
            a_grid[grid_index[0]],
            b_grid[grid_index[1]],
        ])

        def objective(parameters):
            a_value, b_value = parameters
            exact_value = float(exact_shifted_integral(a_value, b_value))
            approx_value = float(method_value(name, a_value, b_value))
            relative = approx_value / exact_value - 1.0
            return -(relative * relative)

        optimized = minimize(
            objective,
            initial,
            method="L-BFGS-B",
            bounds=[(0.0, 0.03), (B_MIN, B_MAX)],
            options={"ftol": 1e-18, "gtol": 1e-12, "maxiter": 1000},
        )
        a_value, b_value = map(float, optimized.x)
        relative = (
            float(method_value(name, a_value, b_value))
            / float(exact_shifted_integral(a_value, b_value))
            - 1.0
        )
        if abs(relative) < float(error[grid_index]):
            a_value = float(a_grid[grid_index[0]])
            b_value = float(b_grid[grid_index[1]])
            relative = (
                float(method_value(name, a_value, b_value))
                / float(exact_shifted_integral(a_value, b_value))
                - 1.0
            )

        shift_rows.append({
            "method": name,
            "evaluations": 8 if name != "Composite-Simpson-9" else 9,
            "worst_relative_error": abs(float(relative)),
            "signed_relative_error": float(relative),
            "worst_a": a_value,
            "worst_b": b_value,
        })

    write_csv(results_dir / "moment_audit.csv", moment_rows)
    write_csv(results_dir / "hierarchy_reproduction.csv", hierarchy_rows)
    write_csv(results_dir / "alternation_points.csv", alternation_rows)
    write_csv(results_dir / "structural_errors.csv", structural_rows)
    write_csv(results_dir / "transfer_functions.csv", transfer_rows)
    write_csv(results_dir / "selector_spots.csv", selector_rows)
    write_csv(results_dir / "shifted_primary_box.csv", shift_rows)

    # Numerical selector map.
    rho_grid = np.linspace(1.05, 5.0, 120)
    tau_grid = np.logspace(-12.0, 12.0, 241)
    transfer_grid = np.zeros((len(rho_grid), len(rules)))
    defects_cache = {k: chebyshev_defects(rules[k]) for k in rules}

    for rho_index, rho in enumerate(rho_grid):
        for k in rules:
            transfer_grid[rho_index, k] = transfer_value(
                rules[k], defects_cache[k], float(rho)
            )[1]

    structural_vector = np.array(
        [structural_cache[k] for k in sorted(rules)]
    )
    risk = (
        transfer_grid[:, None, :]
        + tau_grid[None, :, None] * structural_vector[None, None, :]
    )
    selector = np.argmin(risk, axis=2)

    # Figures.
    hierarchy_array = np.array(
        [row["worst_relative_error"] for row in hierarchy_rows]
    )
    plt.figure(figsize=(7.7, 4.8))
    plt.semilogy(range(5), hierarchy_array, marker="o")
    plt.xlabel("Matched moment depth k")
    plt.ylabel("Worst centered relative error")
    plt.title("Reproduced n=4 Partial-Moment Hierarchy")
    plt.tight_layout()
    plt.savefig(figures_dir / "hierarchy_reproduction.png", dpi=180)
    plt.close()

    plt.figure(figsize=(7.8, 4.9))
    for k in rules:
        values = [
            next(
                row["transfer_upper"]
                for row in transfer_rows
                if row["matched_moments_k"] == k
                and row["rho"] == rho
            )
            for rho in TRANSFER_RHOS
        ]
        plt.semilogy(TRANSFER_RHOS, values, marker="o", label=f"k={k}")
    plt.xlabel(r"$\rho$")
    plt.ylabel(r"$G_k(\rho)$")
    plt.title("Reproduced Transfer Functions")
    plt.legend()
    plt.tight_layout()
    plt.savefig(figures_dir / "transfer_functions.png", dpi=180)
    plt.close()

    plt.figure(figsize=(8.0, 5.0))
    image = plt.imshow(
        selector,
        aspect="auto",
        origin="lower",
        extent=[-12.0, 12.0, 1.05, 5.0],
    )
    plt.colorbar(image, label="Selected k")
    plt.xlabel(r"$\log_{10}\tau$")
    plt.ylabel(r"$\rho$")
    plt.title("Reproduced Numerical Selector Map")
    plt.tight_layout()
    plt.savefig(figures_dir / "selector_map.png", dpi=180)
    plt.close()

    shift_sorted = sorted(
        shift_rows,
        key=lambda row: row["worst_relative_error"],
    )
    plt.figure(figsize=(8.0, 4.8))
    plt.bar(
        [row["method"] for row in shift_sorted],
        [row["worst_relative_error"] for row in shift_sorted],
    )
    plt.yscale("log")
    plt.xticks(rotation=35, ha="right")
    plt.ylabel("Worst relative error")
    plt.title("Shifted-Lorentzian Primary-Box Reproduction")
    plt.tight_layout()
    plt.savefig(figures_dir / "shifted_primary_box.png", dpi=180)
    plt.close()

    summary = {
        "rule_count": len(rules),
        "all_geometry_checks_pass": all(
            row["all_nodes_inside"]
            and row["nodes_ordered"]
            and row["all_weights_positive"]
            for row in hierarchy_rows
        ),
        "all_alternation_counts_pass": all(
            row["expected_alternation_count"]
            == row["observed_alternation_count"]
            for row in hierarchy_rows
        ),
        "all_alternating_signs_pass": all(
            row["alternating_signs"] for row in hierarchy_rows
        ),
        "best_shifted_primary_method": shift_sorted[0]["method"],
        "best_shifted_primary_error":
            shift_sorted[0]["worst_relative_error"],
    }
    (results_dir / "reproduction_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    return summary
