from __future__ import annotations

import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

from media_paths import (
    DEFAULT_DECK_ID,
    deck_json_path,
    manim_render_manifest_path,
    manim_storyboard_path,
    manim_tts_deck_path,
)
from runtime_bootstrap import REPO_ROOT, ensure_directory, require_path
from simple_yaml import dump_yaml, load_yaml_path
from slide_script_workflow import final_script_path, load_slide_scripts


TEMPLATE_NAMES = {
    "title_bullets",
    "definition_math",
    "example_walkthrough",
    "graph_focus",
    "procedure_steps",
    "recap_cards",
}
SLIDE_TYPE_TO_TEMPLATE = {
    "motivation": "title_bullets",
    "overview": "title_bullets",
    "definition": "definition_math",
    "theorem": "definition_math",
    "example": "example_walkthrough",
    "warning": "example_walkthrough",
    "figure": "graph_focus",
    "procedure": "procedure_steps",
    "recap": "recap_cards",
}
DEFAULT_THEME = {
    "name": "sandstone",
    "colors": {
        "background": "#F7F4EA",
        "surface": "#FFFDF8",
        "primary": "#7C4D2F",
        "secondary": "#22577A",
        "accent": "#2F855A",
        "text": "#24313F",
        "muted_text": "#52606D",
        "math": "#1D4ED8",
        "warning": "#C2410C",
        "grid": "#D9E2EC",
    },
    "typography": {
        "title_size": 40,
        "body_size": 28,
        "small_size": 22,
        "math_size": 34,
    },
    "layout": {
        "top_y": 3.05,
        "side_margin": 0.8,
        "content_width": 11.4,
    },
    "transitions": {
        "element_fade": 0.35,
        "bullet_lag": 0.2,
        "section_pause": 0.45,
    },
}
DEFAULT_VIDEO = {
    "aspect_ratio": "16:9",
    "pixel_width": 1920,
    "pixel_height": 1080,
    "frame_rate": 30,
    "preview_scale": 0.5,
}
DEFAULT_TIMING = {
    "lead_in_seconds": 0.15,
    "hold_after_seconds": 0.45,
    "minimum_duration_seconds": 4.0,
}
DEFAULT_BRIDGE_RENDER_HINTS = {
    "tikz_scale_mode": "none",
    "max_width": r"\textwidth",
    "max_height_ratio": 0.58,
    "allow_frame_breaks": False,
}
INLINE_MATH_RE = re.compile(r"\\\((.*?)\\\)")
DISPLAY_MATH_WRAPPER_RE = re.compile(r"^\\\[(?P<body>.*)\\\]$", re.DOTALL)


def resolve_storyboard_path(deck_id: str | None = None, storyboard_path: Path | None = None) -> Path:
    if storyboard_path is not None:
        return storyboard_path.resolve()
    return manim_storyboard_path(REPO_ROOT, deck_id or DEFAULT_DECK_ID).resolve()


def load_storyboard(path: Path) -> dict[str, Any]:
    raw = load_yaml_path(require_path(path.resolve(), "Manim storyboard"))
    storyboard = normalize_storyboard(raw, path)
    validate_hook_paths(storyboard)
    return storyboard


def normalize_storyboard(storyboard: Any, source_path: Path | None = None) -> dict[str, Any]:
    label = f"storyboard {source_path}" if source_path else "storyboard"
    if not isinstance(storyboard, dict):
        raise ValueError(f"{label} must be a mapping.")

    normalized = {
        "deck_id": require_text(storyboard.get("deck_id"), f"{label}.deck_id"),
        "language": require_text(storyboard.get("language"), f"{label}.language"),
        "theme": normalize_theme(storyboard.get("theme"), f"{label}.theme"),
        "video": normalize_video(storyboard.get("video"), f"{label}.video"),
    }

    scenes = storyboard.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        raise ValueError(f"{label}.scenes must be a non-empty array.")

    seen_scene_ids: set[str] = set()
    normalized_scenes: list[dict[str, Any]] = []
    for index, raw_scene in enumerate(scenes, start=1):
        if not isinstance(raw_scene, dict):
            raise ValueError(f"{label}.scenes[{index}] must be a mapping.")
        scene_id = require_text(raw_scene.get("scene_id"), f"{label}.scenes[{index}].scene_id")
        if scene_id in seen_scene_ids:
            raise ValueError(f"Duplicate scene_id '{scene_id}' in {label}.")
        seen_scene_ids.add(scene_id)

        template = require_text(raw_scene.get("template"), f"{label}.scenes[{index}].template")
        if template not in TEMPLATE_NAMES:
            raise ValueError(
                f"Unsupported template '{template}' in {label}.scenes[{index}]. "
                f"Allowed values: {sorted(TEMPLATE_NAMES)}"
            )

        normalized_scene = {
            "scene_number": index,
            "scene_id": scene_id,
            "template": template,
            "title": require_text(raw_scene.get("title"), f"{label}.scenes[{index}].title"),
            "voiceover": require_text(raw_scene.get("voiceover"), f"{label}.scenes[{index}].voiceover"),
            "data": normalize_scene_data(template, raw_scene.get("data"), f"{label}.scenes[{index}].data"),
            "timing": normalize_timing(raw_scene.get("timing"), f"{label}.scenes[{index}].timing"),
            "disabled": require_optional_bool(raw_scene.get("disabled"), f"{label}.scenes[{index}].disabled", False),
        }
        hook = raw_scene.get("hook")
        if hook is not None:
            normalized_scene["hook"] = require_text(hook, f"{label}.scenes[{index}].hook")
        normalized_scenes.append(normalized_scene)

    normalized["scenes"] = normalized_scenes
    return normalized


def normalize_theme(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    theme = deep_merge(DEFAULT_THEME, raw)
    require_text(theme.get("name"), f"{label}.name")
    colors = require_mapping(theme.get("colors"), f"{label}.colors")
    for color_name, color_value in colors.items():
        require_text(color_value, f"{label}.colors.{color_name}")
    typography = require_mapping(theme.get("typography"), f"{label}.typography")
    for size_name in ("title_size", "body_size", "small_size", "math_size"):
        require_number(typography.get(size_name), f"{label}.typography.{size_name}")
    layout = require_mapping(theme.get("layout"), f"{label}.layout")
    for layout_name in ("top_y", "side_margin", "content_width"):
        require_number(layout.get(layout_name), f"{label}.layout.{layout_name}")
    transitions = require_mapping(theme.get("transitions"), f"{label}.transitions")
    for name in ("element_fade", "bullet_lag", "section_pause"):
        require_number(transitions.get(name), f"{label}.transitions.{name}")
    return theme


def normalize_video(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    video = deep_merge(DEFAULT_VIDEO, raw)
    require_text(video.get("aspect_ratio"), f"{label}.aspect_ratio")
    require_positive_int(video.get("pixel_width"), f"{label}.pixel_width")
    require_positive_int(video.get("pixel_height"), f"{label}.pixel_height")
    require_positive_number(video.get("frame_rate"), f"{label}.frame_rate")
    preview_scale = require_positive_number(video.get("preview_scale"), f"{label}.preview_scale")
    if preview_scale > 1:
        raise ValueError(f"{label}.preview_scale must be <= 1.")
    return video


def normalize_timing(value: Any, label: str) -> dict[str, Any]:
    raw = {} if value is None else require_mapping(value, label)
    timing = deep_merge(DEFAULT_TIMING, raw)
    for key in ("lead_in_seconds", "hold_after_seconds", "minimum_duration_seconds"):
        require_non_negative_number(timing.get(key), f"{label}.{key}")
    return timing


def normalize_scene_data(template: str, value: Any, label: str) -> dict[str, Any]:
    data = require_mapping(value, label)
    if template == "title_bullets":
        data["bullets"] = require_string_list(data.get("bullets"), f"{label}.bullets")
        return data
    if template == "definition_math":
        data["statement"] = require_text(data.get("statement"), f"{label}.statement")
        data["math_lines"] = require_string_list(data.get("math_lines"), f"{label}.math_lines")
        if "supporting_bullets" in data:
            data["supporting_bullets"] = require_string_list(data.get("supporting_bullets"), f"{label}.supporting_bullets")
        return data
    if template == "example_walkthrough":
        data["steps"] = require_string_list(data.get("steps"), f"{label}.steps")
        data["takeaway"] = require_text(data.get("takeaway"), f"{label}.takeaway")
        if "math_lines" in data:
            data["math_lines"] = require_string_list(data.get("math_lines"), f"{label}.math_lines")
        return data
    if template == "graph_focus":
        data["axes"] = normalize_axes(data.get("axes"), f"{label}.axes")
        data["plots"] = normalize_plots(data.get("plots"), f"{label}.plots")
        data["annotations"] = normalize_annotations(data.get("annotations"), f"{label}.annotations")
        if "source_figure_tex" in data:
            data["source_figure_tex"] = require_text(data.get("source_figure_tex"), f"{label}.source_figure_tex")
        return data
    if template == "procedure_steps":
        data["steps"] = require_string_list(data.get("steps"), f"{label}.steps")
        data["worked_equations"] = require_string_list(data.get("worked_equations"), f"{label}.worked_equations")
        return data
    if template == "recap_cards":
        data["points"] = require_string_list(data.get("points"), f"{label}.points")
        data["identities"] = require_string_list(data.get("identities"), f"{label}.identities")
        return data
    raise ValueError(f"Unsupported template '{template}'.")


def normalize_axes(value: Any, label: str) -> dict[str, Any]:
    axes = require_mapping(value, label)
    axes["x_range"] = require_number_list(axes.get("x_range"), f"{label}.x_range", min_length=2, max_length=3)
    axes["y_range"] = require_number_list(axes.get("y_range"), f"{label}.y_range", min_length=2, max_length=3)
    axes["x_length"] = require_positive_number(axes.get("x_length"), f"{label}.x_length")
    axes["y_length"] = require_positive_number(axes.get("y_length"), f"{label}.y_length")
    if "include_numbers" in axes:
        axes["include_numbers"] = require_optional_bool(axes.get("include_numbers"), f"{label}.include_numbers", False)
    if "tips" in axes:
        axes["tips"] = require_optional_bool(axes.get("tips"), f"{label}.tips", True)
    return axes


def normalize_plots(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array.")
    normalized: list[dict[str, Any]] = []
    for index, plot in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(plot, entry_label)
        kind = require_text(item.get("kind"), f"{entry_label}.kind")
        if kind not in {"function", "line", "point"}:
            raise ValueError(f"{entry_label}.kind must be one of function, line, point.")
        item["kind"] = kind
        if kind == "function":
            item["expression"] = require_text(item.get("expression"), f"{entry_label}.expression")
            if "x_range" in item:
                item["x_range"] = require_number_list(item.get("x_range"), f"{entry_label}.x_range", min_length=2, max_length=3)
        elif kind == "line":
            item["start"] = require_number_list(item.get("start"), f"{entry_label}.start", exact_length=2)
            item["end"] = require_number_list(item.get("end"), f"{entry_label}.end", exact_length=2)
        else:
            item["point"] = require_number_list(item.get("point"), f"{entry_label}.point", exact_length=2)
            if "radius" in item:
                item["radius"] = require_positive_number(item.get("radius"), f"{entry_label}.radius")
        if "color" in item:
            item["color"] = require_text(item.get("color"), f"{entry_label}.color")
        if "label" in item:
            item["label"] = require_text(item.get("label"), f"{entry_label}.label")
        if "dashed" in item:
            item["dashed"] = require_optional_bool(item.get("dashed"), f"{entry_label}.dashed", False)
        normalized.append(item)
    return normalized


def normalize_annotations(value: Any, label: str) -> list[dict[str, Any]]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{label} must be an array.")
    normalized: list[dict[str, Any]] = []
    for index, annotation in enumerate(value):
        entry_label = f"{label}[{index}]"
        item = require_mapping(annotation, entry_label)
        item["text"] = require_text(item.get("text"), f"{entry_label}.text")
        if "anchor" in item:
            item["anchor"] = require_number_list(item.get("anchor"), f"{entry_label}.anchor", exact_length=2)
        if "side" in item:
            side = require_text(item.get("side"), f"{entry_label}.side")
            if side not in {"left", "right", "up", "down", "center"}:
                raise ValueError(f"{entry_label}.side must be left, right, up, down, or center.")
            item["side"] = side
        normalized.append(item)
    return normalized


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    keys = set(base) | set(override)
    for key in keys:
        base_value = base.get(key)
        override_value = override.get(key)
        if isinstance(base_value, dict) and isinstance(override_value, dict):
            merged[key] = deep_merge(base_value, override_value)
        elif key in override:
            merged[key] = override_value
        else:
            merged[key] = base_value
    return merged


def require_mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a mapping.")
    return dict(value)


def require_text(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string.")
    return value.strip()


def require_string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{label} must be an array of non-empty strings.")
    return [item.strip() for item in value]


def require_number_list(
    value: Any,
    label: str,
    *,
    min_length: int | None = None,
    max_length: int | None = None,
    exact_length: int | None = None,
) -> list[float]:
    if not isinstance(value, list) or not value:
        raise ValueError(f"{label} must be a non-empty array of numbers.")
    if exact_length is not None and len(value) != exact_length:
        raise ValueError(f"{label} must contain exactly {exact_length} numbers.")
    if min_length is not None and len(value) < min_length:
        raise ValueError(f"{label} must contain at least {min_length} numbers.")
    if max_length is not None and len(value) > max_length:
        raise ValueError(f"{label} must contain at most {max_length} numbers.")
    if not all(isinstance(item, (int, float)) for item in value):
        raise ValueError(f"{label} must contain only numbers.")
    return [float(item) for item in value]


def require_number(value: Any, label: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a number.")
    return float(value)


def require_positive_number(value: Any, label: str) -> float:
    number = require_number(value, label)
    if number <= 0:
        raise ValueError(f"{label} must be positive.")
    return number


def require_non_negative_number(value: Any, label: str) -> float:
    number = require_number(value, label)
    if number < 0:
        raise ValueError(f"{label} must be non-negative.")
    return number


def require_positive_int(value: Any, label: str) -> int:
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{label} must be a positive integer.")
    return value


def require_optional_bool(value: Any, label: str, default: bool) -> bool:
    if value is None:
        return default
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean when provided.")
    return value


def load_deck_json(path: Path) -> dict[str, Any]:
    with require_path(path.resolve(), "slide deck JSON").open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_seed_voiceovers(deck: dict[str, Any]) -> tuple[list[str], str]:
    script_file = final_script_path(REPO_ROOT, deck["deck_id"]).resolve()
    if script_file.exists():
        try:
            return load_slide_scripts(script_file, deck, enforce_spoken_math=False), str(script_file)
        except Exception:
            pass
    voiceovers = [require_text(slide.get("script_draft"), f"deck slide {slide.get('slide_id')} script_draft") for slide in deck["slides"]]
    return voiceovers, "deck script_draft"


def build_seed_storyboard(deck: dict[str, Any], voiceovers: list[str] | None = None) -> dict[str, Any]:
    slides = deck.get("slides")
    if not isinstance(slides, list) or not slides:
        raise ValueError("Deck JSON must contain a non-empty slides array.")
    chosen_voiceovers = voiceovers or [slide["script_draft"] for slide in slides]
    if len(chosen_voiceovers) != len(slides):
        raise ValueError("Voiceover count does not match slide count while seeding storyboard.")

    return {
        "deck_id": require_text(deck.get("deck_id"), "deck.deck_id"),
        "language": require_text(deck.get("language"), "deck.language"),
        "theme": DEFAULT_THEME,
        "video": DEFAULT_VIDEO,
        "scenes": [
            build_seed_scene_from_slide(slide, chosen_voiceovers[index])
            for index, slide in enumerate(slides)
        ],
    }


def build_seed_scene_from_slide(slide: dict[str, Any], voiceover: str) -> dict[str, Any]:
    slide_type = require_text(slide.get("slide_type"), f"slide {slide.get('slide_id')} slide_type")
    if slide_type not in SLIDE_TYPE_TO_TEMPLATE:
        raise ValueError(f"Unsupported slide_type '{slide_type}' in deck JSON.")
    template = SLIDE_TYPE_TO_TEMPLATE[slide_type]
    bullets = list(slide.get("bullets", []))
    math_blocks = list(slide.get("math_blocks", []))
    return {
        "scene_id": require_text(slide.get("slide_id"), f"slide {slide.get('slide_number')} slide_id"),
        "template": template,
        "title": require_text(slide.get("title"), f"slide {slide.get('slide_number')} title"),
        "voiceover": require_text(voiceover, f"slide {slide.get('slide_number')} voiceover"),
        "timing": DEFAULT_TIMING,
        "data": build_seed_scene_data(template, slide, bullets, math_blocks),
    }


def build_seed_scene_data(template: str, slide: dict[str, Any], bullets: list[str], math_blocks: list[str]) -> dict[str, Any]:
    if template == "title_bullets":
        return {"bullets": bullets}
    if template == "definition_math":
        return {
            "statement": bullets[0] if bullets else slide["learning_goal"],
            "math_lines": math_blocks,
            "supporting_bullets": bullets[1:],
        }
    if template == "example_walkthrough":
        return {
            "steps": bullets or [slide["learning_goal"]],
            "takeaway": slide["learning_goal"],
            "math_lines": math_blocks,
        }
    if template == "graph_focus":
        annotations = [{"text": item} for item in bullets] if bullets else [{"text": slide["learning_goal"]}]
        return {
            "axes": {
                "x_range": [-3, 3, 1],
                "y_range": [-1, 4, 1],
                "x_length": 6.2,
                "y_length": 4.2,
                "include_numbers": False,
                "tips": True,
            },
            "plots": [],
            "annotations": annotations,
            "source_figure_tex": slide.get("tikz_code") or "",
        }
    if template == "procedure_steps":
        return {
            "steps": bullets or [slide["learning_goal"]],
            "worked_equations": math_blocks,
        }
    if template == "recap_cards":
        return {
            "points": bullets or [slide["learning_goal"]],
            "identities": math_blocks,
        }
    raise ValueError(f"Unsupported template '{template}'.")


def write_storyboard(path: Path, storyboard: dict[str, Any]) -> None:
    ensure_directory(path.parent)
    path.write_text(dump_yaml(strip_runtime_fields(storyboard)), encoding="utf-8")


def strip_runtime_fields(storyboard: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "deck_id": storyboard["deck_id"],
        "language": storyboard["language"],
        "theme": storyboard["theme"],
        "video": storyboard["video"],
        "scenes": [],
    }
    for scene in storyboard["scenes"]:
        item = {
            "scene_id": scene["scene_id"],
            "template": scene["template"],
            "title": scene["title"],
            "voiceover": scene["voiceover"],
            "timing": scene["timing"],
            "data": scene["data"],
        }
        if scene.get("disabled"):
            item["disabled"] = True
        if scene.get("hook"):
            item["hook"] = scene["hook"]
        cleaned["scenes"].append(item)
    return cleaned


def find_scene(storyboard: dict[str, Any], scene_id: str) -> dict[str, Any]:
    for scene in storyboard["scenes"]:
        if scene["scene_id"] == scene_id:
            return scene
    raise KeyError(f"Scene '{scene_id}' was not found in storyboard '{storyboard['deck_id']}'.")


def enabled_scenes(storyboard: dict[str, Any]) -> list[dict[str, Any]]:
    return [scene for scene in storyboard["scenes"] if not scene.get("disabled", False)]


def storyboard_to_bridge_deck(storyboard: dict[str, Any], storyboard_path: Path) -> dict[str, Any]:
    slides = []
    for scene in enabled_scenes(storyboard):
        slides.append(
            {
                "slide_number": scene["scene_number"],
                "slide_id": scene["scene_id"],
                "source_section": storyboard["deck_id"],
                "title": scene["title"],
                "learning_goal": scene["title"],
                "slide_type": scene["template"],
                "bullets": [],
                "math_blocks": [],
                "tikz_code": None,
                "script_draft": scene["voiceover"],
                "render_hints": DEFAULT_BRIDGE_RENDER_HINTS,
            }
        )
    return {
        "deck_id": storyboard["deck_id"],
        "source_file": str(storyboard_path.relative_to(REPO_ROOT)),
        "source_section": storyboard["deck_id"],
        "language": storyboard["language"],
        "slides": slides,
    }


def render_storyboard_script_markdown(storyboard: dict[str, Any], storyboard_path: Path) -> str:
    sections = [
        f"# {storyboard['deck_id']} Final Narration",
        "",
        f"Source file: `{storyboard_path.relative_to(REPO_ROOT)}`",
        f"Deck ID: `{storyboard['deck_id']}`",
        "",
        "This file is regenerated from the Manim storyboard. Edit the storyboard instead of editing this file.",
        "The narration is derived from each scene's `voiceover` field and is exported only to bridge into the existing TTS tools.",
        "",
    ]
    for scene in enabled_scenes(storyboard):
        sections.extend(
            [
                f"## Slide {scene['scene_number']}: {scene['title']}",
                "",
                f"Slide ID: `{scene['scene_id']}`",
                f"Scene template: `{scene['template']}`",
                "",
                "Narration:",
                "",
                scene["voiceover"].strip(),
                "",
            ]
        )
    return "\n".join(sections).strip() + "\n"


def export_storyboard_bridge_files(
    storyboard: dict[str, Any],
    storyboard_path: Path,
    *,
    script_path: Path | None = None,
    deck_path: Path | None = None,
) -> dict[str, Path]:
    resolved_script_path = (script_path or final_script_path(REPO_ROOT, storyboard["deck_id"])).resolve()
    resolved_deck_path = (deck_path or manim_tts_deck_path(REPO_ROOT, storyboard["deck_id"])).resolve()
    ensure_directory(resolved_script_path.parent)
    ensure_directory(resolved_deck_path.parent)

    bridge_deck = storyboard_to_bridge_deck(storyboard, storyboard_path)
    resolved_script_path.write_text(render_storyboard_script_markdown(storyboard, storyboard_path), encoding="utf-8")
    resolved_deck_path.write_text(json.dumps(bridge_deck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"script_path": resolved_script_path, "deck_path": resolved_deck_path}


def scene_fingerprint(storyboard: dict[str, Any], scene: dict[str, Any], quality: str) -> str:
    payload = {
        "deck_id": storyboard["deck_id"],
        "scene": strip_runtime_scene(scene),
        "theme": storyboard["theme"],
        "video": storyboard["video"],
        "quality": quality,
        "engine": template_engine_fingerprint(),
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def strip_runtime_scene(scene: dict[str, Any]) -> dict[str, Any]:
    cleaned = {
        "scene_id": scene["scene_id"],
        "template": scene["template"],
        "title": scene["title"],
        "voiceover": scene["voiceover"],
        "data": scene["data"],
        "timing": scene["timing"],
        "disabled": scene.get("disabled", False),
    }
    if scene.get("hook"):
        cleaned["hook"] = scene["hook"]
    return cleaned


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def template_engine_fingerprint() -> str:
    paths = [
        REPO_ROOT / "tools" / "manim_storyboard_workflow.py",
        REPO_ROOT / "tools" / "manim_runtime.py",
    ]
    template_root = REPO_ROOT / "tools" / "manim_templates"
    if template_root.exists():
        paths.extend(sorted(template_root.rglob("*.py")))
    hasher = hashlib.sha256()
    for path in sorted({candidate.resolve() for candidate in paths if candidate.exists()}):
        hasher.update(str(path.relative_to(REPO_ROOT)).encode("utf-8"))
        hasher.update(path.read_bytes())
    return hasher.hexdigest()


def load_render_manifest(deck_id: str) -> dict[str, Any]:
    path = manim_render_manifest_path(REPO_ROOT, deck_id).resolve()
    if not path.exists():
        return {"deck_id": deck_id, "scenes": {}}
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "scenes" not in data or not isinstance(data["scenes"], dict):
        return {"deck_id": deck_id, "scenes": {}}
    return data


def write_render_manifest(deck_id: str, manifest: dict[str, Any]) -> Path:
    path = manim_render_manifest_path(REPO_ROOT, deck_id).resolve()
    ensure_directory(path.parent)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def resolve_hook_path(import_path: str) -> Path | None:
    module_name, _, attribute_name = import_path.rpartition(".")
    if not module_name or not attribute_name:
        return None
    try:
        spec = importlib.util.find_spec(module_name)
    except ModuleNotFoundError:
        fallback = REPO_ROOT / (module_name.replace(".", "/") + ".py")
        return fallback if fallback.exists() else None
    if spec is None or spec.origin is None or spec.origin in {"built-in", "frozen"}:
        fallback = REPO_ROOT / (module_name.replace(".", "/") + ".py")
        return fallback if fallback.exists() else None
    return Path(spec.origin)


def validate_hook_paths(storyboard: dict[str, Any]) -> None:
    for scene in enabled_scenes(storyboard):
        hook = scene.get("hook")
        if not hook:
            continue
        hook_path = resolve_hook_path(hook)
        if hook_path is None or not hook_path.exists():
            raise ValueError(
                f"Hook '{hook}' for scene '{scene['scene_id']}' could not be resolved to a local Python file."
            )


def suggested_seed_source(deck_id: str) -> Path:
    return deck_json_path(REPO_ROOT, deck_id).resolve()


def default_bridge_paths(deck_id: str) -> dict[str, Path]:
    return {
        "storyboard_path": manim_storyboard_path(REPO_ROOT, deck_id).resolve(),
        "deck_json_path": deck_json_path(REPO_ROOT, deck_id).resolve(),
        "bridge_deck_path": manim_tts_deck_path(REPO_ROOT, deck_id).resolve(),
        "bridge_script_path": final_script_path(REPO_ROOT, deck_id).resolve(),
    }


def to_tex_text(text: str) -> str:
    return INLINE_MATH_RE.sub(lambda match: f"${match.group(1)}$", text.strip())


def to_mathtex_body(display_math: str) -> str:
    stripped = display_math.strip()
    match = DISPLAY_MATH_WRAPPER_RE.match(stripped)
    body = match.group("body") if match else stripped
    return body.strip()
