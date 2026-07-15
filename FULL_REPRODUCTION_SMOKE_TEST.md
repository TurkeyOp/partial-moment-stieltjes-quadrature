# Full reproduction smoke test

Date: 2026-07-15

The public GitHub-ready repository was tested end to end in the build environment with:

```bash
python run_full_reproduction.py
```

Result: **PASS**

Verified outputs:

- full hierarchy audit: 21/21 rules;
- Round 49 rounded-operator selector interval run completed;
- Round 50 precision-fixed Krawczyk run: 6/6 certified;
- independent forward-AD/Arb verification: 6/6 certified;
- public-package integrity check: PASS.

The full run writes regenerated artifacts to `reproduced_results/`, which is excluded by `.gitignore` so that frozen reference artifacts are not overwritten.
