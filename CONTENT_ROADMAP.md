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
| 1 | Foundations: Inverse Functions and Limits | draft | 1.1 Inverse Functions and One-to-One Functions; 1.2 Inverse Trigonometric Functions; 1.3 Limits; 1.4 One-Sided and Infinite Limits; 1.5 Limit Laws; 1.6 The Precise Definition of a Limit |
| 2 | *(TBD — fill in before drafting)* | planned | — |
| 3 | *(TBD)* | planned | — |
| … | | | |

Author note: this list is currently a stub. The first editorial task that ships as part of Phase 3 of the repo restructure should be to commit the remaining chapter titles and section skeletons here — not as a plan to follow rigidly, but as a working hypothesis that reviewers can push back on.

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

### Chapter 1: Foundations — Inverse Functions and Limits

**Status**: draft
**Source file**: [`chapters/ch01_foundations.tex`](chapters/ch01_foundations.tex)
**Estimated length**: *(fill in after first full compile)*

**Role in the arc**
Sets up the two foundational machines of calculus: inverse functions (the algebraic machine for "running a rule backward") and limits (the analytic machine for "approaching without equalling"). The chapter intentionally pairs these because both force the reader to reason about correspondences and approximations rather than about formulas in isolation.

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
