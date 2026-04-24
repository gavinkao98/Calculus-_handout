# Calculus Handout Project

A single-sided A4 **calculus handout** for high-school students self-studying toward college calculus, paired with companion teaching videos. The handout is self-sufficient; the video is reinforcement.

This file is the **repository hub**. It is authoritative for repo layout, preamble structure, and build instructions. Content-authoring rules and media-pipeline rules live in their own files, linked below.

---

## Start here

Pick the task you have, open the linked file.

- **Writing or revising a chapter.** Start with [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md). Fall back to [`CONTENT_SPEC.md`](CONTENT_SPEC.md) when the quickstart does not answer your question. Check [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) before starting a new chapter.
- **Producing a video** (primary path — Manim animations). Start with [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md) for step-by-step, then [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md) for how to translate a finalised section into a YAML storyboard, and [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md) for templates, field contracts, and render commands.
- **Static-slide MP4** (frozen legacy path). Use [`LEGACY_SLIDE_PIPELINE.md`](LEGACY_SLIDE_PIPELINE.md). No new development on this path — use Manim for new work.
- **Designing end-of-section exercises.** [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) (minimum skeleton until the full design round opens).

---

## Golden path

```
  chapters/*.tex  ──▶  inputs/manim_storyboards/<deck_id>.yml
  (CONTENT_SPEC)      (MANIM_STORYBOARD + MANIM_REFERENCE)
                                   │
                                   ▼
                         preview → audio → render
                         (MANIM_CHECKLIST)
                                   │
                                   ▼
                       artifacts/video/<deck_id>_manim.mp4
```

Finalize the chapter content first. Hand-write the storyboard from the finalized LaTeX. Preview scenes one at a time. Render audio and final MP4 once scenes feel right.

---

## Document map

| Layer | File | Purpose |
|---|---|---|
| hub | `README.md` | repo layout, preamble map, build rules |
| content spec | [`CONTENT_SPEC.md`](CONTENT_SPEC.md) | authoritative textbook writing rules |
| content daily | [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md) | 1-2 page author cheat sheet |
| content arc | [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) | chapter order, prereqs, per-chapter core skills |
| content exercises | [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md) | minimum exercise skeleton |
| manim operational | [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md) | phase-by-phase pipeline checklist |
| manim reference | [`MANIM_REFERENCE.md`](MANIM_REFERENCE.md) | field contracts, templates, render commands |
| manim methodology | [`MANIM_STORYBOARD.md`](MANIM_STORYBOARD.md) | LaTeX-to-YAML translation playbook |
| frozen legacy | [`LEGACY_SLIDE_PIPELINE.md`](LEGACY_SLIDE_PIPELINE.md) | static-slide/PDF + TTS + MP4 (no new development) |

---

## Repository Layout

- `main.tex` — LaTeX entry point for the book.
- `chapters/` — chapter source files.
  - `chapters/_chapter_template.tex` — starter skeleton for a new chapter.
  - `chapters/_scratch.tex` — optional local scratch chapter, gated by `\ifincludescratchchapter`.
- `preamble/` — shared LaTeX setup (see *Preamble Map* below).
- `preamble_smoketest.tex` — minimal regression document for preamble-only layout checks.
- `refs/` — bibliography data.
- `tools/` — media-generation scripts plus book-source utilities (`style_lint.py`, `run_preamble_smoketest.py`, and vendored helpers).
- `schemas/` — JSON schema files for generated deck data.
- `inputs/` — reusable raw inputs: voice recordings, section media plans, Manim storyboards.
- `artifacts/` — mostly generated slides, narration, audio, video. Tracked exceptions: `artifacts/scripts/*_final.md`, `artifacts/slides/*.tex`, and `artifacts/manim/*/narration.md`.
- `.github/workflows/` — CI checks.

---

## Preamble Map

`preamble/` is split by responsibility so layout and template behavior can be found quickly:

- `preamble/packages.tex` — package loading: Times text/math fonts (`newtxtext` + `newtxmath`), `microtype`, `amsmath` / `amsthm` / `mathtools`, `graphicx` / `tikz` / `pgfplots`, `float` / `flafter`, `needspace`, `enumitem`, page geometry (3.3 cm margins), headers, `hyperref` / `cleveref`, `mdframed` with `framemethod=TikZ` for `caution` / `strategy`, `xcolor`, and the house inverse-trig operators (`\arccsc`, `\arcsec`, `\arccot`).
- `preamble/colors.tex` — the three-role semantic palette (`colorprimary` blue, `colorcaution` red, `colorauxiliary` gray) driving figures and accent bars on `caution` / `strategy`.
- `preamble/layout.tex` — paragraph indentation and spacing, list spacing, global `\linespread{1.05}`, float placement, running headers and footers, `\Needspace` hooks, shared short-formula helpers (`aligneddisplay`, `conditiondisplay`, `\pairdisplay`), and `\newdisplayenv{name}{begin}{end}` for any new wrapper around `\[...\]` (installs the kernel `\@doendpe` hook via `\AfterEndEnvironment` to suppress stray indents after the environment).
- `preamble/theorem_setup.tex` — per-env chapter-scoped counters for `definition` / `theorem` / `proposition` / `corollary`; the `solution` environment; `caution` and `strategy` (left-colour-bar `\newmdtheoremenv`); page-flow protection hooks; and the `workedexample` semantic wrapper that reserves space for an `example` + `solution` pair as a single unit.
- `preamble/numbering.tex` — equation numbering by chapter.
- `preamble/bibliography.tex` — bibliography backend and source file.

---

## Output Format

Single-sided A4 PDF, meant to be printed one page per sheet and distributed as a handout rather than bound.

- `\documentclass[a4paper,12pt,oneside]{book}` — same margin rule on every page.
- `margin=3.3cm` symmetric; text block near the 66–72 characters-per-line comfort range for 12 pt Times.
- `\linespread{1.05}` — modest extra leading for math-dense prose without sparse pages.
- `\fancyhead[L]` / `\fancyhead[R]` / `\fancyfoot[R]` (not the twoside `[LE]`/`[RO]` pattern).
- `main.tex` wraps `\maketitle` in `\begingroup\hypersetup{pageanchor=false}...\endgroup` to avoid duplicate-destination warnings on the title page.
- `main.tex` keeps `\ifprintbibliography` and `\ifincludescratchchapter` toggles near the top so the bibliography and the scratch chapter stay opt-in.

If the project ever needs a bound-book edition later, minimum changes: switch to `\documentclass[a4paper,12pt,twoside,openright]{book}`, rework `\fancyhead`/`\fancyfoot` to use `[LE]`/`[RO]` pairs, and consider asymmetric `inner`/`outer` margins with a `bindingoffset`.

---

## Build and CI

Local build:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex
```

Before committing a chapter, also run:

```powershell
python tools/style_lint.py
python tools/run_preamble_smoketest.py
```

All three checks run on every push and PR via [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml).

Authority: when repository layout or preamble decisions change, **this file** is authoritative; when writing or typesetting rules change, [`CONTENT_SPEC.md`](CONTENT_SPEC.md) is authoritative.

---

## Media scope note

End-of-section `\subsection*{Exercises}` blocks are for the printed handout only. They are **not** included in slide decks, narration scripts, Manim storyboards, synthesized audio, or rendered video. When planning section media, ignore the exercise block of the source section and build from definitions, theorems, examples, and exposition prose.

---

## Notes

- Local caches, virtual environments, and vendored dependencies live in hidden repo folders such as `.cache/`, `.venv/`, `.deps/`, and `.deps_f5/`.
- The checked-in media exemplar is Section 1.1 *Inverse Functions* (`ch01_inverse_functions`). The Manim storyboard lives at [`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml); the frozen slide plan lives at [`inputs/media_plans/ch01_inverse_functions.json`](inputs/media_plans/ch01_inverse_functions.json).
