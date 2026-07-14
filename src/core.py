"""Core formulas for the reproducibility package."""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq


S_MIN = 0.08 ** 2
S_MAX = 0.12 ** 2
B_MIN = 0.08
B_MAX = 0.12
CHEBYSHEV_MAX_DEGREE = 500
ROOT_GRID_SIZE = 50001


def load_rules(path: Path) -> dict[int, dict[str, np.ndarray | int]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rules: dict[int, dict[str, np.ndarray | int]] = {}

    for key, record in payload["rules"].items():
        k = int(key)
        nodes = np.array(
            [float(value) for value in record["positive_nodes"]],
            dtype=float,
        )
        weights = np.array(
            [float(value) for value in record["pair_weights"]],
            dtype=float,
        )
        rules[k] = {
            "k": k,
            "nodes": nodes,
            "squared_nodes": nodes * nodes,
            "weights": weights,
            "nominal_exactness_degree":
                int(record["nominal_polynomial_exactness_degree"]),
        }

    return rules


def target(s):
    s = np.asarray(s, dtype=float)
    b = np.sqrt(s)
    return 2.0 * np.arctan(1.0 / b) / b


def target_derivative(s):
    s = np.asarray(s, dtype=float)
    b = np.sqrt(s)
    return (
        -1.0 / (b * b * (1.0 + b * b))
        - np.arctan(1.0 / b) / (b ** 3)
    )


def rational_value(rule, s):
    s = np.asarray(s, dtype=float)
    y = np.asarray(rule["squared_nodes"], dtype=float)
    w = np.asarray(rule["weights"], dtype=float)
    return 2.0 * np.sum(
        w[:, None] / (s[None, :] + y[:, None]),
        axis=0,
    )


def rational_derivative(rule, s):
    s = np.asarray(s, dtype=float)
    y = np.asarray(rule["squared_nodes"], dtype=float)
    w = np.asarray(rule["weights"], dtype=float)
    return -2.0 * np.sum(
        w[:, None] / (s[None, :] + y[:, None]) ** 2,
        axis=0,
    )


def relative_error(rule, s):
    s = np.asarray(s, dtype=float)
    return rational_value(rule, s) / target(s) - 1.0


def relative_error_derivative(rule, s):
    s = np.asarray(s, dtype=float)
    r = rational_value(rule, s)
    dr = rational_derivative(rule, s)
    f = target(s)
    df = target_derivative(s)
    return (dr * f - r * df) / (f * f)


def absolute_error(rule, s):
    s = np.asarray(s, dtype=float)
    return rational_value(rule, s) - target(s)


def absolute_error_derivative(rule, s):
    s = np.asarray(s, dtype=float)
    return rational_derivative(rule, s) - target_derivative(s)


def _scalar(function, rule, value: float) -> float:
    return float(function(rule, np.array([value], dtype=float))[0])


def stationary_points(function, rule) -> np.ndarray:
    grid = np.linspace(S_MIN, S_MAX, ROOT_GRID_SIZE)
    values = function(rule, grid)
    roots: list[float] = []

    for index in range(len(grid) - 1):
        left = float(values[index])
        right = float(values[index + 1])

        if not (math.isfinite(left) and math.isfinite(right)):
            continue
        if left == 0.0:
            roots.append(float(grid[index]))
        elif left * right < 0.0:
            roots.append(
                float(
                    brentq(
                        lambda value: _scalar(function, rule, value),
                        float(grid[index]),
                        float(grid[index + 1]),
                        xtol=1e-15,
                        rtol=1e-14,
                        maxiter=200,
                    )
                )
            )

    unique: list[float] = []
    for root in roots:
        if not unique or abs(root - unique[-1]) > 1e-11:
            unique.append(root)
    return np.array(unique, dtype=float)


def relative_extrema(rule) -> tuple[np.ndarray, np.ndarray]:
    points = np.r_[
        S_MIN,
        stationary_points(relative_error_derivative, rule),
        S_MAX,
    ]
    return points, relative_error(rule, points)


def structural_extrema(rule) -> tuple[np.ndarray, np.ndarray]:
    points = np.r_[
        S_MIN,
        stationary_points(absolute_error_derivative, rule),
        S_MAX,
    ]
    return points, absolute_error(rule, points)


def exact_chebyshev_integral(degree: int) -> float:
    if degree == 0:
        return 2.0
    if degree % 2 == 1:
        return 0.0
    return 2.0 / (1.0 - degree * degree)


def chebyshev_defects(rule) -> np.ndarray:
    nodes = np.asarray(rule["nodes"], dtype=float)
    weights = np.asarray(rule["weights"], dtype=float)
    theta = np.arccos(nodes)
    defects = np.zeros(CHEBYSHEV_MAX_DEGREE + 1, dtype=float)

    for degree in range(CHEBYSHEV_MAX_DEGREE + 1):
        if degree % 2 == 1:
            quadrature = 0.0
        else:
            quadrature = 2.0 * np.dot(
                weights,
                np.cos(degree * theta),
            )
        defects[degree] = (
            exact_chebyshev_integral(degree) - quadrature
        )

    return defects


def transfer_value(rule, defects: np.ndarray, rho: float) -> tuple[float, float]:
    degrees = np.arange(CHEBYSHEV_MAX_DEGREE + 1, dtype=float)
    explicit = float(
        np.sum(rho ** (-degrees) * np.abs(defects))
    )
    full_l1 = 2.0 * float(
        np.sum(np.abs(np.asarray(rule["weights"], dtype=float)))
    )
    tail = (
        (2.0 + full_l1)
        * rho ** (-(CHEBYSHEV_MAX_DEGREE + 1))
        / (1.0 - 1.0 / rho)
    )
    return explicit, explicit + tail


def exact_shifted_integral(a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return (
        np.arctan((1.0 - a) / b)
        + np.arctan((1.0 + a) / b)
    ) / b


def hierarchy_shifted_value(rule, a, b):
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    result = np.zeros(np.broadcast(a, b).shape, dtype=float)

    for node, weight in zip(
        np.asarray(rule["nodes"], dtype=float),
        np.asarray(rule["weights"], dtype=float),
    ):
        result += weight * (
            1.0 / ((node - a) ** 2 + b**2)
            + 1.0 / ((node + a) ** 2 + b**2)
        )
    return result
