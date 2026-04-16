# Manim README

This file covers the storyboard-driven Manim pipeline.

Use the other guides for the upstream textbook and slide workflow:

- [`CONTENT_README.md`](CONTENT_README.md): lecture-note writing rules
- [`SLIDES_README.md`](SLIDES_README.md): slide deck generation
- [`SCRIPT_README.md`](SCRIPT_README.md): narration editing rules
- [`VIDEO_README.md`](VIDEO_README.md): static-slide audio + MP4 workflow

## Purpose

This pipeline adds a second video path alongside the existing slide/PDF renderer:

- author a storyboard in `inputs/manim_storyboards/*.yml`
- preview one scene at a time
- render only changed scenes
- optionally bridge the storyboard voiceover into the existing TTS scripts
- concatenate scene videos into one lesson MP4

The storyboard is the source of truth for Manim output. Existing `media plan` and `deck JSON` files are used only to seed a first draft.

## Relevant Paths

- `inputs/manim_storyboards/`: user-edited storyboard YAML files
- `schemas/manim_storyboard.schema.json`: storyboard contract reference
- `tools/seed_manim_storyboard.py`: seed a storyboard from an existing deck JSON
- `tools/preview_manim_scene.py`: render one scene only
- `tools/render_manim_lesson.py`: render the full lesson with scene caching
- `tools/manim_templates/`: reusable scene templates plus optional hooks
- `artifacts/manim/<deck_id>/`: cached scene videos, muxed segments, bridge deck JSON, render manifest
- `artifacts/audio/<deck_id>_manim/`: one WAV per scene when you use the audio bridge
- `artifacts/scripts/<deck_id>_final.md`: generated narration bridge file for the existing TTS tools
- `artifacts/video/<deck_id>_manim.mp4`: final Manim lesson output

## Prerequisites

The runtime scripts need local tools that are separate from this repo:

- `manim` in the active Python environment
- either standalone `ffmpeg` on `PATH`, or the Python package `imageio-ffmpeg`

Without them, the scripts still support validation and seeding, but actual scene rendering will stop with a clear prerequisite error.

## Storyboard Shape

Top-level required fields:

- `deck_id`
- `language`
- `theme`
- `video`
- `scenes`

Each scene requires:

- `scene_id`
- `template`
- `title`
- `voiceover`
- `data`

Optional scene fields:

- `hook`
- `timing`
- `disabled`

Template contracts:

- `title_bullets`: `bullets`
- `definition_math`: `statement`, `math_lines`
- `example_walkthrough`: `steps`, `takeaway`
- `graph_focus`: `axes`, `plots`, `annotations`
- `procedure_steps`: `steps`, `worked_equations`
- `recap_cards`: `points`, `identities`

## Editing Rules

Use these ownership rules to keep the workflow easy to maintain:

- edit scene narration in `voiceover`, not in `artifacts/scripts/*_final.md`
- edit the visual content in `data`
- edit pacing in `timing`
- reserve `hook` for the small number of scenes that genuinely need custom Python

Recommended habit:

- keep one teaching idea per scene
- keep one spoken paragraph per `voiceover`
- keep `voiceover` written for speech and `data` written for the screen

Current behavior note:

- changing `voiceover` or `timing` currently invalidates that scene's cache entry, so the scene will be rendered again before the final mux step
- this keeps the implementation simple and correct, but it means narration-only edits are not yet audio-only rebuilds

## Commands

Seed a storyboard from the existing deck JSON:

```powershell
python .\tools\seed_manim_storyboard.py --deck-id ch01_inverse_functions
```

Preview one scene:

```powershell
python .\tools\preview_manim_scene.py `
  --deck-id ch01_inverse_functions `
  --scene-id one_to_one_definition
```

Preview only the wiring without rendering:

```powershell
python .\tools\preview_manim_scene.py `
  --deck-id ch01_inverse_functions `
  --scene-id horizontal_line_test_figure `
  --dry-run
```

Render the whole lesson:

```powershell
python .\tools\render_manim_lesson.py --deck-id ch01_inverse_functions --quality preview
```

Render a lesson with audio once the scene WAV files exist:

```powershell
python .\tools\render_manim_lesson.py `
  --deck-id ch01_inverse_functions `
  --quality preview `
  --with-audio
```

Validate the lesson pipeline without rendering:

```powershell
python .\tools\render_manim_lesson.py `
  --deck-id ch01_inverse_functions `
  --quality preview `
  --dry-run
```

## Audio Bridge

When you pass `--with-audio`, `render_manim_lesson.py` first exports:

- `artifacts/scripts/<deck_id>_final.md`
- `artifacts/manim/<deck_id>/tts_deck.json`

Those two files let you keep using the existing TTS tools. The renderer expects audio files named like:

- `01_scene_id.wav`
- `02_scene_id.wav`

under `artifacts/audio/<deck_id>_manim/` by default.

If the audio files are missing, the script prints ready-to-run Coqui and F5 bridge commands.

Recommended audio flow:

1. Edit `voiceover` in the storyboard until the spoken wording feels right.
2. Run `render_manim_lesson.py --with-audio` once.
3. If scene WAV files are missing, copy one of the printed TTS commands and generate audio.
4. Re-run `render_manim_lesson.py --with-audio` to mux the lesson.

Equivalent explicit commands are:

### Coqui bridge

```powershell
python .\tools\synthesize_section_audio.py `
  --deck-json artifacts\manim\ch01_inverse_functions\tts_deck.json `
  --script-file artifacts\scripts\ch01_inverse_functions_final.md `
  --output-dir artifacts\audio\ch01_inverse_functions_manim `
  --manifest artifacts\audio\ch01_inverse_functions_manim\manifest.json `
  --coqui-tos-agreed
```

### F5 bridge

```powershell
python .\tools\synthesize_section_audio_f5.py `
  --deck-json artifacts\manim\ch01_inverse_functions\tts_deck.json `
  --script-file artifacts\scripts\ch01_inverse_functions_final.md `
  --output-dir artifacts\audio\ch01_inverse_functions_manim `
  --manifest artifacts\audio\ch01_inverse_functions_manim\manifest.json `
  --reference-mode clone
```

Maintenance rule:

- for Manim lessons, the storyboard `voiceover` is the narration source of truth
- `artifacts/scripts/<deck_id>_final.md` exists only to bridge into the existing TTS scripts
- if you edit the bridge file by hand, your changes will be overwritten the next time the storyboard bridge is exported

Runtime note:

- the render scripts now suppress most MiKTeX and Manim noise, so successful runs usually end with one short completion line

## Hooks

Most scenes should stay inside the template system. Use `hook` only when one scene really needs custom animation.

The hook runs after the template renderer, so a hook can:

- add a small flourish on top of the template scene
- or call `scene.clear()` and build that one scene from scratch

Example hook path:

- `tools.manim_templates.hooks.horizontal_line_test_comparison`
