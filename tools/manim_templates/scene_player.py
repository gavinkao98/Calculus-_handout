from __future__ import annotations

from typing import Any

from manim import Scene

from .registry import render_scene_template


class StoryboardTemplateScene(Scene):
    scene_spec: dict[str, Any] | None = None
    render_context: dict[str, Any] | None = None

    def construct(self) -> None:
        if self.scene_spec is None or self.render_context is None:
            raise RuntimeError("StoryboardTemplateScene was not configured with a scene specification.")
        render_scene_template(self, self.scene_spec, self.render_context)
