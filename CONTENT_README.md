# Calculus Textbook Project: Master Writing Guide

This file is the authoritative writing context for future chapter drafting and revision in this project.
It consolidates:
- the original AI writing brief
- the updated environment-classification rules
- the figure and placement rules tested in Chapter 1
- the editorial decisions already used in the current manuscript

The goal is that later chapters can follow this file directly.

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

Use only this hierarchy unless there is a strong reason not to:
- `chapter`
- `section`
- `subsection`

Avoid deeper hierarchy by default.

Within a section, prefer the following pedagogical order:
1. short introduction or motivation
2. definitions
3. properties, propositions, and theorems
4. proofs when needed
5. examples with solutions
6. exercises only if they are present in the professor manuscript

If the manuscript is disorganized, reorganize it into this structure.

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

### Remark

Use a `remark` for:
- supplementary explanation
- teaching notes
- intuition
- domain restrictions
- notation warnings
- common mistakes
- short historical notes
- short application notes
- comparisons with earlier ideas

A remark is not the main formal result of the section.
A remark usually does not need a proof.

Good uses of `remark` include:
- explaining why a condition is necessary
- explaining principal-value restrictions for inverse trigonometric functions
- warning that `\sin^{-1} x` does not mean `1/\sin x`
- clarifying that the existence of a limit does not imply `f(a)` equals the limit
- presenting the horizontal line test as a geometric teaching criterion when it is not a central theorem of the section
- giving a short historical or real-world motivation in 2 to 5 sentences

Important rule:
Do not hide a genuinely important reusable formal result inside a remark.

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

In short:
- theorem-like statements -> `proof` when warranted
- worked examples -> `solution`

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

1. Include exercises only if they are present in the professor manuscript.
2. Do not invent new exercises to make a section look fuller.
3. Keep professor-provided exercises as the exercise set for that section.
4. Do not delete, merge, split, reorder, rewrite, simplify, or expand professor-provided exercises unless the user explicitly asks for editorial adjustment.
5. If the manuscript includes no exercises, then the section should contain no `exercise` environment.
6. Do not convert exercises into examples unless the source clearly provides guided exposition.

## Numbering Policy

This project uses chapter-based numbering with separate counters for major environment types.

Desired style:
- Definition 1.1, Definition 1.2, ...
- Theorem 1.1, Theorem 1.2, ...
- Proposition 1.1, Proposition 1.2, ...
- Example 1.1, Example 1.2, ...
- Exercise 1.1, Exercise 1.2, ...
- Figure 1.1, Figure 1.2, ...

Do not manually number environments or figures.
Let the project template handle numbering.

Current implementation already supports separate chapter-based counters in `preamble/theorem_setup.tex`.

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
2. Use descriptive labels such as:
   - `fig:horizontal-line-test`
   - `fig:inverse-composition`
   - `fig:restricted-sine`
3. Refer to figures with numbered references, for example:
   - `Figure~\ref{fig:inverse-composition}`
4. Avoid vague phrases such as "the figure below."

## Figure Placement Policy

Place figures as close as reasonably possible to the paragraph where they are discussed, but do not force placement aggressively unless readability truly requires it.

Current house policy in this repository is:
- ordinary figures -> `[!tbp]`
- concept-critical figures -> `[!ht]`

Interpretation:
- `[!tbp]` is for ordinary figures that may float naturally
- `[!ht]` is for figures that should stay close to the surrounding explanation, such as a key concept graph immediately after a definition

Important rules:
1. Do not default to `[H]`.
2. Allow normal floating when possible.
3. Use the core placement only when the teaching flow depends on proximity.
4. A figure may move to the next page if needed.
5. Normal page breaks are acceptable.
6. Only tighten placement if separation damages readability.

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

## Operational Workflow for Future Requests

When asked to draft a chapter or section:
1. identify the mathematical content in the manuscript
2. reorganize if needed
3. standardize notation and terminology
4. classify environments by mathematical role
5. preserve manuscript examples and add only targeted supplementary examples when they materially help
6. decide selectively whether proofs are needed
7. include exercises only if present in the manuscript
8. add figures only when they materially improve understanding
9. use `[!tbp]` or `[!ht]` for figures as appropriate
10. write clean textbook prose
11. output explicit LaTeX content only

## Consistency Check Before Final Output

Before accepting chapter content, verify that:
- the prose is textbook-style
- the structure is coherent
- notation is consistent
- terminology is consistent
- definitions are used only for new concepts
- remarks are used for explanation, warning, intuition, or short historical/application context
- theorems are reserved for major results
- propositions are used for formal but secondary results
- examples use `solution`, not `proof`
- manuscript examples are preserved unless the user asked for editorial replacement
- any added examples have a clear pedagogical purpose
- proofs are used only for genuine proofs
- proofs are included only when warranted
- exercises appear only if they are present in the professor manuscript
- professor-provided exercises are preserved without unauthorized changes
- figures are included only when genuinely helpful
- figure captions are concise and in sentence case
- figure placement uses the project policy
- no custom macros were introduced into chapter files
- the writing follows the project voice

## One-Sentence House Rule

Write each chapter as clean, explicit, textbook-style LaTeX content based primarily on the professor manuscript and secondarily on Stewart, with consistent notation and terminology, careful environment classification, `solution` reserved for worked examples, `proof` reserved for genuine proofs when needed, exercises included only when provided in the manuscript, and figures added only when they genuinely help student understanding.
