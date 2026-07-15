#!/usr/bin/env python3
"""Reproduce the main numerical and interval artifacts into reproduced_results/."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "reproduced_results"


def run(name: str, command: list[str], cwd: Path = ROOT) -> None:
    print(f"[{name}] {' '.join(command)}")
    process = subprocess.run(command, cwd=cwd, text=True)
    if process.returncode:
        raise SystemExit(process.returncode)


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    python = sys.executable

    run(
        "full hierarchy",
        [
            python,
            "src/hierarchy_verifier.py",
            "--nodes", "round43/round43_full_hierarchy_nodes_weights.csv",
            "--alternation", "round43/round43_full_hierarchy_alternation.csv",
            "--summary", "round43/round43_full_hierarchy_summary.csv",
            "--output-dir", "reproduced_results/hierarchy",
            "--grid-size", "50001",
        ],
    )

    round49 = OUT / "round49"
    round49.mkdir()
    shutil.copy2(ROOT / "certificates/round49/round49_interval_certifier_portable.py", round49)
    run("Round 49 selector certificate", [python, "round49_interval_certifier_portable.py"], round49)

    run(
        "Round 50 precision-fixed Krawczyk certificate",
        [
            python,
            "certificates/round50/round50_krawczyk_certifier_precision_fixed.py",
            "--nodes-csv", "round43/round43_full_hierarchy_nodes_weights.csv",
            "--alternation-csv", "round43/round43_full_hierarchy_alternation.csv",
            "--output-dir", "reproduced_results/round50",
            "--mp-dps", "180",
            "--arb-dps", "180",
        ],
    )

    run(
        "Independent forward-AD/Arb verification",
        [
            python,
            "src/independent_round50_verifier.py",
            "--boxes", "reproduced_results/round50/round50_verified_boxes.csv",
            "--alternation", "round43/round43_full_hierarchy_alternation.csv",
            "--frozen-summary", "reproduced_results/round50/round50_certificate_summary.csv",
            "--output-dir", "reproduced_results/independent_round50",
            "--mp-dps", "160",
            "--arb-dps", "160",
        ],
    )

    run("Public package verification", [python, "quick_verify.py"])
    print(f"Reproduction outputs written to: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
