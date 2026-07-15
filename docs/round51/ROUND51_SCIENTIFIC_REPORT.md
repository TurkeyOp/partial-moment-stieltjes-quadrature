# Round 51 Scientific Report

## 1. Objective

Round 51 converts the project from a collection of successful research rounds into a reproducible, internally audited repository. Its central question is not whether another impressive numerical example can be produced, but whether the current claims can be reconstructed through separated code paths and whether manuscript, data, code, and certificates agree.

## 2. Inputs and source of truth

The audit uses:

- Round 43 full-hierarchy nodes, weights, extrema, and summary tables;
- the portable Round 49 Arb selector certifier and frozen results;
- Round 50 certificate boxes, source code, and global-level audit;
- Manuscript Version 2.4 and its five figures.

The Round 43 node and alternation SHA-256 hashes exactly match the input hashes embedded in the Round 50 certificate JSON.

## 3. Complete hierarchy reproduction

A separate `mpmath` implementation re-evaluates all levels for `n=2,3,4`, giving 21 rules in total. It does not import the original construction solver.

Results:

- 21/21 rules pass;
- maximum moment residual: `6.27844981593e-16`;
- maximum discrepancy between stored and independently recomputed extremal values: `5.53553065392e-15`;
- maximum internal stationarity residual: `1.47230528639e-13`;
- 5, 7, and 9 levels are present for `n=2,3,4`, respectively;
- a 50,001-point continuum screen finds no error larger than the supplied extremal level within the stated numerical tolerance.

The dense screen is numerical evidence only. It is not used as a substitute for the alternation theorem or interval proof.

## 4. Round 49 exact rerun

The portable Round 49 certifier was executed from source. It reproduced:

- 9 certified rounded `n=4` operators;
- Chebyshev degree 500;
- subdivision depth 24;
- 344,615 visited cells;
- 104,467 certified leaves;
- 67,841 unresolved leaves;
- certified fraction `0.995956361293792724609375`;
- unresolved fraction `0.004043638706207275390625`.

Thus the principal selector statistics are exactly reproducible in the present environment.

## 5. Round 50 archived rerun

The original Round 50 source was rerun without changing its mathematical implementation:

- 6/6 Krawczyk verdicts are `CERTIFIED`;
- the high-precision analytic-Jacobian audit passes for all six systems;
- the interval monotonicity/curvature audit certifies all six global uniform levels;
- the largest derivative subdivision remains `(4,5)` with 6,697 visited subintervals.

## 6. Precision finding and corrected rerun

The audit identified an import-time precision issue in the ordinary-precision center refinement. The archived module constructed `mpmath` endpoint constants before increasing `mp.mp.dps`. This shifts the Newton center system by approximately `1.67e-18` and `-4.44e-18` at the two endpoints.

This does **not** invalidate the Round 50 interval theorem, because the Arb system used exact decimal endpoint balls. It does mean that the archived near-`1e-180` point-residual diagnostic refers to the slightly shifted midpoint system.

A precision-fixed certifier was created. It instantiates endpoints only after the 180-digit context is active. The corrected run certifies all six systems and has maximum point residual below `2e-180` for the intended exact-endpoint system.

## 7. Independent Krawczyk code path

The principal independent verification artifact is `src/independent_round50_verifier.py`.

Differences from Round 50:

- it does not import the Round 50 module;
- it does not use the handwritten analytic Jacobian;
- it propagates derivatives by forward automatic differentiation over both `mpmath` values and Arb balls;
- it rebuilds the Krawczyk operator from the precision-fixed boxes.

All 6/6 systems are independently certified. The largest independently enclosed matrix norm is approximately `6.625e-7`, still far below one, and all componentwise inclusion margins are positive and near `1e-12`.

The independently generated norm upper bounds differ from the handwritten-Jacobian bounds by up to about 26.4% relatively because the automatic-differentiation expression graph gives different interval dependency widths. This is not a contradiction: both bounds are rigorous and several orders of magnitude below one.

## 8. Manuscript and repository audit

Manuscript Version 2.4 was rebuilt from its LaTeX source:

- 25 pages;
- no undefined references or citations;
- no overfull hboxes;
- extracted text hash matches the frozen PDF;
- rendered comparison at 150 dpi reports 0 changed pages and 0 changed pixels.

Cross-artifact audit:

- 35/35 checks pass;
- 0 critical failures;
- 0 major failures.

Automated regression suite:

- 7/7 tests pass.

## 9. What Round 51 proves and does not prove

### Established

- the complete finite hierarchy data are internally reproducible;
- the Round 49 selector certificate reruns exactly;
- the Round 50 archived certificates rerun;
- precision-fixed exact-endpoint Newton centers and Krawczyk boxes certify all six upper-half systems;
- a separate forward-AD/Arb code path independently certifies the six local boxes;
- manuscript, source data, and certificate statistics are consistent.

### Not established

- third-party replication;
- global uniqueness outside the certified boxes;
- independent reimplementation of the global monotonicity/curvature subdivision;
- a clean offline installation from an empty machine without preinstalled packages;
- specialist confirmation of novelty or theorem positioning.

## 10. Round verdict

**Round 51: COMPLETED.**

The project is now ready for **Round 52: final scientific and submission audit**. Round 52 should update the manuscript to incorporate the Round 51 reproducibility result, conduct the final theorem/notation/claim review, refresh literature and JCAM requirements, and build the specialist-review/submission package.
