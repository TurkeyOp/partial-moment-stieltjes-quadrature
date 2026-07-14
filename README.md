> **New user?** Open [`START_HERE.md`](START_HERE.md). The final paper is [`FINAL_PROJECT_PAPER.pdf`](FINAL_PROJECT_PAPER.pdf).

# Partially Moment-Constrained Positive Stieltjes Minimax Quadrature

This repository accompanies the manuscript by **Tran Minh Duc** on a
positive partial-moment quadrature hierarchy for a centered Stieltjes /
Lorentzian model, exact coefficient-space risk, interval-certified rule
selection, and external-validity stress testing.

## Author

- **Tran Minh Duc**  
  FPT University, Ho Chi Minh City, Vietnam  
  Corresponding author: `ductranminh2107@gmail.com`

## Reproduce the main numerical results

```bash
python -m pip install -r requirements.txt
python run_all.py
```

The command reconstructs the published rounded rules' moment defects,
alternation points, centered errors, structural errors, transfer
functions, selector spot checks, shifted-family stress test, figures,
and seven automated audit tests.

## Repository map

```text
paper/          manuscript and JCAM submission source
rules/          published rounded n=4 rules
src/            independent reproduction formulas
tests/          automated reference audits
data/reference/ frozen values used only after computation
results/        generated numerical outputs
figures/        generated reproducibility figures
docs/round41/   novelty, reference, and specialist-review package
docs/submission submission checklist and cover letter
```

## Scientific scope

The exact alternation theory applies to ideal exact-moment rules. The
published decimal rules are treated as fixed rounded operators and are
validated directly. The shifted-Lorentzian calculation is a local
stress test, not a shifted-family optimality theorem. The repository
does not claim universal superiority over Gaussian or adaptive
quadrature.

## Manuscript

- Review PDF: `paper/jcam/main.pdf`
- LaTeX source: `paper/jcam/main.tex`
- Bibliography: `paper/jcam/references.bib`

## Citation

Citation metadata is provided in `CITATION.cff`.

## License

No license has yet been selected. See `LICENSE_SELECTION_REQUIRED.md`
before making the repository public.

## Reproducibility status

This is an internal independent reimplementation in a separate code
path. It is not a third-party replication or proof-assistant
verification.
