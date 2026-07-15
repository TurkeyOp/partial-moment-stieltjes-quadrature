# MAE Project - Round 50 Certificate Package

This package continues the valid Round 49 state and contains the actual Round 50 computer-assisted proof artifacts.

## Main result

All six upper-half problems `(2,3)`, `(3,4)`, `(3,5)`, `(4,5)`, `(4,6)`, and `(4,7)` are certified.

For each problem:

- a radius-`1e-12` Arb box satisfies strict Krawczyk inclusion;
- `||I - YJ(X)||_infinity < 1`;
- the fixed-sign square system has a unique exact zero in the box;
- nodes are ordered, weights are positive, internal extrema are ordered, and `E > 0`;
- interval derivative and curvature tests certify that `E` is the global uniform relative-error norm on `[0.08,0.12]`;
- the existing class-specific alternation theorem therefore excludes a strictly better rule in `A_{n,k}`.

The result does **not** prove global uniqueness among all equal-norm minimizers, independent replication, or interval root certificates for the lower-half rules.

## Reproduction

```bash
python -m pip install -r requirements.txt
./run_round50.sh
```

The scripts use:

- Python-Flint/Arb 0.9.0;
- mpmath 1.3.0;
- 180 decimal digits for Newton centers and Arb evaluation.

## Key files

- `round50_krawczyk_certifier.py`: square system, analytic Jacobian, Newton refinement, interval Jacobian, Krawczyk certificate.
- `round50_jacobian_audit.py`: high-precision derivative audit of the analytic Jacobian.
- `round50_global_minimax_audit.py`: interval monotonicity and curvature proof for the global alternation level.
- `results/round50_certificate.json`: detailed root certificate metadata.
- `results/round50_verified_boxes.csv`: certified boxes and Krawczyk images.
- `results/round50_residual_intervals.csv`: interval residual enclosures.
- `results/round50_global_minimax_audit.json`: global uniform-level audit.
- `manuscript_v2_4/MANUSCRIPT_VERSION_2_4.pdf`: revised 25-page manuscript.
- `SHA256_MANIFEST.csv`: package checksums.
