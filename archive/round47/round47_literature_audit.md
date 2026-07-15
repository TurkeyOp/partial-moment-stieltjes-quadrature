# Round 47 - Literature and novelty audit

## Bottom line

The audit does **not** confirm that every mathematical component of the
manuscript is new. Several ingredients are established:

- pole-aware and rationally exact quadrature;
- generalized Gaussian quadrature for Chebyshev systems;
- positive exact quadrature and moment-space geometry;
- nonlinear moment-matching construction;
- rational minimax and equioscillation;
- interpolation- and derivative-constrained rational minimax;
- rational approximation of Markov/Stieltjes/Cauchy transforms;
- worst-case quadrature analysis.

The manuscript remains potentially publishable because its strongest
contribution is the **combination** of these ingredients in a particular
model-aware design:

1. positive symmetric Stieltjes residues;
2. relative minimax over a continuum of Lorentzian widths;
3. a variable prefix of polynomial moments at fixed node-pair count;
4. an exact mixed smooth/structural risk selector;
5. a validated partition of the selector domain.

The targeted search found no direct source containing all five features.
That is a search finding, not a proof of novelty.

## Closest competitors

### Gautschi: rational Gauss-type rules

This removes any defensible claim that matching important poles inside a
quadrature construction is new. The present work must be positioned as a
minimax/selection refinement of an established structure-aware principle.

### Huybrechs and moment-space generalized Gaussian theory

Positive interior-node rules exact for ordered Chebyshev systems and
stepwise exactness constructions already exist. Therefore “complete
hierarchy” is too broad as a novelty label. The useful result here is the
feasible-range characterization **inside the proposed Stieltjes minimax
class**.

### Horning and Trefethen: quadrature from rational approximations

This is the closest conceptual neighbor. It makes the transform-
approximation-to-quadrature bridge explicit and interprets Gauss
quadrature through Padé approximation at infinity. The present paper
must distinguish itself through imposed positivity, variable moment
depth, continuum relative minimax, and the exact selector.

### Filip et al.; Zhang and Zhang: rational minimax

Equioscillation and rational minimax are classical, while interpolation-
constrained rational minimax is already an active topic. The manuscript's
alternation theorem should be sold as a concise certificate specialized
to the positive Stieltjes quadrature class.

## Reclassified contributions

### Primary contribution

The combined model-aware path and selector:
\[
\min_{Q\in\mathcal A_{n,k}}
\max_{b\in[0.08,0.12]}
\left|rac{Q[L_b]}{I[L_b]}-1ight|,
\qquad
k^\star=rg\min_k\{G_k(ho)+	au S_k\},
\]
together with a validated rule-selection map.

### Secondary contributions

- complete numerical realization of the path for \(n=2,3,4\);
- class-specific degree/alternation certificate;
- upper-half reconstruction and numerical validation;
- shifted-family scope test.

### Structural results, not stand-alone novelty claims

- \(0\leq k\leq2n\);
- \(\dim\mathcal A_{n,k}=2n-k\);
- impossibility for \(k>2n\);
- recovery of Gauss-Legendre at \(k=2n\);
- exact coefficient-box norm identity.

## Publication-risk decision

The previous title placed too much novelty weight on the word
“hierarchy.” The safer title is:

> **Model-Aware Positive Stieltjes Quadrature: From Structural Minimax
> to Gauss-Legendre**

The paper should use “within the stated class,” “we formulate,”
“we characterize,” and “the targeted search did not identify a direct
match.” It should not use “first,” “unprecedented,” or “the complete
hierarchy” without a class qualifier.

## Residual uncertainty

A specialist in generalized quadrature, moment spaces, or constrained
rational approximation may identify an equivalent formulation under
different terminology. External specialist review remains a genuine
submission blocker.
