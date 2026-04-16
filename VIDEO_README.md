# Video README

This file covers audio synthesis and MP4 rendering for the slide/PDF workflow only.

Use the other guides for upstream stages:

- [`CONTENT_README.md`](CONTENT_README.md): textbook-writing rules
- [`MANIM_README.md`](MANIM_README.md): storyboard-driven Manim workflow, including scene-audio muxing
- [`SLIDES_README.md`](SLIDES_README.md): slide generation and plan rules
- [`SCRIPT_README.md`](SCRIPT_README.md): narration draft/final workflow
- [`README.md`](README.md): repository overview

## Purpose

This stage starts after:

- the slide deck has been generated
- the final narration markdown has been edited and settled

If you are rendering a storyboard-driven Manim lesson instead, use [`MANIM_README.md`](MANIM_README.md). The TTS scripts documented here can still be reused there through the bridge deck and bridge script files, but the narration source of truth is different.

Its job is to:

1. prepare or choose a voice reference
2. synthesize one WAV file per slide
3. validate that the audio set matches the current deck
4. render the final MP4 from slide PDF plus narration WAV files

## Relevant Paths

- `inputs/voice/`: raw voice recordings
- `artifacts/voice/`: processed reference clips
- `artifacts/audio/`: per-slide narration WAVs and manifests
- `artifacts/video/`: final MP4 outputs and intermediate render files
- `tools/preprocess_voice_reference.py`
- `tools/synthesize_section_audio.py`
- `tools/synthesize_section_audio_f5.py`
- `tools/render_section_video.py`

## Voice Reference Preparation

Use the preprocessing tool when you want a cleaned reference clip for voice cloning.

Example:

```powershell
python .\tools\preprocess_voice_reference.py
```

Custom input example:

```powershell
python .\tools\preprocess_voice_reference.py `
  --input inputs\voice\sample_reference.wav `
  --output artifacts\voice\sample_reference_30s.wav
```

Reference-script note:

- keep reference inputs in `.wav` format
- `inputs/voice/reference_script_en.txt` is a recording script template for a new F5 reference clip
- if you pass `--reference-text`, it must match the spoken content of `--reference-wav` word for word
- if you do not know the exact transcript, leave `--reference-text` empty and let the tool transcribe the reference clip first

## Coqui TTS

Script:

- `tools/synthesize_section_audio.py`

What it does:

- reads the deck JSON
- reads the final narration markdown
- synthesizes one WAV per slide
- writes a synthesis manifest

Default example:

```powershell
python .\tools\synthesize_section_audio.py `
  --deck-id ch01_inverse_functions `
  --coqui-tos-agreed
```

Dry-run validation:

```powershell
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --dry-run
```

Useful options:

- `--deck-id`
- `--script-file`
- `--reference-wav`
- `--voice-mode clone|builtin`
- `--device auto|cpu|cuda`
- `--max-slides`
- `--dry-run`

Notes:

- XTTS v2 requires explicit agreement to Coqui CPML terms
- TTS reads the final narration file only
- built-in voices can be routed to a custom output directory if you want to keep multiple audio variants
- in the Manim path, these same TTS tools are used through exported bridge files; see [`MANIM_README.md`](MANIM_README.md)

## F5-TTS

Script:

- `tools/synthesize_section_audio_f5.py`

Clone example:

```powershell
python .\tools\synthesize_section_audio_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone
```

Example-reference mode:

```powershell
python .\tools\synthesize_section_audio_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode example
```

Dry-run validation:

```powershell
python .\tools\synthesize_section_audio_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone `
  --dry-run
```

Useful options:

- `--deck-id`
- `--script-file`
- `--reference-mode clone|example`
- `--reference-wav`
- `--reference-text`
- `--device auto|cpu|cuda`
- `--max-slides`
- `--dry-run`

Clone-mode note:

- F5 clone quality depends on `reference_wav` and `reference_text` matching exactly
- a mismatched transcript can leak stray words from the reference prompt into every slide audio
- the wrapper now auto-transcribes the reference clip locally when `--reference-text` is omitted

## Video Rendering

Script:

- `tools/render_section_video.py`

What it does:

- validates that slide PDF, slide count, and audio filenames match the current deck
- renders slide images from the PDF
- pairs each image with its slide audio
- creates one MP4 segment per slide
- concatenates the segments into a final MP4

Dry-run validation:

```powershell
python .\tools\render_section_video.py --deck-id ch01_inverse_functions --dry-run
```

Basic render:

```powershell
python .\tools\render_section_video.py --deck-id ch01_inverse_functions
```

Render with a custom audio variant:

```powershell
python .\tools\render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

Useful options:

- `--deck-id`
- `--audio-dir`
- `--output`
- `--dry-run`
- `--dpi-scale`
- `--lead-in-seconds`
- `--target-width`
- `--target-height`
- `--crf`

## Recommended Order

### Path A: slide PDF + edited final narration + Coqui clone + MP4

```powershell
python .\tools\preprocess_voice_reference.py
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --dry-run
python .\tools\synthesize_section_audio.py --deck-id ch01_inverse_functions --coqui-tos-agreed
python .\tools\render_section_video.py --deck-id ch01_inverse_functions --dry-run
python .\tools\render_section_video.py --deck-id ch01_inverse_functions
```

### Path B: slide PDF + edited final narration + F5 clone + MP4

```powershell
python .\tools\preprocess_voice_reference.py
python .\tools\synthesize_section_audio_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone `
  --dry-run
python .\tools\synthesize_section_audio_f5.py `
  --deck-id ch01_inverse_functions `
  --reference-mode clone
python .\tools\render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --dry-run
python .\tools\render_section_video.py `
  --deck-id ch01_inverse_functions `
  --audio-dir artifacts\audio\ch01_inverse_functions_f5_clone `
  --output artifacts\video\ch01_inverse_functions_f5_clone.mp4
```

## Troubleshooting

### TTS dry-run fails

Common causes:

- the final narration markdown file is missing
- one `Narration:` block is empty
- slide numbering or slide ids no longer match the current deck

Use [`SCRIPT_README.md`](SCRIPT_README.md) for narration-structure rules.

### Render dry-run fails because audio files are missing

Common causes:

- TTS has not been run yet
- the audio directory belongs to an older deck version
- the slide ids changed after regeneration, so the old WAV filenames are stale

This is why `render_section_video.py --dry-run` exists: it catches the mismatch before a long ffmpeg run.

### XTTS run fails before synthesis

Common causes:

- `--coqui-tos-agreed` was not provided
- the reference WAV is missing
- CUDA was requested but is not available

### Final MP4 render fails

Common causes:

- slide PDF missing
- narration WAVs missing or misnamed
- PDF page count does not match the deck JSON
- ffmpeg could not be resolved through `imageio_ffmpeg`

## Current Constraint

The slide and script workflow is now reusable, but the repository still only ships one checked-in practice deck.

That means the audio and video scripts are now deck-id aware, yet your actual media outputs still depend on whether you have already generated a matching audio set for that deck version.
