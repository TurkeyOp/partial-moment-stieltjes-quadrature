---
title: "Round 52 Scientific and Submission Audit"
author: "Tran Minh Duc"
date: "15 July 2026"
geometry: margin=1in
fontsize: 11pt
---

# Executive verdict

Round 52 is **completed as a final scientific and submission audit**, with the following qualified verdict:

> The manuscript and integrated research package are ready for focused specialist review, but not yet safe for formal JCAM submission because five release/metadata blockers remain.

The scientific audit did not identify a fatal theorem contradiction or a failed numerical certificate. Manuscript Version 2.5 compiles to 27 pages and incorporates the Round 51 reproduction evidence, the endpoint-precision disclosure, a clarified `b` versus `s=b^2` link, and updated publication metadata for the closest literature.

# 1. Scientific audit

Eighteen principal claims were classified by evidence type:

- analytic proof;
- computer-assisted proof;
- numerical verification;
- empirical evidence;
- targeted novelty positioning.

The full decision table is in `THEOREM_CLAIM_AUDIT.csv`. No result was upgraded beyond its evidence. In particular:

- the alternation theorem remains sufficient, not necessary;
- the Krawczyk result proves local uniqueness only inside each box;
- the interval selector is exact only for the finite rounded-operator hierarchy on the stated parameter rectangle;
- the multi-start study remains empirical and uses the original solver;
- the new forward-AD/Arb path is author-produced independent code-path reproduction, not third-party replication;
- the shifted test supports local robustness only;
- novelty remains subject to specialist prior-art review.

## 1.1 Coordinate consistency

The analytic alternation theorem is expressed in `s=b^2`, while the nonlinear systems use extrema in `b`. Version 2.5 now states explicitly that `b -> b^2` is strictly increasing and has positive derivative on `[0.08,0.12]`. Therefore the ordering of extrema, uniform norm, alternating values, and stationarity equations are equivalent in the two coordinates.

## 1.2 Precision finding

The archived Round 50 Newton-center script constructed its two `mpmath` endpoint constants at import-time default precision. The rigorous Arb system always used the exact decimal endpoints, so the proof was not invalidated. The corrected script creates endpoints after the working precision is set, reduces the point residual below `2e-180`, and certifies 6/6 boxes again. The independent forward-AD/Arb path also certifies 6/6.

## 1.3 Reproduction evidence incorporated

Version 2.5 records the Round 51 results:

- 21/21 frozen hierarchy rules pass arithmetic/geometry audits;
- 6/6 upper-half boxes are reproduced through an independent AD/Arb code path;
- the Round 49 portable certifier reproduces 344,615 visited cells and certified area 0.9959563612937927;
- 35/35 cross-artifact checks and 7/7 Round 51 tests pass.

A dense 50,001-point screen is described only as numerical screening, not as a continuum proof.

# 2. Literature and claim audit

Eighteen references were checked. Thirteen are formal journal/book publications and five remain explicitly identified as preprints.

Key upgrades include:

- Gautschi’s published 1993 chapter and 2001 JCAM survey;
- Huybrechs in SIAM Journal on Numerical Analysis;
- Filip et al. in SIAM Journal on Scientific Computing;
- Horning–Trefethen in IMA Journal of Numerical Analysis (2026);
- Keshavarzzadeh–Kirby–Narayan in Journal of Computational Physics;
- Beckermann–Bisch–Luce in Numerical Algorithms;
- Trefethen and Goda–Kazashi–Tanaka in their SIAM journal versions;
- Moore–Kearfott–Cloud, Rump, and Johansson for validated numerics.

Tomanović 2023 was added as a nearby rational Gauss-type comparator. The audit continues to reject broad claims that pole awareness, positivity, constrained rational minimax, equioscillation, or worst-case quadrature are new separately.

# 3. JCAM compliance audit

The audit used the current official Journal of Computational and Applied Mathematics Guide for Authors and Elsevier submission instructions, accessed on 15 July 2026.

Verified requirements:

- editable `elsarticle` source;
- abstract no more than 250 words: **215 words**;
- 1–7 keywords: **6 keywords**;
- highlights: **5 bullets**, maximum **75 characters**;
- separate, cited figure files;
- numbered references with formal publications preferred;
- funding, competing-interest and AI-assistance declarations;
- data-and-code statement with a truthful repository status.

The automated Round 52 audit passes **26/26 checks with no warnings**, and the integrated test suite passes **10/10 tests**.

# 4. Manuscript Version 2.5

The manuscript now contains:

1. a shorter 215-word abstract including the reproduction result;
2. an explicit `b`/`s` equivalence statement;
3. interval-method citations for Krawczyk verification;
4. disclosure and resolution of the Round 50 center-precision issue;
5. a new independent-reproduction and cross-artifact section;
6. corrected limitations distinguishing author-produced and external independence;
7. updated formal publication metadata and DOI records;
8. a truthful provisional data statement.

Build outcome:

- 27 pages;
- no undefined references or citations;
- no overfull boxes;
- 27/27 pages rendered and visually inspected;
- all 18 bibliography entries cited.

# 5. Submission blockers

## B1. Persistent public archive

The complete freeze exists, but it has not been deposited with a DOI or another persistent identifier. The current public GitHub repository contains an earlier baseline.

## B2. License selection

No code license has been selected. This is an author/legal decision and was not made automatically.

## B3. Corresponding-author telephone number

The submission metadata lacks a telephone number.

## B4. Elsevier declaration file

The manuscript declaration is present, but the separate output from Elsevier’s Declaration of Interest tool has not been created.

## B5. Flat submission upload folder

The final Editorial Manager folder must be built after the DOI, license, declarations and manuscript are frozen.

# 6. Readiness assessment

| Layer | Round 52 status |
|---|---|
| Mathematical framework | Mature; specialist audit recommended |
| Full numerical hierarchy | Reproduced |
| Upper-half existence certificates | Certified and independently code-path reproduced |
| Rounded selector certificate | Reproduced |
| Manuscript | Version 2.5 audit draft complete |
| Literature positioning | Updated; not exhaustive |
| JCAM technical compliance | Passed except listed blockers |
| Public archival reproducibility | Not yet closed |
| Formal submission readiness | Not yet safe |

# 7. Next valid round

Round 53 is the **submission freeze**, not another open-ended scientific expansion. Its required closure conditions are:

1. obtain the author’s license decision and telephone number;
2. create a public versioned archive and persistent identifier;
3. replace the provisional data statement with the permanent citation;
4. generate the Elsevier declaration file;
5. build and test the flat Editorial Manager upload package;
6. run a final no-change scientific regression;
7. freeze manuscript, supplement, cover letter, highlights and checksums.

Round 54 should open only for actual specialist or editorial feedback.
