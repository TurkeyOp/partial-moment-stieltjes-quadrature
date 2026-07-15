# Round 45 — Independent multi-start reconstruction

The six upper-half constrained minimax problems were reconstructed from
12 perturbed starts each, for a total of
72 nonlinear solves.

A run was accepted only if nodes were strictly ordered, all weights were
positive, the maximum scaled Remez residual was below \(10^{-8}\), and
the maximum constrained-moment residual was below \(10^{-10}\).

|   n |   k |   accepted_starts |   total_starts |   success_rate |   published_worst_relative_error |   best_reconstructed_worst_relative_error |   best_relative_difference_vs_published |   best_maximum_node_difference_vs_published |   best_maximum_weight_difference_vs_published |   best_maximum_remez_residual |   best_maximum_moment_residual |   dominant_error_cluster_fraction | better_than_published_by_more_than_1e-6_relative   |
|----:|----:|------------------:|---------------:|---------------:|---------------------------------:|------------------------------------------:|----------------------------------------:|--------------------------------------------:|----------------------------------------------:|------------------------------:|-------------------------------:|----------------------------------:|:---------------------------------------------------|
|   2 |   3 |                12 |             12 |       1        |                      0.105006    |                               0.105006    |                             2.64324e-16 |                                 5.55112e-17 |                                   5.55112e-17 |                   2.7754e-15  |                    8.32667e-17 |                                 1 | False                                              |
|   3 |   4 |                10 |             12 |       0.833333 |                      0.0043654   |                               0.0043654   |                             6.77533e-14 |                                 4.44089e-16 |                                   4.996e-16   |                   4.96725e-14 |                    5.55112e-17 |                                 1 | False                                              |
|   3 |   5 |                12 |             12 |       1        |                      0.069808    |                               0.069808    |                             5.30794e-14 |                                 1.28786e-14 |                                   1.32117e-14 |                   1.2922e-14  |                    3.05311e-16 |                                 1 | False                                              |
|   4 |   5 |                 8 |             12 |       0.666667 |                      0.000179433 |                               0.000179433 |                             2.37646e-12 |                                 4.44089e-15 |                                   4.27436e-15 |                   8.70101e-13 |                    2.22045e-16 |                                 1 | False                                              |
|   4 |   6 |                11 |             12 |       0.916667 |                      0.00294322  |                               0.00294322  |                             9.22406e-14 |                                 1.03251e-14 |                                   1.04916e-14 |                   4.3468e-14  |                    1.249e-16   |                                 1 | False                                              |
|   4 |   7 |                12 |             12 |       1        |                      0.0459798   |                               0.0459798   |                             5.11138e-13 |                                 8.95395e-14 |                                   6.43374e-14 |                   5.58373e-15 |                    2.22045e-16 |                                 1 | False                                              |

No accepted run found a solution better than the published rule by more
than \(10^{-6}\) relative in minimax level.

Maximum relative difference between the best reconstructed and
published error levels:

\[
2.376e-12.
\]

Maximum node difference:

\[
8.954e-14.
\]

Maximum weight difference:

\[
6.434e-14.
\]

The evidence does not constitute a proof of global uniqueness, but it
substantially reduces the possibility that the upper-half rules are
isolated local artifacts.

Optimizer-reconstruction blocker resolved:

\[
oxed{str(results["optimizer_reconstruction_blocker_resolved"]).upper()}.
\]

The remaining primary blocker before manuscript Version 2 is frozen for
submission is specialist novelty and theorem review.
