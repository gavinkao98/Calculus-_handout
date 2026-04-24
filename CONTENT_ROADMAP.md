# Content Roadmap

This file carries the **course arc** of the handout: which chapters exist, in what order, what each chapter is responsible for, and how concepts thread across chapters. It is the curricular companion to [`CONTENT_SPEC.md`](CONTENT_SPEC.md) (which governs *how* to write) and [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) (daily author rules).

When you begin a new chapter, update the entry below **before** drafting. When you close a chapter, mark it done and revisit downstream prereq statements.

---

## Audience and positioning

Repeated from [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §1 so authors of any chapter can calibrate quickly:

- motivated high-school student preparing for or self-studying college calculus.
- has strong precalculus; some exposure to mathematical reasoning; not yet an undergraduate-math-major.
- reads the handout as the primary channel. **The handout is self-sufficient**; the companion video is reinforcement, not prerequisite.

Two cross-cutting targets sit above any chapter-specific content:

- **self-sufficiency** — a student who never watches the video can still learn from the handout alone.
- **lookup-friendliness** — a student who forgets a definition in Chapter 5 can find it again via the index, the chapter opening, or the summary.

---

## Chapter list

> **Status legend**: `draft` = actively being written. `skeleton` = structure planned but content not drafted. `planned` = on the roadmap, not yet started. `done` = meets the §15 consistency checklist.

| # | Title | Status | Sections |
|---|---|---|---|
| 1 | Inverse Functions and Limits | draft | 1.1 Inverse Functions and One-to-One Functions; 1.2 Inverse Trigonometric Functions; 1.3 Limits; 1.4 One-Sided and Infinite Limits; 1.5 Limit Laws; 1.6 The Precise Definition of a Limit |
| 2 | Derivatives | planned | 2.1 The Derivative at a Point; 2.2 The Derivative as a Function; 2.3 Differentiation Rules; 2.4 Derivatives of Trigonometric Functions; 2.5 The Chain Rule; 2.6 Implicit Differentiation; 2.7 Derivatives of Inverse Functions; 2.8 Derivatives of Exponential and Logarithmic Functions; 2.9 Higher-Order Derivatives |
| 3-14 | *(TBD — titles added as each chapter is drafted)* | planned | — |

Target scope: Calc I + II + III (single-variable through multivariable vector calculus). Loose Stewart / Rogawski TOC as the reference arc. The natural full arc at this scope runs roughly 14 chapters:

- **Calc I** (Ch 1-4): Inverse Functions and Limits → Derivatives → Applications of Differentiation → Integrals.
- **Calc II** (Ch 5-9): Applications of Integration → Techniques of Integration → Differential Equations → Parametric and Polar Coordinates → Infinite Sequences and Series.
- **Calc III** (Ch 10-14): Vectors and the Geometry of Space → Vector Functions → Partial Derivatives → Multiple Integrals → Vector Calculus.

Titles for Ch 3 onward are **not committed** until the preceding chapter's draft stabilises. The per-workflow decision is explicit: we fill a chapter's full roadmap entry (role, prereqs, core skills, key figures, notation, cautions, open questions) at the moment its immediate predecessor reaches the `draft` status bar — not earlier, since upstream decisions in the predecessor chapter shift what the successor needs to teach.

---

## Per-chapter entry template

Copy this block into the chapter list area when beginning a new chapter.

```
### Chapter N: Title

**Status**: draft | skeleton | planned | done
**Source file**: chapters/chNN_<slug>.tex
**Estimated length**: N pages printed (12 pt, 3.3 cm margins)

**Role in the arc**
- One paragraph on what this chapter does for the reader.
- Why it sits at position N and not earlier/later.

**Prerequisites**
- Chapters this chapter relies on (by section).
- Precalculus facts the reader is expected to bring.
- Notation or environments introduced earlier that this chapter reuses.

**Core skills**
Each item MUST match a bullet in the chapter's "By the end of this chapter, you will be able to:" list.
- skill 1
- skill 2
- skill 3-5

**Key figures**
- figure that every section-opening motivation depends on (one bullet each).

**Handout self-sufficiency vs. video reinforcement**
- What the handout teaches alone.
- What the video adds on top (intuition visualisations, alternative worked examples, pacing).
  The video never carries a fact that the handout does not also state.

**Strategy boxes expected**
- Problem-type → strategy name. E.g. "computing a limit → §1.5 Limit-computation strategy."

**Notation introduced**
- New symbols, macros, or notational conventions. Each one needs an `\index{...}` at first use.

**Common pitfalls (caution boxes)**
- Notation traps.
- Branch-choice or domain-restriction pitfalls.
- Identities that only hold on a subdomain.

**Open questions**
- Decisions not yet made. Flag here and close before declaring the chapter `done`.
```

---

## Chapter 1 (filled exemplar)

### Chapter 1: Inverse Functions and Limits

**Status**: draft
**Source file**: [`chapters/ch01_foundations.tex`](chapters/ch01_foundations.tex) — the filename slug `foundations` is the arc-level tag (Chapter 1 is the *foundations* phase of the arc), not part of the printed chapter title.
**Estimated length**: *(fill in after first full compile)*

**Role in the arc**
Chapter 1 is the **foundations** phase of the course arc. It sets up the two foundational machines of calculus: inverse functions (the algebraic machine for "running a rule backward") and limits (the analytic machine for "approaching without equalling"). The chapter intentionally pairs these because both force the reader to reason about correspondences and approximations rather than about formulas in isolation.

**Prerequisites**
- Precalculus functions: domain, range, composition, graphs.
- Trigonometric functions and their graphs on standard intervals.
- Basic algebra manipulations (factoring, rationalising, completing the square).

**Core skills** (matches the chapter opening bullet list)
- determine whether a function is one-to-one, and find its inverse when it is;
- work with inverse trigonometric functions, their principal-interval restrictions, and the identities that follow;
- compute limits of the forms encountered in Ch. 1 and 2 using substitution, factoring, rationalising, and one-sided analysis;
- decide when a limit fails to exist;
- state and, where required, verify a limit using the $\varepsilon$–$\delta$ definition.

**Key figures**
- inverse-composition diagram (§1.1).
- reflection across $y = x$ for invertible graphs (§1.1).
- restricted-domain trig graphs with principal intervals shaded (§1.2).
- one-sided-limit disagreement example (§1.4).
- $\varepsilon$–$\delta$ tube-and-interval diagram (§1.6).

**Handout self-sufficiency vs. video reinforcement**
- The handout alone carries every definition, every theorem statement, every worked example, and every strategy box.
- The companion videos (one per section, currently exemplified by §1.1) add animated reflection-across-$y=x$ demonstrations, animated $\varepsilon$–$\delta$ tubes that the printed page cannot convey, and a slower verbal walkthrough of notation traps.
- Nothing in the video substitutes for reading the handout — video scenes are marked as reinforcement in [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md).

**Strategy boxes present**
- finding an inverse function (§1.1).
- computing a limit (§1.5).
- verifying an $\varepsilon$–$\delta$ limit (§1.6).

**Notation introduced**
- `\arcsin`, `\arccos`, `\arctan`, `\arccsc`, `\arcsec`, `\arccot` (house inverse-trig operators).
- `\lim_{x \to a} f(x)`, `\lim_{x \to a^-} f(x)`, `\lim_{x \to a^+} f(x)`, `\lim_{x \to \infty} f(x)`.
- $\varepsilon$, $\delta$.

**Common pitfalls (caution boxes present)**
- $\sin^{-1} x$ denotes the inverse sine, not $1/\sin x$.
- $\arcsin(\sin x) = x$ holds only on the principal interval $[-\pi/2, \pi/2]$.

**Open questions**
- End-of-section exercises are still `% TODO` placeholders in all six sections. See [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) for the minimum exercise skeleton that should land before the chapter is declared `done`.

---

## Chapter 2 (filled entry)

### Chapter 2: Derivatives

**Status**: planned
**Source file**: `chapters/ch02_derivatives.tex` (to be created when drafting begins)
**Estimated length**: *(fill in after first full compile)*

**Role in the arc**
Chapter 2 is the **development** phase of Calc I. It converts the limit machinery from Chapter 1 into a working operator: given a function, produce another function describing its instantaneous rate of change. Ch 1 did the heavy conceptual lifting (what does it mean to approach without equalling?); Ch 2 cashes that in algorithmically (how do you differentiate a polynomial, a trig function, a composition?). Every applications chapter that follows — Ch 3 on extrema and optimization, Ch 4's connection to integrals via the Fundamental Theorem, all of Ch 12 on partial derivatives — takes "the derivative" as a known object and builds on it.

**Prerequisites**
- **From Chapter 1**: all six sections, especially §1.3 (limits), §1.4 (one-sided and infinite limits), §1.5 (limit laws), and the `\lim` notation introduced there. The derivative is defined as a limit; students who are shaky on limit manipulation will not survive the definition in §2.1. §1.2 (inverse trig) supplies the identities used in §2.7. §1.6 (ε-δ) is not strictly prerequisite — the derivative is phrased through the algebraic limit, not the ε-δ form — but a student who has seen §1.6 will find §2.1's rigour less jarring.
- **Precalculus**: polynomial, rational, and trigonometric manipulation; function composition (for §2.5); the Pythagorean and addition-of-angle identities (used to derive trig derivatives in §2.4).
- **No prior exposure to derivatives needed** — the chapter assumes the derivative is new.

**Core skills** (will match the chapter opening bullet list)
- state the limit definition of the derivative $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$ and apply it to compute derivatives from first principles for polynomial and root functions;
- use the power, constant-multiple, sum, product, and quotient rules to differentiate algebraic combinations of elementary functions;
- differentiate trigonometric, inverse trigonometric, exponential, and logarithmic functions;
- apply the chain rule to compositions, including nested compositions of three or more functions;
- differentiate implicitly when a relation cannot be solved for $y$ in closed form;
- compute higher-order derivatives and interpret $f''$ geometrically (concavity) and physically (acceleration).

**Key figures**
- secant-to-tangent limit diagram (§2.1): a curve with a sequence of secant lines converging to a tangent line as $h \to 0$.
- the derivative as a function (§2.2): a pair of graphs showing $f$ above and $f'$ below, aligned on the $x$-axis so zeros, extrema, and sign changes line up visually.
- product rule geometric picture (§2.3): a rectangle with sides $f$ and $g$, showing how the area changes in response to small increments in each side.
- chain rule as composed mapping (§2.5): stacked input-intermediate-output axes showing how a change at the input propagates through the intermediate to the output.
- implicit differentiation (§2.6): the circle $x^2 + y^2 = r^2$ with a tangent line drawn at a non-trivial point, used to motivate why solving for $y$ first is awkward.
- inverse-function derivative geometric picture (§2.7): the reflection-across-$y=x$ figure from Ch 1 reused, with tangent slopes at corresponding points marked as reciprocals.
- higher-order derivatives (§2.9): a single function graphed alongside $f'$ and $f''$ on aligned axes to show the hierarchy of slopes and curvatures.

**Handout self-sufficiency vs. video reinforcement**
- The handout alone carries the limit definition, every differentiation rule with a proof sketch, every worked example, and every strategy box.
- The companion videos add: (a) animated secant-to-tangent convergence that is hard to convey on a static page; (b) a dynamic slope-of-tangent-line demo where the tangent point sweeps across a curve and the slope is plotted below in real time, showing $f'$ emerging as a function; (c) narrated chain-rule intuition using successive mapping animations.
- Nothing in the video substitutes for reading the handout; promotion direction stays *video → handout*, never the reverse.

**Strategy boxes expected**
- *Choosing a differentiation rule* (§2.3 or §2.5): decision tree — is the expression a sum? a product? a quotient? a composition? solved / implicit? This is the highest-leverage strategy box in the chapter, because rule selection is the skill students struggle with the most.
- *Implicit differentiation* (§2.6): a 4-step method — (1) differentiate both sides with respect to $x$, treating $y$ as a function of $x$; (2) collect $dy/dx$ terms; (3) solve for $dy/dx$; (4) substitute a specific point if requested.
- *Inverse-function derivative* (§2.7): the formula $(f^{-1})'(y) = 1 / f'(x)$ at $y = f(x)$, with "when is this useful" guidance (when $f$ is hard to invert explicitly but $f'$ is easy, e.g., deriving $\arcsin'$ from $\sin'$).

**Notation introduced**
- $f'(x)$, $\dfrac{dy}{dx}$, $\dfrac{df}{dx}$, $\dfrac{d}{dx}[f(x)]$, $f''(x)$, $f^{(n)}(x)$ — the four conventional derivative notations, introduced with explicit guidance on when each is most natural. Index entries at first use for each of prime notation and Leibniz notation.
- $\Delta x$, $\Delta y$, $h$ — increment notation; flagged in a caution that $\Delta x$ and $h$ are synonyms in this context.
- $(f^{-1})'(x)$ — inverse-function derivative; notation chosen to avoid the $1/f'$ ambiguity.

**Common pitfalls (caution boxes)**
- *Power rule domain*: $\frac{d}{dx}[x^n] = n x^{n-1}$ holds for any real $n$ when $x > 0$; the subtleties for $n$ rational or $x \le 0$ need separate treatment. A caution flags this and defers the full treatment.
- *Quotient rule asymmetry*: $\frac{d}{dx}\left[\frac{f}{g}\right] = \frac{f'g - g'f}{g^2}$ is not symmetric in $f$ and $g$; order of terms in the numerator matters.
- *Chain rule is not multiplication*: $\frac{dy}{dx} \ne \frac{dy}{du} \cdot \frac{du}{dx}$ in the sense of two independent fractions; the Leibniz notation for the chain rule is a single expression whose internal consistency is a consequence of the rule, not an application of fraction algebra.
- *Implicit answers stay implicit*: $dy/dx$ from implicit differentiation is typically expressed in terms of both $x$ and $y$. Do not attempt to eliminate $y$ unless the problem explicitly demands a single-variable form.

**Open questions**
- *Timing of $e^x$ and $\ln x$ derivatives* (§2.8): the elegant derivation uses the limit $\lim_{h \to 0} \frac{e^h - 1}{h} = 1$, which in turn motivates *defining* $e$ as the base for which this limit equals 1. Stewart defers this partially (treats $e^x$ in a derivative chapter but defers the rigorous definition to after integration); Rogawski introduces $e$ more assertively up front. Decide at drafting time whether Ch 2 gives a rigorous derivation, a motivated informal derivation, or a *"we will justify this in Ch 4"* forward reference with the rule stated as given.
- *Section 2.7 vs 2.8 order*: inverse trig derivatives can be obtained either (a) via the inverse-function derivative rule (depends on §2.7), or (b) directly via implicit differentiation on $\sin(y) = x$. Current §2.7–§2.8 ordering assumes (a). If (b) turns out cleaner in draft, the two sections may swap.
- *Higher-order-derivative worked examples*: pick 2-3 canonical ones for §2.9 — candidates include $\sin$ / $\cos$ cycling through four derivatives, polynomials eventually vanishing, and the connection to velocity / acceleration. Decision deferred to drafting.

---

## Cross-chapter notation threading

A calculus handout that students flip back through needs notation to remain stable once introduced. Record decisions here the first time they are made; later chapters cite this section rather than re-deciding.

- `\arcsin` / `\arccos` / `\arctan` are the operators in the book. `\sin^{-1}`, `\cos^{-1}`, `\tan^{-1}` appear only inside a caution box when first warning against the reciprocal misreading.
- Domain restrictions are written inline inside `conditiondisplay` when they apply to one formula; moved to a `caution` when they are easy to forget.
- Equation numbers are per-chapter (`(1.3)`, `(2.7)`) and appear only when the equation is referenced later or is a formal statement (see spec §6).

*(Extend this list as later chapters introduce new convention decisions.)*

---

## Handout–video boundary (repeating rule)

For every chapter, the author **MUST** verify:

- the handout stands alone. A student without video access can still complete the chapter.
- the video does not introduce a fact, definition, or theorem not present in the handout.
- the video is free to add visual intuition, pacing, or alternative worked examples; these are reinforcement, not prerequisites.

When in doubt, promote a fact from video into the handout, not the other way around.

---

## Reviewing the roadmap

Revisit this file after every chapter reaches `done`. Typical updates:

- close the chapter's `Open questions` block or move remaining items into a follow-up issue.
- update cross-references that reach forward from earlier chapters to this chapter.
- check whether later chapters' `Prerequisites` blocks still list the right earlier sections after any restructuring.

If the overall arc changes — e.g. two chapters should merge, or a chapter should move earlier in the book — update this file **before** editing chapter sources. The roadmap is the plan; the chapter sources are the implementation.
