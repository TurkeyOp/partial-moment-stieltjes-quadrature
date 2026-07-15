# Round 43 plan — construct the upper-half hierarchy

## Objective

Solve the missing constrained minimax problems

\[
n<k<2n
\]

for \(n=2,3,4\), then join them to the existing lower-half rules and the
known Gaussian endpoint.

## Required outputs

1. Positive nodes and weights for every missing \((n,k)\).
2. Moment residual audit.
3. Alternation count \(2n-k+1\).
4. Worst centered relative error.
5. Comparison with the empirical product law.
6. Positivity and conditioning audit.
7. Selector impact: determine whether any upper-half rule is optimal on
   the existing \((\rho,\tau)\) domain.
8. Manuscript decision:
   - include full hierarchy;
   - or retain lower half and justify exclusion quantitatively.

## Stop conditions

The optimizer result must not be accepted unless:

- all nodes are strictly ordered in \((0,1)\);
- all weights are positive;
- constrained moments are satisfied at high precision;
- the expected alternation count is recovered;
- independent restarts converge to the same error level.

## Scientific question

Does the full hierarchy approach Gauss--Legendre smoothly, or does
structural accuracy collapse before the Gaussian endpoint?
