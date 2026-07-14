# Partially Moment-Constrained Positive Stieltjes Minimax Quadrature
## Exact Coefficient-Space Risk and Interval-Certified Rule Selection

**Status:** research manuscript draft; novelty not yet confirmed.

## Abstract

We study fixed-budget quadrature for integrands containing a nearly
singular centered Lorentzian component together with an incompletely
specified smooth residual. For \(n\) positive symmetric node pairs, we
introduce a hierarchy indexed by \(k\), \(0\le k\le n\), in which the
associated type-\([n-1|n]\) Stieltjes rational rule matches the first
\(k\) moments at infinity. The endpoints are unrestricted positive
rational minimax approximation (\(k=0\)) and polynomial-exact
quadrature of degree \(2n-1\) (\(k=n\)). We derive a numerator-degree
bound \(2n-k-1\) for differences within a fixed class, yielding a
\(2n-k+1\)-point alternation certificate. High-precision constructions
for \(n=2,3,4\) quantify the price of each added moment condition and
suggest an approximately separable error surface, although no
asymptotic product law is claimed. For smooth residuals described by
Chebyshev coefficient boxes \(|a_j|\le C\rho^{-j}\), we obtain the exact
worst-case quadrature error
\[
C G_k(\rho),\qquad
G_k(\rho)=\sum_{j\ge0}\rho^{-j}|I[T_j]-Q_k[T_j]|.
\]
For the mixed residual-plus-Lorentzian class, the exact normalized risk
is \(G_k(\rho)+\tau S_k\), where \(\tau=c_{\max}/C\) and \(S_k\) is the
structural worst-case error. Finally, numerical interval arithmetic is
applied directly to the published rounded rules. Adaptive subdivision
certifies a unique selected rule on **99.970295%** of the
tested \((\rho,\log_{10}\tau)\) domain, leaving only thin transition
bands unresolved.

## 1. Introduction

Classical Gaussian quadrature allocates its degrees of freedom to
polynomial exactness. This is often effective for smooth integrands, but
it can be inefficient when the dominant difficulty is a nearby pole.
Rationally exact quadrature and generalized Gaussian rules address
known non-polynomial structure, while adaptive methods remain preferable
when little structural information is available.

The intermediate situation is less clear: a practitioner may know that
a positive Markov-type component is present, yet also expect an unknown
smooth background. A rule optimized only for the pole family can be
extremely accurate on the structural component but biased on constants
or low-degree polynomials. A fully polynomial-exact rule protects the
background but sacrifices much of the available structural accuracy.

This paper introduces a parameter \(k\) controlling that trade-off.
The resulting family is not proposed as universally superior. It is a
specialized framework for quantified partial structural information.

### 1.1 Contributions

1. A positive Stieltjes minimax hierarchy indexed by node count \(n\)
   and matched-moment depth \(k\).
2. A zero-count alternation certificate with \(2n-k+1\) extrema.
3. An exact coefficient-box risk and model-aware selector.
4. Interval-certified numerical realization for the distributed rounded
   rules.

The broad ideas of rational quadrature, generalized exactness,
constrained rational minimax and positive worst-case quadrature all have
substantial prior art. The contribution claim is limited to the
specific combined framework described here.

## 2. Model transformation and moment constraints

Let

\[
I[f]=\int_{-1}^{1}f(x)\,dx
\]

and let

\[
B=[b_-,b_+]\subset(0,\infty),
\qquad
S=[\sigma_-,\sigma_+]=[b_-^2,b_+^2].
\]

For \(b>0\), define

\[
L_b(x)=\frac{1}{x^2+b^2}.
\]

After \(s=b^2\) and \(y=x^2\),

\[
F(s)
:=
I[L_{\sqrt{s}}]
=
\int_0^1\frac{y^{-1/2}}{s+y}\,dy
=
\frac{2}{\sqrt{s}}\arctan\frac{1}{\sqrt{s}}.
\]

Thus \(F(s)>0\) for \(s>0\).

A symmetric \(n\)-pair quadrature rule is

\[
Q[f]
=
\sum_{j=1}^{n}
w_j\bigl(f(-x_j)+f(x_j)\bigr),
\]

where

\[
0<x_1<\cdots<x_n<1,
\qquad
w_j>0.
\]

Write \(y_j=x_j^2\). Its structural response is

\[
r_Q(s)
=
Q[L_{\sqrt{s}}]
=
2\sum_{j=1}^{n}\frac{w_j}{s+y_j}.
\]

It has a monic denominator of degree \(n\), poles
\(-y_j\in(-1,0)\), and positive residues \(2w_j\).

### 2.1 Moment-constrained class

For \(0\le k\le n\), define \(\mathcal A_{n,k}\) as the set of positive
symmetric \(n\)-pair rules satisfying

\[
\sum_{j=1}^{n}w_jy_j^\ell
=
\frac{1}{2\ell+1},
\qquad
\ell=0,\ldots,k-1.
\]

For \(k=0\), no moment condition is imposed.

### Lemma 1 — Moment conditions and polynomial exactness

A symmetric rule \(Q\) belongs to \(\mathcal A_{n,k}\) if and only if it
is exact for every polynomial of degree at most \(2k-1\).

#### Proof

Odd polynomials are integrated exactly by symmetry. For an even
monomial,

\[
Q[x^{2\ell}]
=
2\sum_{j=1}^{n}w_jy_j^\ell,
\qquad
I[x^{2\ell}]
=
\frac{2}{2\ell+1}.
\]

Thus exactness for \(\ell=0,\ldots,k-1\) is equivalent to the defining
moment conditions. Together with odd exactness, this is equivalent to
exactness on \(\mathbb P_{2k-1}\). \(\square\)

### Lemma 2 — Moment conditions and Laurent matching

For every integer \(m\ge1\),

\[
F(s)
=
2\sum_{\ell=0}^{m-1}
\frac{(-1)^\ell}{2\ell+1}s^{-\ell-1}
+
O(s^{-m-1})
\]

and

\[
r_Q(s)
=
2\sum_{\ell=0}^{m-1}
(-1)^\ell
\left(
\sum_{j=1}^{n}w_jy_j^\ell
\right)
s^{-\ell-1}
+
O(s^{-m-1})
\]

as \(s\to\infty\). Consequently,

\[
Q\in\mathcal A_{n,k}
\Longleftrightarrow
r_Q(s)-F(s)=O(s^{-k-1}).
\]

#### Proof

The finite geometric expansion of \(1/(s+y)\) has a remainder uniform
for \(y\in[0,1]\). Integrating it against \(y^{-1/2}\,dy\) gives the
expansion of \(F\); summing it against the discrete measure
\(2\sum_jw_j\delta_{y_j}\) gives the expansion of \(r_Q\). The first
\(k\) coefficients agree exactly when the first \(k\) moments agree.
\(\square\)

## 3. Degree reduction and alternation theory

Write

\[
r_i(s)=\frac{p_i(s)}{q_i(s)},
\qquad i=1,2,
\]

where \(q_i\) is monic of degree \(n\) and \(p_i\) has degree at most
\(n-1\).

### Proposition 3 — Degree reduction from shared moments

If \(r_1,r_2\in\mathcal A_{n,k}\), then

\[
r_1(s)-r_2(s)
=
\frac{H(s)}{q_1(s)q_2(s)}
\]

with

\[
\deg H\le2n-k-1,
\]

unless \(H\equiv0\).

#### Proof

The generic numerator \(H=p_1q_2-p_2q_1\) has degree at most
\(2n-1\). Lemma 2 gives

\[
r_1(s)-r_2(s)=O(s^{-k-1}).
\]

Since \(q_1q_2\) is monic of degree \(2n\), a nonzero numerator of
degree \(d\) would imply \(r_1-r_2=O(s^{d-2n})\). Therefore

\[
d-2n\le-k-1,
\]

or \(d\le2n-k-1\). \(\square\)

### 3.1 Alternation certificate

For \(Q\in\mathcal A_{n,k}\), define

\[
\varepsilon_Q(s)
=
\frac{r_Q(s)}{F(s)}-1,
\qquad s\in S.
\]

### Theorem 4 — Conditional minimax certificate

Let \(Q^\star\in\mathcal A_{n,k}\). Suppose there exist

\[
\sigma_-\le s_0<s_1<\cdots<s_{2n-k}\le\sigma_+
\]

and \(E>0\) such that

\[
\|\varepsilon_{Q^\star}\|_{\infty,S}=E
\]

and

\[
\varepsilon_{Q^\star}(s_i)
=
\theta(-1)^iE,
\qquad
\theta\in\{-1,1\}.
\]

Then no \(Q\in\mathcal A_{n,k}\) satisfies

\[
\|\varepsilon_Q\|_{\infty,S}<E.
\]

Hence \(Q^\star\) is minimax in \(\mathcal A_{n,k}\).

#### Proof

Suppose a competitor \(Q\) has strictly smaller uniform error. At every
alternation point, the sign of
\(\varepsilon_{Q^\star}(s_i)-\varepsilon_Q(s_i)\) equals the sign of
\(\varepsilon_{Q^\star}(s_i)\). Because \(F(s)>0\),

\[
\varepsilon_{Q^\star}-\varepsilon_Q
=
\frac{r_{Q^\star}-r_Q}{F}
\]

alternates sign at \(2n-k+1\) points and therefore has at least
\(2n-k\) distinct zeros. Proposition 3 permits at most \(2n-k-1\)
zeros for a nonzero difference numerator. If the rational responses are
identical, the competitor cannot have smaller error. This contradiction
proves the result. \(\square\)

### Remark 5 — Scope

The theorem excludes a strictly better competitor in the stated class.
It does not establish unconditional uniqueness, optimality over
different node counts, or optimality over adaptive algorithms.

## 4. Numerical hierarchy

High-precision equioscillation systems were solved for all
\(0\le k\le n\) with \(n=2,3,4\):

|   node_pairs_n |   matched_moments_k |   polynomial_exactness_degree |   alternation_points |   minimax_relative_error |
|---------------:|--------------------:|------------------------------:|---------------------:|-------------------------:|
|              2 |                   0 |                            -1 |                    5 |              2.37087e-05 |
|              2 |                   1 |                             1 |                    4 |              0.000392337 |
|              2 |                   2 |                             3 |                    3 |              0.00646016  |
|              3 |                   0 |                            -1 |                    7 |              5.94593e-08 |
|              3 |                   1 |                             1 |                    6 |              9.82604e-07 |
|              3 |                   2 |                             3 |                    5 |              1.61736e-05 |
|              3 |                   3 |                             5 |                    4 |              0.000265842 |
|              4 |                   0 |                            -1 |                    9 |              1.49062e-10 |
|              4 |                   1 |                             1 |                    8 |              2.46063e-09 |
|              4 |                   2 |                             3 |                    7 |              4.04864e-08 |
|              4 |                   3 |                             5 |                    6 |              6.65355e-07 |
|              4 |                   4 |                             7 |                    5 |              1.09282e-05 |

All reported rules have negative real rational poles and positive
partial-fraction residues.

### 5.1 Price of exactness

For fixed \(n\), adding one matched moment increases target-family error
by a factor near 16.4 in the computed range. A log-linear fit gives
\[
E_{n,k}
\approx
3.796066
(0.0025036066)^n
(16.4649436816)^k.
\]
This model has a maximum in-sample relative error of
**0.360%** and predicts the held-out \(n=4\) row within
**0.594%**. It remains an empirical observation, not a
convergence theorem.

## 5. Exact coefficient-space risk and selector

For a fixed rule \(Q\), define

\[
\Delta_j(Q)=I[T_j]-Q[T_j].
\]

For \(C\ge0\), \(\rho>1\), define

\[
\mathcal H(C,\rho)
=
\left\{
h(x)=\sum_{j=0}^{\infty}a_jT_j(x):
a_j\in\mathbb R,\;
|a_j|\le C\rho^{-j}
\right\}.
\]

The coefficient condition gives uniform convergence on \([-1,1]\).

### Theorem 6 — Exact coefficient-box norm

For every fixed quadrature rule \(Q\),

\[
\sup_{h\in\mathcal H(C,\rho)}
|I[h]-Q[h]|
=
C G_Q(\rho),
\]

where

\[
G_Q(\rho)
=
\sum_{j=0}^{\infty}
\rho^{-j}|\Delta_j(Q)|.
\]

#### Proof

Bounded linearity and uniform convergence give

\[
I[h]-Q[h]
=
\sum_{j=0}^{\infty}a_j\Delta_j(Q).
\]

The triangle inequality gives the upper bound. It is attained by

\[
a_j^\star
=
C\rho^{-j}
\operatorname{sign}\Delta_j(Q),
\]

with \(\operatorname{sign}(0)=0\). \(\square\)

### 5.1 Exact mixed-class risk

Define

\[
S_Q
=
\max_{b\in B}|I[L_b]-Q[L_b]|.
\]

The maximum exists by continuity and compactness.

### Theorem 7 — Additive exact worst-case risk

For

\[
f=h+cL_b,
\qquad
h\in\mathcal H(C,\rho),
\quad
|c|\le c_{\max},
\quad
b\in B,
\]

one has

\[
\sup_f|I[f]-Q[f]|
=
C G_Q(\rho)+c_{\max}S_Q.
\]

#### Proof

The triangle inequality gives the upper bound. Select \(b^\star\)
attaining \(S_Q\), choose the sign of \(c\) to make the structural
error positive, and independently choose the sign-aligned extremizer
from Theorem 6. Their errors add with the same sign. \(\square\)

### Corollary 8 — Exact model-aware selector

For rules \(Q_0,\ldots,Q_m\) and \(C>0\), put
\(\tau=c_{\max}/C\). The exact robust decision on the stated class is

\[
k^\star(\rho,\tau)
\in
\arg\min_k
\left[
G_{Q_k}(\rho)+\tau S_{Q_k}
\right].
\]

If \(C=0\), select a rule minimizing \(S_{Q_k}\).

## 6. Interval certification of distributed rules

The public rule tables contain decimal approximations. We therefore
certify the rounded rules themselves.

1. Low-degree rounding defects are enclosed rather than set to zero.
2. Structural errors are bounded by interval Taylor enclosures.
3. Chebyshev defects are enclosed through degree 500.
4. The transfer tail is bounded geometrically.
5. A cell is assigned \(k\) only if
   \[
   R_k^+<R_\ell^-
   \quad\text{for all }\ell\ne k.
   \]

A fixed grid certifies **95.6849%** of the domain. Seven levels
of adaptive refinement increase coverage to
\[
\boxed{99.970295%}.
\]
The remaining **0.029705%** is localized in thin transition
bands.

### 6.2 Ideal versus rounded rules

The minimax and degree-reduction results apply to ideal rules

\[
Q^\star_{n,k}\in\mathcal A_{n,k}
\]

that satisfy the moments exactly. The distributed artifacts are rounded
rules

\[
\widetilde Q_{n,k}.
\]

For rounded rules:

- Theorems 6 and 7 remain exact because they apply to any fixed rule.
- Actual low-degree defects must be retained.
- The exact degree bound and alternation theorem do not follow from a
  nominal \(k\)-label alone.
- Rounds 32–33 certify the rounded rules as numerical operators.
- High-precision alternation evidence concerns the idealized constructed
  solutions before publication rounding.

This separation is part of the formal claim structure.

## 7. External-validity stress test

Without retraining, the published rules were tested on

\[
L_{a,b}(x)
=
rac{1}{(x-a)^2+b^2},
\qquad
|a|\le0.03,\quad
0.08\le b\le0.12.
\]

For the \(n=4,\;k=0\) rule, the worst relative error was

\[
4.522335968815e-06.
\]

The rule remained substantially more accurate than the fixed-budget
Gauss--Legendre and composite Simpson baselines. Its error was,
however, inflated by a factor of approximately

\[
30338.5
\]

relative to the centered minimax value. This is a qualified stress-test
result, not a shifted-family minimax theorem.


## 8. Independent verification code path

A standalone verifier reconstructed the \(n=4\) hierarchy from only the
published rounded nodes, weights and manuscript formulas. It recovered
the alternation counts \(9,8,7,6,5\), centered errors, structural
errors, transfer functions and selector spot checks.

All declared comparisons passed. The maximum transfer-function relative
difference was

\[
2.731e-12.
\]

This is an internal independent reimplementation, not an external
third-party replication.


## 9. Relation to prior work


Gautschi's rational Gauss-type rules and later rationally exact
quadrature establish that known external poles can be incorporated
directly. Generalized Gaussian quadrature extends exactness to
Chebyshev systems, and optimization-based cubature methods jointly
select nodes and weights. Positive interpolatory cubature ensures
positive formulas for general finite-dimensional spaces. Rational
approximation of Markov functions provides the relevant pole and residue
structure. Recent interpolation-constrained rational minimax algorithms
are especially close conceptually because moment conditions at infinity
are interpolation constraints.

Consequently, this manuscript does not claim novelty for constrained
rational minimax, positive rational quadrature or generalized exactness
in isolation. The research hypothesis is that the particular
partial-moment Markov hierarchy, its quadrature interpretation, exact
coefficient-box selector and certification of rounded rules form a
distinct combined contribution.

## 10. Limitations

- The design family is centered and one-dimensional.
- The product-law fit is empirical.
- The interval computations are validated numerics, not a formal proof.
- Certification applies to rounded published rules.
- No finite-sample procedure can certify arbitrary unseen residuals.
- A broader structural-family experiment and independent implementation
  remain necessary before submission.
- Novelty is not confirmed by the present literature search.

## 11. Conclusion

Partial moment constraints provide a controlled bridge between a highly
specialized rational minimax rule and a polynomial-exact quadrature
formula. The hierarchy quantifies the price of smooth-background
protection. On weighted Chebyshev coefficient boxes, rule selection is
governed by an exact error-functional norm, and most of the tested
parameter domain can be assigned a rule by interval-separated risk
enclosures. The resulting framework is best interpreted as a
specialized, assumption-aware quadrature methodology rather than a
universal replacement for Gaussian or adaptive integration.

## References

1. W. Gautschi, *Gauss-type quadrature rules for rational functions*,
   1993.
2. D. Huybrechs, *On the computation of Gaussian quadrature rules for
   Chebyshev sets of linearly independent functions*, 2017.
3. V. Keshavarzzadeh, R. M. Kirby, and A. Narayan, *Generation of
   Nested Quadrature Rules for Generic Weight Functions via Numerical
   Optimization*, 2018.
4. J. F. van Diejen and E. Emsiz, *Quadrature rules from finite
   orthogonality relations for Bernstein-Szegő polynomials*, 2019.
5. J. Glaubitz, *Constructing Positive Interpolatory Cubature
   Formulas*, 2020.
6. B. Beckermann, J. Bisch, and R. Luce, *On the rational approximation
   of Markov functions*, 2021.
7. L. N. Trefethen, *Exactness of quadrature formulas*, 2021.
8. J. A. Hernández, J. R. Bravo, and S. Ares de Parga, *CECM*, 2023.
9. J. R. Bravo et al., *A subspace-adaptive weights cubature method*,
   2023.
10. W. Van Assche, *A Golub–Welsch version for simultaneous Gaussian
    quadrature*, 2023.
11. T. Goda, Y. Kazashi, and K. Tanaka, *How sharp are error bounds?*,
    2024.
12. R. Nailwal and A. Zalar, *Gaussian Quadratures with prescribed
    nodes via moment theory*, 2024.
13. L.-H. Zhang and Y.-N. Zhang, *b-d-Lawson: interpolation constrained
    rational minimax approximation*, 2025.
14. S. Hayakawa, *Convex-Geometric Error Bounds for Positive-Weight
    Kernel Quadrature*, 2026.
