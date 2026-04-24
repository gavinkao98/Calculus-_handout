# Author Quickstart

This is the short daily-reference companion to [`CONTENT_SPEC.md`](CONTENT_SPEC.md). Use it while you are writing; go to the spec only when the quickstart does not answer your question or when you are about to deviate from a rule.

If you are new to the project, also skim [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) once to understand where your chapter sits in the arc.

---

## Register in one line

Stewart / Rogawski tone: accessible to a motivated high-schooler self-studying, full sentences with explicit connectives, intuition before formalism, warm without being chatty. Not Spivak, not lecture shorthand.

- default pronoun: **we**. Reserve **you** for gentle reminders or forward-reference (*"you will see this again in §4.2"*).
- every formal environment **SHOULD** have one *"Informally, ..."* sentence of intuition either inside or in the paragraph immediately before it.

---

## Environment cheat sheet

Pick the environment that matches the semantic role. Do not nest formal environments.

| Env | Use for |
|---|---|
| `definition` | introduces a term the chapter will use. Include `\index{...}` at first occurrence. |
| `theorem` | headline result of the section. `\begin{theorem}[Name]` + matching `\index{Name}`. |
| `proposition` | useful, reusable, but not the section's headline. |
| `corollary` | pedagogically worth calling out immediate consequence. |
| `example` + `solution` | always paired, always wrapped in `workedexample`. No solo `example`. |
| `workedexample` | semantic wrapper around exactly one `example`+`solution`. Not a page-break trick. |
| `proof` | genuine proof. Not for worked calculations. Optional (see spec §5). |
| `remark` | aside, notation note, short historical note, forward reference. **Not** main-line knowledge. |
| `caution` | notation trap or easy-to-miss restriction, 1-3 sentences. Left red accent. |
| `strategy` | method box with numbered steps ("given a problem of type X, do..."). |
| `exercise` | lives in `\subsection*{Exercises}`. See [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md). |

Soft density targets per section: **2-3 remarks**, **≥1 strategy** when worked examples share a method.

---

## Chapter opening (MUST)

```latex
\chapter{Title In Title Case}

Overview paragraph (1-2 paragraphs). Establish the chapter's
motivation and how it connects to the previous chapter.

\paragraph{By the end of this chapter, you will be able to:}
\begin{itemize}
  \item skill 1 (verb-first: "compute", "verify", "recognize");
  \item skill 2;
  \item skill 3-5.
\end{itemize}

\section{First Section Title}
...
```

Chapter end **MUST** have `\section*{Summary}` with definitions / theorems / formulas blocks. See spec §4.

---

## Section opening

1-2 paragraphs of motivation. A purely computational section may open with a single connecting sentence. Do not open a section with a definition or display math.

---

## Formula display: 5 modes

| Mode | When |
|---|---|
| inline `\(...\)` | short formula that belongs to the sentence. |
| display `\[...\]` | visually central formula or multi-step calculation. |
| `aligneddisplay` | short top-to-bottom peers or derivation steps. |
| `conditiondisplay` | formula with trailing domain / range / branch condition needing its own spacing. |
| `\pairdisplay{A}{B}` | exactly two short formulas compared left-to-right. Auto-stacks if too wide. |

Rules of thumb:
- one mode per local math unit. Do not mix centered, aligned, and prose-condition in the same step.
- `\qedhere` on the last display line of a `solution` that ends in display math.
- `\solutionbreak` at the start of a `solution` body that begins with a block (list or display math).
- **No** `\iff`-helper macros. For formal "A iff B", use display math with `\Longleftrightarrow`.

---

## Figure rule

- palette is three roles only: blue = primary, red = caution/counterexample, gray = auxiliary. See `preamble/colors.tex`.
- do not encode meaning in colour alone — also use line style, labels, or markers (figures must survive grayscale print).
- default placement `[H]`. Declare an exception in a comment if you use `[htbp]`.
- captions: sentence case, end with a period, describe mathematical purpose.
- **worked-example figures** must not reveal the quantity the example asks the reader to compute.
- figure density target: one figure at each important definition / theorem, and roughly every 2-3 examples in computational sections.

---

## Index rule

`\index{...}` at **first occurrence** of:
- every defined term;
- every named theorem;
- every notation (e.g. `\arcsin`, `\lim_{x \to a}`);
- every key example the reader will want to flip back to;
- every applied setting (physics, economics) introduced in the chapter;
- every notation trap (also flagged by `caution`).

Rule of thumb: **if a reader will flip back to find it, it goes in the index**. Purely local symbols or one-off throwaway setups do not.

---

## Cross-references and labels

- always `\cref{...}` / `\Cref{...}`. Never manual prefix like `Theorem~\ref{...}`.
- `\eqref{...}` for equation references.
- label format: `type:short-desc`, hyphens only. Examples: `def:one-to-one`, `thm:ivt`, `eq:limit-law-sum`, `fig:inverse-reflection`.
- equation numbers only on equations that will be referenced later or are formal statements.

---

## Prose typography

- emphasis: `\emph{...}` only, and only for first mention of a new term or a rare load-bearing phrase. **No** `\textbf{...}` or `\textit{...}` in prose (style lint enforces this).
- quotes: TeX style `` ``...'' ``. **No** ASCII `"..."` (style lint enforces).
- dashes: `--` for numeric range (*pp. 12--18*), `---` for aside dashes. No unicode em-dash in source.
- ellipses: `\ldots` in math, `\dots` in prose.

---

## What chapter files **MUST NOT** contain

- `\newcommand`, `\renewcommand`, `\def`, `\newenvironment`, `\providecommand` (new helpers go in `preamble/`).
- `\newpage`, `\pagebreak`, `\clearpage` (pagination is handled globally).
- Manual cross-reference prefixes (*Figure~\ref{...}*).
- ASCII straight quotes.
- `\textbf` / `\textit` in prose.
- `\footnote`, `\marginpar`, or manual `\hypertarget` **inside** a `workedexample` body.

---

## Before committing

Run locally:

```powershell
python tools/style_lint.py
python tools/run_preamble_smoketest.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

All three **MUST** pass. They also run on every push and PR via [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml).

For the full consistency checklist (positioning, register, structure, environments, typography, ...), see the checklist at the end of [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §15.

---

## When to leave the quickstart

Go to the spec for:
- **§3** — full register guidance, style do/don't, voice-reference sample.
- **§5** — full environment policy, per-environment typical uses and rationale.
- **§6** — manual numbering edge cases, paired definitions at different precision levels.
- **§7** — full display decision tree, cohesion rules, delimiter sizing.
- **§9** — notation table.
- **§13** — exception protocol (how to document a rule deviation).

If a rule in the spec seems wrong after you have tried to write within it, do not silently deviate. File an exception comment (§13) and propose the rule change.
