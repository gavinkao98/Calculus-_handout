# Calculus Textbook Project: Master Writing Guide

**Version 2.0.4** — adds four structural rules codified from the Chapter 1 review and closes two rule-vs-manuscript gaps: the index policy is now backed by real build infrastructure (`imakeidx`, `\makeindex`, `\printindex`), and end-of-section exercise placeholders are formalized via TODO markers and Known Open Items tracking (maintained in [`README.md`](README.md)). Earlier foundations (rationale framework, shared counters for formal statements, two-tier exercise policy, cross-reference/typography/index/exception protocols) are retained from v2.0.

This file is the authoritative writing context for future chapter drafting and revision in this project.
It consolidates:
- the original AI writing brief
- the updated environment-classification rules
- the figure and placement rules tested in Chapter 1
- the editorial decisions already used in the current manuscript

The goal is that later chapters can follow this file directly.

## How To Read This Document

Most rules in this document are followed by a **Rationale** line. The rules are the normative layer (what to do); the rationale is the interpretive layer (why the rule exists, so contributors facing an edge case can reason from purpose rather than strict text). When a rule and its rationale appear to conflict in a new situation, treat it as a signal to revise the rule rather than to invent a silent exception.

For the repository overview, see [`README.md`](README.md).
For the storyboard-driven Manim workflow, see [`MANIM_README.md`](MANIM_README.md).
For the slide/PDF audio and video workflow, see [`VIDEO_README.md`](VIDEO_README.md).

## Project Purpose

This project creates a unified calculus textbook in LaTeX from manuscripts written by multiple instructors.

The goal is not to preserve manuscript layout or note-taking style.
The goal is to preserve and standardize:
- mathematical meaning
- logical structure
- pedagogical intent

The final book should read like a coherent textbook written in one voice.

## Content Layout

- `main.tex`: document structure only
- `preamble/`: packages, layout, theorem setup, numbering, bibliography
- `preamble/packages.tex`: shared package loading
- `preamble/layout.tex`: global spacing, float, header/footer, and chapter-title layout
- `preamble/theorem_setup.tex`: theorem-like environments, `solution`, stronger pagination protection for formal result blocks, and lighter flow rules for examples, solutions, and proofs
- `preamble/numbering.tex`: numbering rules such as equation numbering
- `preamble/bibliography.tex`: bibliography backend and source registration
- `chapters/`: one file per chapter
- `refs/`: bibliography database

For chapter-writing tasks, work primarily in the relevant file inside `chapters/`.

## Core Source Priority

1. The professor manuscripts are the primary source.
2. Stewart, *Calculus: Early Transcendentals*, is the secondary reference.
3. Stewart may be used to fill gaps, smooth exposition, supply standard phrasing, or confirm standard organization.
4. If the manuscript and Stewart differ, prefer the manuscript unless there is a clear mathematical error.
5. Do not invent new mathematical content casually unless it is supported by the manuscript or by standard textbook treatment.

## Output Mode for Chapter Writing

When asked to draft or revise a chapter or section:

1. Output LaTeX content only.
2. Do not generate `\documentclass`, package lists, preamble code, bibliography setup, or formatting code unless explicitly asked.
3. Do not generate full project files unless explicitly asked.
4. When writing a chapter or section, produce only the content body that belongs in the chapter file.
5. Focus on mathematical content and pedagogy, not template engineering.

## General Editorial Principle

Treat each manuscript as a content source, not a layout source.

Do not preserve:
- handwritten page layout
- note-style fragmentation
- board-style arrows
- decorative color usage
- margin comments
- decorative boxes
- informal blackboard shorthand

Convert manuscript material into formal textbook exposition.

## Document Structure

Use this hierarchy for numbered, table-of-contents-bearing headings:
- `chapter`
- `section`
- `subsection`

A fourth level is permitted in the form of `\paragraph{...}` (unnumbered, not entered in the table of contents) when a subsection contains three or more short logical units that each deserve a visual heading but do not justify a numbered subsection. Do not use `\subsubsection`.

Rationale: limiting numbered depth to three levels keeps the table of contents readable and discourages over-fragmentation. `\paragraph` gives a lightweight way to structure small units without inflating the ToC, which is especially useful for sections such as "Computational Techniques" where five short techniques share a common theme but do not each deserve a numbered subsection.

A section title must not duplicate substantial portions of its parent chapter title. If the chapter title lists the themes the chapter will cover, each section's title should name one of those themes, not repeat the full list. For example, a chapter titled "Inverse Functions and One-to-One Functions" should have a section titled "Inverse Functions" (or "One-to-One Functions"), not another "Inverse Functions and One-to-One Functions."

Rationale: a section title that echoes the chapter title carries no information for the reader and makes the table of contents look like it is stuttering. Section titles earn their place in the ToC by naming the specific theme they develop.

### Heading capitalization

- `\chapter{...}` and `\section{...}` titles use Title Case (e.g., "Inverse Functions and One-to-One Functions", "The Limit of a Function").
- `\subsection{...}` and `\paragraph{...}` titles use sentence case (e.g., "Computing limits algebraically", "Restricted sine and arcsine").
- Proper nouns remain capitalized regardless of case style (e.g., "Newton's method", "Stewart's notation").
- Subsection titles should name the unifying theme of their content, not merely enumerate the objects treated within. Prefer "Limits of piecewise-defined functions" over "The absolute value function and the greatest integer function"; prefer "Restricted sine and arcsine" over "sin, arcsin, and their graphs."

Rationale: the contrast signals hierarchy visually. Title-cased sections function as named landmarks a reader looks up in the ToC; sentence-cased subsections read as continuations of the running argument. Consistency here makes the ToC feel typeset rather than improvised. Naming the theme rather than the ingredients makes subsection titles useful in the ToC: the reader learns what the subsection is about, not which specific functions happen to be the examples.

Within a section, prefer the following pedagogical order:
1. short introduction or motivation
2. definitions
3. properties, propositions, and theorems
4. proofs when needed
5. examples with solutions
6. exercises (inline or end-of-section; see Exercise Policy)

If the manuscript is disorganized, reorganize it into this structure.

## Chapter Opening and Closing Norms

Every chapter must open with an overview of one to two paragraphs, placed immediately after the `\chapter{...}` line and before the first `\section{...}`. The overview should:
- identify the mathematical territory the chapter covers
- name the connection to earlier chapters
- preview the central results the reader should look forward to

The overview is prose, not a definition, theorem, or remark. It does not itself introduce new notation.

Chapters may end with an optional short summary under `\section*{Summary}`. If included, the summary is at most one page, does not appear in the numbered section sequence, and may list key definitions and theorems without reproducing full statements. Do not use a summary to introduce new results.

Rationale: a fixed opening template gives multi-author contributions a common rhythm and makes later review easier. Chapter-opening motivation is one of the most visible style markers in a textbook, and unifying it has outsized impact on perceived voice.

## Approved Environment Set

Use only the following standard environments unless explicitly instructed otherwise:
- `definition`
- `theorem`
- `lemma`
- `proposition`
- `corollary`
- `example`
- `remark`
- `exercise`
- `solution`
- `proof`

Interpret manuscript labels by mathematical role, not surface wording.

Examples:
- Def / Definition -> `definition`
- Property -> `proposition`
- Thm -> `theorem`
- Note -> `remark`
- Homework / Practice -> `exercise`
- Worked calculation -> `example` followed by `solution`

## Environment Classification Rules

### Definition

Use a `definition` only when introducing a new mathematical concept or term for the first time.

A definition answers:
"What does this mean?"

Definitions should be:
- precise
- formal
- concise

Do not mix examples, long explanation, historical comments, or intuition into a definition.

Use `definition` for topics such as:
- limit
- left-hand limit
- right-hand limit
- continuity
- differentiability
- derivative
- integrability
- one-to-one function
- inverse function
- inverse trigonometric functions
- local maximum / minimum
- absolute maximum / minimum

Do not introduce a `\begin{definition}` for a term that the current chapter will neither use nor develop. A formal, numbered definition makes a promise to the reader that the term is now available for reuse in the text that follows. If a term needs to be previewed because it will be studied in a later chapter, write it as forward-looking prose (optionally with an index entry), not as a numbered formal statement.

Rationale: numbered definitions are load-bearing references. Using one for a term the chapter never invokes again dilutes the signal that "this environment flags something you will be expected to recall," and clutters the cross-reference graph. Forward-looking prose preserves the preview without making the false promise.

### Remark

Use a `remark` only for genuine asides, warnings, or supplementary comments that are not part of the main exposition. A remark should feel like a sidebar the student could skip without losing the main thread.

Good uses of `remark` include:
- notation warnings (e.g., `\sin^{-1} x` does not mean `1/\sin x`)
- branch-choice conventions that differ between sources (e.g., which principal range is used for `\arcsec x`)
- identity restrictions that are easy to overlook (e.g., `\arcsin(\sin x)=x` holds only on the principal interval)
- the horizontal line test as a named geometric criterion
- short historical notes (2 to 5 sentences)
- forward references to later chapters (e.g., "continuity will be studied systematically later")

Do NOT use a `remark` for:
- main-line knowledge that every student must read (write it as prose instead)
- domain and range statements that follow directly from a definition (state them as a plain sentence after the definition)
- core conceptual points such as "the limit does not depend on f(a)" or "∞ is not a real number" (these belong in the running text)
- verbal summaries of theorem statements (place them as prose after the theorem)
- content that, if skipped, would leave a gap in the student's understanding

A remark is not the main formal result of the section.
A remark usually does not need a proof.

Important rules:
1. Do not hide a genuinely important reusable formal result inside a remark.
2. If the content is part of the logical flow of the section, it should be prose, not a remark.
3. When in doubt, prefer prose over remark. A chapter with fewer than 15 remarks is usually healthier than one with 30.

### Theorem

Use a `theorem` only for the main and important results of a section or chapter.

A theorem should be a result students are expected to remember and reuse later.
Do not label too many results as theorems.

Typical `theorem` topics:
- core limit laws
- squeeze theorem
- intermediate value theorem
- extreme value theorem
- mean value theorem
- fundamental theorem of calculus
- major derivative and integral rules
- a function has an inverse if and only if it is one-to-one, when this is the main result of the section

### Proposition

Use a `proposition` for a formal mathematical result that is worth stating but is not the main result of the section.

A proposition is appropriate for:
- formal supporting facts
- technical results
- basic consequences of definitions
- algebraic properties of inverse functions
- secondary but reusable results

Typical `proposition` topics:
- `f^{-1}(f(x)) = x` and `f(f^{-1}(y)) = y`
- uniqueness of limits
- the criterion for a two-sided limit from one-sided limits
- standard identities for inverse trigonometric functions

### Lemma and Corollary

Use a `lemma` only when an intermediate result is genuinely needed for a later proof.
Use a `corollary` only when a result follows immediately from a theorem or proposition and naming the consequence improves pedagogy.

Do not add lemmas or corollaries mechanically.

## Practical Decision Rule

Before choosing an environment, ask:

- Am I introducing a new term or concept?
  Use `definition`.

- Am I giving explanation, intuition, warning, notation guidance, or short historical/application context?
  Use `remark`.

- Is this the main formal result of the section?
  Use `theorem`.

- Is this a formal result, but not the main result of the section?
  Use `proposition`.

## Example, Solution, and Proof Policy

This rule is mandatory.

1. Use `solution` for worked examples.
2. Use `proof` only for genuine proofs of mathematical statements.
3. Do not label ordinary worked examples as `proof`.
4. A theorem, proposition, lemma, or corollary may be followed by a `proof`.
5. Not every theorem-like statement requires a proof.
6. Include a proof only when at least one of the following holds:
   - the manuscript contains a proof
   - the proof is logically important for the chapter
   - the proof is pedagogically important for student understanding
7. If a theorem or proposition appears without a proof in the manuscript, it may remain without a proof unless a proof is clearly needed.
8. Do not add proofs to every theorem-like statement automatically.
9. An `example` should be followed by a `solution` if a worked-out answer is included.
10. `exercise` environments should normally appear without solutions unless the user explicitly asks for a solutions version.
11. The `solution` environment has its own visual style distinct from `proof`: a bold "Solution." label (not italic), upright body text, and a trailing QED box. Do not implement `solution` as an alias for `proof`.

In short:
- theorem-like statements -> `proof` when warranted
- worked examples -> `solution`, visually distinct from `proof`

Rationale: students scan textbook pages for cues that tell them "this is how to work a problem" versus "this is how to justify a theorem." If `solution` and `proof` look identical, that affordance is lost. The visual distinction is cheap to set once in the template and high-value for every subsequent reader.

## Example Selection Policy

1. Preserve professor-manuscript examples unless the user explicitly asks for cuts or restructuring.
2. Do not delete, merge, or substantially rewrite a manuscript example unless there is a clear editorial reason and the user has asked for that level of intervention.
3. Additional examples may be added when they materially improve student understanding.
4. Good reasons to add an example include:
   - illustrating a central theorem
   - covering a standard case missing from the manuscript
   - reinforcing a common source of confusion
   - giving a slightly more challenging example after a basic one
5. Added examples should be concise, pedagogically purposeful, and consistent with the level of the section.
6. Do not add filler examples simply to make a section look more complete.

## Exercise Policy

This project distinguishes two kinds of exercises: inline exercises and end-of-section exercises.

### Inline exercises

Inline exercises are short problems placed within a section, near the relevant definition or example. They are drawn exclusively from the professor manuscript.

1. Include inline exercises only if they are present in the professor manuscript.
2. Do not invent new inline exercises.
3. Do not delete, merge, split, reorder, rewrite, simplify, or expand manuscript inline exercises unless the user explicitly asks for editorial adjustment.
4. Do not convert inline exercises into examples unless the source clearly provides guided exposition.
5. Use the `exercise` environment for all inline exercises.

### End-of-section exercises

End-of-section exercises are collected problem sets at the end of each section, under a `\subsection*{Exercises}` heading (or `\paragraph{Exercises.}` for short sets).

1. End-of-section problem sets may combine manuscript problems with supplementary problems written for the textbook.
2. Manuscript problems appear first in the set; supplementary problems follow.
3. Supplementary problems must be clearly marked. Use a `\paragraph{Supplementary.}` heading within the exercise set, or prefix each supplementary problem with a dagger (`$^\dagger$`) and explain the convention once in the front matter.
4. Use the `exercise` environment for both manuscript and supplementary problems; the distinction is carried by placement and marking, not by a different environment.
5. End-of-section exercises normally appear without solutions unless the user explicitly asks for a solutions version.
6. Do not add supplementary problems to fill space. Every supplementary problem must target a specific skill or case not covered by manuscript problems.

This is the target policy. Chapters that do not yet have end-of-section exercises must carry a placeholder comment at each section end in the form `% TODO: add \subsection*{Exercises} block with end-of-section problems for Section <N.M>.` The TODO marker makes the gap visible in the source and must be replaced with real exercise content before the chapter is considered complete. A chapter without either the final `\subsection*{Exercises}` block or the TODO placeholder is out of compliance.

Rationale: the manuscript is the primary source, but a calculus textbook without any end-of-section problems is not usable as a primary text. The two-tier structure preserves manuscript authority (inline material is untouchable) while letting the editor produce a publishable book with practice material that manuscripts often lack. Explicit TODO placeholders keep the rule authoritative without pretending every chapter is already finished, and make the remaining work auditable.

## Numbering Policy

This project uses chapter-based numbering with a single shared counter for all formal statements.

### Shared counter group

The following environments share one counter, incremented in order of appearance within a chapter:
- `definition`
- `theorem`
- `proposition`
- `lemma`
- `corollary`

Desired style (actual numbering will depend on the order in which they appear):
- Definition 1.1
- Theorem 1.2
- Proposition 1.3
- Definition 1.4
- Theorem 1.5

The number reflects a statement's position in the running sequence of formal statements, not its position among statements of the same type.

### Separate counters

The following environments each have their own counter, reset at the start of every chapter:
- `example` — Example 1.1, Example 1.2, ...
- `exercise` — Exercise 1.1, Exercise 1.2, ...
- `remark` — Remark 1.1, Remark 1.2, ...
- `figure` — Figure 1.1, Figure 1.2, ...
- `equation` — (1.1), (1.2), ... (see Equation Numbering Policy)

### Manual numbering

Do not manually number environments or figures. Let the project template handle numbering.

Rationale: a shared counter for formal statements lets the reader infer position from the number alone — "Theorem 1.5 is just after Definition 1.4" is immediately obvious, whereas with separate counters they could be pages apart. Examples, exercises, remarks, and figures keep their own counters because they are browsed as indexed collections: a student looking for "Example 1.3" wants the third worked example, not the third item of mixed type.

Implementation note: `preamble/theorem_setup.tex` implements the shared counter group with the `aliascnt` package rather than amsthm's `[theorem]` optional argument. The pattern for each non-master environment is:

```latex
\newaliascnt{proposition}{theorem}
\newtheorem{proposition}[proposition]{Proposition}
\aliascntresetthe{proposition}
```

This keeps the counter-name that amsthm records distinct for each environment (so `cleveref` resolves `\cref{prop:...}` as "Proposition", `\cref{def:...}` as "Definition", and so on) while the step still happens on the master `theorem` counter, which is chapter-scoped. The plain `\newtheorem{foo}[theorem]{Foo}` shortcut is not used because amsthm tags every label from it with counter name `theorem`, which would make `cleveref` print every formal-statement reference as "Theorem" regardless of the environment actually used.

If you add a new formal-statement environment in the future, follow the three-line aliascnt pattern above and add the matching `\crefname` / `\Crefname` declarations near the bottom of the file.

## Equation Numbering Policy

Number a display equation if and only if at least one of the following holds:
- the equation is referenced later in the same chapter via `\eqref{...}` or `\cref{...}`
- the equation is referenced in a later chapter
- the equation is the formal statement of a theorem, proposition, lemma, or corollary

Otherwise, use unnumbered display math `\[...\]` or unnumbered `align*` / `gather*`.

Rules:
1. Equations inside a `definition` body are unnumbered unless referenced elsewhere.
2. Equations inside `example` and `solution` bodies are unnumbered unless referenced later.
3. Chains of equality in a worked computation use unnumbered `align*` or stacked `\[...\]` blocks.
4. Do not number every display equation by default. A number is a promise that the equation will be named later.

Rationale: over-numbered equations clutter the page and dilute the signal value of a number. When `(1.17)` appears unreferenced, the reader spends a moment confirming the chapter does not depend on it. Reserving numbers for genuine anchor points makes the numbers themselves informative.

## Cross-Reference Policy

The project uses the `cleveref` package to generate cross-reference prefixes automatically.

Rules:
1. Use `\cref{label}` for all in-prose references. The package inserts the correct prefix (Figure, Theorem, Definition, Section, etc.).
2. Use `\Cref{label}` only when the reference starts a sentence and must be capitalized.
3. Do not write `Figure~\ref{...}`, `Theorem~\ref{...}`, `Section~\ref{...}`, or any other manual prefix. Let `cleveref` control the prefix.
4. `\eqref{label}` remains preferred for equation references because it inserts the parentheses automatically.
5. Label format: `type:short-description`, where `type` is one of `fig`, `thm`, `def`, `prop`, `lem`, `cor`, `eq`, `sec`, `subsec`, `ex`, `exer`, `rem`.
   - Good: `fig:horizontal-line-test`, `thm:squeeze`, `def:limit`, `eq:fundamental-theorem`.
   - Bad: `fig1`, `eq2`, `thm-important`, `horizontal_line`.
6. Labels use hyphens for word separation, not underscores or camelCase.

Rationale: mixing `\cref` and manual `\ref` produces inconsistent spacing and capitalization across the book. Centralizing on `\cref` also means a later decision to change "Theorem" to "Thm." in running text can be done in one package configuration, not 300 files.

### Paired definitions at different precision levels

Some concepts — most notably "limit" — receive both an informal introduction and a later precise (epsilon-delta) restatement. When a concept is defined twice at different precision levels:

1. Use distinct label keys that indicate the precision level, such as `def:limit-informal` and `def:limit-precise`.
2. The second definition should explicitly cross-reference the first: "This formalizes the informal notion introduced in \cref{def:limit-informal}."
3. The first definition should forward-reference the second: "A precise formulation is given in \cref{def:limit-precise}."
4. Both definitions share the formal-statement counter group (see Numbering Policy) and count as two separate `definition` environments.

Rationale: students returning to look up "limit" should find both versions and understand the relationship between them immediately. Silent duplication without cross-linkage is a common source of confusion in multi-author calculus texts.

## Notation Policy

Notation must remain consistent across all chapters.

Use standard notation such as:
- `\arcsin x`, `\arccos x`, `\arctan x`
- `\sin`, `\cos`, `\tan`, `\ln`, `\exp`
- `e^x`
- `f'(x)` for general derivative notation
- `\dfrac{d}{dx}` when an explicit derivative operator is needed
- `\lim_{x \to a} f(x) = L`
- `\lim_{x \to a^-}`, `\lim_{x \to a^+}`
- `\mathbb{R}`
- interval notation such as `(a,b)`, `[a,b]`, `[a,b)`, and so on

Do not switch notation style from chapter to chapter without a strong reason.

When a manuscript adopts a less-common but mathematically legitimate convention, such as a principal range for an inverse trigonometric function, preserve it unless there is a strong reason to change it.
If the convention may surprise students, add a brief `remark` noting a common alternative and clarifying the choice made in this text.

## Formula Display Policy

Use three levels of formula presentation consistently throughout the book.

### Inline Math

Use inline math `\(...\)` for formulas that are short and behave as part of a sentence.

Typical uses:
- single symbols and variables
- function names and short expressions
- short intervals
- short limits
- short derivative notation

Examples:
- `\(f\) is continuous at \(a\)`
- `\(\lim_{x\to a} f(x)=L\)`
- `\(f'(x)\)`

### Display Math

Use display math `\[...\]` when the formula is the visual focus of the sentence or when readability benefits from separation.

Typical uses:
- the main formula in a definition
- theorem and proposition statements
- multi-step calculations
- long fractions
- identities to be emphasized
- expressions in example prompts such as "Evaluate" or "Show that"
- piecewise definitions

If the reader should stop and look carefully at the formula, prefer display math.

### Inline Math with `\displaystyle`

Use `\(\displaystyle ...\)` only sparingly.

This is appropriate only when:
- the formula must remain inside the sentence, and
- it contains a large fraction, integral, sum, or limit that becomes hard to read in ordinary inline style.

Examples:
- `the difference quotient \(\displaystyle \frac{f(x+h)-f(x)}{h}\)`
- `the definite integral \(\displaystyle \int_a^b f(x)\,dx\)`

Do not use `\displaystyle` as the default way to make formulas look important.
If a formula is important enough to stand out, it usually should be moved to display math instead.

### Inline Fractions: `\frac` vs `\dfrac`

When a fraction appears in inline math, `\frac` produces a smaller, cramped version. If the same fraction also appears nearby in display math, the size jump is visually jarring. Use `\dfrac` in inline math for substantive fractions whose display-size counterpart appears nearby.

Use `\dfrac` for:
- fractions with expressions in the numerator or denominator, such as `\(\dfrac{1}{x^2}\)`, `\(\dfrac{2x}{x-3}\)`, `\(\dfrac{\varepsilon}{4}\)`
- fractions in example statements, figure captions, or prose that also appear in adjacent display equations

Keep `\frac` for:
- simple well-known constants in interval notation, such as `\(\frac{\pi}{2}\)`, `\(\frac{3\pi}{2}\)` — using `\dfrac` inside `\left[...\right]` brackets would make them disproportionately tall
- symbolic indeterminate-form notation such as `\(\frac{0}{0}\)`
- any fraction already inside display math (display math renders `\frac` at full size automatically)

### Formulas in Tables

Inside tables, prefer `\tfrac` or plain-text forms instead of `\dfrac` unless the larger display style is genuinely necessary.
This helps keep table rows compact and visually even.

### House Rule for Formula Choice

- short formula inside a sentence -> inline math
- main formula or visually central expression -> display math
- inline formula with large operators only when the sentence must remain unbroken -> inline math with `\displaystyle`

Avoid scattering large `\displaystyle` expressions through prose when ordinary inline or display math would be clearer.

## Terminology Policy

Choose one standard term and use it consistently.

Examples:
- one-to-one
- inverse function
- inverse sine / arcsine
- squeeze theorem
- increasing / decreasing
- limit
- derivative
- tangent line

If the manuscript uses multiple synonymous expressions, normalize them.

## Writing Style

The book should read like a formal undergraduate textbook that is still accessible to strong high school students.

Prefer:
- concise mathematical prose
- complete sentences
- direct statements
- clear transitions
- standard proof flow
- guided examples

Avoid:
- lecture-note fragments
- casual spoken fillers
- blackboard shorthand
- overly chatty language
- unexplained jumps in logic

Useful transitions include:
- Therefore,
- Hence,
- Thus,
- By definition,
- It follows that,
- From this identity,
- Applying the previous theorem,

### Voice and Person

Use the first-person plural "we" for instructional prose. Examples:
- "We now introduce the precise definition."
- "We want to find \(\cos y\)."
- "Applying the previous theorem, we obtain..."

Do not use "you" or "the reader" as the subject of instructional prose. Do not use "I" or "the author" at any point in the main text.

Imperative mood is also acceptable and is standard for setting up examples and proofs:
- "Let \(f\) be a one-to-one function."
- "Observe that both sides vanish at \(x=0\)."
- "Consider the function \(g(x)=x^2\)."

Rationale: "we" carries the student along with the argument without putting them on the spot; "you" turns exposition into instruction-giving; "I" is inappropriate in a multi-author text. Imperative mood is neutral and traditional for mathematical setup sentences.

### Voice Reference

The following passage (adapted from the Chapter 1 opening) exemplifies the target voice. When in doubt about tone, consistency, or register, compare a draft against this sample.

> A function can have an inverse only when each output comes from exactly one input. This motivates the following definition.
>
> **Definition.** Let \(f\) be a function with domain \(A\). We say that \(f\) is *one-to-one* if \(f(x_1)\ne f(x_2)\) whenever \(x_1\ne x_2\).
>
> Not every function has an inverse. A function can have an inverse only if each output corresponds to exactly one input; in other words, the function must be one-to-one. For \(g(x)=x^2\) on \([-1,1]\), the value \(\tfrac14\) comes from both \(\tfrac12\) and \(-\tfrac12\). Therefore \(g^{-1}(\tfrac14)\) is not well defined.

Key features of this voice:
- short declarative sentences
- explicit logical connectives ("therefore", "in other words", "because")
- motivation precedes formalism by at most one or two sentences
- the first mathematical object the student meets is often a concrete example, not an abstract formulation
- `\emph{...}` marks the newly introduced term inside the definition

Rationale: multi-author projects drift in tone even with clear rules. A fixed reference paragraph lets contributors calibrate against a concrete sample rather than interpreting abstract guidelines.

## Pedagogical Style

Assume the text is teaching students, not merely recording mathematics.

Therefore:
1. Definitions should be stated clearly.
2. Examples should be instructive, not merely computational.
3. Solutions should explain the key step or idea, not just present algebraic manipulation.
4. Proofs should be readable and logically complete when included.
5. Exercises should be grammatically complete and appropriately placed.

## Short Historical and Application Notes

Short historical or applied motivation is encouraged when it genuinely helps students understand why a topic matters.

Use such notes sparingly.

Best locations:
- chapter openings
- section openings
- immediately before an important new concept

Recommended length:
- usually 2 to 5 sentences

Good uses:
- motivating inverse functions with real conversion formulas
- motivating inverse trigonometric functions with angle recovery from ratios
- giving a brief note on Newton, Leibniz, and the later rigorization of limits

Do not let history or applications overwhelm the mathematics.

## Typography Policy

Consistent micro-typography matters for a textbook-grade document.

### Dashes

- Hyphen (`-`): for hyphenated words such as "one-to-one", "left-hand", "real-valued".
- En dash (`--`): for numerical and page ranges, such as "pages 12--15", "the interval 3--5".
- Em dash (`---`): for parenthetical interruptions in prose. Use sparingly; a comma or a pair of parentheses is usually better.

### Ellipses

Use `\dots` (context-aware) rather than hard-coding `\ldots` or three literal periods.

Examples:
- In text: `the sequence \(a_1, a_2, \dots, a_n\)`
- In display math with operators: `\(a_1 + a_2 + \dots + a_n\)` — LaTeX selects `\cdots` automatically.

### Math spacing

- Binary relations and operators: no explicit spacing (`\ne`, `\le`, `\ge`, `+`, `-`). LaTeX inserts the correct spacing.
- Differentials in integrals: thin space before the differential, such as `\int_a^b f(x)\,dx`.
- Function application: no space (`f(g(x))`, not `f( g(x) )`).
- Use `\,`, `\;`, or `\quad` only when symbol alignment or readability actually requires it.

### Delimiters

- Use `\left...\right` when the enclosed expression contains tall objects (fractions at full size, nested radicals, large operators).
- Use fixed-size delimiters for short expressions: prefer `(x+1)` over `\left(x+1\right)`.
- For interval notation with small displayed fractions, `\left[-\tfrac{\pi}{2}, \tfrac{\pi}{2}\right]` is appropriate because `\tfrac` keeps the fraction at reduced height.

### Quotation marks

- Double quotation marks in prose: `` ``...'' `` (double backtick open, double apostrophe close).
- Single quotation marks: `` `...' ``.
- Do not use straight ASCII quotes (`"..."`) in chapter files.

### Emphasis

- Emphasize newly introduced terms with `\emph{...}` inside the `definition` body.
- Do not use `\textbf{...}` or `\textit{...}` in running text for emphasis.
- Reserve bold for environment labels and theorem statements, which the template already handles.
- Do not emphasize the same term twice.

Rationale: micro-typography is invisible when consistent and distracting when inconsistent. Locking these details at the rule level means contributors do not have to think about them, and an automated checker can eventually verify compliance.

## Figure Policy

Figures are used for teaching, not decoration.

Add a figure only when it genuinely improves understanding, especially for:
- function graphs
- geometric interpretations
- domain and range illustrations
- one-to-one and inverse-function diagrams
- horizontal line test or vertical line test illustrations
- limit behavior
- one-sided limits
- asymptotes
- tangent lines
- inverse trigonometric triangles
- other strongly visual concepts

Do not add decorative or unnecessary figures.

In worked examples, a figure must not pre-label the quantity that the example's own derivation is about to produce. If the example asks the reader to compute a side length, angle, or coordinate, label that quantity with a variable (or leave it unlabelled) in the accompanying figure; let the prose derive its value. Pre-filling the answer on the diagram turns the example into a picture to be copied rather than a calculation to be followed.

Rationale: figures in a textbook are part of the pedagogy, not just illustration. A diagram that already shows "`3`" next to the side the student is supposed to solve for removes the reason to read the solution. Using a variable (for example, `a`) in the figure and computing `a = 3` in the text keeps the figure and the prose doing complementary jobs.

## Figure Tool Choice

Use:
- `pgfplots` for coordinate graphs, plotted functions, asymptotes, and analytic behavior
- `TikZ` for conceptual diagrams, mapping diagrams, intervals, arrows, and geometric sketches

In general:
- function graph -> `pgfplots`
- teaching diagram -> `TikZ`

## Figure Style

All figures should be:
- clean
- simple
- mathematically clear
- textbook-like

Avoid:
- excessive color
- decorative shading
- artistic effects
- cluttered labels
- handwritten styling

Use color only when it clearly distinguishes mathematical roles, and keep the figure readable in grayscale as much as possible.

## Caption Policy

Every figure should have a short, clear caption.

Rules:
1. Use sentence case.
2. Keep captions concise and mathematical.
3. End captions with a period.
4. Describe the mathematical purpose of the figure.
5. Avoid vague captions such as "Graph" or "Diagram."

Good caption models:
- Geometric interpretation of the horizontal line test.
- One-to-one function and its inverse.
- The sine function on `\mathbb{R}` is not one-to-one.

## Figure Labels and References

1. Every important figure should have a label.
2. Use descriptive labels following the `type:description` format specified in the Cross-Reference Policy:
   - `fig:horizontal-line-test`
   - `fig:inverse-composition`
   - `fig:restricted-sine`
3. Refer to figures with `\cref{fig:...}` (or `\Cref{fig:...}` at the start of a sentence). Do not use `Figure~\ref{fig:...}` manually; `cleveref` inserts the "Figure" prefix for you.
4. Avoid vague phrases such as "the figure below."

Rationale: see Cross-Reference Policy. Figures are cross-referenced more than any other environment, so the uniform-prefix rule matters most here.

## Figure Placement Policy

In a teaching-oriented document, figures must appear immediately next to the text that discusses them. Allowing figures to float away forces students to flip pages, which disrupts the reading flow.

Current house policy in this repository is:
- all figures -> `[H]` (requires the `float` package)

Rationale:
- Every figure in this textbook is tied to a specific definition, example, or remark. Proximity is always pedagogically important.
- The `\raggedbottom` setting (in `preamble/layout.tex`) prevents excessive vertical stretching that `[H]` placement can sometimes cause with the `book` class.

Important rules:
1. Default to `[H]` so that figures stay exactly where the source places them.
2. If a page break leaves too much white space before an `[H]` figure, first try to adjust the surrounding text (rewording, trimming, or reordering a nearby paragraph). If prose adjustment does not resolve the problem and the figure is the primary concern of the page, either a manual `\newpage` or a fallback to `[htbp]` is permitted as a **documented exception** (see Exception Protocol).
3. Keep figures reasonably sized so that they fit on the same page as the text that introduces them.

Rationale: `[H]` is pedagogically preferred because it pins the figure where the prose references it, but LaTeX cannot always honor `[H]` without producing ugly white space. Treating placement fallback as a documented exception, rather than a silent choice, keeps the default behavior enforceable while admitting that no policy fits every page.

## Size and Layout Policy for Figures

1. Figures should be large enough to read comfortably.
2. Do not make figures unnecessarily wide or tall.
3. Side-by-side figures are appropriate only when comparison is pedagogically important.
4. If labels become cramped, stack figures vertically instead.
5. Multi-part figures should be used only when the comparison itself is part of the lesson.

## Professor Manuscript Priority for Figures

1. If the manuscript already contains a figure idea, preserve its mathematical purpose.
2. Redraw figures in a clean textbook style.
3. Do not preserve handwritten visual style.
4. Do not invent unnecessary figures to fill space.

## Index Policy

The book has a back-of-book index.

Mandatory `\index{...}` entries:
- every term introduced by a `definition` environment (the primary term and any synonyms used elsewhere)
- every named theorem ("Squeeze theorem", "Intermediate value theorem", "Mean value theorem", "Fundamental theorem of calculus", etc.)
- every notation the book defines (for example `\arcsin`, `\lim`, `\int`)

Optional `\index{...}` entries:
- important examples ("greatest integer function", "\(1/x\) near 0")
- proper names of mathematicians when first mentioned in a historical note

Rules:
1. Place the `\index{...}` command at the first occurrence of the term, not at every later mention.
2. Use sentence-case keys: `\index{one-to-one function}`, not `\index{One-to-One Function}`.
3. Use subentries via `!` for grouped concepts: `\index{limit!one-sided}`, `\index{limit!infinite}`.
4. Do not index a term that appears only inside the index entry of another term.
5. For notation, use `\index{sort-key@$\text{symbol}$}` so the index sorts under the spelled-out key but displays the glyph. Examples:
   - `\index{limit@$\lim$}`
   - `\index{arcsine@$\arcsin$}`
   - `\index{integral@$\int$}`
   The portion before `@` is the sort key; the portion after is what appears in the printed index.

Rationale: a searchable index is one of the few durable affordances a printed textbook offers. A chapter without index entries forces the index to be reconstructed from scratch at the end of the project, and the reconstruction is never as good as entries placed while the material is fresh.

### Build chain

The index must be compiled as part of the document build, not left as dead `\index{...}` calls in the source.

1. `preamble/packages.tex` loads `imakeidx` (after `hyperref` and `cleveref`, to integrate page-link behavior correctly).
2. `main.tex` declares the index in the preamble with `\makeindex[columns=2,title=Index,intoc]`; this opens the `.idx` stream, reserves two-column layout, labels the printed index `Index`, and adds the index to the table of contents.
3. `main.tex` emits the index in the back matter with `\printindex`, placed after any bibliography and before `\end{document}`.
4. Compilation requires three passes with an `makeindex` invocation between the first and second pass:
   - `pdflatex main`
   - `makeindex main`
   - `pdflatex main`
   - `pdflatex main` (final pass resolves page numbers in cross-references)
5. `latexmk -pdf main` is acceptable as a shortcut; it runs the passes above automatically.

Rationale: a rule requiring index entries is only as strong as the build that consumes them. Fixing the build chain at the preamble level, once, guarantees that every `\index{...}` added in a chapter file becomes a real index line without the author having to think about the pipeline.

## LaTeX Source Policy

All generated LaTeX should be explicit, conservative, and easy to read.

Rules:
1. Use standard LaTeX environments explicitly.
2. Do not invent custom macros in chapter files.
3. Do not use shorthand theorem wrappers.
4. Do not redefine standard commands in chapter files.
5. Do not use single-letter macros in generated chapter content.
6. Do not hide structure behind custom wrappers.
7. Do not insert manual `\newpage`, `\pagebreak`, or `\clearpage` in chapter files just to keep theorem-like blocks, remarks, examples, solutions, or proofs together.
8. The template already handles that pagination in `preamble/theorem_setup.tex`, with stronger protection for formal result blocks and lighter flow for examples, solutions, and proofs; if a split still looks bad, fix the template or the local content structure deliberately instead of adding ad hoc page breaks.
9. Narrow exception: a manual `\newpage` is permitted to resolve a specific figure-placement or block-split issue that the template cannot handle, but only when documented under the Exception Protocol.

Preferred style:

```latex
\begin{definition}
...
\end{definition}

\begin{theorem}
...
\end{theorem}

\begin{proof}
...
\end{proof}

\begin{example}
...
\end{example}

\begin{solution}
...
\end{solution}
```

## Exception Protocol

Individual chapters may occasionally need to deviate from a rule in this document. When that happens, the deviation must be recorded, not hidden.

1. Document the exception in a comment at the top of the chapter file, immediately after the `\chapter{...}` command:

   ```latex
   % Exception: uses [htbp] placement for Figure 1.9 to avoid a full blank page.
   % Rule: Figure Placement Policy rule 1 (default [H]).
   % Reason: the four-panel figure is taller than the typical [H] budget,
   %         and forcing it produces a near-blank page.
   ```

2. If an exception recurs across chapters, raise it for rule revision rather than compounding local exceptions.
3. Do not silently deviate. A chapter without an exception comment is presumed to follow all rules in this document.
4. When a rule is revised because of repeated exceptions, bump the document version at the top of this file and note the change briefly in a `## Changelog` section (add one if not yet present).

Rationale: rules evolve. An explicit exception record turns deviations from noise into data, so the rule book can adapt based on where the rules actually fail in practice. It also protects the consistency claim: rule adherence is verifiable only if exceptions are declared.

## Operational Workflow for Future Requests

When asked to draft a chapter or section:
1. identify the mathematical content in the manuscript
2. reorganize if needed
3. standardize notation and terminology
4. classify environments by mathematical role
5. preserve manuscript examples and add only targeted supplementary examples when they materially help
6. decide selectively whether proofs are needed
7. include inline exercises only if present in the manuscript; add an end-of-section problem set per Exercise Policy, marking any supplementary problems explicitly
8. add figures only when they materially improve understanding
9. default to `[H]` for figure placement; when `[H]` produces an unsatisfactory page, fall back to `[htbp]` (or a manual `\newpage`) and record the deviation under the Exception Protocol
10. write clean textbook prose
11. output explicit LaTeX content only

## Consistency Check Before Final Output

Before accepting chapter content, verify that:

Structure and voice:
- the prose is textbook-style
- the chapter opens with a one-to-two-paragraph overview (Chapter Opening Norm)
- section titles use Title Case; subsection titles use sentence case
- the hierarchy stays within chapter / section / subsection; any fourth-level heading uses `\paragraph`
- first-person plural "we" is used for instructional prose
- the writing matches the Voice Reference sample

Notation and terminology:
- notation is consistent with the Notation Policy
- terminology is consistent (one term per concept)
- `\emph{...}` is used for newly introduced terms, not `\textbf` or `\textit`

Environments:
- definitions are used only for new concepts
- remarks are used for explanation, warning, intuition, or short historical/application context
- no remark contains main-line knowledge a student must read
- theorems are reserved for major results
- propositions are used for formal but secondary results
- examples use `solution`, not `proof`
- `solution` is visually distinct from `proof`
- manuscript examples are preserved unless the user asked for editorial replacement
- any added examples have a clear pedagogical purpose
- proofs are used only for genuine proofs, and only when warranted

Numbering and references:
- formal-statement numbering is shared across definition/theorem/proposition/lemma/corollary
- concepts defined twice at different precision levels cross-reference each other
- display equations are numbered only if referenced or stated as a formal result
- cross-references use `\cref` (or `\Cref` at sentence start), never `Figure~\ref`
- label keys follow the `type:short-description` format

Exercises:
- inline exercises appear only if present in the manuscript
- end-of-section supplementary problems are marked explicitly

Figures:
- figures are included only when genuinely helpful
- figure captions are concise, in sentence case, and end with a period
- figure placement uses `[H]` by default; exceptions are documented

Typography and index:
- dashes, ellipses, math spacing, and delimiters follow the Typography Policy
- quotation marks use TeX-style (`` `` '' ``) not ASCII (`"`)
- index entries are placed at the first occurrence of every defined term and every named theorem

Source hygiene:
- no custom macros were introduced into chapter files
- any deviation from the rules is documented under the Exception Protocol

## One-Sentence House Rule

Write each chapter as clean, explicit, textbook-style LaTeX content based primarily on the professor manuscript and secondarily on Stewart, using consistent notation and terminology, careful environment classification, shared counters for formal statements, `solution` reserved for worked examples and visually distinct from `proof`, `proof` reserved for genuine proofs when needed, inline exercises drawn only from the manuscript, end-of-section exercises marked clearly when supplementary, figures added only when they genuinely help student understanding and referenced via `\cref`, index entries placed at first occurrence, and every deviation from the rules documented explicitly.

## Changelog

- **v2.0.4** — closed two rule-vs-manuscript gaps exposed by the Chapter 1 review. Added a Build chain subsection under Index Policy describing the `imakeidx` wiring (`\usepackage{imakeidx}`, `\makeindex[columns=2,title=Index,intoc]`, `\printindex`) and the three-pass compile chain, so the index rule is backed by real build infrastructure. Added an explicit TODO-placeholder convention and rationale to End-of-section exercises, and introduced a Known Open Items subsection under Consistency Check to track rules that are authoritative for style but not yet fully realized in every chapter. No existing rules weakened.
- **v2.0.3** — codified four rules that emerged from the Chapter 1 structural review: section titles must not duplicate the parent chapter title (Document Structure); subsection titles should name the unifying theme rather than enumerate ingredients (Heading capitalization); figures in worked examples must not pre-label the quantity the derivation is about to produce (Figure Policy); and `\begin{definition}` must not be used for terms the chapter will neither use nor develop (Environment Classification Rules → Definition).
- **v2.0.2** — rewrote the Numbering Policy implementation note to describe the `aliascnt` pattern actually used in `preamble/theorem_setup.tex`; fixed the Index Policy notation example to include an explicit sort key.
- **v2.0.1** — reconciled stale Operational Workflow items (exercise rule and figure-placement rule) with the revised Exercise Policy and Figure Placement Policy. No rule changes.
- **v2.0** — introduced rationale framework, shared counters for formal statements, `\paragraph`-level fourth tier, Chapter Opening and Closing Norms, two-tier Exercise Policy, Equation Numbering Policy, Cross-Reference Policy, Voice and Person subsection with Voice Reference, Typography Policy, Index Policy, Exception Protocol, Heading Capitalization rule, Paired Definitions rule, and extended Consistency Check. Resolved conflict between Figure Placement and LaTeX Source rules.
- **v1.0** — initial version.
