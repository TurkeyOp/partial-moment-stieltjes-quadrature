# Round 51 Precision Finding

## Finding

The archived Round 50 Newton certifier defined:

```python
BLEFT = mp.mpf('0.08')
BRIGHT = mp.mpf('0.12')
```

at module import time, before `mp.mp.dps` was raised to 180. In a fresh process, the stored values are:

- `BLEFT = 0.08000000000000000166533453693773481063544750213623046875`;
- `BRIGHT = 0.11999999999999999555910790149937383830547332763671875`.

Their deviations from the intended exact decimals are approximately:

- `+1.66533453694e-18` at the left endpoint;
- `-4.44089209850e-18` at the right endpoint.

This explains why independently evaluating the saved Newton centers at exact decimal endpoints gives equal-error residuals of order `1e-17`, despite the archived point residual field being near `1e-180`.

## Why the Round 50 certificate remains valid

The rigorous interval evaluator in Round 50 used:

```python
arb('0.08')
arb('0.12')
```

inside the Arb square system. Therefore the Krawczyk inclusion, residual intervals, ordering margins, and existence/uniqueness conclusion were for the intended exact-decimal endpoint system. The import-time issue affected the numerical center-refinement diagnostic, not the interval theorem.

## Correction

`round50_krawczyk_certifier_precision_fixed.py` stores endpoint text and constructs `mp.mpf` values only after the requested precision is active. The corrected run:

- certifies all six systems;
- has maximum point residual below `2e-180`;
- retains Krawczyk norm bounds far below one;
- is independently re-certified by the Round 51 forward-AD/Arb verifier.

## Claim impact

- **No retraction of the Round 50 existence/uniqueness certificate is required.**
- The archived `point_residual_max` values should not be interpreted as residuals of the exact-decimal endpoint system.
- Future repository and manuscript-supporting data should use the precision-fixed outputs.
