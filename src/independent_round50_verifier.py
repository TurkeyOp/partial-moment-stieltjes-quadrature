#!/usr/bin/env python3
"""Independent Round 50 Krawczyk reproduction using forward AD.

The original Round 50 certifier uses a handwritten analytic Jacobian.
This verifier reconstructs the same published square systems from frozen
boxes, but obtains both midpoint and interval Jacobians through a small
forward-mode automatic-differentiation implementation. It never imports
Round 50 source code.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypeVar

import mpmath as mp
from flint import arb, ctx

T = TypeVar("T")
PROBLEMS = [(2, 3), (3, 4), (3, 5), (4, 5), (4, 6), (4, 7)]


@dataclass
class Dual(Generic[T]):
    val: T
    der: list[T]

    def _coerce(self, other: Any) -> "Dual[T]":
        if isinstance(other, Dual):
            return other
        return Dual(other, [self.val * 0 for _ in self.der])

    def __add__(self, other: Any) -> "Dual[T]":
        rhs = self._coerce(other)
        return Dual(self.val + rhs.val, [a + b for a, b in zip(self.der, rhs.der)])

    __radd__ = __add__

    def __neg__(self) -> "Dual[T]":
        return Dual(-self.val, [-value for value in self.der])

    def __sub__(self, other: Any) -> "Dual[T]":
        return self + (-self._coerce(other))

    def __rsub__(self, other: Any) -> "Dual[T]":
        return self._coerce(other) - self

    def __mul__(self, other: Any) -> "Dual[T]":
        rhs = self._coerce(other)
        return Dual(
            self.val * rhs.val,
            [a * rhs.val + self.val * b for a, b in zip(self.der, rhs.der)],
        )

    __rmul__ = __mul__

    def reciprocal(self) -> "Dual[T]":
        denominator = self.val * self.val
        return Dual(1 / self.val, [-value / denominator for value in self.der])

    def __truediv__(self, other: Any) -> "Dual[T]":
        return self * self._coerce(other).reciprocal()

    def __rtruediv__(self, other: Any) -> "Dual[T]":
        return self._coerce(other) / self

    def __pow__(self, power: int) -> "Dual[T]":
        if not isinstance(power, int):
            raise TypeError("Dual powers must be integers")
        if power == 0:
            return Dual(self.val * 0 + 1, [self.val * 0 for _ in self.der])
        if power < 0:
            return (self ** (-power)).reciprocal()
        return Dual(
            self.val ** power,
            [power * (self.val ** (power - 1)) * value for value in self.der],
        )


def scalar_atan(value: T) -> T:
    if isinstance(value, arb):
        return value.atan()
    return mp.atan(value)


def dual_atan(value: Dual[T]) -> Dual[T]:
    denominator = 1 + value.val * value.val
    return Dual(scalar_atan(value.val), [entry / denominator for entry in value.der])


def dual_variables(values: list[T]) -> list[Dual[T]]:
    size = len(values)
    variables: list[Dual[T]] = []
    for i, value in enumerate(values):
        zero = value * 0
        derivative = [zero for _ in range(size)]
        derivative[i] = zero + 1
        variables.append(Dual(value, derivative))
    return variables


def system_dual(values: list[T], n: int, k: int, signs: list[int], left: T, right: T) -> list[Dual[T]]:
    z = dual_variables(values)
    d = 2 * n - k
    q = d - 1
    y = z[:n]
    w = z[n : 2 * n]
    internal_b = z[2 * n : 2 * n + q]
    E = z[-1]
    bs: list[Any] = [left] + internal_b + [right]
    equations: list[Dual[T]] = []

    exact_one = z[0].val * 0 + 1
    for ell in range(k):
        moment = sum((w[j] * (y[j] ** ell) for j in range(n)), 0)
        equations.append(moment - exact_one / (2 * ell + 1))

    epsilon: list[Dual[T]] = []
    epsilon_b: list[Dual[T]] = []
    for b_raw in bs:
        if isinstance(b_raw, Dual):
            b = b_raw
        else:
            template = z[0]
            b = Dual(b_raw, [template.val * 0 for _ in template.der])
        F = 2 * dual_atan(1 / b) / b
        Fb = -2 / (b * (1 + b * b)) - 2 * dual_atan(1 / b) / (b * b)
        denominators = [b * b + yj for yj in y]
        response = 2 * sum((w[j] / denominators[j] for j in range(n)), 0)
        response_b = -4 * b * sum((w[j] / (denominators[j] ** 2) for j in range(n)), 0)
        eps = response / F - 1
        eps_b = (response_b * F - response * Fb) / (F * F)
        epsilon.append(eps)
        epsilon_b.append(eps_b)

    for i, eps in enumerate(epsilon):
        equations.append(eps - signs[i] * E)
    equations.extend(epsilon_b[1:-1])

    expected = 4 * n - k
    if len(equations) != expected:
        raise AssertionError(f"System size mismatch for {(n, k)}: {len(equations)} != {expected}")
    return equations


def evaluate_with_jacobian(values: list[T], n: int, k: int, signs: list[int], left: T, right: T) -> tuple[list[T], list[list[T]]]:
    equations = system_dual(values, n, k, signs, left, right)
    return [eq.val for eq in equations], [eq.der for eq in equations]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"No rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def load_signs(path: Path) -> dict[tuple[int, int], list[int]]:
    grouped: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(path):
        grouped[(int(row["node_pairs_n"]), int(row["matched_moments_k"]))].append(row)
    result: dict[tuple[int, int], list[int]] = {}
    for key, rows in grouped.items():
        rows.sort(key=lambda row: int(row["extremum_index"]))
        result[key] = [1 if mp.mpf(row["relative_error"]) > 0 else -1 for row in rows]
    return result


def load_boxes(path: Path) -> dict[tuple[int, int], list[dict[str, str]]]:
    grouped: dict[tuple[int, int], list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(path):
        grouped[(int(row["n"]), int(row["k"]))].append(row)
    return grouped


def abs_upper(value: arb) -> float:
    return float(value.abs_upper())


def mp_to_arb(value: mp.mpf) -> arb:
    return arb(mp.nstr(value, 160))


def names(n: int, k: int) -> list[str]:
    q = 2 * n - k - 1
    return (
        [f"y_{i + 1}" for i in range(n)]
        + [f"w_{i + 1}" for i in range(n)]
        + [f"b_{i + 1}" for i in range(q)]
        + ["E"]
    )


def certify_problem(n: int, k: int, rows: list[dict[str, str]], signs: list[int]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    expected_names = names(n, k)
    actual_names = [row["variable"] for row in rows]
    if actual_names != expected_names:
        raise ValueError(f"Variable order mismatch for {(n, k)}: {actual_names} != {expected_names}")

    center = [mp.mpf(row["center"]) for row in rows]
    radius = mp.mpf(rows[0]["radius"])
    if any(mp.mpf(row["radius"]) != radius for row in rows):
        raise ValueError(f"Nonuniform radius for {(n, k)}")

    mp_values, mp_jacobian_list = evaluate_with_jacobian(center, n, k, signs, mp.mpf("0.08"), mp.mpf("0.12"))
    Jmp = mp.matrix(mp_jacobian_list)
    Ymp = Jmp ** -1
    point_residual = max(abs(value) for value in mp_values)

    X = [arb(mp.nstr(value, 160), mp.nstr(radius, 40)) for value in center]
    z_arb = [mp_to_arb(value) for value in center]
    fpoint, _ = evaluate_with_jacobian(z_arb, n, k, signs, arb("0.08"), arb("0.12"))
    residual_intervals, JX = evaluate_with_jacobian(X, n, k, signs, arb("0.08"), arb("0.12"))
    size = len(center)
    Y = [[mp_to_arb(Ymp[i, j]) for j in range(size)] for i in range(size)]

    B: list[list[arb]] = [[arb(0) for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            product = sum((Y[i][p] * JX[p][j] for p in range(size)), arb(0))
            B[i][j] = (arb(1) if i == j else arb(0)) - product

    zero_balls = [arb(0, mp.nstr(radius, 40)) for _ in range(size)]
    K: list[arb] = []
    margins: list[float] = []
    inclusions: list[bool] = []
    for i in range(size):
        correction = z_arb[i] - sum((Y[i][p] * fpoint[p] for p in range(size)), arb(0))
        image = correction + sum((B[i][j] * zero_balls[j] for j in range(size)), arb(0))
        K.append(image)
        left_margin = image.lower() - X[i].lower()
        right_margin = X[i].upper() - image.upper()
        inclusions.append(bool(left_margin > 0 and right_margin > 0))
        margins.append(min(float(left_margin), float(right_margin)))

    q_norm = max(sum(abs_upper(B[i][j]) for j in range(size)) for i in range(size))
    residual_contains_zero = [bool(value.lower() <= 0 and value.upper() >= 0) for value in residual_intervals]

    y = X[:n]
    w = X[n : 2 * n]
    q = 2 * n - k - 1
    internal_b = X[2 * n : 2 * n + q]
    E = X[-1]
    y_margins = [float(y[0].lower())]
    y_margins.extend(float(y[j + 1].lower() - y[j].upper()) for j in range(n - 1))
    y_margins.append(float(arb(1) - y[-1].upper()))
    weight_margins = [float(value.lower()) for value in w]
    b_margins: list[float] = []
    if internal_b:
        b_margins.append(float(internal_b[0].lower() - arb("0.08")))
        b_margins.extend(float(internal_b[j + 1].lower() - internal_b[j].upper()) for j in range(len(internal_b) - 1))
        b_margins.append(float(arb("0.12") - internal_b[-1].upper()))

    success = all([
        all(inclusions),
        q_norm < 1,
        all(residual_contains_zero),
        min(y_margins) > 0,
        min(weight_margins) > 0,
        not b_margins or min(b_margins) > 0,
        float(E.lower()) > 0,
    ])

    component_rows: list[dict[str, Any]] = []
    for index, variable in enumerate(expected_names):
        component_rows.append({
            "n": n,
            "k": k,
            "variable": variable,
            "center": mp.nstr(center[index], 80),
            "radius": mp.nstr(radius, 12),
            "box_lower": str(X[index].lower()),
            "box_upper": str(X[index].upper()),
            "independent_krawczyk_lower": str(K[index].lower()),
            "independent_krawczyk_upper": str(K[index].upper()),
            "strictly_included": inclusions[index],
            "inclusion_margin": margins[index],
        })

    summary = {
        "n": n,
        "k": k,
        "unknowns": size,
        "equations": len(mp_values),
        "internal_extrema": q,
        "method": "forward automatic differentiation over mpmath and Arb",
        "point_residual_max": mp.nstr(point_residual, 20),
        "krawczyk_q_norm_upper": q_norm,
        "minimum_inclusion_margin": min(margins),
        "minimum_y_ordering_margin": min(y_margins),
        "minimum_weight_lower_bound": min(weight_margins),
        "minimum_b_ordering_margin": min(b_margins) if b_margins else None,
        "E_lower_bound": float(E.lower()),
        "all_components_strictly_included": all(inclusions),
        "all_residual_intervals_contain_zero": all(residual_contains_zero),
        "verdict": "INDEPENDENTLY_CERTIFIED" if success else "FAILED",
    }
    return summary, component_rows


def audit(boxes_path: Path, alternation_path: Path, frozen_summary_path: Path, output_dir: Path, mp_dps: int, arb_dps: int) -> dict[str, Any]:
    mp.mp.dps = mp_dps
    ctx.dps = arb_dps
    boxes = load_boxes(boxes_path)
    signs = load_signs(alternation_path)
    frozen_rows = {(int(row["n"]), int(row["k"])): row for row in read_csv(frozen_summary_path)}

    summaries: list[dict[str, Any]] = []
    components: list[dict[str, Any]] = []
    for problem in PROBLEMS:
        summary, rows = certify_problem(problem[0], problem[1], boxes[problem], signs[problem])
        frozen = frozen_rows[problem]
        summary["frozen_round50_q_norm"] = float(frozen["krawczyk_q_norm_upper"])
        summary["q_norm_relative_difference"] = abs(summary["krawczyk_q_norm_upper"] - summary["frozen_round50_q_norm"]) / summary["frozen_round50_q_norm"]
        summary["agrees_with_frozen_verdict"] = frozen["verdict"] == "CERTIFIED" and summary["verdict"] == "INDEPENDENTLY_CERTIFIED"
        summaries.append(summary)
        components.extend(rows)
        print(problem, summary["verdict"], "qnorm", summary["krawczyk_q_norm_upper"])

    write_csv(output_dir / "independent_krawczyk_summary.csv", summaries)
    write_csv(output_dir / "independent_krawczyk_components.csv", components)
    payload = {
        "method": "independent forward-mode AD Krawczyk verifier",
        "does_not_import_round50_code": True,
        "mp_decimal_digits": mp_dps,
        "arb_decimal_digits": arb_dps,
        "problem_count": len(summaries),
        "all_six_independently_certified": all(row["verdict"] == "INDEPENDENTLY_CERTIFIED" for row in summaries),
        "all_verdicts_agree_with_round50": all(row["agrees_with_frozen_verdict"] for row in summaries),
        "maximum_q_norm_relative_difference": max(row["q_norm_relative_difference"] for row in summaries),
        "problems": summaries,
        "claim_scope": {
            "proved": [
                "strict Krawczyk inclusion for each reconstructed fixed-sign system box",
                "local uniqueness inside each verified box",
                "positive ordered rule geometry inside each box",
            ],
            "not_proved_by_this_verifier": [
                "global uniqueness outside the boxes",
                "global minimax level without the separate interval monotonicity/curvature audit",
                "third-party replication",
            ],
        },
    }
    (output_dir / "independent_krawczyk_results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boxes", type=Path, required=True)
    parser.add_argument("--alternation", type=Path, required=True)
    parser.add_argument("--frozen-summary", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--mp-dps", type=int, default=160)
    parser.add_argument("--arb-dps", type=int, default=160)
    args = parser.parse_args()
    payload = audit(args.boxes, args.alternation, args.frozen_summary, args.output_dir, args.mp_dps, args.arb_dps)
    print(json.dumps({key: value for key, value in payload.items() if key != "problems"}, indent=2))
    return 0 if payload["all_six_independently_certified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
