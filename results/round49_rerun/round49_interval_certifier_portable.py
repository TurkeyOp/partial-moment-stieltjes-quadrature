
from __future__ import annotations

from decimal import Decimal, getcontext
from pathlib import Path
import csv
import functools
import heapq
import json
import math
import time

from flint import arb, ctx
import pandas as pd

ctx.dps = 80
getcontext().prec = 100

ROOT = Path(__file__).resolve().parent
PACKAGE_ROOT = Path(__file__).resolve().parents[2]
NODES_CSV = (
    PACKAGE_ROOT
    / "round43"
    / "round43_full_hierarchy_nodes_weights.csv"
)

B_LEFT = Decimal("0.08")
B_RIGHT = Decimal("0.12")
RHO_LEFT = Decimal("1.05")
RHO_RIGHT = Decimal("5")
T_LEFT = Decimal("-12")
T_RIGHT = Decimal("12")
MAX_DEGREE = 500
MAX_DEPTH = 24


def float_down_from_arb(x: arb) -> float:
    return math.nextafter(float(x.lower()), -math.inf)


def float_up_from_arb(x: arb) -> float:
    return math.nextafter(float(x.upper()), math.inf)


def abs_lower_float(x: arb) -> float:
    return max(
        0.0,
        math.nextafter(float(x.abs_lower()), -math.inf),
    )


def abs_upper_float(x: arb) -> float:
    return math.nextafter(float(x.abs_upper()), math.inf)


def decimal_interval(left: Decimal, right: Decimal) -> arb:
    midpoint = (left + right) / 2
    radius = (right - left) / 2
    return arb(str(midpoint), str(radius))


def decimal_point(value: Decimal) -> arb:
    return arb(str(value))


def add_down(left: float, right: float) -> float:
    return math.nextafter(left + right, -math.inf)


def add_up(left: float, right: float) -> float:
    return math.nextafter(left + right, math.inf)


def multiply_down(left: float, right: float) -> float:
    return math.nextafter(left * right, -math.inf)


def multiply_up(left: float, right: float) -> float:
    return math.nextafter(left * right, math.inf)


def load_rules() -> dict[int, list[tuple[str, str]]]:
    rules: dict[int, list[tuple[str, str]]] = {}
    with NODES_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if int(row["node_pairs_n"]) != 4:
                continue
            k = int(row["matched_moments_k"])
            rules.setdefault(k, []).append(
                (
                    row["positive_node_x"],
                    row["pair_weight"],
                )
            )
    return rules


RULES = load_rules()


def structural_functions(rule: list[tuple[str, str]]):
    nodes = [arb(node) for node, _ in rule]
    weights = [arb(weight) for _, weight in rule]
    squared_nodes = [node * node for node in nodes]

    def error(width: arb) -> arb:
        exact = 2 * (1 / width).atan() / width
        quadrature = sum(
            2 * weight / (width * width + squared_node)
            for weight, squared_node in zip(weights, squared_nodes)
        )
        return exact - quadrature

    def derivative(width: arb) -> arb:
        exact_derivative = (
            -2 / (width * (1 + width * width))
            - 2 * (1 / width).atan() / (width * width)
        )
        quadrature_derivative = sum(
            -4
            * width
            * weight
            / (
                (width * width + squared_node)
                * (width * width + squared_node)
            )
            for weight, squared_node in zip(weights, squared_nodes)
        )
        return exact_derivative - quadrature_derivative

    return error, derivative


def structural_interval_upper(
    error,
    derivative,
    left: Decimal,
    right: Decimal,
) -> float:
    width_ball = decimal_interval(left, right)
    midpoint = (left + right) / 2
    half_width = (right - left) / 2

    direct = error(width_ball)
    mean_value = (
        error(decimal_point(midpoint))
        + derivative(width_ball) * arb(0, str(half_width))
    )
    return min(
        abs_upper_float(direct),
        abs_upper_float(mean_value),
    )


def certify_structural_maximum(
    k: int,
    relative_tolerance: float = 1e-12,
    absolute_tolerance: float = 1e-18,
    maximum_splits: int = 1_000_000,
):
    error, derivative = structural_functions(RULES[k])

    lower = 0.0
    witness = B_LEFT

    # Point witnesses improve the branch-and-bound lower bound.
    for index in range(2001):
        width = (
            B_LEFT
            + (B_RIGHT - B_LEFT)
            * Decimal(index)
            / Decimal(2000)
        )
        value = abs_lower_float(error(decimal_point(width)))
        if value > lower:
            lower = value
            witness = width

    active = []
    counter = 0
    initial_upper = structural_interval_upper(
        error,
        derivative,
        B_LEFT,
        B_RIGHT,
    )
    heapq.heappush(
        active,
        (-initial_upper, counter, B_LEFT, B_RIGHT),
    )
    counter += 1

    maximum_pruned_upper = lower
    split_count = 0

    def threshold() -> float:
        return (
            lower * (1 + relative_tolerance)
            + absolute_tolerance
        )

    while active:
        largest_active_upper = -active[0][0]
        if largest_active_upper <= threshold():
            maximum_pruned_upper = max(
                maximum_pruned_upper,
                largest_active_upper,
            )
            break

        _, _, left, right = heapq.heappop(active)
        midpoint = (left + right) / 2

        point_value = abs_lower_float(
            error(decimal_point(midpoint))
        )
        if point_value > lower:
            lower = point_value
            witness = midpoint

        for child_left, child_right in (
            (left, midpoint),
            (midpoint, right),
        ):
            child_upper = structural_interval_upper(
                error,
                derivative,
                child_left,
                child_right,
            )
            if child_upper <= threshold():
                maximum_pruned_upper = max(
                    maximum_pruned_upper,
                    child_upper,
                )
            else:
                heapq.heappush(
                    active,
                    (
                        -child_upper,
                        counter,
                        child_left,
                        child_right,
                    ),
                )
                counter += 1

        split_count += 1
        if split_count >= maximum_splits:
            raise RuntimeError(
                f"Structural certification did not converge for k={k}."
            )

    active_upper = -active[0][0] if active else lower
    upper = max(
        lower,
        maximum_pruned_upper,
        active_upper,
    )

    return {
        "k": k,
        "lower": lower,
        "upper": upper,
        "relative_width": (upper - lower) / lower,
        "witness_b": str(witness),
        "split_count": split_count,
    }


def compute_defect_intervals():
    records = []
    lower_coefficients = {}
    upper_coefficients = {}
    operator_norm_upper = {}

    for k, rule_strings in RULES.items():
        rule = [
            (arb(node), arb(weight))
            for node, weight in rule_strings
        ]
        lower_values = []
        upper_values = []

        for degree in range(MAX_DEGREE + 1):
            if degree % 2 == 1:
                defect = arb(0)
            else:
                integral = (
                    arb(2)
                    if degree == 0
                    else arb(2) / arb(1 - degree * degree)
                )
                quadrature = sum(
                    2
                    * weight
                    * node.chebyshev_t(degree)
                    for node, weight in rule
                )
                defect = integral - quadrature

            lower = abs_lower_float(defect)
            upper = abs_upper_float(defect)
            lower_values.append(lower)
            upper_values.append(upper)
            records.append(
                {
                    "k": k,
                    "degree": degree,
                    "absolute_defect_lower": lower,
                    "absolute_defect_upper": upper,
                    "interval_width": upper - lower,
                }
            )

        lower_coefficients[k] = lower_values
        upper_coefficients[k] = upper_values
        operator_norm_upper[k] = float_up_from_arb(
            arb(2)
            + sum(2 * weight for _, weight in rule)
        )

    return (
        pd.DataFrame(records),
        lower_coefficients,
        upper_coefficients,
        operator_norm_upper,
    )


def make_g_point_evaluator(
    lower_coefficients,
    upper_coefficients,
    operator_norm_upper,
):
    @functools.lru_cache(maxsize=None)
    def evaluate(k: int, rho_text: str):
        rho_ball = arb(rho_text)
        reciprocal_ball = 1 / rho_ball
        reciprocal_lower = float_down_from_arb(
            reciprocal_ball
        )
        reciprocal_upper = float_up_from_arb(
            reciprocal_ball
        )

        lower = 0.0
        upper = 0.0
        for coefficient_lower, coefficient_upper in zip(
            reversed(lower_coefficients[k]),
            reversed(upper_coefficients[k]),
        ):
            lower = add_down(
                multiply_down(lower, reciprocal_lower),
                coefficient_lower,
            )
            upper = add_up(
                multiply_up(upper, reciprocal_upper),
                coefficient_upper,
            )

        tail = (
            arb(str(operator_norm_upper[k]))
            * reciprocal_ball ** (MAX_DEGREE + 1)
            / (1 - reciprocal_ball)
        )
        upper = add_up(upper, float_up_from_arb(tail))
        return lower, upper

    return evaluate


@functools.lru_cache(maxsize=None)
def tau_point(t_text: str):
    t_ball = arb(t_text)
    value = (t_ball * arb(10).log()).exp()
    return (
        float_down_from_arb(value),
        float_up_from_arb(value),
    )


def certify_selector(
    structural_records,
    lower_coefficients,
    upper_coefficients,
    operator_norm_upper,
):
    structural_lower = {
        int(record["k"]): float(record["lower"])
        for record in structural_records
    }
    structural_upper = {
        int(record["k"]): float(record["upper"])
        for record in structural_records
    }
    g_point = make_g_point_evaluator(
        lower_coefficients,
        upper_coefficients,
        operator_norm_upper,
    )

    def risk_bounds(cell):
        rho_left, rho_right, t_left, t_right = cell
        tau_lower, _ = tau_point(str(t_left))
        _, tau_upper = tau_point(str(t_right))

        lower_bounds = []
        upper_bounds = []
        for k in range(9):
            g_lower, _ = g_point(k, str(rho_right))
            _, g_upper = g_point(k, str(rho_left))
            lower_bounds.append(
                add_down(
                    g_lower,
                    multiply_down(
                        tau_lower,
                        structural_lower[k],
                    ),
                )
            )
            upper_bounds.append(
                add_up(
                    g_upper,
                    multiply_up(
                        tau_upper,
                        structural_upper[k],
                    ),
                )
            )
        return lower_bounds, upper_bounds

    stack = [
        (
            RHO_LEFT,
            RHO_RIGHT,
            T_LEFT,
            T_RIGHT,
            0,
        )
    ]
    certified = []
    unresolved = []
    visited = 0

    while stack:
        rho_left, rho_right, t_left, t_right, depth = (
            stack.pop()
        )
        visited += 1
        lower_bounds, upper_bounds = risk_bounds(
            (rho_left, rho_right, t_left, t_right)
        )

        best = min(range(9), key=upper_bounds.__getitem__)
        competitor_lower = min(
            lower_bounds[index]
            for index in range(9)
            if index != best
        )

        if upper_bounds[best] < competitor_lower:
            certified.append(
                {
                    "rho_lower": str(rho_left),
                    "rho_upper": str(rho_right),
                    "log10_tau_lower": str(t_left),
                    "log10_tau_upper": str(t_right),
                    "depth": depth,
                    "selected_k": best,
                    "winner_upper": upper_bounds[best],
                    "competitor_lower": competitor_lower,
                    "separation_margin": (
                        competitor_lower - upper_bounds[best]
                    ),
                }
            )
            continue

        if depth >= MAX_DEPTH:
            unresolved.append(
                {
                    "rho_lower": str(rho_left),
                    "rho_upper": str(rho_right),
                    "log10_tau_lower": str(t_left),
                    "log10_tau_upper": str(t_right),
                    "depth": depth,
                }
            )
            continue

        normalized_rho_width = (
            (rho_right - rho_left)
            / (RHO_RIGHT - RHO_LEFT)
        )
        normalized_t_width = (
            (t_right - t_left)
            / (T_RIGHT - T_LEFT)
        )

        if normalized_rho_width >= normalized_t_width:
            midpoint = (rho_left + rho_right) / 2
            stack.append(
                (
                    midpoint,
                    rho_right,
                    t_left,
                    t_right,
                    depth + 1,
                )
            )
            stack.append(
                (
                    rho_left,
                    midpoint,
                    t_left,
                    t_right,
                    depth + 1,
                )
            )
        else:
            midpoint = (t_left + t_right) / 2
            stack.append(
                (
                    rho_left,
                    rho_right,
                    midpoint,
                    t_right,
                    depth + 1,
                )
            )
            stack.append(
                (
                    rho_left,
                    rho_right,
                    t_left,
                    midpoint,
                    depth + 1,
                )
            )

    total_area = (
        (RHO_RIGHT - RHO_LEFT)
        * (T_RIGHT - T_LEFT)
    )

    def cell_area(record):
        return (
            (
                Decimal(record["rho_upper"])
                - Decimal(record["rho_lower"])
            )
            * (
                Decimal(record["log10_tau_upper"])
                - Decimal(record["log10_tau_lower"])
            )
        )

    certified_area = sum(
        (cell_area(record) for record in certified),
        Decimal(0),
    )
    unresolved_area = sum(
        (cell_area(record) for record in unresolved),
        Decimal(0),
    )

    fractions = []
    for k in range(9):
        area = sum(
            (
                cell_area(record)
                for record in certified
                if int(record["selected_k"]) == k
            ),
            Decimal(0),
        )
        fractions.append(
            {
                "k": k,
                "certified_coordinate_area": str(area),
                "fraction_of_total_domain": str(
                    area / total_area
                ),
                "fraction_of_certified_area": str(
                    area / certified_area
                ),
            }
        )

    return {
        "certified": pd.DataFrame(certified),
        "unresolved": pd.DataFrame(unresolved),
        "fractions": pd.DataFrame(fractions),
        "visited_cells": visited,
        "certified_area": certified_area,
        "unresolved_area": unresolved_area,
        "total_area": total_area,
        "coverage": certified_area / total_area,
        "unresolved_fraction": unresolved_area / total_area,
        "g_cache": g_point.cache_info()._asdict(),
        "tau_cache": tau_point.cache_info()._asdict(),
    }


def main():
    start = time.time()

    structural_records = [
        certify_structural_maximum(k)
        for k in range(9)
    ]
    structural_frame = pd.DataFrame(structural_records)
    structural_frame.to_csv(
        ROOT / "round49_structural_interval_enclosures.csv",
        index=False,
    )

    (
        defect_frame,
        lower_coefficients,
        upper_coefficients,
        operator_norm_upper,
    ) = compute_defect_intervals()
    defect_frame.to_csv(
        ROOT / "round49_chebyshev_defect_intervals.csv",
        index=False,
    )

    selector = certify_selector(
        structural_records,
        lower_coefficients,
        upper_coefficients,
        operator_norm_upper,
    )
    selector["certified"].to_csv(
        ROOT / "round49_interval_certified_leaves.csv",
        index=False,
    )
    selector["unresolved"].to_csv(
        ROOT / "round49_interval_unresolved_leaves.csv",
        index=False,
    )
    selector["fractions"].to_csv(
        ROOT / "round49_interval_selection_fractions.csv",
        index=False,
    )

    results = {
        "arithmetic": (
            "Python-FLint/Arb 80-digit ball arithmetic; "
            "outward-rounded IEEE-754 aggregation"
        ),
        "maximum_chebyshev_degree": MAX_DEGREE,
        "selector_maximum_depth": MAX_DEPTH,
        "structural_rules_certified": 9,
        "structural_witness_b_all": sorted(
            set(
                record["witness_b"]
                for record in structural_records
            )
        ),
        "maximum_structural_relative_width": max(
            record["relative_width"]
            for record in structural_records
        ),
        "visited_selector_cells": selector["visited_cells"],
        "certified_leaf_count": len(selector["certified"]),
        "unresolved_leaf_count": len(selector["unresolved"]),
        "certified_coordinate_area": str(
            selector["certified_area"]
        ),
        "unresolved_coordinate_area": str(
            selector["unresolved_area"]
        ),
        "total_coordinate_area": str(selector["total_area"]),
        "certified_fraction": str(selector["coverage"]),
        "unresolved_fraction": str(
            selector["unresolved_fraction"]
        ),
        "g_cache": selector["g_cache"],
        "tau_cache": selector["tau_cache"],
        "runtime_seconds": time.time() - start,
    }
    (ROOT / "round49_interval_results.json").write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
