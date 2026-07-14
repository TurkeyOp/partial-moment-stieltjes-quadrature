# Novelty defense and limits

## Status

**Novelty is not confirmed.** This document states the most defensible
position and the questions that a specialist must evaluate before
submission.

## Broad ideas that are prior art

The manuscript must not claim novelty for rationally exact quadrature,
generalized Gaussian quadrature, numerical moment matching, positive
cubature, Markov-function rational approximation, simultaneous
quadrature, shared-support cubature, or interpolation-constrained
rational minimax approximation.

## Closest novelty risk

Interpolation constraints at infinity can be interpreted as rational
interpolation constraints. The b-d-Lawson literature therefore makes it
unsafe to claim that constrained rational minimax approximation itself
is new. Gautschi and Huybrechs make it unsafe to claim that incorporating
non-polynomial structure into quadrature is new.

## Most defensible combined contribution

The paper's strongest contribution claim is the combination of:

1. a positive quadrature hierarchy indexed by a partial number of
   moment-at-infinity constraints;
2. the specific difference-numerator bound and resulting
   \(2n-k+1\) alternation certificate in that hierarchy;
3. an attained coefficient-box risk \(G_k(\rho)+\tau S_k\) used to
   select moment depth;
4. direct validated certification of the rounded distributed rules;
5. a one-command independent verification path.

## Claims that must remain prohibited

- first quadrature method to use rational information;
- universal improvement over Gaussian or adaptive quadrature;
- unconditional uniqueness of the minimax rule;
- exact minimaxity of decimal-rounded rules from their nominal label;
- a proved asymptotic product law;
- automatic detection of the correct model class;
- formal or third-party verification.

## Specialist decision requested

A specialist should decide whether the exact combination above is
sufficiently differentiated for publication, and whether the
alternation statement requires citation to a more general constrained
rational Chebyshev theorem.
