#!/usr/bin/env python3
"""Lightweight integrity check for the public GitHub package."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ERRORS: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def read_json(rel: str):
    path = ROOT / rel
    require(path.is_file(), f"Missing required JSON: {rel}")
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def check_manifest() -> None:
    manifest = ROOT / "SHA256_MANIFEST.csv"
    if not manifest.is_file():
        ERRORS.append("Missing SHA256_MANIFEST.csv")
        return
    with manifest.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    require(len(rows) >= 250, f"Manifest unexpectedly small: {len(rows)} entries")
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            ERRORS.append(f"Manifest file missing: {row['path']}")
            continue
        if path.stat().st_size != int(row["size_bytes"]):
            ERRORS.append(f"Manifest size mismatch: {row['path']}")
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != row["sha256"]:
            ERRORS.append(f"Manifest SHA-256 mismatch: {row['path']}")


def main() -> int:
    require((ROOT / "LICENSE").read_text(encoding="utf-8").startswith("MIT License"), "MIT LICENSE missing or altered")
    require((ROOT / "paper/current/MANUSCRIPT_VERSION_2_5.pdf").is_file(), "Current manuscript PDF missing")
    require((ROOT / "paper/current/main.tex").is_file(), "Current manuscript source missing")

    hierarchy = read_json("results/hierarchy/full_hierarchy_summary.json")
    require(hierarchy.get("rule_count") == 21, "Full hierarchy does not contain 21 rules")
    require(hierarchy.get("all_rules_pass") is True, "Frozen hierarchy audit is not PASS")

    independent = read_json("results/independent_round50_precision_fixed/independent_krawczyk_results.json")
    require(independent.get("problem_count") == 6, "Independent verifier does not contain six problems")
    require(independent.get("all_six_independently_certified") is True, "Independent 6/6 certificate flag is not true")

    round49 = read_json("data/reference/round49/round49_interval_results.json")
    require(str(round49.get("certified_fraction")) == "0.995956361293792724609375", "Round 49 certified fraction changed")
    require(round49.get("structural_rules_certified") == 9, "Round 49 does not certify nine rounded rules")

    round50 = read_json("data/reference/round50/round50_certificate.json")
    require(round50.get("all_six_certified") is True, "Round 50 6/6 certificate flag is not true")
    require(len(round50.get("problems", {})) == 6, "Round 50 certificate does not contain six systems")

    prohibited_parts = {"submission", "__pycache__"}
    prohibited_names = {
        "cover_letter_jcam.docx",
        "cover_letter_jcam.pdf",
        "declaration_of_competing_interests_DRAFT.docx",
        "LICENSE_SELECTION_REQUIRED.md",
    }
    for path in ROOT.rglob("*"):
        if any(part in prohibited_parts for part in path.parts):
            ERRORS.append(f"Public package contains prohibited path: {path.relative_to(ROOT)}")
        if path.name in prohibited_names:
            ERRORS.append(f"Public package contains submission-only file: {path.relative_to(ROOT)}")
        if path.is_file() and path.stat().st_size > 100 * 1024 * 1024:
            ERRORS.append(f"File exceeds GitHub 100 MiB limit: {path.relative_to(ROOT)}")

    check_manifest()

    if ERRORS:
        print("PUBLIC RELEASE QUICK VERIFY: FAIL")
        for error in ERRORS[:50]:
            print(f"- {error}")
        return 1
    print("PUBLIC RELEASE QUICK VERIFY: PASS")
    print("- MIT license present")
    print("- 21/21 hierarchy rules frozen as PASS")
    print("- 6/6 independent Krawczyk boxes frozen as certified")
    print("- Round 49 selector fraction matches the certified reference")
    print("- No submission-only or oversized files detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
