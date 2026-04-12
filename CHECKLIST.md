# Workflow Checklist

This is the shortest operational checklist for the media pipeline.

Use the full guides when you need details:

- [`SLIDES_README.md`](SLIDES_README.md)
- [`SCRIPT_README.md`](SCRIPT_README.md)
- [`VIDEO_README.md`](VIDEO_README.md)

## 1. Finalize The Lecture Notes

- Finish the section in `chapters/*.tex` first.
- Do not start polishing narration before the mathematical structure is stable.
- If the section structure changes, expect the slide plan to need updates too.

## 2. Check Or Edit The Slide Plan

- Open `inputs/media_plans/<deck_id>.json`.
- Confirm:
  - `source_file`
  - `source_section`
  - slide order
  - `slide_id`
  - `title`
  - `learning_goal`
  - `bullets`
  - `script_draft`
- If you want to change slide selection rules for one section, edit this plan file.

## 3. Generate Slides And Narration Files

```powershell
python .\tools\generate_section_media.py --deck-id ch01_inverse_functions --compile auto
```

Check that these files were regenerated:

- `artifacts/slide_spec/<deck_id>.json`
- `artifacts/slides/<deck_id>.tex`
- `artifacts/slides/<deck_id>.pdf`
- `artifacts/scripts/<deck_id>_draft.md`

Remember:

- `*_draft.md` is disposable and regenerated
- `*_final.md` is user-owned and preserved

## 4. Edit Narration In The Right File

- Edit only `artifacts/scripts/<deck_id>_final.md`.
- Do not hand-edit `*_draft.md`.
- You may add:
  - transitions
  - pacing changes
  - warnings
  - a joke or brief aside
- Keep these structural lines intact:
  - `## Slide N: ...`
  - `Slide ID: ...`
  - `Narration:`

Quick narration review before you move on:

- does each slide narration have one main teaching job?
- do neighboring slides complement each other instead of repeating each other?
- does spoken math sound like speech rather than raw LaTeX?
- does the final recap slide close the loop back to the opening motivation?
- raw LaTeX in a `Narration:` block will now fail TTS validation

## 5. Validate Narration Before TTS

Coqui:

```powershell
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --dry-run
```

F5:

```powershell
python .\tools\synthesize_section_audio_f5.py --deck-id ch01_inverse_functions --reference-mode clone --dry-run
```

If dry-run fails, do not start a long synthesis run yet.

## 6. Run TTS

Coqui clone:

```powershell
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --coqui-tos-agreed
```

F5 clone:

```powershell
python .\tools\synthesize_section_audio_f5.py --deck-id ch01_inverse_functions --reference-mode clone
```

Check that the output WAV filenames match the current slide ids.
If you pass `--reference-text`, make sure it is the exact transcript of the reference WAV.

## 7. Validate Video Inputs

```powershell
python .\tools\render_section_video.py --deck-id ch01_inverse_functions --dry-run
```

If this fails, the usual causes are:

- missing audio
- old audio filenames from an older deck version
- slide count mismatch between PDF and deck JSON

## 8. Render The MP4

```powershell
python .\tools\render_section_video.py --deck-id ch01_inverse_functions
```

Or use a custom audio set:

```powershell
python .\tools\render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

## 9. If The Deck Changes Later

- Regenerate slides first.
- Re-check `*_draft.md`.
- Keep `*_final.md`, but manually sync it if slide ids or slide count changed.
- Re-run TTS for the new deck version.
- Re-run video dry-run before rendering.

## 10. Where To Change Rules

- Per-section slide content:
  `inputs/media_plans/<deck_id>.json`
- Repo-wide slide generation or Beamer rendering:
  `tools/generate_section_media.py`
- Narration markdown format:
  `tools/slide_script_workflow.py`
- Audio/video path defaults:
  `tools/media_paths.py`

## Quick Rule

- Math backbone lives in the lecture notes and slide plan.
- Personality lives in `*_final.md`.
- TTS only reads `*_final.md`.
- Never trust old audio after the deck changes.
