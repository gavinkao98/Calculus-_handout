# Exercises: Minimum Skeleton

Full exercise-system design is deferred until the book's main content is largely complete (see [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §14). This file is the **minimum skeleton** — the decisions that should be locked before chapters start accumulating real exercises, so that later work does not have to retrofit every section.

Anything in this file marked *(TBD)* is explicitly open. Anything not marked *(TBD)* is a working decision that authors should follow until this file revises it.

---

## What lives in the spec vs. here

[`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5 (`exercise` environment) + §14 (deferred design) establish:

- every section end **MUST** carry either a real `\subsection*{Exercises}` block or the TODO placeholder comment `% TODO: add \subsection*{Exercises} block with end-of-section problems for Section N.M.`
- exercises are **book-only** — they do not flow into slides, narration, or Manim storyboards (see [`README.md`](README.md) *Media scope*).
- the full exercise system (difficulty markers, answer appendix, inline self-check variants, hint format) is **deferred**.

This file sits between the placeholder rule and the full deferred design. It pins down the minimum so that when the full design opens, it is refining existing structure, not inventing from scratch.

---

## Minimum per-section target *(working decision)*

- **8–12 exercises per section**, front-loaded toward the conceptual and computational end of the spectrum for early chapters.
- Shorter sections may go as low as 6. Strongly computational sections may go as high as 15.
- A section with fewer than 6 exercises is out of compliance once it leaves the TODO-placeholder state.

Rationale: enough to give self-study readers repeated practice on each new skill, few enough that a motivated reader can work every exercise without burning a weekend.

---

## Type mix *(working decision)*

Every section's exercise block **SHOULD** include at least one of each type that applies. Not every section needs every type.

| Type | Purpose | Target share of block |
|---|---|---|
| `conceptual` | "why" or "what fails if" — forces the reader to state a definition or decide whether a condition holds. | ≥ 20% |
| `computational` | direct application of a method to a clean input. | 40–60% |
| `reasoning` | short proofs, counterexample construction, "for which inputs does this identity hold?" | ≥ 10% |
| `applied` *(optional)* | physics / economics / geometry setup where applicable. | 0–20% |

The type taxonomy used inside the `exercise` environment itself is *(TBD)* — possible options include a `type=` key-value argument, a `\begin{exercise}[conceptual]` optional label, or no in-source marker (type enforced only by author judgment). Pick one in the full design round.

---

## Answers and hints *(working decision)*

Two decisions are load-bearing:

- **do exercises carry an answer at all?**
  Working default: **selected computational exercises carry a final numerical or symbolic answer** at the end of the book, so a self-study reader can check their work without seeing a full solution. Conceptual and reasoning exercises default to no answer key.
- **do exercises carry hints?**
  Working default: **no inline hints for exercises**. If an exercise needs a hint to be approachable, it is probably set up wrong, and a preceding worked example should carry the idea instead.

The answer-appendix format (end of chapter vs. end of book, selection criterion, encoding in source) is *(TBD)*.

---

## Difficulty markers *(deferred)*

Deliberately not decided yet. The full design round will choose between:

- no markers at all (simplest — order within section carries difficulty).
- ⭐ / ⭐⭐ / ⭐⭐⭐ inline markers.
- letter codes (`A`, `B`, `C`).
- separate `\subsection*{Exercises}` and `\subsection*{Challenge Problems}` blocks.

Until that decision lands, **do not** encode difficulty in exercise sources. Ordering within the block is the only allowed difficulty signal.

---

## Numbering and labels *(working decision)*

- exercises are numbered per section: `1`, `2`, ..., restart at each new section.
- labels follow the project label convention in [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md): `ex:sectionslug-descriptor`. Example: `ex:limits-squeeze-1`.
- labels **SHOULD** appear on exercises that later sections will cite. Most exercises do not need labels.

---

## Format inside `\subsection*{Exercises}` *(working decision)*

```latex
\subsection*{Exercises}

\begin{exercise}
  Prompt text.
\end{exercise}

\begin{exercise}
  Another prompt. May contain display math, inline math, and short
  multi-part structure using \texttt{enumerate}.
\end{exercise}
```

Multi-part exercises use `enumerate` inside the `exercise` body. Do not invent new environments for sub-parts until the full design round.

---

## What NOT to do before the full design round

These are the traps we want to avoid accumulating before the exercise system is designed properly:

- **do not** invent per-chapter exercise macros. If a shortcut seems helpful, note it in the chapter's open-questions list in [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) rather than adding a `\newcommand`.
- **do not** mix slide or narration content into exercise prompts — exercises are book-only.
- **do not** seed the answer appendix until the selection criterion and format are locked.
- **do not** mark difficulty in the source.
- **do not** include hints inline.

---

## When this file is upgraded

Trigger: **a solid majority of chapters have complete main content** (per spec §14).

At that point, the dedicated exercise design round will:

1. audit what's already in the TODO placeholders and the real exercise blocks that have accumulated.
2. decide the deferred items: difficulty markers, answer appendix format, hint policy, in-source type taxonomy, environment variants (self-check, challenge).
3. replace this skeleton file with the full spec, bumping a version number.
4. retrofit existing exercise blocks to the new spec, one chapter at a time.

Until then, anything not covered here should err on the side of **simple and reversible** — treat exercises as prose-with-a-frame rather than as a domain-specific sub-system.
