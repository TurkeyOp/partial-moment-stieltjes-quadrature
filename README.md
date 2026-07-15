# Model-Aware Positive Stieltjes Quadrature

Reproducibility repository for the manuscript:

> **Model-Aware Positive Stieltjes Quadrature: From Structural Minimax to Gauss–Legendre**  
> Tran Minh Duc, FPT University, Ho Chi Minh City, Vietnam

This repository contains the current manuscript, the full finite quadrature hierarchy for \(n=2,3,4\), interval certificates, frozen reference data, independent author-produced verification code, and the valid research history through Round 52.

## Current scientific status

- Full hierarchy: **21/21 rules** for \(n=2,3,4\) and \(0\le k\le 2n\).
- Six upper-half nonlinear systems: **6/6 locally existence-and-uniqueness certified** with Krawczyk/Arb boxes.
- Independent forward-AD/Arb code path: **6/6 boxes re-certified** without importing the Round 50 implementation.
- Rounded \(n=4\) mixed-model selector: **99.59563612937927%** of the stated parameter rectangle uniquely certified.
- Current manuscript: `paper/current/MANUSCRIPT_VERSION_2_5.pdf`.

The repository does **not** claim third-party replication, global uniqueness outside the certified boxes, universal superiority, or exhaustive novelty.

## Quick verification

The quick check uses only Python's standard library and validates the frozen public package:

```bash
python quick_verify.py
```

Expected result:

```text
PUBLIC RELEASE QUICK VERIFY: PASS
```

## Full numerical reproduction

Install the locked Python dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-lock.txt
```

Then run:

```bash
python run_full_reproduction.py
```

The full run reproduces the hierarchy audit, Round 49 interval selector certificate, Round 50 Krawczyk certificates, and the independent forward-AD/Arb verification. Building the manuscript additionally requires a LaTeX installation with `latexmk`.

## Repository map

- `paper/current/` — current manuscript source, figures, and frozen PDF.
- `round43/` — full hierarchy nodes, weights, alternation points, and summaries.
- `certificates/round49/` — portable Arb selector certifier.
- `certificates/round50/` — Krawczyk and global minimax interval certifiers.
- `src/` — independent hierarchy and forward-AD/Arb verification paths.
- `data/reference/` — frozen machine-readable reference artifacts.
- `results/` — frozen outputs used for direct comparison.
- `docs/round51/`, `docs/round52/` — reproduction and final scientific-audit reports.
- `specialist_review/` — focused package for theorem, numerical-analysis, and novelty review.
- `archive/` — valid historical artifacts from Rounds 42–50.

See `START_HERE.md` and `PROJECT_MAP.md` for the recommended reading order.

## Citation

Citation metadata is provided in `CITATION.cff`. Until a journal DOI is assigned, cite the manuscript and this repository URL.

## License

The source code in this repository is released under the **MIT License**. See `LICENSE`.

The manuscript and third-party bibliographic material remain subject to their respective copyright terms; the MIT License primarily governs the repository software and associated original code.

## Reproducibility and claim discipline

The repository distinguishes:

1. analytic proof;
2. computer-assisted interval certification;
3. numerical verification;
4. empirical evidence;
5. novelty statements still requiring specialist judgment.

The detailed claim audit is in `docs/round52/THEOREM_CLAIM_AUDIT.csv`.
