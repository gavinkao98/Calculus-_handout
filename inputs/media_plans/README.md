# Media Plans

This directory stores section-level slide-generation plans.

Each plan file declares:

- the source LaTeX file
- the source section title
- the deck id
- the ordered slide list
- the curated slide bullets and narration draft
- the source selectors used to pull display math or figure content from the lecture notes

The current generator reads these plans through:

```powershell
python .\tools\generate_section_media.py --plan inputs\media_plans\ch01_inverse_functions.json
```

Or, equivalently, by deck id:

```powershell
python .\tools\generate_section_media.py --deck-id ch01_inverse_functions
```

The generated deck JSON can also be used to seed a storyboard-driven Manim lesson:

```powershell
python .\tools\seed_manim_storyboard.py --deck-id ch01_inverse_functions
```

## Selector Pattern

Selectors point to LaTeX environments inside one section:

```json
{
  "kind": "definition",
  "index": 0
}
```

Supported usage in the current generator:

- `math_blocks`: either a literal LaTeX string or an object with:
  - `block`: a selector
  - `math_index`: zero-based display-math index inside that block
- `tikz_code`: either `null`, a literal LaTeX string, or an object with:
  - `block`: a selector that points to a `figure`
- `source_refs`: optional traceability selectors that must resolve successfully, even when the slide content is editorial rather than directly extracted

## Current Rule

Plans should stay slide-native:

- one slide, one learning goal
- formal definitions, theorems, assumptions, and final formulas remain mathematically exact
- long explanations become bullets or narration, not slide paragraphs
- figures should be selected explicitly instead of copied ad hoc into Python

Manim note:

- media plans and deck JSON can seed a storyboard draft
- after seeding, the storyboard YAML becomes the runtime source of truth for the Manim path
