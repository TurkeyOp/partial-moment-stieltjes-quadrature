# Start here

## For readers of the manuscript

1. Open `paper/current/MANUSCRIPT_VERSION_2_5.pdf`.
2. Read `docs/round52/ROUND52_SCIENTIFIC_REPORT.md` for the final scientific audit.
3. Read `docs/round52/THEOREM_CLAIM_AUDIT.csv` for the scope of each major claim.
4. Inspect `round43/` for the published hierarchy data.
5. Inspect `data/reference/round49/` and `data/reference/round50/` for the frozen interval certificates.

## For reproducibility reviewers

1. Run `python quick_verify.py`.
2. Create a clean environment from `requirements-lock.txt`.
3. Run `python run_full_reproduction.py`.
4. Compare reproduced outputs with `data/reference/` and `results/`.
5. Read `docs/round51/ROUND51_SCIENTIFIC_REPORT.md` and `docs/round51/ROUND51_PRECISION_FINDING.md`.

## Important scope limits

- The independent verifier is an author-produced independent code path, not a third-party replication.
- Round 49 certifies the selector for rounded published operators over the stated finite hierarchy and parameter rectangle.
- Round 50 certifies unique exact zeros only inside the reported Krawczyk boxes.
- The shifted-family experiment supports local robustness within the tested box, not shifted-family minimax or shift invariance.
