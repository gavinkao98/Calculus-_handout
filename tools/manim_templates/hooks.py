"""Compatibility re-exports for legacy hook paths.

New hooks should live under ``tools/manim_hooks/`` so they can be grouped by
chapter or topic without bloating the template package itself.
"""

from __future__ import annotations

from manim_hooks.ch01_inverse_functions import horizontal_line_test_comparison

__all__ = ["horizontal_line_test_comparison"]
