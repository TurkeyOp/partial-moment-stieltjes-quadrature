# Proof dependency map

## Definitions

1. Ordered positive parameter domain \(\mathcal P_n\).
2. Moment level set \(\Theta_{n,k}\).
3. Operator class \(\mathcal A_{n,k}\).
4. Structural interval \(S=[0.08^2,0.12^2]\).

## Logical dependencies

### Moment equivalence lemma

Uses symmetry and uniform finite-order expansion at infinity.

### Representation uniqueness lemma

Uses simple poles, positive nonzero residues, and ordered distinct nodes.

### Feasible-range theorem

- Nonemptiness: standard Gaussian quadrature for
  \(d\mu(y)=y^{-1/2}dy\).
- Dimension: full row rank of \(DM_k\), then regular-level-set theorem.
- Impossibility: nonnegative squared node polynomial of degree \(2n\).
- Endpoint uniqueness: monic orthogonal polynomial uniqueness and
  a nonsingular Vandermonde system.

### Difference-degree proposition

Uses the moment-equivalence lemma for \(k\ge1\); the \(k=0\) decay is
automatic.

### Alternation certificate

Uses continuity, positivity of \(F\), the difference-degree proposition,
and uniqueness of the ordered positive representation.

### Coefficient-box theorem

Uses absolute/uniform Chebyshev convergence and boundedness of \(I-Q\).

### Mixed-risk theorem

Uses coefficient-box attainability, compactness of \(B\), and independent
choice of the signs of \(h\) and \(c\).

### Selector statement

Exact only over the finite candidate set. Numerical rule identification
still depends on computed values of \(G_Q\) and \(S_Q\).

## Open proof obligations

1. Computer-assisted existence of exact equioscillating upper-half rules.
2. Necessity and equal-norm uniqueness in the nonlinear positive class.
3. Rigorous interval certification of the selector map.
4. Independent implementation of the optimizer.
