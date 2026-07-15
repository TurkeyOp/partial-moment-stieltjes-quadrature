# Scientific audit decisions — Round 52

## Accepted without change

- Feasible range `0 <= k <= 2n` and dimension `2n-k`.
- Gaussian endpoint identification.
- Difference-numerator degree bound.
- Sufficient alternation result stated as exclusion of a strictly better competitor.
- Exact Chebyshev coefficient-box norm and mixed-risk selector within the finite hierarchy.
- Round 49 scope for rounded operators.
- Round 50 scope for six exact upper-half square systems.

## Clarified in Version 2.5

1. **`b` versus `s=b^2`.** The minimax theorem uses `s`; the nonlinear certificate uses `b`. Strict monotonicity and `2b>0` on the interval make order, stationarity and supremum statements equivalent.
2. **Round 50 endpoint precision finding.** The archived non-rigorous Newton center used import-time `mpmath` endpoint constants. Arb used exact decimal endpoints, so the proof remained valid. A precision-corrected rerun and a separate AD/Arb verifier both certify 6/6 boxes.
3. **Independent reproduction wording.** The new path is independent at code/Jacobian-construction level but is author-produced, not third-party replication.
4. **Round 49 versus Round 50.** The selector certificate concerns rounded published operators; the root certificates concern six exact nonlinear systems. Neither is used to overstate the other.
5. **Data availability.** The public GitHub repository is an older baseline. The manuscript no longer claims that Version 2.5 materials are already publicly archived.

## Claims deliberately not made

- necessity of alternation;
- uniqueness among all equal-norm minimizers;
- global uniqueness outside certified boxes;
- interval root certificates for lower-half rules;
- optimality outside the finite candidate hierarchy;
- shifted-family minimaxity or shift invariance;
- universal superiority;
- exhaustive or first-in-literature novelty.

## Remaining scientific gate

The manuscript is ready for a focused specialist review. The highest-value review questions are theorem assumptions/boundary cases, the derivative/curvature coverage proof, and possible direct prior art under alternative terminology.
