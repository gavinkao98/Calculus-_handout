"""Scene template renderers — "Midnight Canvas" design.

Design philosophy
-----------------
Dark background, luminous mathematics, no chrome.  Every pixel is either
mathematical content or negative space that focuses the eye.  Animations
serve a pedagogical purpose: things *write on* when introduced, *transform*
when evolved, *highlight* when important, and *fade* when finished.

Colour semantics
~~~~~~~~~~~~~~~~
- **cyan / secondary**: formal concepts (definitions, propositions)
- **gold / accent**: key results (theorems, important insights)
- **coral / warning**: counterexamples, failures, "watch out"
- **green / success**: verified, correct, QED
- **off-white / primary**: titles and neutral labels
- **light grey / text**: body prose
"""

from __future__ import annotations

from typing import Any

from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LEFT,
    Line,
    MathTex,
    RIGHT,
    Tex,
    TransformMatchingTex,
    UP,
    VGroup,
    Write,
)

from manim_storyboard_workflow import to_mathtex_body, to_tex_text

from .helpers import parbox_tex, theme_color
from .graph_utils import safe_eval_expression
from .layout import SceneLayout


# ═══════════════════════════════════════════════════════════════════════════
# Internal helpers
# ═══════════════════════════════════════════════════════════════════════════

def _ct_color_name(spec: dict[str, Any], ctx: dict[str, Any]) -> str:
    """Accent colour name for the scene's content_type."""
    ct = spec.get("content_type", "definition")
    return ctx["theme"].get("content_type_colors", {}).get(ct, "secondary")


def _ct_label(spec: dict[str, Any]) -> str:
    return spec.get("content_type", "definition").upper()


def _math_text(entry) -> str:
    return entry["text"] if isinstance(entry, dict) else entry


def _math_anim(entry) -> str:
    return entry.get("animation", "write") if isinstance(entry, dict) else "write"


def _make_math(entry, theme, *, max_w: float = 8.0) -> MathTex:
    m = MathTex(
        to_mathtex_body(_math_text(entry)),
        substrings_to_isolate=["="],
        color=theme_color(theme, "math"),
        font_size=float(theme["typography"]["math_size"]),
    )
    if m.width > max_w:
        m.scale_to_fit_width(max_w)
    return m


def _pace(theme: dict[str, Any], band: str = "normal") -> float:
    transitions = theme["transitions"]
    if band == "quick":
        return float(transitions.get("quick_step", 0.35))
    if band == "hero":
        return float(transitions.get("hero_write", 1.6))
    if band == "decay":
        return float(transitions.get("context_decay", 0.25))
    return float(transitions.get("write_speed", 0.8))


def _equals_anchor(mob: MathTex):
    return mob.get_part_by_tex("=")


def _resolve_math_layout(layout_mode: str, math_mobs: list[MathTex]) -> str:
    if layout_mode != "auto":
        return layout_mode
    anchored = sum(1 for mob in math_mobs if _equals_anchor(mob) is not None)
    return "equals_aligned" if anchored >= 2 else "left"


def _arrange_math_stack(math_mobs: list[MathTex], *, buff: float, layout_mode: str) -> VGroup:
    group = VGroup(*math_mobs).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    if _resolve_math_layout(layout_mode, math_mobs) != "equals_aligned":
        return group

    anchored = [(mob, _equals_anchor(mob)) for mob in math_mobs]
    anchored = [(mob, anchor) for mob, anchor in anchored if anchor is not None]
    if len(anchored) < 2:
        return group

    target_x = anchored[0][1].get_center()[0]
    for mob, anchor in anchored[1:]:
        mob.shift((target_x - anchor.get_center()[0]) * RIGHT)
    return group


def _dim_previous(scene, mobjects: list[Any], theme) -> None:
    animations = []
    context_color = theme["colors"].get("context", theme["colors"].get("muted_text"))
    for mob in mobjects:
        if mob is None:
            continue
        animations.append(mob.animate.set_color(context_color).set_opacity(0.55))
    if animations:
        scene.play(*animations, run_time=_pace(theme, "decay"))


def _transform_from_previous(scene, previous_mob: MathTex, mob: MathTex, theme) -> None:
    source = previous_mob.copy().set_color(theme_color(theme, "math")).set_opacity(1.0)
    scene.add(source)
    scene.play(
        TransformMatchingTex(source, mob),
        run_time=_pace(theme, "normal"),
    )
    scene.remove(source)


def _play_math(scene, mob, anim: str, theme, *, previous_mob: MathTex | None = None) -> None:
    speed = _pace(theme, "normal")
    quick = _pace(theme, "quick")
    if anim == "highlight":
        if mob.width > 8.0:
            scene.play(FadeIn(mob, shift=0.1 * UP), run_time=_pace(theme, "hero"))
        else:
            scene.play(Write(mob), run_time=_pace(theme, "hero"))
        # Brief glow: flash the highlight colour, then settle
        mob_copy = mob.copy().set_color(theme_color(theme, "highlight"))
        scene.play(FadeIn(mob_copy, run_time=0.2))
        scene.play(FadeOut(mob_copy, run_time=0.3))
    elif anim == "transform_from_previous" and previous_mob is not None:
        _transform_from_previous(scene, previous_mob, mob, theme)
    elif anim == "fade":
        scene.play(FadeIn(mob, shift=0.1 * UP), run_time=quick)
    else:  # "write"
        if mob.width > 8.0:
            scene.play(FadeIn(mob, shift=0.1 * UP), run_time=speed)
        else:
            scene.play(Write(mob), run_time=speed)


def _title(text: str, theme, *, layout: SceneLayout) -> Tex:
    t = Tex(
        rf"\textbf{{{to_tex_text(text)}}}",
        color=theme_color(theme, "primary"),
        font_size=float(theme["typography"]["title_size"]),
    )
    layout.place_title(t)
    return t


def _thin_rule(width: float, theme, color_name: str = "secondary") -> Line:
    """A slender horizontal rule — the *only* decoration we use."""
    return Line(
        LEFT * width / 2, RIGHT * width / 2,
        color=theme_color(theme, color_name),
        stroke_width=1.5,
        stroke_opacity=0.6,
    )


def _label(text: str, theme, *, color_name: str = "muted_text", size_key: str = "small_size") -> Tex:
    return Tex(
        to_tex_text(text),
        color=theme_color(theme, color_name),
        font_size=float(theme["typography"][size_key]),
    )


# ═══════════════════════════════════════════════════════════════════════════
# 1  TITLE + BULLETS — opening / overview
# ═══════════════════════════════════════════════════════════════════════════

def render_title_bullets(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]

    title = _title(spec["title"], theme, layout=lay)

    bullets = []
    cycle = ["secondary", "accent", "warning"]
    for i, text in enumerate(data["bullets"]):
        dot = Dot(radius=0.06, color=theme_color(theme, cycle[i % len(cycle)]))
        tex = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(text)}", 9.0),
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        row = VGroup(dot, tex).arrange(RIGHT, buff=0.25)
        bullets.append(row)

    group = VGroup(*bullets).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    lay.place_primary(group, title, buff=0.7)

    # Animate
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.wait(0.2)
    for b in bullets:
        scene.play(FadeIn(b, shift=0.12 * RIGHT), run_time=0.45)
    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 2  DEFINITION / THEOREM — the formal statement
# ═══════════════════════════════════════════════════════════════════════════

def render_definition_math(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]
    color = _ct_color_name(spec, ctx)

    # Title
    title = _title(spec["title"], theme, layout=lay)

    # Subtle type label to the right
    lbl = _label(_ct_label(spec), theme, color_name=color, size_key="section_label_size")
    lbl.next_to(title, RIGHT, buff=0.4)
    lbl.align_to(title, DOWN)

    # Thin horizontal rule
    rule = _thin_rule(lay.usable_width() * 0.85, theme, color)
    rule.next_to(title, DOWN, buff=0.35)

    # Statement
    stmt = Tex(
        parbox_tex(rf"\raggedright {to_tex_text(data['statement'])}", 10.0),
        color=theme_color(theme, "text"),
        font_size=float(theme["typography"]["body_size"]),
    )
    stmt.next_to(rule, DOWN, buff=0.45)
    stmt.align_to([lay.left_edge + 0.3, 0, 0], LEFT)

    # Math lines — centred, generous spacing
    maths = [_make_math(e, theme) for e in data["math_lines"]]
    if maths:
        mg = VGroup(*maths).arrange(DOWN, buff=0.45)
        mg.next_to(stmt, DOWN, buff=0.55)

    # Supporting notes (dim)
    support = data.get("supporting_bullets", [])
    support_group = None
    if support:
        items = []
        for s in support:
            t = Tex(
                parbox_tex(rf"\raggedright {to_tex_text(s)}", 9.0),
                color=theme_color(theme, "muted_text"),
                font_size=float(theme["typography"]["small_size"]),
            )
            items.append(t)
        support_group = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ref = mg if maths else stmt
        support_group.next_to(ref, DOWN, buff=0.5)
        support_group.align_to(stmt, LEFT)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(FadeIn(lbl, shift=0.08 * LEFT), run_time=0.3)
    scene.play(Create(rule), run_time=0.35)
    scene.play(FadeIn(stmt, shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(0.25)

    for i, m in enumerate(maths):
        previous_math = maths[i - 1] if i > 0 else None
        _play_math(scene, m, _math_anim(data["math_lines"][i]), theme, previous_mob=previous_math)
        scene.wait(0.15)

    if support_group:
        scene.play(FadeIn(support_group, shift=0.08 * UP), run_time=0.5)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 3  EXAMPLE WALKTHROUGH — step-by-step with math workspace
# ═══════════════════════════════════════════════════════════════════════════

def render_example_walkthrough(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]
    color = _ct_color_name(spec, ctx)
    quick = _pace(theme, "quick")

    title = _title(spec["title"], theme, layout=lay)
    lbl = _label("EXAMPLE", theme, color_name=color, size_key="section_label_size")
    lbl.next_to(title, RIGHT, buff=0.4)
    lbl.align_to(title, DOWN)

    rule = _thin_rule(lay.usable_width() * 0.85, theme, color)
    rule.next_to(title, DOWN, buff=0.35)

    steps = data["steps"]
    math_lines = data.get("math_lines", [])

    # Build step text
    step_mobs = []
    for i, s in enumerate(steps, 1):
        num = Tex(
            rf"\textbf{{{i}.}}",
            color=theme_color(theme, color),
            font_size=float(theme["typography"]["body_size"]),
        )
        txt = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(s)}", 5.6),
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        row = VGroup(num, txt).arrange(RIGHT, buff=0.2)
        step_mobs.append(row)

    steps_group = VGroup(*step_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    steps_group.next_to(rule, DOWN, buff=0.5)
    steps_group.align_to([lay.left_edge + 0.3, 0, 0], LEFT)

    # Math on the right
    math_mobs = [_make_math(e, theme, max_w=5.0) for e in math_lines]
    if math_mobs:
        mw = _arrange_math_stack(math_mobs, buff=0.35, layout_mode=data.get("math_layout", "auto"))
        mw.next_to(steps_group, RIGHT, buff=0.8)
        mw.align_to(steps_group, UP)

    # Takeaway — a single coloured line at the bottom
    takeaway = Tex(
        parbox_tex(rf"\raggedright {to_tex_text(data['takeaway'])}", 9.0),
        color=theme_color(theme, "accent"),
        font_size=float(theme["typography"]["small_size"]),
    )
    bottom_ref = steps_group if not math_mobs else VGroup(steps_group, mw)
    takeaway.next_to(bottom_ref, DOWN, buff=0.5)
    takeaway.align_to([lay.left_edge + 0.3, 0, 0], LEFT)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(FadeIn(lbl, shift=0.08 * LEFT), run_time=quick)
    scene.play(Create(rule), run_time=quick)

    decay_previous = data.get("decay_previous", True)
    active_step = None
    active_math = None
    for i, row in enumerate(step_mobs):
        current_anim = _math_anim(math_lines[i]) if i < len(math_mobs) else None
        if decay_previous:
            to_dim = [active_step]
            if not (current_anim == "transform_from_previous" and active_math is not None):
                to_dim.append(active_math)
            _dim_previous(scene, to_dim, theme)
        scene.play(FadeIn(row, shift=0.1 * RIGHT), run_time=quick)
        previous_math = active_math
        active_step = row
        if i < len(math_mobs):
            _play_math(
                scene,
                math_mobs[i],
                _math_anim(math_lines[i]),
                theme,
                previous_mob=previous_math,
            )
            active_math = math_mobs[i]
        scene.wait(0.1)

    # Remaining math
    for j in range(len(step_mobs), len(math_mobs)):
        previous_math = active_math
        current_anim = _math_anim(math_lines[j])
        if decay_previous:
            to_dim = []
            if not (current_anim == "transform_from_previous" and active_math is not None):
                to_dim.append(active_math)
            _dim_previous(scene, to_dim, theme)
        _play_math(
            scene,
            math_mobs[j],
            _math_anim(math_lines[j]),
            theme,
            previous_mob=previous_math,
        )
        active_math = math_mobs[j]

    scene.play(FadeIn(takeaway, shift=0.08 * UP), run_time=0.4)
    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 4  GRAPH FOCUS — full-width, curves trace out
# ═══════════════════════════════════════════════════════════════════════════

_LABEL_SIDE_MAP = {"up": UP, "down": DOWN, "left": LEFT, "right": RIGHT}

# Manim frame boundary (default 16:9 camera).
_FRAME_BOTTOM = -3.8


def _resolve_label_side(side_str: str | None, default) -> Any:
    """Convert an optional string like ``"up"`` to a Manim direction vector."""
    if side_str is None:
        return default
    return _LABEL_SIDE_MAP.get(side_str.lower(), default)


def _label_at_curve_edge(
    label: Mobject, graph: Mobject, axes, x_val: float | None,
    side, buff: float,
) -> None:
    """Position *label* near a specific x-value on the curve.

    If *x_val* is given, the label is placed next to the point on the
    graph closest to that x-coordinate.  Otherwise it falls back to the
    bounding-box edge determined by *side*.
    """
    if x_val is not None:
        try:
            pt = graph.point_from_proportion(
                axes.x_axis.point_to_proportion(axes.c2p(x_val, 0))
            )
        except Exception:
            pt = None
        if pt is not None:
            label.next_to(pt, side, buff=buff)
            return
    label.next_to(graph, side, buff=buff)


def _clamp_to_frame(mob: Mobject) -> None:
    """Shift *mob* up if it extends below the visible frame."""
    bottom = mob.get_bottom()[1]
    if bottom < _FRAME_BOTTOM:
        mob.shift(((_FRAME_BOTTOM - bottom) + 0.05) * UP)


def render_graph_focus(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]

    title = _title(spec["title"], theme, layout=lay)

    ac = data["axes"]
    axes = Axes(
        x_range=ac["x_range"],
        y_range=ac["y_range"],
        x_length=float(ac.get("x_length", 8.5)),
        y_length=float(ac.get("y_length", 4.8)),
        axis_config={
            "color": theme_color(theme, "grid"),
            "stroke_width": 1.5,
        },
        tips=bool(ac.get("tips", True)),
    )
    axes.next_to(title, DOWN, buff=0.55)

    # Plots
    plot_mobs = []
    label_mobs = []
    for p in data["plots"]:
        c = p.get("color", theme_color(theme, "secondary"))
        if p["kind"] == "function":
            xr = p.get("x_range", ac["x_range"])
            # Dense sampling so curves are accurate even where the
            # derivative is large (e.g. cube root near its inflection).
            # Smoothing is kept ON — with 4000 points the Bézier pass
            # polishes the result instead of distorting it.
            step = (xr[1] - xr[0]) / 4000
            g = axes.plot(
                lambda x, expr=p["expression"]: safe_eval_expression(expr, x),
                x_range=[xr[0], xr[1], step],
                color=c, stroke_width=3,
            )
            plot_mobs.append(("function", g))
            if p.get("label"):
                lb = Tex(p["label"], color=c, font_size=float(theme["typography"]["small_size"]))
                side = _resolve_label_side(p.get("label_side"), UP)
                label_x = p.get("label_x")
                _label_at_curve_edge(lb, g, axes, label_x, side, buff=0.15)
                label_mobs.append(lb)
        elif p["kind"] == "line":
            cls = DashedLine if p.get("dashed") else Line
            ln = cls(axes.c2p(*p["start"]), axes.c2p(*p["end"]),
                     color=c, stroke_width=3)
            plot_mobs.append(("line", ln))
            if p.get("label"):
                lb = Tex(p["label"], color=c, font_size=float(theme["typography"]["small_size"]))
                side = _resolve_label_side(p.get("label_side"), RIGHT)
                lb.next_to(ln, side, buff=0.12)
                label_mobs.append(lb)
        else:
            d = Dot(axes.c2p(*p["point"]), color=c, radius=float(p.get("radius", 0.08)))
            plot_mobs.append(("point", d))
            if p.get("label"):
                lb = Tex(p["label"], color=c, font_size=float(theme["typography"]["small_size"]))
                side = _resolve_label_side(p.get("label_side"), UP)
                lb.next_to(d, side, buff=0.1)
                label_mobs.append(lb)

    # Clamp all labels into the visible frame.
    for lb in label_mobs:
        _clamp_to_frame(lb)

    # Annotations as floating text below axes
    ann_mobs = []
    for a in data["annotations"]:
        t = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(a['text'])}", 6.5),
            color=theme_color(theme, "muted_text"),
            font_size=float(theme["typography"]["caption_size"]),
        )
        ann_mobs.append(t)
    if ann_mobs:
        ann_group = VGroup(*ann_mobs).arrange(RIGHT, buff=0.6)
        ann_group.next_to(axes, DOWN, buff=0.35)
        _clamp_to_frame(ann_group)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(Create(axes), run_time=0.8)

    for kind, mob in plot_mobs:
        if kind == "function":
            scene.play(Create(mob), run_time=0.9)
        elif kind == "point":
            scene.play(GrowFromCenter(mob), run_time=0.3)
        else:
            scene.play(FadeIn(mob, shift=0.06 * UP), run_time=0.35)

    if label_mobs:
        scene.play(*[FadeIn(lb, shift=0.05 * UP) for lb in label_mobs], run_time=0.35)

    for am in ann_mobs:
        scene.play(FadeIn(am, shift=0.08 * UP), run_time=0.4)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 5  PROCEDURE STEPS — numbered flow
# ═══════════════════════════════════════════════════════════════════════════

def render_procedure_steps(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]
    color = _ct_color_name(spec, ctx)
    quick = _pace(theme, "quick")

    title = _title(spec["title"], theme, layout=lay)
    rule = _thin_rule(lay.usable_width() * 0.85, theme, color)
    rule.next_to(title, DOWN, buff=0.35)

    # Steps: large coloured number + text
    step_mobs = []
    for i, s in enumerate(data["steps"], 1):
        num = Tex(
            rf"\textbf{{{i}}}",
            color=theme_color(theme, color),
            font_size=float(theme["typography"]["title_size"]),
        )
        txt = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(s)}", 8.5),
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        row = VGroup(num, txt).arrange(RIGHT, buff=0.3)
        step_mobs.append(row)

    step_group = VGroup(*step_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    step_group.next_to(rule, DOWN, buff=0.5)
    step_group.align_to([lay.left_edge + 0.5, 0, 0], LEFT)

    # Equations below steps
    eqs = data["worked_equations"]
    math_mobs = [_make_math(e, theme, max_w=8.0) for e in eqs]
    eq_group = None
    if math_mobs:
        eq_group = _arrange_math_stack(math_mobs, buff=0.4, layout_mode=data.get("math_layout", "auto"))
        eq_group.next_to(step_group, DOWN, buff=0.55)
        eq_group.align_to(step_group, LEFT)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(Create(rule), run_time=quick)

    for row in step_mobs:
        scene.play(FadeIn(row, shift=0.1 * RIGHT), run_time=quick)

    if math_mobs:
        scene.wait(0.2)
        for j, m in enumerate(math_mobs):
            previous_math = math_mobs[j - 1] if j > 0 else None
            _play_math(scene, m, _math_anim(eqs[j]), theme, previous_mob=previous_math)
            scene.wait(0.1)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 6  RECAP — key points + identities
# ═══════════════════════════════════════════════════════════════════════════

def render_recap_cards(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]

    title = _title(spec["title"], theme, layout=lay)
    rule = _thin_rule(lay.usable_width() * 0.85, theme, "accent")
    rule.next_to(title, DOWN, buff=0.35)

    # Points — each as a coloured bullet
    cycle = ["secondary", "accent", "success"]
    points = []
    for i, p in enumerate(data["points"]):
        dot = Dot(radius=0.05, color=theme_color(theme, cycle[i % len(cycle)]))
        txt = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(p)}", 9.0),
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        row = VGroup(dot, txt).arrange(RIGHT, buff=0.25)
        points.append(row)
    pts_group = VGroup(*points).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    pts_group.next_to(rule, DOWN, buff=0.5)
    pts_group.align_to([lay.left_edge + 0.3, 0, 0], LEFT)

    # Identities
    ids_ = data.get("identities", [])
    math_mobs = [_make_math(e, theme) for e in ids_]
    id_group = None
    if math_mobs:
        id_group = VGroup(*math_mobs).arrange(DOWN, buff=0.4)
        id_group.next_to(pts_group, DOWN, buff=0.5)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(Create(rule), run_time=0.3)

    for row in points:
        scene.play(FadeIn(row, shift=0.1 * RIGHT), run_time=0.4)

    if math_mobs:
        scene.wait(0.2)
        for j, m in enumerate(math_mobs):
            _play_math(scene, m, _math_anim(ids_[j]), theme)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 7  SECTION TRANSITION — cinematic chapter card
# ═══════════════════════════════════════════════════════════════════════════

def render_section_transition(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    data = spec["data"]

    # Large centred title
    title = Tex(
        rf"\textbf{{{to_tex_text(spec['title'])}}}",
        color=theme_color(theme, "primary"),
        font_size=float(theme["typography"]["title_size"]) + 6,
    )
    title.move_to([0, 0.6, 0])

    # Short decorative rule
    rule = _thin_rule(3.5, theme, "accent")
    rule.next_to(title, DOWN, buff=0.3)

    sub = data.get("subtitle")
    sub_mob = None
    if sub:
        sub_mob = Tex(
            to_tex_text(sub),
            color=theme_color(theme, "muted_text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        sub_mob.next_to(rule, DOWN, buff=0.35)

    upcoming = data.get("upcoming", [])
    up_mobs = []
    if upcoming:
        for u in upcoming:
            t = Tex(
                rf"\textbullet\ {to_tex_text(u)}",
                color=theme_color(theme, "text"),
                font_size=float(theme["typography"]["small_size"]),
            )
            up_mobs.append(t)
        ug = VGroup(*up_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        ref = sub_mob if sub_mob else rule
        ug.next_to(ref, DOWN, buff=0.5)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.12 * DOWN, scale=0.94), run_time=0.6)
    scene.play(Create(rule), run_time=0.3)
    if sub_mob:
        scene.play(FadeIn(sub_mob, shift=0.08 * UP), run_time=0.4)
    for u in up_mobs:
        scene.play(FadeIn(u, shift=0.1 * RIGHT), run_time=0.35)
    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 8  THEOREM + PROOF
# ═══════════════════════════════════════════════════════════════════════════

def render_theorem_proof(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]

    title = _title(spec["title"], theme, layout=lay)
    lbl = _label("THEOREM", theme, color_name="accent", size_key="section_label_size")
    lbl.next_to(title, RIGHT, buff=0.4)
    lbl.align_to(title, DOWN)

    rule = _thin_rule(lay.usable_width() * 0.85, theme, "accent")
    rule.next_to(title, DOWN, buff=0.35)

    # Theorem statement — italic, in accent-adjacent colour
    stmt = Tex(
        parbox_tex(rf"\raggedright \textit{{{to_tex_text(data['theorem_statement'])}}}", 10.0),
        color=theme_color(theme, "text"),
        font_size=float(theme["typography"]["body_size"]),
    )
    stmt.next_to(rule, DOWN, buff=0.45)
    stmt.align_to([lay.left_edge + 0.3, 0, 0], LEFT)

    # Proof label
    proof_lbl = Tex(
        r"\textit{Proof.}",
        color=theme_color(theme, "muted_text"),
        font_size=float(theme["typography"]["body_size"]),
    )
    proof_lbl.next_to(stmt, DOWN, buff=0.5)
    proof_lbl.align_to(stmt, LEFT)

    # Proof steps
    p_mobs = []
    for s in data["proof_steps"]:
        t = Tex(
            parbox_tex(rf"\raggedright {to_tex_text(s)}", 9.5),
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        )
        p_mobs.append(t)
    pg = VGroup(*p_mobs).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    pg.next_to(proof_lbl, DOWN, buff=0.3)
    pg.align_to(proof_lbl, LEFT)

    # QED
    qed = None
    if data.get("qed", True):
        qed = Tex(r"$\blacksquare$", color=theme_color(theme, "success"),
                   font_size=float(theme["typography"]["body_size"]))
        qed.next_to(pg, DOWN, buff=0.25)
        qed.align_to(pg, RIGHT)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(FadeIn(lbl, shift=0.08 * LEFT), run_time=0.3)
    scene.play(Create(rule), run_time=0.3)
    scene.play(FadeIn(stmt, shift=0.1 * RIGHT), run_time=0.5)
    scene.wait(0.4)
    scene.play(FadeIn(proof_lbl, shift=0.06 * RIGHT), run_time=0.3)

    for pm in p_mobs:
        scene.play(FadeIn(pm, shift=0.08 * RIGHT), run_time=0.45)

    if qed:
        scene.play(FadeIn(qed), run_time=0.25)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# 9  COMPARISON — side-by-side
# ═══════════════════════════════════════════════════════════════════════════

def render_comparison(scene, spec: dict[str, Any], ctx: dict[str, Any]) -> None:
    theme = ctx["theme"]
    lay = SceneLayout(theme)
    data = spec["data"]

    title = _title(spec["title"], theme, layout=lay)
    rule = _thin_rule(lay.usable_width() * 0.85, theme, "secondary")
    rule.next_to(title, DOWN, buff=0.35)

    def _col(side_data):
        c = side_data.get("color", "secondary")
        # Column header — just coloured text
        header = Tex(
            rf"\textbf{{{to_tex_text(side_data['label'])}}}",
            color=theme_color(theme, c),
            font_size=float(theme["typography"]["body_size"]) + 2,
        )
        items = []
        for it in side_data["items"]:
            t = Tex(
                parbox_tex(rf"\raggedright {to_tex_text(it)}", 4.5),
                color=theme_color(theme, "text"),
                font_size=float(theme["typography"]["body_size"]) - 2,
            )
            items.append(t)
        col_items = VGroup(header, *items)

        math_mob = None
        if side_data.get("math"):
            math_mob = MathTex(
                to_mathtex_body(side_data["math"]),
                color=theme_color(theme, "math"),
                font_size=float(theme["typography"]["math_size"]) - 2,
            )
            if math_mob.width > 4.5:
                math_mob.scale_to_fit_width(4.5)
            col_items.add(math_mob)

        col_items.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        return col_items, c

    left_col, lc = _col(data["left"])
    right_col, rc = _col(data["right"])

    # Thin vertical divider
    divider = Line(UP * 2.5, DOWN * 2.5,
                   color=theme_color(theme, "grid"), stroke_width=1, stroke_opacity=0.5)

    pair = VGroup(left_col, divider, right_col).arrange(RIGHT, buff=0.8)
    pair.next_to(rule, DOWN, buff=0.55)

    # ── Animate ──
    scene.play(FadeIn(title, shift=0.15 * DOWN), run_time=0.5)
    scene.play(Create(rule), run_time=0.3)

    # Left column builds
    for mob in left_col:
        scene.play(FadeIn(mob, shift=0.1 * RIGHT), run_time=0.4)

    scene.play(FadeIn(divider), run_time=0.2)

    # Right column builds
    for mob in right_col:
        scene.play(FadeIn(mob, shift=0.1 * RIGHT), run_time=0.4)

    scene.wait(float(theme["transitions"]["section_pause"]))


# ═══════════════════════════════════════════════════════════════════════════
# Expression evaluator (graph_focus)
# ═══════════════════════════════════════════════════════════════════════════

