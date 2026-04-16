from __future__ import annotations

import argparse
from pathlib import Path

from manim_runtime import concat_scene_videos, mux_scene_video_with_audio, render_storyboard_scene
from manim_storyboard_workflow import (
    default_bridge_paths,
    enabled_scenes,
    export_storyboard_bridge_files,
    load_render_manifest,
    load_storyboard,
    resolve_storyboard_path,
    scene_fingerprint,
    write_render_manifest,
)
from media_paths import (
    DEFAULT_DECK_ID,
    audio_dir_path,
    audio_manifest_path,
    manim_scene_output_path,
    manim_segment_output_path,
    video_output_path,
)
from runtime_bootstrap import REPO_ROOT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a full Manim lesson from a storyboard, with per-scene caching."
    )
    parser.add_argument("--deck-id", default=DEFAULT_DECK_ID)
    parser.add_argument("--storyboard", type=Path)
    parser.add_argument("--quality", choices=("preview", "final"), default="preview")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--with-audio", action="store_true")
    parser.add_argument("--audio-dir", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    storyboard_path = resolve_storyboard_path(args.deck_id, args.storyboard)
    storyboard = load_storyboard(storyboard_path)
    scenes = enabled_scenes(storyboard)
    if not scenes:
        raise ValueError(f"No enabled scenes were found in storyboard {storyboard_path}.")

    output = (
        args.output
        or video_output_path(REPO_ROOT, f"{storyboard['deck_id']}_manim")
    ).resolve()
    manifest = load_render_manifest(storyboard["deck_id"])
    rendered_scene_paths: list[Path] = []

    for scene in scenes:
        output_path = manim_scene_output_path(REPO_ROOT, storyboard["deck_id"], scene["scene_number"], scene["scene_id"]).resolve()
        fingerprint = scene_fingerprint(storyboard, scene, args.quality)
        cached = manifest.setdefault("scenes", {}).get(scene["scene_id"], {})
        if (
            not args.force
            and output_path.exists()
            and cached.get("fingerprint") == fingerprint
            and cached.get("quality") == args.quality
        ):
            rendered_scene_paths.append(output_path)
            continue

        if args.dry_run:
            rendered_scene_paths.append(output_path)
            continue

        rendered = render_storyboard_scene(storyboard_path, storyboard, scene, output_path, args.quality)
        manifest["scenes"][scene["scene_id"]] = {
            "fingerprint": fingerprint,
            "quality": args.quality,
            "output_file": str(rendered),
        }
        rendered_scene_paths.append(rendered)

    if not args.dry_run:
        write_render_manifest(storyboard["deck_id"], manifest)

    if args.with_audio:
        bridge_files = (
            default_bridge_paths(storyboard["deck_id"])
            if args.dry_run
            else export_storyboard_bridge_files(storyboard, storyboard_path)
        )
        audio_dir = (args.audio_dir or audio_dir_path(REPO_ROOT, storyboard["deck_id"], "manim")).resolve()
        audio_files = resolve_audio_files(
            storyboard["deck_id"],
            scenes,
            audio_dir,
            bridge_files.get("deck_path", bridge_files["bridge_deck_path"]),
            bridge_files.get("script_path", bridge_files["bridge_script_path"]),
        )
        segment_paths = [
            manim_segment_output_path(REPO_ROOT, storyboard["deck_id"], scene["scene_number"], scene["scene_id"]).resolve()
            for scene in scenes
        ]
        if args.dry_run:
            print(
                f"Validated storyboard, bridge files, and audio alignment for {len(scenes)} scenes. "
                f"Final output would be {output}"
            )
            return 0
        muxed_segments = []
        for scene, scene_video, audio_file, segment_path in zip(scenes, rendered_scene_paths, audio_files, segment_paths):
            muxed_segments.append(mux_scene_video_with_audio(scene_video, audio_file, segment_path, scene["timing"]))
        concat_scene_videos(muxed_segments, output, with_audio=True)
        print(f"Rendered Manim lesson with audio to {output}")
        return 0

    if args.dry_run:
        print(
            f"Validated storyboard for {len(scenes)} scenes at quality '{args.quality}'. "
            f"Final output would be {output}"
        )
        return 0

    concat_scene_videos(rendered_scene_paths, output, with_audio=False)
    print(f"Rendered Manim lesson to {output}")
    return 0


def resolve_audio_files(
    deck_id: str,
    scenes: list[dict],
    audio_dir: Path,
    bridge_deck_path: Path,
    bridge_script_path: Path,
) -> list[Path]:
    if not audio_dir.exists():
        raise FileNotFoundError(build_audio_error(deck_id, audio_dir, bridge_deck_path, bridge_script_path))

    resolved: list[Path] = []
    missing: list[str] = []
    for scene in scenes:
        filename = f"{scene['scene_number']:02d}_{scene['scene_id']}.wav"
        path = (audio_dir / filename).resolve()
        if not path.exists():
            missing.append(filename)
            continue
        resolved.append(path)

    if missing:
        raise FileNotFoundError(
            build_audio_error(deck_id, audio_dir, bridge_deck_path, bridge_script_path, missing[0])
        )
    return resolved


def build_audio_error(
    deck_id: str,
    audio_dir: Path,
    bridge_deck_path: Path,
    bridge_script_path: Path,
    first_missing: str | None = None,
) -> str:
    missing_detail = f" First missing file: {first_missing}." if first_missing else ""
    manifest_path = audio_manifest_path(REPO_ROOT, deck_id, "manim").resolve()
    coqui_cmd = (
        "python .\\tools\\synthesize_section_audio.py "
        f"--deck-json {bridge_deck_path} --script-file {bridge_script_path} "
        f"--output-dir {audio_dir} --manifest {manifest_path} --coqui-tos-agreed"
    )
    f5_cmd = (
        "python .\\tools\\synthesize_section_audio_f5.py "
        f"--deck-json {bridge_deck_path} --script-file {bridge_script_path} "
        f"--output-dir {audio_dir} --manifest {manifest_path} --reference-mode clone"
    )
    return (
        f"Expected scene audio files were not found in {audio_dir}.{missing_detail} "
        "The storyboard bridge files were written, so you can synthesize audio with one of these commands:\n"
        f"{coqui_cmd}\n{f5_cmd}"
    )


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, KeyError, RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))
