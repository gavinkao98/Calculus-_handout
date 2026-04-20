# Manim README

Storyboard-driven animation pipeline for producing calculus teaching videos.

Related guides:

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

## Design: Midnight Canvas

The visual system follows a **dark canvas, luminous math, zero chrome** philosophy. Content floats on a deep dark background; colours carry mathematical meaning; animations serve a pedagogical purpose.

### Colour semantics

| Role | Colour | Meaning |
|------|--------|---------|
| Background | `#0b0c10` deep navy-black | Mathematics emerges from darkness |
| Titles | `#e8e8f0` off-white | Neutral, never competes with math |
| Definitions / propositions | `#4cc9f0` cool cyan | Cold = precise, formal |
| Theorems / key results | `#f9a825` warm gold | Warm = important, remember this |
| Math expressions | `#7df9ff` electric blue | Maximum contrast on dark canvas |
| Counterexamples / warnings | `#ff6b6b` coral red | "Watch out" |
| Verified / QED | `#06d6a0` emerald | Correct, complete |
| Body text | `#c8c8d8` light grey | Readable without glare |
| Faded context | `#505060` slate grey | Earlier steps remain visible without competing |

### Layout principles

- No cards, no borders, no badges, no chips — the content *is* the design
- Only decoration: a thin horizontal rule (`_thin_rule`) separating title from content
- Enlarged typography (title 44, body 30, math 38) — video is not a textbook
- Wide margins (1.2 Manim units) for breathing room
- Vertical-flow layout managed by `SceneLayout` — no cramped side-by-side cards

### Animation language

- Math equations **write on** (`Write`) like chalk on a blackboard
- Graph curves **trace out** (`Create`) from left to right
- Key results **flash gold** (highlight animation) to grab attention
- Older steps and equations **decay into slate** once the focus moves on
- Algebra workspaces **align on the equals sign** when multiple lines support it
- Steps appear **one at a time** — every moment has exactly one focal point
- Scenes end with a unified `FadeOut` — clean exit into darkness

### Template differentiation

Templates are distinguished by **animation rhythm and content structure**, not by decorative widgets:

| Template | Feel | How it differs |
|----------|------|----------------|
| `definition_math` | Measured | Statement first, then math writes on slowly |
| `example_walkthrough` | Interactive | Steps and math alternate, old context dims, derivations can align on `=` |
| `graph_focus` | Visual star | Full-width graph, curves trace out, labels float in |
| `procedure_steps` | Sequential | Large coloured numbers lead each step, equations below with optional `=` alignment |
| `section_transition` | Cinematic | Centred title, gold rule, brief and elegant |
| `recap_cards` | Gathering | Coloured dot bullets, identities write on with presence |
| `theorem_proof` | Formal | Italic statement, "Proof." label, steps build, QED symbol |
| `comparison` | Parallel | Two columns with a thin vertical divider |
| `title_bullets` | Opening | Coloured dots cycle through cyan / gold / coral |

## Architecture

```
tools/manim_templates/
  __init__.py           module entry point
  layout.py             SceneLayout — vertical-flow zone manager
  components.py         visual elements (accent bars, callouts, highlight boxes, etc.)
  animations.py         animation utilities (write_math, scene_exit, reveal_groups)
  templates.py          9 scene template renderers ("Midnight Canvas" design)
  helpers.py            base building blocks (titles, bullet lists, math stacks, cards)
  hooks.py              compatibility re-exports for legacy hook paths
  registry.py           template dispatch + hook resolution
  scene_player.py       StoryboardTemplateScene + scene exit
tools/manim_hooks/
  __init__.py           chapter-scoped hook namespace
  ch01_inverse_functions.py
```

## Relevant Paths

- `inputs/manim_storyboards/`: user-edited storyboard YAML files
- `schemas/manim_storyboard.schema.json`: storyboard contract reference
- `tools/seed_manim_storyboard.py`: seed a storyboard from an existing deck JSON
- `tools/preview_manim_scene.py`: render one scene only
- `tools/preview_graph_focus.py`: fast Matplotlib debug preview for `graph_focus` scenes
- `tools/render_manim_lesson.py`: render the full lesson with scene caching
- `tools/sync_narration_back.py`: sync edited `narration.md` back into the storyboard YAML
- `tools/manim_templates/`: reusable scene templates plus legacy hook compatibility
- `tools/manim_hooks/`: recommended home for chapter/topic-specific custom hooks
- `artifacts/manim/<deck_id>/`: cached scene videos, muxed segments, bridge deck JSON, render manifest
- `artifacts/manim/<deck_id>/graph_previews/`: lightweight graph debug PNGs
- `artifacts/manim/<deck_id>/narration.md`: Manim narration file (proofread and sync back to YAML)
- `artifacts/audio/<deck_id>_manim/`: one WAV per scene when you use the audio bridge
- `artifacts/video/<deck_id>_manim.mp4`: final Manim lesson output

## Prerequisites

The runtime scripts need local tools that are separate from this repo:

- `manim` in the active Python environment
- either standalone `ffmpeg` on `PATH`, or the Python package `imageio-ffmpeg`
- optional: `matplotlib` if you want to use `preview_graph_focus.py`

Without them, the scripts still support validation and seeding, but actual scene rendering will stop with a clear prerequisite error.

## Storyboard Shape

Top-level required fields:

- `deck_id`
- `language`
- `theme` — omit all sub-keys to use the Midnight Canvas defaults
- `video`
- `scenes`

Each scene requires:

- `scene_id`
- `template`
- `title`
- `voiceover`
- `data`

Optional scene fields:

- `hook` — dotted import path to a custom animation function
- `timing` — `lead_in_seconds`, `hold_after_seconds`, `minimum_duration_seconds`
- `disabled` — skip this scene during rendering
- `content_type` — `definition`, `theorem`, `lemma`, `proposition`, `example`, `warning`, `procedure`, `recap`. Controls accent colour. Inferred from template if omitted.
- `scene_exit` — `fade`, `hold` (recommended for audio), `none`. Use `hold` when the voiceover is longer than the animation so the content remains visible while the narration finishes
- `reveal_groups` — optional progressive-reveal timing

### Templates (9)

| Template | Required data | Description |
|----------|--------------|-------------|
| `title_bullets` | `bullets` | Opening or overview scene |
| `definition_math` | `statement`, `math_lines` | Formal definitions and theorems |
| `example_walkthrough` | `steps`, `takeaway` | Worked examples with math workspace; optional `math_layout`, `decay_previous` |
| `graph_focus` | `axes`, `plots`, `annotations` | Full-width graph with floating labels |
| `procedure_steps` | `steps`, `worked_equations` | Numbered step-by-step procedures; optional `math_layout` |
| `recap_cards` | `points`, `identities` | Summary with coloured bullet points |
| `section_transition` | (optional `subtitle`, `upcoming`) | Cinematic topic-change interlude |
| `theorem_proof` | `theorem_statement`, `proof_steps` | Theorem + step-by-step proof + QED |
| `comparison` | `left`, `right` | Side-by-side concept comparison |

### Math lines extended format

Backward compatible — plain strings still work:

```yaml
math_lines:
  # Plain string:
  - "\\[f(x)=x^2\\]"
  # Extended dict with animation hint:
  - text: "\\[f^{-1}(x)=\\sqrt{x}\\]"
    animation: "highlight"  # write | fade | highlight | transform_from_previous
```

`transform_from_previous` is useful for algebra scenes where one displayed equation should visibly evolve into the next.

### Math workspace controls

`example_walkthrough` and `procedure_steps` support an optional `math_layout` field:

```yaml
data:
  math_layout: "equals_aligned"   # auto | left | equals_aligned
  decay_previous: true            # example_walkthrough only; defaults to true
  math_lines:
    - "\\[y = x^3 + 2\\]"
    - text: "\\[x = \\sqrt[3]{y - 2}\\]"
      animation: "transform_from_previous"
    - text: "\\[f^{-1}(x) = \\sqrt[3]{x - 2}\\]"
      animation: "highlight"
```

Guidance:

- use `auto` when you want the template to align only scenes that clearly behave like algebra derivations
- use `equals_aligned` when multiple lines should share a fixed `=` anchor
- use `left` for mixed text-heavy formulas where alignment by `=` would feel forced

### YAML multiline strings

When a narration paragraph or LaTeX block becomes hard to read as one escaped line, you may use YAML block scalars:

```yaml
voiceover: >
  Start with y = x^3 + 2.
  Solve for x, then swap x and y.

data:
  statement: |
    A function \(f\) is one-to-one if different inputs
    always produce different outputs.
```

The local YAML loader supports both `|` and `>` forms, and `sync_narration_back.py` can now write block scalars back into the storyboard when a narration becomes multi-line.

### Graph authoring rules (`graph_focus`)

Follow these rules when writing `graph_focus` scenes to avoid rendering problems.

**Expression helpers**

The evaluator provides these functions: `sin`, `cos`, `tan`, `sqrt`, `exp`, `log`, `cbrt`, `abs`, `pi`, `e`.

Use `cbrt(expr)` for cube roots — **never** write `expr**(1/3)` for negative inputs. Python's `**` on negative bases with fractional exponents produces complex numbers and breaks Manim's plotter.

```yaml
# WRONG — produces a gap/kink near x = 2:
expression: "(x - 2)**(1/3) if x >= 2 else -(2 - x)**(1/3)"

# CORRECT — smooth and continuous everywhere:
expression: "cbrt(x - 2)"
```

**Label positioning**

Every plot entry supports two optional fields:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `label_side` | `up` / `down` / `left` / `right` | `up` for functions/points, `right` for lines | Which side of the curve/line the label sits on |
| `label_x` | number | (centre of curve) | Place the label near this x-coordinate on the curve |

Always set `label_side` and `label_x` when two curves are close together or a label would overlap the `y = x` line:

```yaml
plots:
  - kind: "function"
    expression: "x**3 + 2"
    label: "$f(x) = x^3 + 2$"
    label_side: "up"
    label_x: -0.8       # label near the left end of the curve
  - kind: "function"
    expression: "cbrt(x - 2)"
    label: "$f^{-1}(x)$"
    label_side: "down"
    label_x: 4.0         # label near the right end, away from y=x
```

If you only want to debug curve placement or `label_x`, use the fast preview tool instead of running Manim:

```powershell
python .\tools\preview_graph_focus.py `
  --deck-id ch01_inverse_functions `
  --scene-id cubic_graph_reflection
```

**Domain restriction**

When illustrating a restricted domain, set `x_range` on the plot to exactly the restricted interval. Do not rely on the axes range to clip the curve:

```yaml
# x² restricted to x ≥ 0
- kind: "function"
  expression: "x**2"
  x_range: [0, 2.05]    # starts at 0, not at the axes minimum
```

**Annotations**

Annotations are clamped to the visible frame automatically. Keep annotation text short (one sentence). The text box is 6.5 units wide.

### Theme system

The theme block controls colours, typography, layout zones, animation timing, and content-type colour mapping. Every field has a default — set `theme: {name: "midnight"}` in the storyboard and `deep_merge` fills the rest from `DEFAULT_THEME`. Override individual values as needed:

```yaml
theme:
  name: "midnight"
  colors:
    background: "#0b0c10"
    math: "#7df9ff"
    context: "#505060"
    # ... any subset; unspecified keys use defaults
  typography:
    title_size: 44
    body_size: 30
    math_size: 38
  transitions:
    quick_step: 0.35      # small step / FadeIn beats
    write_speed: 0.8      # normal equation reveal
    hero_write: 1.6       # major highlighted result
    context_decay: 0.25   # dim old context into slate
    section_pause: 0.6    # hold at end of scene
    exit_fade: 0.5        # FadeOut duration
  content_type_colors:
    definition: "secondary"
    theorem: "accent"
    example: "highlight"
```

## Editing Rules

Use these ownership rules to keep the workflow easy to maintain:

- edit scene narration either in the YAML `voiceover` field **or** in `artifacts/manim/<deck_id>/narration.md` (see Narration Proofreading below)
- edit the visual content in `data`
- edit pacing in `timing`
- reserve `hook` for the small number of scenes that genuinely need custom Python; default rhythm, context decay, and equation alignment now live in the shared templates

Title convention:

- use math notation in titles whenever the title references a specific function or expression: `"Graphs of $f$ and $f^{-1}$"`, not `"Graphs of f and f-inverse"`
- concept names stay as plain text: `"The Horizontal Line Test"`, `"Key Takeaways"`
- `$...$` in titles is rendered by `Tex` inside `\textbf{}`; math symbols will appear in normal math weight while surrounding text is bold

Recommended habit:

- keep one teaching idea per scene
- keep one spoken paragraph per `voiceover`
- keep `voiceover` written for speech and `data` written for the screen

Current behavior note:

- scene caching is now based on the visual payload only: template, title, data, theme, hook, and related render code
- changing `voiceover` or `timing` no longer forces a Manim re-render; narration-only edits reuse the cached silent scene video and only rebuild bridge/audio outputs as needed

## Narration Proofreading

The `narration.md` file is a clean, readable transcript of all scene narrations — ideal for proofreading. It lives inside `artifacts/manim/<deck_id>/`, separate from the Beamer pipeline's scripts. You can edit it directly and sync changes back to the storyboard YAML.

### Proofread-and-sync workflow

1. Export the narration file (this happens automatically when rendering):

    ```powershell
    python .\tools\render_manim_lesson.py --deck-id ch01_inverse_functions --quality preview --with-audio
    ```

    If scene WAV files do not exist yet, the command still writes `narration.md` and `tts_deck.json`, then stops with ready-to-run TTS instructions.

2. Open `artifacts/manim/ch01_inverse_functions/narration.md` and edit the narration text. Fix wording, add jokes, correct errors — anything under a `Narration:` heading is fair game. **Do not change the `Slide ID` lines.**

   Also leave the hidden `voiceover-hash` comment lines untouched so the sync step can detect stale narration exports.

3. Preview what changed:

    ```powershell
    python .\tools\sync_narration_back.py --deck-id ch01_inverse_functions --dry-run
    ```

4. Write changes back to the YAML:

    ```powershell
    python .\tools\sync_narration_back.py --deck-id ch01_inverse_functions
    ```

    The script creates a `.yml.bak` backup before writing.
    If the YAML narration changed after `narration.md` was exported, the sync step now stops with a stale-file conflict warning. Re-export the narration file, or use `--force` only when you intentionally want the markdown edits to win.

### What the sync script does and does not touch

- **Touches**: only the `voiceover` field of scenes whose narration changed.
- **Does not touch**: `data`, `timing`, `template`, `hook`, or any other field.
- **Safety**: refuses to run if a scene ID in the markdown is not found in the YAML.
- **Conflict protection**: compares each hidden `voiceover-hash` comment against the current YAML before writing, so simultaneous YAML + markdown narration edits do not silently overwrite each other.

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

Preview a `graph_focus` scene with Matplotlib for fast `label_x` / curve debugging:

```powershell
python .\tools\preview_graph_focus.py `
  --deck-id ch01_inverse_functions `
  --scene-id cubic_graph_reflection
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

Sync edited narration from `narration.md` back to the storyboard:

```powershell
python .\tools\sync_narration_back.py --deck-id ch01_inverse_functions
```

Preview narration changes without writing:

```powershell
python .\tools\sync_narration_back.py --deck-id ch01_inverse_functions --dry-run
```

## Audio Bridge

When you pass `--with-audio`, `render_manim_lesson.py` first exports:

- `artifacts/manim/<deck_id>/narration.md`
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
  --script-file artifacts\manim\ch01_inverse_functions\narration.md `
  --output-dir artifacts\audio\ch01_inverse_functions_manim `
  --manifest artifacts\audio\ch01_inverse_functions_manim\manifest.json `
  --coqui-tos-agreed
```

### F5 bridge

```powershell
python .\tools\synthesize_section_audio_f5.py `
  --deck-json artifacts\manim\ch01_inverse_functions\tts_deck.json `
  --script-file artifacts\manim\ch01_inverse_functions\narration.md `
  --output-dir artifacts\audio\ch01_inverse_functions_manim `
  --manifest artifacts\audio\ch01_inverse_functions_manim\manifest.json `
  --reference-mode clone
```

Maintenance rule:

- for Manim lessons, the storyboard `voiceover` is the narration source of truth
- `artifacts/manim/<deck_id>/narration.md` is the Manim narration transcript (separate from the Beamer `artifacts/scripts/` pipeline)
- you may edit `narration.md` for proofreading, then run `sync_narration_back.py` to write changes back to the YAML (see Narration Proofreading above)
- if you edit `narration.md` but do **not** sync, your changes will be overwritten the next time the bridge is exported

Runtime note:

- the render scripts now suppress most MiKTeX and Manim noise, so successful runs usually end with one short completion line

## Hooks

Most scenes should stay inside the template system. Use `hook` only when one scene really needs custom animation.

The hook runs after the template renderer, so a hook can:

- add a small flourish on top of the template scene
- or call `scene.clear()` and build that one scene from scratch

Recommended convention:

- put reusable chapter/topic hooks under `tools/manim_hooks/`
- use dotted import paths like `tools.manim_hooks.ch01_inverse_functions.horizontal_line_test_comparison`
- keep `tools/manim_templates/hooks.py` only as a backwards-compatible shim for older paths

Example hook path:

- `tools.manim_hooks.ch01_inverse_functions.horizontal_line_test_comparison`

## Workflow: LaTeX to Video

The Manim pipeline is **independent** from the slide/PDF pipeline. Storyboards are designed directly from the LaTeX source (`chapters/*.tex`), not seeded from the deck JSON. This allows the two approaches to be compared side by side.

Once a chapter's LaTeX content is finalised, the path to a teaching video is:

1. **Design** — read the LaTeX source and write a storyboard YAML from scratch, choosing templates, writing voiceover, and structuring data for animation
2. **Preview** — `preview_manim_scene.py` renders one scene at a time for rapid iteration
3. **Proofread** — export `narration.md`, review and edit the narration, then run `sync_narration_back.py` to push corrections back to the YAML
4. **Audio** — synthesise voiceover audio via the TTS bridge (Coqui or F5)
5. **Render** — `render_manim_lesson.py --with-audio` produces the final lesson MP4

See [`MANIM_CHECKLIST.md`](MANIM_CHECKLIST.md) for the full step-by-step checklist.

The seeding script (`seed_manim_storyboard.py`) still exists for bootstrapping a first draft from an existing deck JSON, but the recommended workflow is to design the storyboard independently to take full advantage of Manim's animation capabilities.
