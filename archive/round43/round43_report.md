# Round 43 — Complete upper-half hierarchy

## Main result

The missing constrained minimax rules were constructed for

\[
(n,k)=(2,3),(3,4),(3,5),(4,5),(4,6),(4,7),
\]

and joined to the lower-half rules and Gaussian endpoints.

All new rules have ordered nodes, positive weights, matched moments,
and the expected \(2n-k+1\) alternating extrema.

## n=4 transition

|   matched_moments_k |   effective_free_parameters |   polynomial_exactness_degree |   worst_relative_error |   relative_deviation_from_extrapolation |   minimum_pair_weight |
|--------------------:|----------------------------:|------------------------------:|-----------------------:|----------------------------------------:|----------------------:|
|                   4 |                           4 |                             7 |            1.09282e-05 |                             -0.00296782 |             0.0765951 |
|                   5 |                           3 |                             9 |            0.000179433 |                             -0.00573135 |             0.101407  |
|                   6 |                           2 |                            11 |            0.00294322  |                             -0.00948061 |             0.149011  |
|                   7 |                           1 |                            13 |            0.0459798   |                             -0.0601742  |             0.126194  |
|                   8 |                           0 |                            15 |            0.43005     |                             -0.466126   |             0.101229  |

The centered structural error progresses as

\[
k=4:\ 1.09	imes10^{-5},
\quad
k=5:\ 1.79	imes10^{-4},
\]

\[
k=6:\ 2.94	imes10^{-3},
\quad
k=7:\ 4.60	imes10^{-2},
\]

\[
k=8:\ 4.30	imes10^{-1}.
\]

The upper-half transition is smooth and remains close to the
approximately constant moment-price pattern through \(k=7\). The final
Gaussian endpoint is already in an order-one error regime.

## Selector impact

Upper-half rules are selected on

\[
50.0932\%
\]

of the tested selector grid. Selected upper-half values are

\[
[5, 6, 7, 8].
\]

Therefore completing the upper half is not merely cosmetic: it changes
the practical rule-selection map whenever this fraction is nonzero.

## Manuscript decision

The manuscript should now define the full feasible hierarchy

\[
0\le k\le2n,
\]

identify \(k=2n\) with Gauss--Legendre, and present the existing
\(k\le n\) regime as the high-structural-accuracy lower half.
