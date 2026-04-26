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

## Authoring workflow

Chapters originate as **manuscripts written by different teachers** who have split the book between them. Claude interacts with those manuscripts in three distinct modes; the rules differ by mode. Get the mode right before acting.

The modes form a small state machine, not a fixed pipeline:

- **New manuscript arrives.** Run **Mode A** (drafting). Mode A produces a textbook draft from the manuscript and closes with an amplification audit.
- **Mode A draft, before user sign-off.** **Mode B** (curation review) may run as a ready-for-review audit on the draft.
- **Sign-off complete; chapter committed to `main`.** No further mode runs without an explicit user invocation.
- **An already-signed-off chapter needs more depth.** Run **Mode C** (enrichment pass). Mode C only adds, never restructures.
- **After Mode C.** **Mode B must run**, scoped to the new `[pass: enrichment]` markers Mode C produced.

In short: A drafts, C enriches an existing draft, B audits — B is the only mode that runs as a follow-up to another mode. The valid transitions are A → (optional B) → sign-off → (optional C → required B) → ….

### Mode A — Manuscript-to-textbook drafting (Claude converts a new manuscript to LaTeX)

Use this mode when the user forwards a manuscript and asks Claude to produce a chapter file. Claude's role:

1. Receive the manuscript from the user.
2. Convert it into project-compliant LaTeX at `chapters/chNN_<slug>.tex`, following [`CONTENT_SPEC.md`](CONTENT_SPEC.md) and [`CONTENT_QUICKSTART.md`](CONTENT_QUICKSTART.md).
3. Expand around the manuscript where completeness or the Stewart / Rogawski self-study register benefits from it. The expansion policy below describes what kinds of additions are in-policy and how they must be marked.
4. Update [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) to reflect what the manuscript actually decided, replacing any pre-manuscript working-hypothesis entries.

#### The manuscript is the main axis

Every manuscript topic, example, remark, proof, and figure idea appears in the chapter in the order the manuscript presents them, rewritten into project-compliant LaTeX. Claude does **not** skip manuscript content, does **not** reorder it without reason, and does **not** rewrite its mathematical substance. Expansions wrap around manuscript content; they never replace it.

If a reorder or structural regroup is genuinely useful, record it in the chapter's roadmap entry under *Open questions* so the user can sign off during review.

#### Expansion policy — liberal in scope, visible by marker

Claude may expand around the manuscript without pre-authorisation, on the condition that **every expansion is marked** in the LaTeX source so post-hoc review is tractable. The marker takes the form

```latex
% expansion:<category> [pass: <pass-id>] [source: <brief source>] — <one-line description>
```

placed on the line immediately preceding the expansion content. The bracket hints are optional individually but obey strict rules when present:

- `<category>` is required and must be drawn from the table below.
- `[pass: <pass-id>]` identifies which mode-pass introduced the expansion. Omit it in Mode A — an `% expansion:` marker without a `[pass: ...]` hint is taken to be original Mode A drafting (the marker itself is still required, only the `[pass: ...]` hint is optional). **Required** for Mode C, with the literal value `[pass: enrichment]`, so post-hoc review can distinguish original drafting from later enrichment.
- `[source: <brief source>]` cites the reference an expansion draws on. Optional in general; **required** for `history`-category named content per the Named-content rule below, and recommended for any expansion whose accuracy depends on a specific reference.
- When both hints are present, **`[pass: ...]` precedes `[source: ...]`**. The order is fixed so `book_style_lint` can detect malformed markers; markers in the wrong order are a lint error.
- Unknown bracket keys are a lint error — only `pass` and `source` are recognised. A typo like `[soure: …]` would otherwise silently strip the hint from review.

Recognised categories (the `book_style_lint` check enforces this list):

| Category | Purpose |
|---|---|
| `history` | math-history context: how the concept was developed, why the notation was chosen |
| `application` | real-world connection: physics, economics, geometry, engineering tie-in |
| `formula` | derived identity / corollary that follows from what the manuscript proved or defined |
| `summary` | synthesis paragraph tying a block of examples or a proof back together |
| `figure` | figure idea the manuscript implies via prose but does not draw |
| `example` | supplementary `workedexample` illustrating a technique the manuscript introduced |
| `intuition` | motivation paragraph before a formal statement, or an *Informally, ...* gloss |
| `strategy` | `strategy` box distilling a method shared by multiple manuscript examples |
| `caution` | `caution` box for subtle restrictions, notation traps, or common errors |

The category list is intentionally small; when a durable new type appears, grow this table in the same commit that introduces the first marker of the new category, and the lint will accept it going forward.

Post-hoc review then becomes

```powershell
grep "^% expansion:" chapters/chNN_*.tex
```

— the user sees every non-manuscript addition at a glance and decides *keep*, *rewrite*, or *remove* per marker, without having to diff the full chapter against the manuscript.

#### Named-content: mark with a source, do not self-censor

Named content — specific historical figures, dates, centuries, proper-name attributions, named results — is **permitted** in drafting mode. The user has indicated they will manually verify names and dates during post-hoc review, so Claude's job is to include the content when it fits the Stewart / Rogawski register and to mark a source (or the nearest standard reference) so review is efficient.

Pattern:

```latex
% expansion:history [source: <specific source OR "standard calculus-textbook historical note">] — <description>
```

- If Claude can identify a specific source (e.g. *Stewart 8e §2.4 historical note*, *Rogawski 4e Ch 2*, *Wikipedia "History of calculus"*), cite it in the marker. That lets the user verify against one place rather than guessing.
- If the content is a common textbook-register passage that most calculus books share — the Newton / Leibniz origin, the nineteenth-century ε-δ resolution, Archimedes and the method of exhaustion — use `[source: standard calculus-textbook historical note]` with a short description of what Claude drew on. The user treats this as *"I will check the claim is non-controversial"* rather than *"I will look up one specific page."*
- **Direct quotations** still require a specific source. Quoting a mathematician verbatim is the highest-risk subclass; if no specific source is available, paraphrase instead of quote.

The spirit: Claude should err toward **including** pedagogically helpful named content rather than self-censoring to be safe. The marker makes the content reviewable; the source tag makes review efficient. Self-censorship produces thin chapters; over-inclusion produces chapters the user quickly trims at review. The cost of the first is much higher than the cost of the second.

#### Expansion density calibration

The correct density target is **Stewart / Rogawski self-study textbook**, not minimalist manuscript translation. Concretely that means:

- multiple `example` expansions per major technique are welcome when they illustrate different angles;
- synthesis prose (connecting paragraphs, summarising conclusions, pulling threads together) should be generous, not sparse;
- historical openings, applied tie-ins, and intuitive framing for the opening of each section are the default, not the exception;
- `strategy` and `caution` boxes for standard pitfalls are part of the house voice.

The committed Chapter 1 before the fresh Mode A pass (commit `f701c02`) is a useful density reference — that draft, written by the user, shows the intended richness. When in doubt, Claude should lean toward more expansion (with markers) rather than less. Under-expansion is harder to fix after the fact than over-expansion, because users can always delete a marked expansion during review but rarely write additional expansion during review.

#### Volumetric sanity check (soft, not enforced)

No hard rule on expansion-to-manuscript ratio, just a self-check: if a section's `% expansion:` markers dominate to the point where the manuscript content is hard to find amid the expansions, something has drifted. Flag it in the chapter's roadmap *Open questions* so the ratio can be reviewed during sign-off. Otherwise, amplify freely.

#### Non-repetition rule: different depth, different framing

Pedagogical repetition (a key concept returning at chapter open, section open, and Summary) is fine and often helpful — but **only if each resurface is at a different depth or with a different frame**. The same-depth rehash is what produces the "didn't we just read this?" feeling. Four concrete mechanisms keep expansions from stepping on each other:

1. **Per-category role clauses.** Each expansion category has a narrow job and explicitly avoids the jobs of neighboring categories:
   - **Chapter overview** (`intuition`): describes the chapter's arc — which two or three themes it develops and how they connect. Does **not** predict what each section will teach; that is the job of the learning-outcomes list and of each section's own opener.
   - **Learning outcomes** (`summary`): a verb-first bullet list of operational skills (*decide*, *compute*, *apply*). Does **not** explain the concepts or give their motivation; that is the body's job.
   - **Section opener** (`intuition` or `application`): motivates *this* section specifically, including how it builds on the previous section. Does **not** restate the chapter overview, and does **not** list what the next section will cover.
   - **Informally gloss** (`intuition`, inside a `definition`): one vernacular sentence. Does **not** become a motivation paragraph, an example, or a preview of the surrounding theorem.
   - **Strategy box** (`strategy`): distils a method already demonstrated by two or more worked examples in the same section. Does **not** repeat the worked examples' prose; it names the steps.
   - **Caution** (`caution`): one specific trap or subtle restriction. Does **not** restate the definition or theorem it attaches to; readers still have those nearby.
   - **Summary** (`summary`, chapter end): one-line reminders per item (a definition by its one-clause essence, a theorem by its condition-and-conclusion, a formula as the bare identity). Does **not** reprove, re-derive, or re-motivate.

2. **Point, don't repeat.** When a concept introduced earlier returns, use an explicit cross-reference (`\cref{sec:foo}`, *"as introduced in §1.3, the limit of..."*) rather than restating the content. A cross-reference is honest: it signals "we have this, here is where." A restatement is dishonest: it pretends the concept is new.

3. **Depth-layered resurfacing.** The same concept may appear three times (chapter open, section open, Summary) if each appearance is at a different depth:
   - chapter open: one sentence placing the concept in the arc;
   - section open: one paragraph on why this section sharpens the concept;
   - Summary: one-line reminder.
   Three occurrences at the same depth = repetition; three at different depths = spiral review.

4. **Drafting-end self-check.** After the chapter is drafted, scan the first sentence after each `% expansion:` marker in order. If any two consecutive expansions open with the same claim or concept, collapse one into a cross-reference. In particular, scan chapter overview against §1 opener, each section opener against the previous section's closing, and Summary items against learning outcomes — those are the three places where same-depth rehash most often slips in.

If an expansion does not have a job that the other expansions are not already doing, it should either be rewritten to carve out a distinct role or deleted.

#### Mode A closes with an amplification audit

A Mode A pass is not finished when the manuscript has been converted into LaTeX. Before handing the chapter back, Claude walks each section against the per-section checklist below and, for every item that is not satisfied, **either fills the gap or records the deliberate omission in the chapter's roadmap entry under *Open questions***. This audit is what turns a typeset manuscript into a textbook draft; without it, the density-calibration target above is aspirational rather than enforced.

Per-section checklist (each item is *fill or record* — silently skipping is what the rule exists to prevent):

1. **Section opener.** Does the section open with a motivation paragraph that ties back to the previous section or the chapter arc? (`intuition` or `application`)
2. **Definition glosses.** Does each new definition have at least one informal gloss or intuition pass before the formal statement? (`intuition`)
3. **Worked-example density.** Does each new technique have at least one supplementary `workedexample` beyond what the manuscript supplied? (`example`) — *exception when the manuscript already supplies multiple worked examples per technique; record this in roadmap if it applies.*
4. **Boundary case or counterexample.** Does the section include at least one boundary case, counterexample, or non-example showing where the technique fails? (`example` or `caution`)
5. **Caution boxes.** Are common errors, sign traps, or notational pitfalls captured as `caution` boxes? (`caution`)
6. **Strategy distillation.** When two or more examples in the section share a method, is the method distilled into a `strategy` box? (`strategy`)
7. **Visual reasoning.** Are concepts that benefit from a picture carried by at least a `figure` idea (the asset itself can be deferred to media work)? (`figure`)
8. **Closing synthesis.** Does the section close with synthesis prose that pulls the examples and theorems back to the section's headline result? (`summary`)

A *no* on any item is acceptable provided the deliberate omission is recorded — the rule is **fill or record**, not "every section must score 8/8". Recording the omission in roadmap *Open questions* lets the user agree, push back, or supply the missing piece during sign-off; silently skipping the item produces the "translated handout" feel the textbook density target exists to prevent.

#### Still forbidden in drafting mode

- skipping manuscript content (the manuscript is the axis);
- rewriting the mathematical substance of a manuscript claim (method of proof, choice of variable, definition form);
- inventing exercises — exercise inventories come from the manuscript (see [`CONTENT_EXERCISES.md`](CONTENT_EXERCISES.md));
- unmarked expansions — every non-translation addition takes an `% expansion:` marker;
- named content that violates the Named-content guardrail above.

Supplying a proof the manuscript omitted is a borderline case: per [`CONTENT_SPEC.md`](CONTENT_SPEC.md) §5 proofs are optional and omission is the default. Claude **may** add a proof as an `expansion:formula` (for a short derivation) or `expansion:example` (for a worked case) when the proof is short, standard, and illustrative; multi-page proofs or proofs that require material the chapter has not introduced need explicit user authorisation.

### Mode B — Curation review (Claude audits existing content)

Use this mode when Claude is asked to audit existing chapter content against the manuscript, the spec, or the current draft state. Per the workflow state machine above, Mode B has three valid entry points:

- a Mode A draft, before user sign-off (ready-for-review audit);
- a chapter that has been committed to `main` (recurring spec-compliance or accuracy review);
- the output of a Mode C enrichment pass (**required** follow-up scoped to the new `[pass: enrichment]` markers).

**Committed content is authorised content.** The user has signed off on what landed in `main`; Claude must **not** treat pre-existing expansions beyond the manuscript as "hallucination" just because they are not verbatim in the manuscript — the user may have authored the expansion themselves during the original drafting pass.

#### Per-marker verdict (Keep / Rewrite / Move / Cut)

For chapters that carry `% expansion:` markers, Mode B walks every marker in the file and assigns one of four verdicts. Verdicts are **reported to the user per marker**; Claude does not act on them unilaterally.

| Verdict | Meaning | What Claude does |
|---|---|---|
| **Keep** | Correct, in the right place, register matches Stewart / Rogawski, not duplicating a neighbouring expansion. | Note as Keep; no change. |
| **Rewrite** | Direction is right but execution needs work — register slip, redundancy with a neighbour, awkward phrasing, accuracy nit. | Propose the rewrite inline so the user can accept or revise. |
| **Move** | Content has value but belongs elsewhere — earlier section, end-of-chapter Summary, a `strategy` box instead of an `example`, or even a later chapter where it would have proper setup. | **Propose only.** Describe the move, do not execute it. |
| **Cut** | Correct but not pedagogically load-bearing here — duplicates a neighbour at the same depth, or restates content that is already clear from the body. | Propose deletion with one sentence on why. |

**`Move` is propose-only.** This is the verdict most likely to be misused. A Mode B run that quietly relocates expansions across sections under cover of "moves" defeats the audit's purpose: every cross-section restructure is a structural decision the user must enact. Even within a single section, a Move that changes ordering or environment type (e.g., `example` → `strategy`) is a proposal, not an action.

When Mode B runs as the required follow-up to Mode C, scope the verdict pass to the new `[pass: enrichment]` markers — the original Mode A markers were already audited at sign-off and re-auditing them would invite churn.

#### Other Mode B findings (alongside the verdicts)

Independently of the per-marker verdict, Claude flags:

- **Spec compliance** — rule violations against [`CONTENT_SPEC.md`](CONTENT_SPEC.md): disallowed display helpers, `\textbf` / `\textit` in prose, ASCII quotes, manual cross-reference prefixes, `\newcommand` in chapter files, missing chapter opening structure, etc. These are definite defects; propose fixes.
- **Notation drift** from the manuscript — e.g., the manuscript uses `[x]` and the `.tex` silently uses `\lfloor x \rfloor`. Surface this as a question for the user, not as a hallucination. The user may have intentionally upgraded the notation, or may want to realign to the manuscript.
- **Mathematical correctness** — if a statement looks wrong, surface it as *"please verify X"*, not as *"I'm removing X because it's not in the manuscript."*
- **Missing content from the manuscript** — if the manuscript covers a topic the `.tex` skips, flag the gap so the user can decide whether the omission was intentional.
- **Structural decisions** — section splits, theorem names, and similar editorial choices. Surface as questions; do not change unilaterally.

#### What Claude must not do in Mode B

- treat content in the `.tex` that is absent from the manuscript as hallucination by default;
- silently remove or rewrite user-authored expansions on the grounds that they lack a manuscript anchor;
- act on a `Move` verdict — `Move` is always propose-only, including within a single section;
- propose deletion of historical notes, extra worked examples, or extra remarks without first asking whether they were user-authored expansion or drafting-mode hallucination;
- re-audit `% expansion:` markers without `[pass: enrichment]` when the entry point was a Mode C follow-up — those are out of scope for that run.

The operative question in Mode B is *"is this content correct, compliant, and in the right place?"* — not *"is this content in the manuscript?"* Only in Mode A does the second question become load-bearing.

### Mode C — Enrichment pass (Claude adds depth to a signed-off chapter)

Use this mode when an already-signed-off chapter would benefit from additional textbook depth and the user explicitly asks Claude to enrich it. Mode C exists because the natural place to "amplify a chapter" is *after* the manuscript axis has been settled at sign-off, not by re-entering Mode A and risking changes to the axis itself.

#### What Mode C may do

- add `intuition`, `example`, `figure`, `caution`, `strategy`, `application`, `formula`, `history`, or `summary` expansions, each marked exactly as in Mode A (`% expansion:<category> …`) **but with the required `[pass: enrichment]` hint** so post-hoc review can distinguish original drafting from enrichment;
- close with the same per-section amplification audit Mode A uses — walk each section against the checklist, fill any gap that is now visible, or record the gap in roadmap *Open questions*. The audit is what makes Mode C an enrichment pass rather than a scattered top-up.

#### What Mode C must not do

- alter the manuscript's main axis: no reordering of sections, no rewriting of definitions or theorem statements, no replacement or deletion of existing expansions (those are Mode B's `Move` and `Cut` verdicts, and stay propose-only);
- add `% expansion:` lines without `[pass: enrichment]` — that pretends the addition is original drafting and pollutes the audit trail;
- run as a final step. Every Mode C run **must be followed by a Mode B audit scoped to the new `[pass: enrichment]` markers**. The state machine above is non-negotiable on this point: a Mode C pass that ships without a Mode B follow-up is incomplete.

The non-repetition rule, the named-content rule, and the density-calibration target apply to Mode C exactly as they do to Mode A — the only thing Mode C changes is the marker hint and the prohibition on touching the existing axis.

### When manuscript and spec disagree (applies in any mode)

- **Formatting**: [`CONTENT_SPEC.md`](CONTENT_SPEC.md) wins. Rewrite the manuscript's phrasing to comply (e.g., `\textbf{...}` → `\emph{...}` in prose, ASCII quotes → TeX quotes, manual cross-reference prefixes → `\cref{}`). The mathematics is unchanged.
- **Mathematical content**: the manuscript wins. If the manuscript proves a theorem a particular way, preserve the method; if the manuscript defines a term in a specific form, preserve that form. Notational differences from §9 of the spec get reconciled to the house convention, with a `caution` note if the reconciliation is non-trivial.
- **Genuine conflicts** (manuscript insists on a rule the spec forbids for editorial reasons, not mathematical ones): ask the user. Record the decision in the chapter's roadmap entry under *Open questions*.

Per-chapter manuscript tracking — who wrote it, when it was received, conversion status, and any user-authored expansion notes — lives in each chapter's entry in [`CONTENT_ROADMAP.md`](CONTENT_ROADMAP.md) under **Manuscript source**.

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
- `tools/` — media-generation scripts plus book-source utilities (`book_style_lint.py`, `book_preamble_smoketest.py`, and vendored helpers).
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
python tools/book_style_lint.py
python tools/book_preamble_smoketest.py
python tools/book_docs_lint.py
```

All four checks (the three above plus the `latexmk` build) run on every push and PR via [`.github/workflows/latex-checks.yml`](.github/workflows/latex-checks.yml). `book_docs_lint.py` scans markdown for stale `tools/<name>.py` command references and broken relative links, so doc-rename drift cannot slip through review unnoticed.

Authority: when repository layout or preamble decisions change, **this file** is authoritative; when writing or typesetting rules change, [`CONTENT_SPEC.md`](CONTENT_SPEC.md) is authoritative.

---

## Media scope note

End-of-section `\subsection*{Exercises}` blocks are for the printed handout only. They are **not** included in slide decks, narration scripts, Manim storyboards, synthesized audio, or rendered video. When planning section media, ignore the exercise block of the source section and build from definitions, theorems, examples, and exposition prose.

---

## Notes

- Local caches, virtual environments, and vendored dependencies live in hidden repo folders such as `.cache/`, `.venv/`, `.deps/`, and `.deps_f5/`.
- The checked-in media exemplar is Section 1.1 *Inverse Functions* (`ch01_inverse_functions`). The Manim storyboard lives at [`inputs/manim_storyboards/ch01_inverse_functions.yml`](inputs/manim_storyboards/ch01_inverse_functions.yml); the frozen slide plan lives at [`inputs/media_plans/ch01_inverse_functions.json`](inputs/media_plans/ch01_inverse_functions.json).
