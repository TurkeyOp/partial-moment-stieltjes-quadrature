#!/usr/bin/env python3
"""Reproduce the main tables/figures and run the audit tests."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    for relative in ["results", "figures"]:
        destination = ROOT / relative
        if destination.exists():
            shutil.rmtree(destination)
        destination.mkdir(parents=True)

    sys.path.insert(0, str(ROOT))
    from src.reproduce import reproduce

    summary = reproduce(ROOT)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(ROOT / "tests"),
            "-v",
        ],
        cwd=ROOT,
    )
    if completed.returncode != 0:
        return completed.returncode

    manifest = {
        "completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "rules_sha256": sha256(ROOT / "rules/published_n4_rules.json"),
        "summary": summary,
        "tests_passed": True,
    }
    (ROOT / "results/run_manifest.json").write_text(
        json.dumps(manifest, indent=2),
        encoding="utf-8",
    )
    print()
    print("Reproduction completed successfully.")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
