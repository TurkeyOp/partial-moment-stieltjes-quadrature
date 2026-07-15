#!/usr/bin/env python3
"""Create a cross-platform SHA-256 manifest.

UTF-8 text files are canonicalized to LF before size/hash calculation so
Windows and Linux checkouts verify identically. Binary files are hashed byte
for byte.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "SHA256_MANIFEST.csv"
SKIP_PARTS = {".git", "__pycache__"}
BINARY_SUFFIXES = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".zip", ".gz",
    ".bz2", ".xz", ".7z", ".npy", ".npz", ".pkl", ".pickle", ".pyc",
    ".so", ".dll", ".dylib", ".exe", ".bin", ".woff", ".woff2", ".ttf",
    ".otf", ".ico",
}


def canonical_bytes(path: Path) -> bytes:
    raw = path.read_bytes()
    if path.suffix.lower() in BINARY_SUFFIXES or b"\x00" in raw:
        return raw
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def included(path: Path) -> bool:
    if not path.is_file() or path == MANIFEST:
        return False
    rel = path.relative_to(ROOT)
    if any(part in SKIP_PARTS for part in rel.parts):
        return False
    rel_posix = rel.as_posix()
    if rel_posix.startswith("results/round52/") and rel_posix.endswith(".log"):
        return False
    return True


def main() -> int:
    rows = []
    for path in sorted(ROOT.rglob("*")):
        if not included(path):
            continue
        payload = canonical_bytes(path)
        rows.append({
            "path": path.relative_to(ROOT).as_posix(),
            "size_bytes": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(),
        })
    with MANIFEST.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["path", "size_bytes", "sha256"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} cross-platform checksums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
