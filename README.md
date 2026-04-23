# Calculus Textbook Project

This repository has two separate working tracks:

- textbook content authoring
- slide, narration, and video generation

Use the dedicated guides instead of treating this file as the full rulebook.

Operational checklists (shortest path to a finished artifact):

- [`SLIDES_CHECKLIST.md`](SLIDES_CHECKLIST.md): slide/PDF pipeline checklist
- [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md): Manim animation pipeline checklist

Full references:

- [`CONTENT_README.md`](CONTENT_README.md): authoritative textbook writing and editorial rules
- [`SLIDES_README.md`](SLIDES_README.md): slide-generation workflow and plan rules
- [`SCRIPT_README.md`](SCRIPT_README.md): narration draft/final workflow (slide/PDF path)
- [`VIDEO_README.md`](VIDEO_README.md): audio synthesis and MP4 rendering (slide/PDF path)
- [`MANIM_README.md`](MANIM_README.md): storyboard-driven Manim workflow
- [`STORYBOARD_AUTHORING.md`](STORYBOARD_AUTHORING.md): translation guide for turning a finalized chapter section into a Manim storyboard YAML

## Repository Layout

- `main.tex`: main LaTeX entry point for the book
- `chapters/`: chapter source files
- `chapters/_chapter_template.tex`: starter skeleton for drafting a new chapter in the house style
- `chapters/_scratch.tex`: optional local scratch chapter, gated by `\ifincludescratchchapter` in `main.tex`
- `preamble/`: shared LaTeX setup
- `preamble_smoketest.tex`: minimal regression document for preamble-only layout checks
- `refs/`: bibliography data
- `.github/workflows/`: CI checks for the book source
- `tools/`: media-generation scripts plus book-source support utilities such as `style_lint.py`, `run_preamble_smoketest.py`, and vendored helpers like `loguru.py`
- `schemas/`: JSON schema files for generated deck data
- `inputs/`: reusable raw inputs such as source voice recordings, section media plans, and Manim storyboards
- `artifacts/`: mostly generated slides, narration, audio, and video outputs; the tracked exceptions are `artifacts/scripts/*_final.md`, `artifacts/slides/*.tex`, and `artifacts/manim/*/narration.md`

Authoring note:
- `workedexample` is the canonical semantic wrapper for exactly one `example` + `solution` pair; it is not just a page-break trick or visual macro
- keep `\footnote`, `\marginpar`, and manual `\hypertarget` outside `workedexample`

Voice-reference note:
- keep new voice reference inputs under `inputs/voice/` as `.wav` files
- `inputs/voice/reference_script_en.txt` is a starter script for recording a new F5 reference clip
- if you pass `--reference-text` to F5 clone mode, it must be the verbatim transcript of that exact reference WAV
- do not reuse `reference_script_en.txt` as the transcript for unrelated sample clips unless the clip was recorded from that script

Media-plan note:
- keep section slide plans under `inputs/media_plans/`
- each plan selects one source section and defines the slide sequence, learning goals, and source selectors used for extracted formulas or figures

Manim-storyboard note:
- keep storyboard files under `inputs/manim_storyboards/`
- **recommended workflow**: write the storyboard by hand directly from the finalized LaTeX source in `chapters/*.tex`, following the translation rules in [`STORYBOARD_AUTHORING.md`](STORYBOARD_AUTHORING.md)
- **legacy bootstrap**: `tools/seed_manim_storyboard.py` produces a first-draft YAML from an existing deck JSON (from the slide/PDF pipeline). Seeding is retained for one-off bootstrapping; it is not the designed path and a seeded draft still needs substantial manual revision to reach the quality bar described in `STORYBOARD_AUTHORING.md`
- the storyboard owns Manim `voiceover` text and can optionally bridge back into the existing TTS scripts
- `render_manim_lesson.py --with-audio` writes bridge files to `artifacts/manim/<deck_id>/narration.md` and `artifacts/manim/<deck_id>/tts_deck.json`
- you can edit `narration.md` for proofreading, then run `sync_narration_back.py` to push changes back to the YAML
- for the Manim path, the storyboard is the source of truth; `narration.md` is a readable editing surface that syncs back

## Preamble Map

The `preamble/` directory is split by responsibility so layout and template behavior can be found quickly:

- `preamble/packages.tex`: shared package loading for Times-style text and math fonts (`newtxtext` + `newtxmath`), micro-typography (`microtype`), math (`amsmath`, `amsthm`, `mathtools`), figures (`graphicx`, `tikz`, `pgfplots`), float handling (`float`, `flafter`), page-break control (`needspace`), lists (`enumitem`), page geometry (`margin=3.3cm`, see *Output Format* below), headers, cross-references (`hyperref`, `cleveref`), and house inverse-trig operators (`\arccsc`, `\arcsec`, `\arccot` via `\DeclareMathOperator`, added when `physics` was removed)
- `preamble/layout.tex`: paragraph indentation and spacing, list spacing, global line spread (`\linespread{1.05}` to give display math breathing room at 12pt Times), float placement parameters, running headers and footers, chapter-title spacing, `\Needspace` hooks on `\section` and `\subsection`, shared short-formula display helpers such as `aligneddisplay`, `conditiondisplay`, `\pairdisplay`, `\iffwithconditions`, and `\iffstackeddisplay`, and the `\newdisplayenv{name}{begin}{end}` helper used to declare any new environment that wraps `\[...\]` so `\parindent` is correctly suppressed on the following paragraph (the helper installs LaTeX's kernel `\@doendpe` hook in the outer scope via `\AfterEndEnvironment`)
- `preamble/theorem_setup.tex`: theorem-like environment definitions, chapter-based counters for those environments, the `solution` environment, stronger page-bottom protection for formal result blocks, lighter page-flow protection for examples, exercises, remarks, and proofs, and the `workedexample` semantic wrapper that measures and reserves space for an `example`+`solution` pair as one unit
- `preamble/numbering.tex`: equation numbering by chapter
- `preamble/bibliography.tex`: bibliography backend and bibliography source file

## Output Format

The book is produced as a **single-sided A4 PDF**, meant to be printed one page per sheet and distributed as a handout rather than bound into a book. The preamble and `main.tex` reflect that:

- `\documentclass[a4paper,12pt,oneside]{book}`: `oneside` makes every page follow the same margin rule, so there is no inner/outer asymmetry
- `margin=3.3cm` symmetric on all four sides, giving a text block near the 66-72 characters-per-line comfort range for 12pt Times
- `\linespread{1.05}` provides modest extra leading for math-dense prose without making pages feel sparse
- `\fancyhead[L]`/`\fancyhead[R]`/`\fancyfoot[R]` (not the `[LE]`/`[RO]` twoside pattern) place the chapter mark, section mark, and page number consistently on every page
- `main.tex` wraps `\maketitle` in `\begingroup\hypersetup{pageanchor=false}...\endgroup` to avoid duplicate-destination warnings on the title page; no manual `\clearpage` is needed because `titlepage` handles the page break internally
- `main.tex` keeps `\ifprintbibliography` and `\ifincludescratchchapter` toggles near the top so bibliography output and local scratch content can stay opt-in instead of accidentally shipping

If the project ever needs a bound-book edition later, the minimum changes are: switch to `\documentclass[a4paper,12pt,twoside,openright]{book}`, rework `\fancyhead`/`\fancyfoot` to use `[LE]`/`[RO]` pairs, and consider asymmetric `inner`/`outer` margins with a `bindingoffset`.

## Recent Book-Source Infrastructure

Recent repository-level changes worth knowing before editing the book:

- text and math fonts now use `newtxtext` + `newtxmath` instead of `lmodern`, and `microtype` is enabled for spacing/protrusion improvements
- the old `physics` package was removed; the house inverse-trig operators are declared explicitly in `preamble/packages.tex`
- `hyperref` now carries PDF metadata (`pdftitle`, `pdfauthor`, numbered/open bookmarks) and the title page avoids duplicate page-anchor warnings
- `preamble/layout.tex` now owns the single-sided handout defaults: symmetric 3.3 cm margins, `\linespread{1.05}`, and oneside-style running heads/feet
- `\newdisplayenv` uses LaTeX's kernel `\@doendpe` hook so prose after custom display wrappers does not pick up a stray paragraph indent
- Chapter 1 figure code was adjusted to compile warning-free, including the inverse-composition diagram sizing and the sine-graph marker overlay
- book-source checks now include a regex style lint, a dedicated preamble smoke test, and a GitHub Actions workflow that runs both plus a full `latexmk` build

Template pagination note:
- formal result blocks such as `theorem`, `lemma`, `proposition`, `corollary`, and `definition` reserve more vertical space before they start
- `example`, `exercise`, `solution`, and `proof` use lighter protection and may span pages naturally
- `\section` and `\subsection` headings reserve a few baselines of the following body text, so a heading cannot be stranded alone at the bottom of a page
- `workedexample` measures the combined `example`+`solution` height once (capped at 16 baselines) and reserves that much space, so short pairs stay together without forcing a break for near-page-height units
- do not add manual `\newpage`, `\pagebreak`, or `\clearpage` in chapter files just to keep these blocks together unless a task explicitly calls for a local exception

## Formula Display Strategy

Use this as the quick authoring rule for how formulas should appear on the page:

- keep short formulas inline when they belong naturally to the sentence
- in `solution`, keep `Solution.` inline when the body begins with prose
- if a `solution` begins with `enumerate`, `itemize`, or display math, place `\solutionbreak` before the first block
- if the last line of a `solution` is displayed math, place `\qedhere` on that last displayed line so the closing box does not drift to a separate line
- within one local math unit, prefer one display grammar instead of mixing centered displays, aligned blocks, and prose-side conditions for the same step
- keep one-off conditions such as `provided that ...` in prose when they apply to only one formula
- use ordinary display math for visually central formulas or multi-step calculations
- use `aligneddisplay` for short related formulas that should be read top-to-bottom
- use `conditiondisplay` when formulas carry trailing domain/range/branch conditions that need explicit spacing
- use `\pairdisplay{...}{...}` only when exactly two short formulas are meant to be compared left-to-right; it auto-stacks if either side gets too wide
- do not use `aligneddisplay` just to line up unrelated factual statements; if two short facts are being compared, prefer `\pairdisplay{...}{...}` or ordinary display math
- use `\iffwithconditions{...}{...}{...}` when the brace itself means one grouped restriction or condition set
- use `\iffstackeddisplay{...}{...}{...}` when one formal statement is equivalent to two equal-status stacked conditions
- in displayed formal equivalences, prefer `\Longleftrightarrow` over a separate text line saying `if and only if`

For the full decision rules and examples, see the `## Formula Display Policy` section in [`CONTENT_README.md`](CONTENT_README.md).

## Which File To Read

If you are writing or revising textbook content:
- start with [`CONTENT_README.md`](CONTENT_README.md)
- then work in the relevant file under `chapters/`

If you are generating media, first decide which pipeline:

- slide/PDF path -- start with [`SLIDES_CHECKLIST.md`](SLIDES_CHECKLIST.md) for the end-to-end steps; drill into [`SLIDES_README.md`](SLIDES_README.md), [`SCRIPT_README.md`](SCRIPT_README.md), and [`VIDEO_README.md`](VIDEO_README.md) when you need details; scripts live under `tools/`
- Manim animation path -- start with [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md) for the phase-by-phase steps; use [`MANIM_README.md`](MANIM_README.md) for the full reference

## Current Scope

The book source is general, but the checked-in textbook draft is currently centered on Chapter 1:

- `chapters/ch01_foundations.tex` now drafts the full Chapter 1 arc: inverse functions, inverse trigonometric functions, limits, one-sided and infinite limits, limit laws, and the precise definition of a limit
- end-of-section exercises are still placeholders in that chapter; see *Known open items* below
- the media pipeline exemplar is still Section 1.1 ("Inverse Functions"), even though the book chapter itself now extends well beyond that section
- the storyboard [`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml) -- currently v2, hand-authored against `STORYBOARD_AUTHORING.md` v1.2 with 19 scenes including two `section_transition` interludes and three supplementary `graph_focus` visualizations not present in the book prose
- the slide/PDF pipeline plan [`inputs/media_plans/ch01_inverse_functions.json`](inputs/media_plans/ch01_inverse_functions.json) -- still tracked for the slide path; the Manim path no longer depends on this plan
- generated and reviewable media assets under `artifacts/` -- last preview render produced an 8:09 MP4 at 960x540 with Coqui Jenny builtin narration covering all 19 scenes; see *Known open items* below for the follow-up pacing issue

### Known open items

Project-level tracking of rules that are authoritative in [`CONTENT_README.md`](CONTENT_README.md) or [`STORYBOARD_AUTHORING.md`](STORYBOARD_AUTHORING.md) but not yet fully realized in every in-scope chapter:

- **End-of-section exercises.** Chapter 1 currently carries `% TODO: add \subsection*{Exercises} block ...` placeholders at the end of every section (1.1 through 1.6). The Exercise Policy in `CONTENT_README.md` is the target; the TODO markers are the audit trail. Replacing each TODO with a real exercise block is the remaining work.
- **Manim scene pacing vs. narration.** The pipeline synchronizes only scene-total duration (`scene_exit: "hold"` + `minimum_duration_seconds` floor), not within-scene animation beats. In the current Section 1.1 render, `example_walkthrough` scenes with `decay_previous: true` (the default) can dim earlier `math_lines` before the TTS narration reaches its verbal reference to those lines. The rule is now encoded in `STORYBOARD_AUTHORING.md` v1.3 as a SHOULD (set `data.decay_previous: false` whenever the voiceover calls back by name to an earlier step). Remaining work is the audit pass: walk every existing `example_walkthrough` scene in `inputs/manim_storyboards/` and apply the rule where applicable; optionally also slow `theme.transitions.context_decay` globally.

Entries in this list are not exceptions to the rules (per-chapter exceptions are documented under the Exception Protocol in `CONTENT_README.md`). They are known incomplete areas where the rule has been written before the content has been filled in. An item is removed from this list only when the corresponding rule is fully satisfied in every in-scope chapter.

### Media scope: exercises are book-only

End-of-section `\subsection*{Exercises}` blocks are for student self-practice on the printed/PDF book only. They are **not** included in any media pipeline -- not in slide decks, narration scripts, Manim storyboards, synthesized audio, or rendered video. When planning a section media plan or Manim storyboard, ignore the exercise block of the source section and build the storyboard from the definitions, theorems, examples, and exposition prose. The book-level exercise TODOs under *Known open items* are therefore not a blocker for video readiness.

## Media Workflow Snapshot

The current media flow is intentionally staged:

1. finish the lecture-note version in `chapters/*.tex`
2. generate slide artifacts plus a narration draft and narration final file from a section media plan
3. revise only the final narration file until the spoken version is ready
4. synthesize audio from the final narration file
5. render the MP4 from slide PDF plus narration WAV files

The Manim path now exists in parallel:

1. hand-write `inputs/manim_storyboards/<deck_id>.yml` directly from the LaTeX chapter source, following [`STORYBOARD_AUTHORING.md`](STORYBOARD_AUTHORING.md) (or, as a legacy bootstrap, run `tools/seed_manim_storyboard.py` against an existing deck JSON and then hand-revise the seeded YAML into compliance)
2. edit storyboard scenes, `voiceover`, timings, and optional hooks directly
3. preview one scene at a time until the animation feels right
4. run `render_manim_lesson.py --with-audio` once to export the bridge narration files
5. synthesize one WAV per scene into `artifacts/audio/<deck_id>_manim/`
6. rerun `render_manim_lesson.py --with-audio` to mux scene audio into `artifacts/video/<deck_id>_manim.mp4`

Narration ownership rule -- the two pipelines use different source-of-truth models, summarized side-by-side below:

| Aspect | Slide/PDF path | Manim animation path |
|---|---|---|
| Source of truth | `artifacts/scripts/<deck_id>_final.md` | `voiceover` field per scene in `inputs/manim_storyboards/<deck_id>.yml` |
| Regenerated & disposable | `artifacts/scripts/<deck_id>_draft.md` | n/a -- no draft/final split |
| Editable mirror | n/a -- edit the final file in place | `artifacts/manim/<deck_id>/narration.md` |
| TTS reads from | `*_final.md` | bridge files (`tts_deck.json` + `narration.md`) exported from the storyboard |
| Sync mechanism | none needed -- edit in place | `tools/sync_narration_back.py` pushes `narration.md` edits back into the YAML |
| Where to put a joke or aside | the relevant `Narration:` block in `*_final.md` | the scene's `voiceover` in the YAML, or in `narration.md` followed by a sync-back |

Version-control rule:

- commit `artifacts/scripts/*_final.md` when you want narration edits in project history
- commit `artifacts/slides/*.tex` when you want the generated Beamer source in project history
- commit `inputs/manim_storyboards/*.yml` when you want Manim animation and narration edits in project history
- commit `artifacts/manim/*/narration.md` when you want the Manim narration in project history (the storyboard remains canonical)
- do not commit `*_draft.md`, slide PDFs, or LaTeX build artifacts under `artifacts/`

For the actual commands and file paths, use:

- [`MANIM_README.md`](MANIM_README.md)
- [`SLIDES_README.md`](SLIDES_README.md)
- [`SCRIPT_README.md`](SCRIPT_README.md)
- [`VIDEO_README.md`](VIDEO_README.md)

## Quality Checks

For book-source changes, run these checks before committing:

- `python tools/style_lint.py` -- regex linter (forbids manual cross-reference prefixes such as `Figure~\ref{...}`, manual page-break commands like `\newpage`/`\pagebreak`/`\clearpage` in chapter or `main.tex` source, and ASCII `"..."` quotes)
- `python tools/run_preamble_smoketest.py` -- compiles `preamble_smoketest.tex` and checks that continuation prose after `aligneddisplay` / `conditiondisplay` is not spuriously indented (guards the `\newdisplayenv` `\@doendpe` hook)
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -file-line-error main.tex`

The same three checks run on every push and pull request via [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml).

`main.tex` keeps two explicit toggles near the top:

- `\ifprintbibliography` controls whether `\printbibliography` is emitted
- `\ifincludescratchchapter` controls whether `chapters/_scratch.tex` is included (the scratch chapter defaults to off so a local work-in-progress draft does not accidentally ship with the book)

## Notes

- `style_guide.md` is only a short redirect note now.
- Local caches, virtual environments, and vendored dependencies live in hidden repo folders such as `.cache/`, `.venv/`, `.deps/`, and `.deps_f5/`.
