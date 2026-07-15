# Round 48 - Theorem and assumption red-team audit

## Executive conclusion

The analytical core is substantially stronger after revision. The
feasible-range theorem, endpoint identification, zero-count minimax
certificate, coefficient-box norm, and mixed-risk formula can be stated
rigorously once their domains and assumptions are made explicit.

The most serious finding was not a theorem failure. It was the use of
“validated” and “certified” for a selector computation whose structural
margins were based on dense sampling and an inflated derivative estimate,
not verified interval arithmetic. Manuscript Version 2.2 corrects this
to **conservative numerical screening**.

## Theorems that survive the audit

### Feasible range and dimension

The Jacobian rank argument is valid on the open ordered positive
parameter domain. The revised version correctly treats the level set as
a parameter manifold and handles \(k=0\) separately.

### Impossibility beyond \(2n\)

The squared node polynomial gives a clean contradiction for every
\(k\ge2n+1\). No positivity of the weights is required for the zero
discrete value, but positivity is part of the admissible class and is
used elsewhere.

### Gauss-Legendre endpoint

The endpoint is now proved through transformed Gaussian quadrature,
orthogonal-polynomial uniqueness, and unique weights. This closes the
largest omission in the former proof.

### Alternation certificate

The zero-count proof is valid as a sufficient global-minimax certificate
inside the stated class. It does not establish necessity or uniqueness
among equal-error minimizers.

### Exact coefficient and mixed risks

Both formulas are exact after defining the coefficient box precisely.
The mixed-risk attainability proof requires the compactness of the
structural parameter interval and the independent sign choices.

## Claims that were weakened

- “Validated/certified selector” -> “conservatively screened selector.”
- “Independent reconstruction” -> “multi-start sensitivity study.”
- “Continuous path” implications -> “discrete nested hierarchy.”
- “Exact numerical certificate” -> “numerical evidence for a conditional theorem.”
- “Globally optimal selector” -> “exact selector among the finite candidates.”

## Remaining blockers

1. Rigorous interval or computer-assisted validation of the selector.
2. Computer-assisted existence of exact upper-half equioscillating rules,
   should the journal demand theorem-level numerical existence.
3. An optimizer implementation written independently of the current
   codebase.
4. External specialist review of equivalence to moment-space or
   constrained-rational formulations.

## Submission decision

Version 2.2 is more defensible than Versions 2 and 2.1. It is suitable
for specialist circulation. It should not yet be described as fully
submission-frozen because the selector is screened, not rigorously
certified.
