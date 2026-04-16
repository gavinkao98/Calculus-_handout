from __future__ import annotations

import math
from typing import Any

from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    DrawBorderThenFill,
    FadeIn,
    LEFT,
    Line,
    RIGHT,
    Tex,
    UP,
    VGroup,
)

from .helpers import (
    fade_in_group,
    make_bullet_list,
    make_card,
    make_chip,
    make_math_stack,
    make_title,
    theme_color,
)


def render_title_bullets(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    title = make_title(scene_spec["title"], theme)
    bullets = make_bullet_list(scene_spec["data"]["bullets"], theme, width_cm=9.6)
    card = make_card(bullets, theme)
    card.next_to(title, DOWN, aligned_edge=LEFT, buff=0.55)
    accent = make_chip("Core Idea", theme, color_name="secondary")
    accent.next_to(card, DOWN, aligned_edge=LEFT, buff=0.35)

    scene.play(FadeIn(title, shift=0.2 * DOWN), run_time=0.6)
    scene.play(DrawBorderThenFill(card[0]), run_time=0.5)
    fade_in_group(scene, list(card[1]), lag_ratio=float(theme["transitions"]["bullet_lag"]), shift=0.12 * RIGHT)
    scene.play(FadeIn(accent, shift=0.1 * UP), run_time=0.35)
    scene.wait(float(theme["transitions"]["section_pause"]))


def render_definition_math(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    data = scene_spec["data"]
    title = make_title(scene_spec["title"], theme)
    statement = make_card(
        Tex(
            rf"\parbox{{6.4cm}}{{\raggedright \textbf{{Statement.}} {data['statement']}}}",
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["body_size"]),
        ),
        theme,
    )
    statement.next_to(title, DOWN, aligned_edge=LEFT, buff=0.5)

    math_stack = make_math_stack(data["math_lines"], theme)
    math_card = make_card(math_stack, theme)
    math_card.next_to(statement, RIGHT, buff=0.55)
    math_card.align_to(statement, UP)

    supporting = data.get("supporting_bullets", [])
    note_group = None
    if supporting:
        note_group = make_card(make_bullet_list(supporting, theme, width_cm=6.0), theme)
        note_group.next_to(statement, DOWN, aligned_edge=LEFT, buff=0.35)

    scene.play(FadeIn(title, shift=0.18 * DOWN), run_time=0.55)
    scene.play(DrawBorderThenFill(statement[0]), FadeIn(statement[1], shift=0.12 * RIGHT), run_time=0.65)
    scene.play(DrawBorderThenFill(math_card[0]), FadeIn(math_card[1], shift=0.12 * UP), run_time=0.65)
    if note_group is not None:
        scene.play(DrawBorderThenFill(note_group[0]), FadeIn(note_group[1], shift=0.1 * UP), run_time=0.45)
    scene.wait(float(theme["transitions"]["section_pause"]))


def render_example_walkthrough(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    data = scene_spec["data"]
    title = make_title(scene_spec["title"], theme)
    steps = make_card(make_bullet_list(data["steps"], theme, width_cm=6.5), theme)
    steps.next_to(title, DOWN, aligned_edge=LEFT, buff=0.5)

    math_lines = data.get("math_lines", [])
    math_card = None
    if math_lines:
        math_card = make_card(make_math_stack(math_lines, theme, max_width=4.7), theme)
        math_card.next_to(steps, RIGHT, buff=0.55)
        math_card.align_to(steps, UP)

    takeaway = make_chip(data["takeaway"], theme, color_name="accent", width_cm=5.2)
    takeaway.next_to(steps, DOWN, aligned_edge=LEFT, buff=0.35)

    scene.play(FadeIn(title, shift=0.16 * DOWN), run_time=0.55)
    scene.play(DrawBorderThenFill(steps[0]), run_time=0.45)
    fade_in_group(scene, list(steps[1]), lag_ratio=float(theme["transitions"]["bullet_lag"]), shift=0.1 * RIGHT)
    if math_card is not None:
        scene.play(DrawBorderThenFill(math_card[0]), FadeIn(math_card[1], shift=0.1 * UP), run_time=0.55)
    scene.play(FadeIn(takeaway, shift=0.08 * UP), run_time=0.3)
    scene.wait(float(theme["transitions"]["section_pause"]))


def render_graph_focus(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    data = scene_spec["data"]
    title = make_title(scene_spec["title"], theme)

    axes_config = data["axes"]
    axes = Axes(
        x_range=axes_config["x_range"],
        y_range=axes_config["y_range"],
        x_length=float(axes_config["x_length"]),
        y_length=float(axes_config["y_length"]),
        axis_config={"color": theme_color(theme, "grid")},
        tips=bool(axes_config.get("tips", True)),
    )
    axes.next_to(title, DOWN, aligned_edge=LEFT, buff=0.55)
    axes.shift(0.15 * RIGHT)

    plot_group = VGroup()
    label_group = VGroup()
    for plot in data["plots"]:
        color = plot.get("color", theme_color(theme, "secondary"))
        if plot["kind"] == "function":
            x_range = plot.get("x_range", axes_config["x_range"])
            graph = axes.plot(
                lambda x, expr=plot["expression"]: safe_eval_expression(expr, x),
                x_range=x_range,
                color=color,
            )
            plot_group.add(graph)
            if plot.get("label"):
                label = Tex(plot["label"], color=color, font_size=float(theme["typography"]["small_size"]))
                label.next_to(graph, UP, buff=0.15)
                label_group.add(label)
        elif plot["kind"] == "line":
            line_cls = DashedLine if plot.get("dashed") else Line
            line = line_cls(
                axes.c2p(*plot["start"]),
                axes.c2p(*plot["end"]),
                color=color,
                stroke_width=4,
            )
            plot_group.add(line)
            if plot.get("label"):
                label = Tex(plot["label"], color=color, font_size=float(theme["typography"]["small_size"]))
                label.next_to(line, RIGHT, buff=0.12)
                label_group.add(label)
        else:
            dot = Dot(axes.c2p(*plot["point"]), color=color, radius=float(plot.get("radius", 0.07)))
            plot_group.add(dot)
            if plot.get("label"):
                label = Tex(plot["label"], color=color, font_size=float(theme["typography"]["small_size"]))
                label.next_to(dot, UP, buff=0.1)
                label_group.add(label)

    if len(plot_group) == 0:
        placeholder = make_card(
            Tex(
                rf"\parbox{{5.6cm}}{{\centering Add `plots` data or a `hook` for this scene.}}",
                color=theme_color(theme, "muted_text"),
                font_size=float(theme["typography"]["body_size"]),
            ),
            theme,
        )
        placeholder.move_to(axes.get_center())
        plot_group.add(placeholder)

    annotations = [entry["text"] for entry in data["annotations"]]
    annotation_card = make_card(make_bullet_list(annotations, theme, width_cm=4.8), theme)
    annotation_card.next_to(axes, RIGHT, buff=0.65)
    annotation_card.align_to(axes, UP)

    scene.play(FadeIn(title, shift=0.16 * DOWN), run_time=0.55)
    scene.play(Create(axes), run_time=0.8)
    scene.play(FadeIn(plot_group, shift=0.08 * UP), run_time=0.7)
    if len(label_group) > 0:
        scene.play(FadeIn(label_group, shift=0.05 * UP), run_time=0.35)
    scene.play(DrawBorderThenFill(annotation_card[0]), FadeIn(annotation_card[1], shift=0.08 * RIGHT), run_time=0.55)
    scene.wait(float(theme["transitions"]["section_pause"]))


def render_procedure_steps(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    data = scene_spec["data"]
    title = make_title(scene_spec["title"], theme)
    steps = make_card(make_bullet_list(data["steps"], theme, width_cm=6.4, numbered=True), theme)
    steps.next_to(title, DOWN, aligned_edge=LEFT, buff=0.52)

    equations = make_card(make_math_stack(data["worked_equations"], theme, max_width=4.8), theme)
    equations.next_to(steps, RIGHT, buff=0.58)
    equations.align_to(steps, UP)

    scene.play(FadeIn(title, shift=0.16 * DOWN), run_time=0.55)
    scene.play(DrawBorderThenFill(steps[0]), run_time=0.4)
    fade_in_group(scene, list(steps[1]), lag_ratio=float(theme["transitions"]["bullet_lag"]), shift=0.12 * RIGHT)
    scene.play(DrawBorderThenFill(equations[0]), FadeIn(equations[1], shift=0.1 * UP), run_time=0.55)
    scene.wait(float(theme["transitions"]["section_pause"]))


def render_recap_cards(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    data = scene_spec["data"]
    title = make_title(scene_spec["title"], theme)
    points = make_card(make_bullet_list(data["points"], theme, width_cm=5.9), theme)
    points.next_to(title, DOWN, aligned_edge=LEFT, buff=0.52)

    identities = make_card(make_math_stack(data["identities"], theme, max_width=5.0), theme)
    identities.next_to(points, RIGHT, buff=0.6)
    identities.align_to(points, UP)

    close = make_chip("Verify by Composition", theme, color_name="secondary", width_cm=4.8)
    close.next_to(points, DOWN, aligned_edge=LEFT, buff=0.35)

    scene.play(FadeIn(title, shift=0.16 * DOWN), run_time=0.55)
    scene.play(DrawBorderThenFill(points[0]), run_time=0.45)
    fade_in_group(scene, list(points[1]), lag_ratio=float(theme["transitions"]["bullet_lag"]), shift=0.12 * RIGHT)
    scene.play(DrawBorderThenFill(identities[0]), FadeIn(identities[1], shift=0.1 * UP), run_time=0.55)
    scene.play(FadeIn(close, shift=0.08 * UP), run_time=0.3)
    scene.wait(float(theme["transitions"]["section_pause"]))


def safe_eval_expression(expression: str, x: float) -> float:
    namespace = {
        "x": x,
        "math": math,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "sqrt": math.sqrt,
        "exp": math.exp,
        "log": math.log,
        "pi": math.pi,
        "e": math.e,
        "abs": abs,
    }
    return float(eval(expression, {"__builtins__": {}}, namespace))
