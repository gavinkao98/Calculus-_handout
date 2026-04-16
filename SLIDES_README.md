# Slides README

This file covers slide generation only.

Use the other guides for adjacent work:

- [`CONTENT_README.md`](CONTENT_README.md): textbook-writing rules
- [`SCRIPT_README.md`](SCRIPT_README.md): narration draft/final workflow
- [`VIDEO_README.md`](VIDEO_README.md): audio synthesis and MP4 rendering
- [`README.md`](README.md): repository overview

## Purpose

The slide workflow turns a finalized lecture-note section into:

- deck JSON
- Beamer `.tex`
- slide PDF
- narration draft markdown
- narration final markdown

The generator is now plan-driven. The checked-in practice plan is:

- source file: `chapters/ch01_foundations.tex`
- source section: `Inverse Functions and One-to-One Functions`
- deck id: `ch01_inverse_functions`
- plan file: `inputs/media_plans/ch01_inverse_functions.json`

## Relevant Paths

- `chapters/`: lecture-note LaTeX source
- `inputs/media_plans/`: section media plans
- `artifacts/slide_spec/`: generated deck JSON
- `artifacts/slides/`: generated Beamer `.tex` and slide PDF; the `.tex` file may be checked in, while the PDF remains generated output
- `artifacts/scripts/`: generated narration draft and final files; the final file is the user-owned version-control copy
- `tools/generate_section_media.py`: generator
- `schemas/slide_deck.schema.json`: deck schema

## Workflow

1. Finalize the mathematical content in `chapters/*.tex`.
2. Create or revise `inputs/media_plans/<deck_id>.json`.
3. Run the generator.
4. Inspect the generated deck JSON, Beamer source, and PDF.
5. Hand off narration editing to [`SCRIPT_README.md`](SCRIPT_README.md).

Example:

```powershell
python .\tools\generate_section_media.py --deck-id ch01_inverse_functions --compile auto
```

If you only want JSON, `.tex`, and narration markdown:

```powershell
python .\tools\generate_section_media.py --deck-id ch01_inverse_functions --compile never
```

## Plan Structure

Each plan file controls one section deck. The main fields are:

- `deck_id`
- `source_file`
- `source_section`
- `language`
- `defaults.render_hints`
- `slides`

Each slide entry usually contains:

- `slide_id`
- `title`
- `learning_goal`
- `slide_type`
- `bullets`
- `math_blocks`
- `tikz_code`
- `script_draft`
- `source_refs`
- optional `render_hints`

For selector syntax, see [inputs/media_plans/README.md](inputs/media_plans/README.md).

## Current Selection Rules

The current workflow does not dump LaTeX environments onto slides verbatim. The selection policy is:

- cover the whole section, not just the opening subsection
- give each slide one teaching job
- keep formal definitions, theorem statements, assumptions, and final formulas mathematically exact
- compress prose-heavy remarks into short bullets
- keep examples focused on one key computation or one key warning
- prefer a figure slide when the graph or diagram teaches faster than text
- leave transitions and extra explanation to narration instead of overloading the slide

Closely related narration rule:

- neighboring slides should divide responsibilities cleanly
- definition slides should carry the logical statement
- figure slides should carry the visual reading
- recap slides should close the loop rather than restating the whole section

## Where To Change Slide Rules

Use these layers:

- section-specific content selection:
  edit `inputs/media_plans/<deck_id>.json`
- section-specific wording for titles, bullets, and draft narration:
  edit the same plan file
- repo-wide slide selection or density policy:
  edit `tools/generate_section_media.py`
- repo-wide Beamer appearance:
  edit `tools/generate_section_media.py`
- allowed slide types or render-hint schema:
  edit `schemas/slide_deck.schema.json` and keep the generator in sync

In practice:

- if you want to add or remove one example from one section, change the plan file
- if you want all decks to enforce a stricter slide-density rule, change the generator
- if you want all decks to use a different Beamer layout, change the generator
- if you want all decks to keep adjacent narration from repeating the same logic, change the generator or review checklist rather than patching one section at a time

## Generator Behavior

Important behavior:

- the draft narration file is always regenerated
- the final narration file is seeded once and then preserved
- if the preserved final file no longer matches the current deck, the generator warns instead of overwriting your edits
- the generator validates plan structure and fails fast when a selector no longer matches the LaTeX section
- the generator defaults to `--compile auto`
- the compile command explicitly enables MiKTeX's installer

Version-control note:

- commit `artifacts/slides/<deck_id>.tex` when you want the generated Beamer source in Git history
- commit `artifacts/scripts/<deck_id>_final.md` when narration edits for that deck should be preserved in Git history
- keep `artifacts/slides/<deck_id>.pdf` and LaTeX build byproducts as generated outputs, not tracked sources

Compile modes:

- `--compile auto`: compile if LaTeX tools are available
- `--compile never`: skip PDF compilation
- `--compile require`: fail if compilation prerequisites are missing

Beamer compilation depends on:

- `latexmk`
- `pdflatex`
- `beamer.cls`

## Troubleshooting

### Generator fails after lecture-note edits

Common causes:

- a `math_index` no longer matches the display-math blocks inside a referenced environment
- a `figure` selector points to the wrong figure after the section changed
- an environment occurrence index in the plan is no longer correct

The fix is usually to update the plan file, not to patch the generated JSON.

### PDF does not compile

Check:

- `latexmk`
- `pdflatex`
- `beamer.cls`
- MiKTeX package installation has been resolved for unattended runs

### Slide deck changes but final narration stays old

This is expected. The generator preserves the final narration file on purpose.

Use [`SCRIPT_README.md`](SCRIPT_README.md) for the workflow that syncs or edits narration after a deck change.
