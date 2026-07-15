# Round 49 - Rigorous interval validation feasibility study

## Decision

The feasibility study succeeded. The former sampled screening can be
replaced by a computer-assisted interval certificate for the rounded
selector.

## Arithmetic

The structural functions and Chebyshev defects were evaluated with
80-decimal-digit Python-FLint/Arb ball arithmetic. Arb is designed for
arbitrary-precision midpoint-radius interval arithmetic with rigorous
error bounds. The selector aggregation uses outward-rounded IEEE-754
operations on nonnegative coefficient bounds.

## Structural maxima

All nine quantities

\[
S_k=\max_{b\in[0.08,0.12]}
|I[L_b]-\widetilde Q_k[L_b]|
\]

were enclosed by adaptive branch-and-bound using both natural interval
extensions and mean-value forms. Every largest lower witness occurs at
\(b=0.08\). The maximum relative enclosure width is
1.437e-10.

## Smooth-risk terms

Absolute Chebyshev defects were enclosed through degree 500. The
infinite remainder was bounded by the operator norm and a geometric
tail. This yields rigorous endpoint bounds for \(G_k(ho)\).

## Selector certificate

- Maximum subdivision depth: 24
- Visited cells: 344,615
- Certified leaves: 104,467
- Unresolved leaves: 67,841
- Certified coordinate-area fraction: 99.595636%
- Unresolved coordinate-area fraction: 0.404364%

A cell is certified only under strict interval separation: the winner's
risk upper bound must lie below every competitor's risk lower bound.

## Interpretation

This result certifies the selector for the **rounded published
operators** and the stated mixed model. It does not certify the existence
or uniqueness of the ideal nonlinear equioscillating solutions.
