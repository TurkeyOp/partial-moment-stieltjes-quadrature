# Round 50 Change Log

1. Reconstructed the square moment/equal-error/stationarity systems directly from Round 43 data.
2. Derived and implemented the full analytic Jacobian, including second derivatives with respect to internal extrema.
3. Refined all six roots at 180 decimal digits.
4. Certified strict Krawczyk inclusion in uniform coordinate boxes of radius `1e-12`.
5. Certified `||I-YJ(X)||_infinity < 1`, interval Jacobian nonsingularity, ordering, positivity, and `E > 0`.
6. Audited the analytic Jacobian against high-precision numerical differentiation.
7. Added interval derivative-sign subdivision and curvature-sign tests, proving that each alternating level is the global uniform norm.
8. Revised and compiled Manuscript Version 2.4 (25 pages).
9. Added self-contained data, rerun script, results, and SHA-256 manifest.
