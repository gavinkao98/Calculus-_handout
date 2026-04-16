from __future__ import annotations

from typing import Any

from manim import Axes, DashedLine, Dot, DOWN, FadeIn, LEFT, Line, RIGHT, Tex, UP, VGroup

from .helpers import make_card, make_title, theme_color


def horizontal_line_test_comparison(scene, scene_spec: dict[str, Any], context: dict[str, Any]) -> None:
    theme = context["theme"]
    scene.clear()

    title = make_title(scene_spec["title"], theme)
    subtitle = make_card(
        Tex(
            r"\parbox{10.5cm}{\centering One side passes the test; the other side fails because one output comes from two inputs.}",
            color=theme_color(theme, "text"),
            font_size=float(theme["typography"]["small_size"]),
        ),
        theme,
    )
    subtitle.next_to(title, DOWN, buff=0.32)

    left_axes = Axes(
        x_range=[-2, 2, 1],
        y_range=[-2, 2, 1],
        x_length=4.3,
        y_length=3.5,
        axis_config={"color": theme_color(theme, "grid")},
    )
    right_axes = Axes(
        x_range=[-2, 2, 1],
        y_range=[-0.5, 3, 1],
        x_length=4.3,
        y_length=3.5,
        axis_config={"color": theme_color(theme, "grid")},
    )
    pair = VGroup(left_axes, right_axes).arrange(RIGHT, buff=1.0)
    pair.next_to(subtitle, DOWN, buff=0.55)

    left_graph = Line(left_axes.c2p(-1.35, -1.35), left_axes.c2p(1.3, 1.3), color=theme_color(theme, "secondary"), stroke_width=5)
    left_line = DashedLine(left_axes.c2p(-1.9, 1.0), left_axes.c2p(1.3, 1.0), color=theme_color(theme, "warning"))
    left_point = Dot(left_axes.c2p(1.0, 1.0), color=theme_color(theme, "accent"))
    left_label = Tex("One hit only", color=theme_color(theme, "accent"), font_size=float(theme["typography"]["small_size"]))
    left_label.next_to(left_axes, DOWN, buff=0.22)

    right_graph = right_axes.plot(lambda x: 1.15 * x * x, x_range=[-1.35, 1.35], color=theme_color(theme, "secondary"))
    right_line = DashedLine(right_axes.c2p(-1.8, 1.25), right_axes.c2p(1.8, 1.25), color=theme_color(theme, "warning"))
    right_points = VGroup(
        Dot(right_axes.c2p(-1.04, 1.25), color=theme_color(theme, "accent")),
        Dot(right_axes.c2p(1.04, 1.25), color=theme_color(theme, "accent")),
    )
    right_label = Tex("Two hits: not invertible", color=theme_color(theme, "warning"), font_size=float(theme["typography"]["small_size"]))
    right_label.next_to(right_axes, DOWN, buff=0.22)

    scene.play(FadeIn(title, shift=0.16 * UP), run_time=0.45)
    scene.play(FadeIn(subtitle, shift=0.12 * UP), run_time=0.45)
    scene.play(FadeIn(pair, shift=0.1 * UP), run_time=0.55)
    scene.play(FadeIn(VGroup(left_graph, left_line, left_point), shift=0.08 * UP), run_time=0.45)
    scene.play(FadeIn(VGroup(right_graph, right_line, right_points), shift=0.08 * UP), run_time=0.45)
    scene.play(FadeIn(VGroup(left_label, right_label), shift=0.06 * UP), run_time=0.3)
    scene.wait(float(theme["transitions"]["section_pause"]))
