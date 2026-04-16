# Script README

This file covers narration drafting and editing for the slide/PDF workflow only.

Use the other guides for adjacent work:

- [`CONTENT_README.md`](CONTENT_README.md): textbook-writing rules
- [`MANIM_README.md`](MANIM_README.md): storyboard-driven Manim workflow with scene-level `voiceover`
- [`SLIDES_README.md`](SLIDES_README.md): slide generation and plan rules
- [`VIDEO_README.md`](VIDEO_README.md): audio synthesis and MP4 rendering
- [`README.md`](README.md): repository overview

## Purpose

The narration workflow sits between slide generation and audio/video production.

Its job is to keep two things separate:

- mathematically faithful slide content derived from the lecture notes
- spoken narration that can be more conversational, pedagogical, or stylistically lively

That means you are allowed to make the narration sound human, as long as the mathematics stays correct.

Important scope note:

- this file governs `artifacts/scripts/<deck_id>_final.md` for the slide/PDF path
- it does not govern Manim storyboard narration
- for Manim lessons, edit each scene's `voiceover` field in `inputs/manim_storyboards/*.yml`

## Relevant Paths

- `artifacts/scripts/<deck_id>_draft.md`: regenerated draft narration, disposable, and normally ignored by Git
- `artifacts/scripts/<deck_id>_final.md`: user-owned narration file and the version-control copy you should keep
- `tools/slide_script_workflow.py`: markdown rendering and parsing rules
- `tools/synthesize_section_audio.py`: Coqui TTS reads the final narration file
- `tools/synthesize_section_audio_f5.py`: F5-TTS reads the final narration file

## Draft And Final

The workflow is:

1. generate or regenerate slides
2. generator rewrites `*_draft.md`
3. generator seeds `*_final.md` once if it does not exist
4. after that, you edit only `*_final.md`
5. TTS reads only `*_final.md`

Important rule:

- do not hand-edit the draft file
- do hand-edit the final file
- commit the final file when you want narration changes to remain in project history

## What You May Edit In The Final File

You may edit the narration text freely inside each slide section.

Good edits include:

- smoother transitions
- shorter or longer explanations
- warnings about common mistakes
- spoken emphasis
- a light joke or brief aside
- better pacing for video delivery

So if you want to insert a joke, the correct place is the relevant `Narration:` block in `artifacts/scripts/<deck_id>_final.md`.

## What You Should Not Change

Keep these structural lines intact:

- `## Slide N: ...`
- `Slide ID: ...`
- `Narration:`

Do not:

- renumber slides by hand
- delete the `Narration:` marker
- change a slide id in the final file without regenerating the deck

If those structural markers drift, the TTS scripts will reject the file.

## Mathematical Guardrail

The narration can sound less like a textbook, but it should not break the math.

Keep these accurate:

- definitions
- theorem statements
- assumptions and domain restrictions
- final conclusions
- any statement that a student could later quote as mathematics

## Narration Quality Rules

Use these reusable rules when writing or reviewing narration:

- each slide narration should have one main teaching job
- adjacent slides should complement each other instead of repeating the same logic
- warning or example slides should not fully consume a theorem that is supposed to land later
- spoken math should sound like speech, not raw LaTeX source
- raw LaTeX inside a `Narration:` block is now a hard error for TTS validation
- the recap slide should close the loop by recalling the opening motivation, question, or representative example

Examples:

- a definition slide explains the rule; a figure slide reads the picture
- a warning slide shows failure; the theorem slide states the full criterion
- say "x squared on minus one to one" rather than leaving raw inline LaTeX for TTS to stumble over

## Validation

Before a long TTS run, validate the final narration file:

```powershell
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --dry-run
python .\tools\synthesize_section_audio_f5.py --deck-id ch01_inverse_functions --reference-mode clone --dry-run
```

Those checks confirm:

- the final narration file exists
- each slide still has a narration block
- slide numbering and slide ids still match the current deck

## If The Deck Changes

If you regenerate slides and the deck structure changes, the generator will preserve your final narration file instead of overwriting it.

That is intentional, but it also means you may need to manually sync the final file when:

- a slide was added
- a slide was removed
- a slide id changed
- the slide order changed

In that situation, the dry-run validation step should be your first check.

## Where To Change Script Rules

Use these layers:

- per-section narration wording:
  edit `artifacts/scripts/<deck_id>_final.md`
- seeded draft wording for future regenerations:
  edit `inputs/media_plans/<deck_id>.json`
- markdown structure and parser rules:
  edit `tools/slide_script_workflow.py`

In practice:

- if you want one joke in one section, edit the final narration file
- if you want every freshly generated draft to start with a different tone, edit the plan file
- if you want the markdown format itself to change, edit `tools/slide_script_workflow.py`
- if you are working on a Manim lesson instead, do not edit the generated bridge markdown; edit the storyboard `voiceover` instead

Version-control shortcut:

- `*_final.md` is the tracked narration artifact
- `*_draft.md` remains regenerated working output

## Troubleshooting

### TTS says the narration file does not match the deck

Common causes:

- a slide id changed after regeneration
- a slide heading was edited manually
- one slide section is missing its `Narration:` block

### You accidentally edited the draft file

Regenerate the section media again. The draft file is disposable by design.

### You want to keep a funny line without risking the math

Put the joke in narration, not in slide bullets or extracted formulas.

That keeps the formal backbone on the slide while leaving the spoken layer flexible.

### Two neighboring slides sound repetitive

Check whether one of them should be narrowed:

- definition slide:
  keep the logical rule
- figure slide:
  keep the reading of the picture
- theorem slide:
  keep the formal criterion
- recap slide:
  add closure rather than repeating the theorem one more time
