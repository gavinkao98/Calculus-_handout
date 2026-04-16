# Calculus Textbook Project

This repository has two separate working tracks:

- textbook content authoring
- slide, narration, and video generation

Use the dedicated guides instead of treating this file as the full rulebook:

- [`CHECKLIST.md`](CHECKLIST.md): one-page operational checklist for the media workflow
- [`CONTENT_README.md`](CONTENT_README.md): authoritative textbook writing and editorial rules
- [`MANIM_README.md`](MANIM_README.md): storyboard-driven Manim workflow
- [`SLIDES_README.md`](SLIDES_README.md): slide-generation workflow and plan rules
- [`SCRIPT_README.md`](SCRIPT_README.md): narration draft/final workflow
- [`VIDEO_README.md`](VIDEO_README.md): audio synthesis and MP4 rendering

## Repository Layout

- `main.tex`: main LaTeX entry point for the book
- `chapters/`: chapter source files
- `preamble/`: shared LaTeX setup
- `refs/`: bibliography data
- `tools/`: media-generation scripts
- `schemas/`: JSON schema files for generated deck data
- `inputs/`: reusable raw inputs such as source voice recordings, section media plans, and Manim storyboards
- `artifacts/`: mostly generated slides, narration, audio, and video outputs; the tracked exceptions are `artifacts/scripts/*_final.md` and `artifacts/slides/*.tex`

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
- use `tools/seed_manim_storyboard.py` to draft a storyboard from an existing deck JSON, then edit the YAML directly
- the storyboard owns Manim `voiceover` text and can optionally bridge back into the existing TTS scripts
- `render_manim_lesson.py --with-audio` writes bridge files to `artifacts/scripts/<deck_id>_final.md` and `artifacts/manim/<deck_id>/tts_deck.json`
- for the Manim path, treat the storyboard as the source of truth and treat the generated bridge script as a derived file

## Preamble Map

The `preamble/` directory is split by responsibility so layout and template behavior can be found quickly:

- `preamble/packages.tex`: shared package loading for math (`amsmath`, `amsthm`, `mathtools`), figures (`graphicx`, `tikz`, `pgfplots`), float handling (`float`, `flafter`), page-break control (`needspace`), lists (`enumitem`), page geometry, headers, and cross-references (`hyperref`, `cleveref`)
- `preamble/layout.tex`: paragraph indentation and spacing, list spacing, float placement parameters, running headers and footers, and chapter-title spacing
- `preamble/theorem_setup.tex`: theorem-like environment definitions, chapter-based counters for those environments, the `solution` environment, stronger page-bottom protection for formal result blocks, and lighter page-flow protection for examples, exercises, remarks, and proofs
- `preamble/numbering.tex`: equation numbering by chapter
- `preamble/bibliography.tex`: bibliography backend and bibliography source file

Template pagination note:
- formal result blocks such as `theorem`, `lemma`, `proposition`, `corollary`, and `definition` reserve more vertical space before they start
- `example`, `exercise`, `solution`, and `proof` use lighter protection and may span pages naturally
- do not add manual `\newpage`, `\pagebreak`, or `\clearpage` in chapter files just to keep these blocks together unless a task explicitly calls for a local exception

## Which File To Read

If you are writing or revising textbook content:
- start with [`CONTENT_README.md`](CONTENT_README.md)
- then work in the relevant file under `chapters/`

If you are generating media:
- use [`CHECKLIST.md`](CHECKLIST.md) when you want the shortest end-to-end operational path
- use [`MANIM_README.md`](MANIM_README.md) when you want the storyboard-driven Manim path
- start with [`SLIDES_README.md`](SLIDES_README.md)
- then use [`SCRIPT_README.md`](SCRIPT_README.md) when editing narration
- then use [`VIDEO_README.md`](VIDEO_README.md) for audio and MP4 rendering
- then use the scripts under `tools/`

## Current Scope

The book source is general, and the slide generator is now plan-driven. At the moment, the checked-in practice plan is still centered on:

- `chapters/ch01_foundations.tex`
- the section `Inverse Functions and One-to-One Functions`
- the plan `inputs/media_plans/ch01_inverse_functions.json`
- the storyboard `inputs/manim_storyboards/ch01_inverse_functions.yml`
- generated and reviewable media assets under `artifacts/`

## Media Workflow Snapshot

The current media flow is intentionally staged:

1. finish the lecture-note version in `chapters/*.tex`
2. generate slide artifacts plus a narration draft and narration final file from a section media plan
3. revise only the final narration file until the spoken version is ready
4. synthesize audio from the final narration file
5. render the MP4 from slide PDF plus narration WAV files

The Manim path now exists in parallel:

1. seed `inputs/manim_storyboards/<deck_id>.yml` from an existing deck JSON
2. edit storyboard scenes, `voiceover`, timings, and optional hooks directly
3. preview one scene at a time until the animation feels right
4. run `render_manim_lesson.py --with-audio` once to export the bridge narration files
5. synthesize one WAV per scene into `artifacts/audio/<deck_id>_manim/`
6. rerun `render_manim_lesson.py --with-audio` to mux scene audio into `artifacts/video/<deck_id>_manim.mp4`

Narration ownership rule:

- slide/PDF path: `*_draft.md` is regenerated and disposable
- slide/PDF path: `*_final.md` is user-owned, should be edited directly, and is the narration source read by the slide-based TTS tools
- Manim path: each scene's `voiceover` in `inputs/manim_storyboards/*.yml` is user-owned and should be edited directly
- Manim path: `artifacts/scripts/*_final.md` is regenerated from the storyboard as a TTS bridge file and should not be edited by hand
- if you want to add a joke or a more conversational line for a Manim lesson, put it in the storyboard `voiceover`; for the slide/PDF path, put it in `*_final.md`

Version-control rule:

- commit `artifacts/scripts/*_final.md` when you want narration edits in project history
- commit `artifacts/slides/*.tex` when you want the generated Beamer source in project history
- commit `inputs/manim_storyboards/*.yml` when you want Manim animation and narration edits in project history
- if a Manim deck uses the TTS bridge, the generated `artifacts/scripts/*_final.md` can be committed as a derived snapshot, but the storyboard remains canonical
- do not commit `*_draft.md`, slide PDFs, or LaTeX build artifacts under `artifacts/`

For the actual commands and file paths, use:

- [`MANIM_README.md`](MANIM_README.md)
- [`SLIDES_README.md`](SLIDES_README.md)
- [`SCRIPT_README.md`](SCRIPT_README.md)
- [`VIDEO_README.md`](VIDEO_README.md)

## Notes

- `style_guide.md` is only a short redirect note now.
- Local caches, virtual environments, and vendored dependencies live in hidden repo folders such as `.cache/`, `.venv/`, `.deps/`, and `.deps_f5/`.
