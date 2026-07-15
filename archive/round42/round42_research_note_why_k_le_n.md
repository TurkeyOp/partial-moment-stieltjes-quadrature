# Research Note 01

## Why does the current hierarchy stop at \(k\le n\)?

### Executive conclusion

The current cutoff \(k\le n\) is **not the maximal cutoff imposed by
degrees of freedom or positivity**.

For a symmetric rule with \(n\) positive node pairs,

\[
Q[f]=\sum_{j=1}^{n}w_j\{f(-x_j)+f(x_j)\},
\]

there are \(2n\) free real parameters:

\[
(x_1,\ldots,x_n,w_1,\ldots,w_n).
\]

The mathematically maximal moment depth is

\[
\boxed{0\le k\le 2n},
\]

not \(0\le k\le n\).

At \(k=2n\), the rule is the ordinary \(2n\)-point Gauss--Legendre
rule, written in symmetric-pair form. For \(k>2n\), matching all the
requested moments is impossible.

Therefore the manuscript's present \(k=0,\ldots,n\) sequence should be
described as a **lower-half partial-moment hierarchy**, chosen to retain
substantial structural design freedom. It should not be described as
the full feasible hierarchy.

---

## 1. Parameter space

Set

\[
y_j=x_j^2,
\qquad
0<y_1<\cdots<y_n<1,
\qquad
w_j>0.
\]

The parameter space is the open set

\[
\mathcal P_n
=
\left\{
(y,w)\in\mathbb R^{2n}:
0<y_1<\cdots<y_n<1,\;w_j>0
\right\}.
\]

Define the moment map

\[
M_k:\mathcal P_n\to\mathbb R^k,
\]

\[
M_k(y,w)
=
\left(
\sum_{j=1}^{n}w_jy_j^\ell
\right)_{\ell=0}^{k-1}.
\]

The target vector is

\[
m_k
=
\left(
\frac{1}{2\ell+1}
\right)_{\ell=0}^{k-1}.
\]

The admissible set is

\[
\mathcal A_{n,k}
=
M_k^{-1}(m_k).
\]

---

## 2. Rank theorem for the moment map

### Proposition

At every point of \(\mathcal P_n\), the Jacobian of \(M_k\) has full row
rank \(k\) for every \(k\le 2n\).

### Proof

Assume a linear combination of the Jacobian rows vanishes. Let

\[
p(y)=\sum_{\ell=0}^{k-1}c_\ell y^\ell.
\]

The columns obtained by differentiating with respect to \(w_j\) give

\[
p(y_j)=0,
\qquad j=1,\ldots,n.
\]

The columns obtained by differentiating with respect to \(y_j\) give

\[
w_jp'(y_j)=0.
\]

Since \(w_j>0\),

\[
p'(y_j)=0.
\]

Thus every \(y_j\) is a double root of \(p\), so a nonzero \(p\) would
have degree at least \(2n\). But

\[
\deg p\le k-1\le2n-1.
\]

Therefore \(p\equiv0\), hence all \(c_\ell=0\). The Jacobian rows are
linearly independent. \(\square\)

### Consequence

By the implicit-function theorem, whenever \(\mathcal A_{n,k}\) is
nonempty,

\[
\boxed{
\dim \mathcal A_{n,k}=2n-k,
\qquad 0\le k\le2n.
}
\]

This explains the alternation count

\[
(2n-k)+1=2n-k+1
\]

as the nonlinear-family dimension plus one.

---

## 3. What happens at \(k=2n\)?

At \(k=2n\),

\[
\dim\mathcal A_{n,2n}=0.
\]

The first \(2n\) moments determine the positive \(n\)-node Gaussian rule
for the transformed measure

\[
d\mu(y)=y^{-1/2}\,dy
\quad\text{on }[0,1].
\]

Under \(y=x^2\), this is exactly the positive half of the
\(2n\)-point Gauss--Legendre rule on \([-1,1]\).

The corresponding polynomial exactness is

\[
2k-1=4n-1.
\]

Hence the true maximal endpoint is

\[
\boxed{
k=2n
\Longleftrightarrow
\text{\(2n\)-point Gauss--Legendre}.
}
\]

The predicted alternation count is then

\[
2n-2n+1=1.
\]

This is mathematically consistent but no longer represents a nontrivial
minimax optimization: there are no remaining design degrees of freedom.

---

## 4. Why is \(k>2n\) impossible?

Suppose an \(n\)-node rule in \(y\) matched moments through degree
\(2n\). Define

\[
g(y)=\prod_{j=1}^{n}(y-y_j)^2.
\]

Then \(g\) has degree \(2n\), is nonnegative, and is not identically
zero. The discrete rule gives

\[
Q[g]=0,
\]

because \(g(y_j)=0\) at every node. But the exact integral satisfies

\[
\int_0^1 g(y)y^{-1/2}\,dy>0.
\]

This contradicts exactness through degree \(2n\). Therefore

\[
\boxed{k\le2n}
\]

is the maximal feasible moment depth.

---

## 5. What does the current \(k\le n\) cutoff mean?

For the current paper,

\[
0\le k\le n
\]

leaves at least \(n\) free parameters:

\[
\dim\mathcal A_{n,k}=2n-k\ge n.
\]

Thus even the endpoint \(k=n\) still retains a substantial
target-family minimax design space.

For \(n=4\):

| \(k\) | Remaining dimension | Polynomial exactness |
|---:|---:|---:|
| 0 | 8 | none imposed |
| 1 | 7 | 1 |
| 2 | 6 | 3 |
| 3 | 5 | 5 |
| 4 | 4 | 7 |
| 5 | 3 | 9 |
| 6 | 2 | 11 |
| 7 | 1 | 13 |
| 8 | 0 | 15, Gauss--Legendre |

Therefore \(k=n\) is not the Gaussian endpoint. It is the midpoint in
constraint count and the point where half of the original parameter
freedom remains.

The current cutoff can be defended as a **design choice**:

> The paper studies the lower half of the feasible hierarchy, where at
> least \(n\) structural design degrees of freedom remain.

It cannot be defended as a mathematical impossibility beyond \(n\).

---

## 6. Numerical consequence for \(n=4\)

The current \(k=4\) rule has centered worst relative error approximately

\[
1.09\times10^{-5}.
\]

The true maximal endpoint \(k=8\), namely the 8-point Gauss--Legendre
rule, has worst relative error approximately

\[
4.30\times10^{-1}
\]

on the same narrow Lorentzian family.

Thus extending to the Gaussian endpoint produces a very large loss of
structural accuracy. This strongly supports studying the lower half,
but it does not eliminate the need to explain or numerically examine
the upper half.

---

## 7. Implication for the manuscript

### Statements that must be corrected

Avoid:

> The hierarchy runs from structural minimax at \(k=0\) to the
> polynomial-exact endpoint at \(k=n\).

This wording suggests that \(k=n\) is the maximal polynomial endpoint.

Use:

> We study the lower-half hierarchy \(0\le k\le n\), for which at least
> \(n\) structural design degrees of freedom remain. The full feasible
> moment range is \(0\le k\le2n\), with \(k=2n\) equal to the
> \(2n\)-point Gauss--Legendre rule.

### What can remain unchanged

The moment--Laurent equivalence, numerator-degree bound, and conditional
alternation theorem extend naturally to every feasible

\[
0\le k\le2n.
\]

The exact coefficient-box risk also remains unchanged.

---

## 8. Is extending the numerical hierarchy necessary?

### For mathematical correctness

Yes, the paper must at least acknowledge the full feasible range and
justify the lower-half restriction.

### For a stronger JCAM submission

A numerical construction of the missing rules

\[
k=n+1,\ldots,2n-1
\]

is strongly recommended. It would answer whether:

- positive minimax rules continue to exist;
- the approximately constant error penalty persists;
- the selector ever chooses upper-half rules;
- the transition toward Gauss--Legendre is smooth or singular.

### What should not be done

Do not simply append the Gaussian endpoint and pretend the upper-half
hierarchy has been characterized. The intermediate constrained minimax
problems still need to be solved and audited.

---

## 9. Final verdict

The feedback questioning \(k\le n\) identified a genuine theoretical
gap in exposition.

The corrected conclusion is:

\[
\boxed{
\text{The full feasible range is }0\le k\le2n.
}
\]

\[
\boxed{
\text{The existing paper studies only the lower half }0\le k\le n.
}
\]

This does not invalidate the existing results. It changes their scope
and creates a precise next research task: construct and analyze the
upper-half rules.
