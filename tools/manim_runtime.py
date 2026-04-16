from __future__ import annotations

import importlib.util
import os
import re
import shutil
import subprocess
import wave
from pathlib import Path
from typing import Any

from runtime_bootstrap import REPO_ROOT, ensure_directory, require_path


def ensure_manim_available() -> None:
    if importlib.util.find_spec("manim") is None:
        raise RuntimeError(
            "Manim is not installed in the current Python environment. "
            "Install it before using preview_manim_scene.py or render_manim_lesson.py."
        )


def quality_video_settings(video: dict[str, Any], quality: str) -> dict[str, int]:
    if quality not in {"preview", "final"}:
        raise ValueError(f"Unsupported quality '{quality}'.")
    if quality == "final":
        return {
            "pixel_width": ensure_even(int(video["pixel_width"])),
            "pixel_height": ensure_even(int(video["pixel_height"])),
            "frame_rate": int(video["frame_rate"]),
        }
    scale = float(video.get("preview_scale", 0.5))
    return {
        "pixel_width": ensure_even(max(640, int(int(video["pixel_width"]) * scale))),
        "pixel_height": ensure_even(max(360, int(int(video["pixel_height"]) * scale))),
        "frame_rate": min(24, int(video["frame_rate"])),
    }


def ensure_even(value: int) -> int:
    return value if value % 2 == 0 else value + 1


def render_storyboard_scene(
    storyboard_path: Path,
    storyboard: dict[str, Any],
    scene_spec: dict[str, Any],
    output_path: Path,
    quality: str,
) -> Path:
    ensure_manim_available()
    ensure_miktex_env()
    ensure_ffmpeg_env()
    patch_manim_tex_runtime()
    from manim import tempconfig

    from manim_templates.scene_player import StoryboardTemplateScene

    settings = quality_video_settings(storyboard["video"], quality)
    ensure_directory(output_path.parent)
    temp_media_dir = ensure_directory(output_path.parent / ".manim_tmp" / output_path.stem)

    context = {
        "repo_root": REPO_ROOT,
        "storyboard_path": storyboard_path,
        "storyboard": storyboard,
        "theme": storyboard["theme"],
        "video": {**storyboard["video"], **settings},
    }
    config = {
        "media_dir": str(temp_media_dir),
        "output_file": output_path.stem,
        "write_to_movie": True,
        "save_last_frame": False,
        "disable_caching": True,
        "disable_caching_warning": True,
        "background_color": storyboard["theme"]["colors"]["background"],
        "pixel_width": settings["pixel_width"],
        "pixel_height": settings["pixel_height"],
        "frame_rate": settings["frame_rate"],
        "format": "mp4",
        "progress_bar": "none",
        "verbosity": "WARNING",
        "ffmpeg_loglevel": "ERROR",
    }

    StoryboardTemplateScene.scene_spec = scene_spec
    StoryboardTemplateScene.render_context = context
    try:
        with tempconfig(config):
            player = StoryboardTemplateScene()
            player.render()
            movie_path = Path(player.renderer.file_writer.movie_file_path).resolve()
    finally:
        StoryboardTemplateScene.scene_spec = None
        StoryboardTemplateScene.render_context = None

    if not movie_path.exists():
        raise FileNotFoundError(f"Manim render completed without an output file: {movie_path}")

    if output_path.exists():
        output_path.unlink()
    shutil.copy2(movie_path, output_path)
    return output_path.resolve()


def resolve_ffmpeg_tool(tool_name: str) -> str:
    if tool_name == "ffmpeg":
        return resolve_ffmpeg_executable()
    executable = shutil.which(tool_name)
    if executable:
        return executable
    raise RuntimeError(
        f"{tool_name} was not found on PATH. Install FFmpeg before running the Manim lesson renderer."
    )


def resolve_ffmpeg_executable() -> str:
    executable = shutil.which("ffmpeg")
    if executable:
        return executable

    if importlib.util.find_spec("imageio_ffmpeg") is not None:
        import imageio_ffmpeg

        bundled = str(Path(imageio_ffmpeg.get_ffmpeg_exe()).resolve())
        bundled_dir = str(Path(bundled).parent)
        os.environ.setdefault("IMAGEIO_FFMPEG_EXE", bundled)
        path_entries = os.environ.get("PATH", "")
        if bundled_dir not in path_entries.split(os.pathsep):
            os.environ["PATH"] = bundled_dir + os.pathsep + path_entries
        return bundled

    raise RuntimeError(
        "FFmpeg is not available. Install standalone FFmpeg or install the Python package "
        "`imageio-ffmpeg` in the active environment."
    )


def ensure_ffmpeg_env() -> None:
    resolve_ffmpeg_executable()


def ensure_miktex_env() -> None:
    miktex_data = ensure_directory(REPO_ROOT / ".cache" / "miktex-data")
    miktex_config = ensure_directory(REPO_ROOT / ".cache" / "miktex-config")
    ensure_directory(miktex_data / "miktex" / "log")
    os.environ.setdefault("HOME", str(REPO_ROOT))
    os.environ["MIKTEX_USERDATA"] = str(miktex_data)
    os.environ["MIKTEX_USERCONFIG"] = str(miktex_config)


def patch_manim_tex_runtime() -> None:
    from manim.utils import tex_file_writing

    if getattr(tex_file_writing, "_storyboard_quiet_miktex_patch", False):
        return

    original_run = tex_file_writing.subprocess.run

    def quiet_tex_run(command: Any, *args: Any, **kwargs: Any) -> subprocess.CompletedProcess[Any]:
        rewritten = rewrite_manim_tex_command(command)
        executable = manim_tex_executable_name(rewritten)
        if executable in {"latex", "pdflatex", "luatex", "lualatex", "xelatex", "dvisvgm"}:
            kwargs.setdefault("stdout", subprocess.DEVNULL)
            kwargs.setdefault("stderr", subprocess.DEVNULL)
        return original_run(rewritten, *args, **kwargs)

    tex_file_writing.subprocess.run = quiet_tex_run
    tex_file_writing._storyboard_quiet_miktex_patch = True


def rewrite_manim_tex_command(command: Any) -> Any:
    if not isinstance(command, list) or not command:
        return command

    executable = manim_tex_executable_name(command)
    if executable == "dvisvgm" and executable_uses_miktex(command[0]):
        return inject_cli_flags(
            command,
            [
                "--miktex-disable-maintenance",
                "--miktex-disable-diagnose",
                "--no-mktexmf",
            ],
        )
    if executable in {"latex", "pdflatex", "luatex", "lualatex", "xelatex"} and executable_uses_miktex(
        command[0]
    ):
        return inject_cli_flags(
            command,
            [
                "--miktex-disable-maintenance",
                "--miktex-disable-diagnose",
                "-disable-installer",
            ],
        )
    return command


def inject_cli_flags(command: list[Any], flags: list[str]) -> list[Any]:
    existing = {str(value) for value in command[1:]}
    rewritten = list(command)
    insert_at = 1
    for flag in flags:
        if flag not in existing:
            rewritten.insert(insert_at, flag)
            insert_at += 1
    return rewritten


def manim_tex_executable_name(command: Any) -> str | None:
    if isinstance(command, list) and command:
        return Path(str(command[0])).name.lower()
    return None


def executable_uses_miktex(executable: Any) -> bool:
    resolved = shutil.which(str(executable)) or str(executable)
    return "miktex" in str(resolved).lower()


def run_ffmpeg(command: list[str]) -> None:
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(
            "FFmpeg command failed.\n"
            f"Command: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )


def probe_video_duration(path: Path) -> float:
    ffmpeg = resolve_ffmpeg_tool("ffmpeg")
    result = subprocess.run(
        [
            ffmpeg,
            str(require_path(path.resolve(), "scene video")),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    duration_text = result.stderr or result.stdout
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", duration_text)
    if not match:
        raise RuntimeError(f"Could not determine video duration for {path}.\n{duration_text}")
    hours = int(match.group(1))
    minutes = int(match.group(2))
    seconds = float(match.group(3))
    return hours * 3600 + minutes * 60 + seconds


def probe_wav_duration(path: Path) -> float:
    with wave.open(str(require_path(path.resolve(), "scene audio WAV")), "rb") as handle:
        frame_count = handle.getnframes()
        sample_rate = handle.getframerate()
    if sample_rate <= 0:
        raise RuntimeError(f"Invalid sample rate for audio file {path}.")
    return frame_count / sample_rate


def mux_scene_video_with_audio(
    video_path: Path,
    audio_path: Path,
    output_path: Path,
    timing: dict[str, Any],
) -> Path:
    ffmpeg = resolve_ffmpeg_tool("ffmpeg")
    ensure_directory(output_path.parent)
    video_duration = probe_video_duration(video_path)
    audio_duration = probe_wav_duration(audio_path)
    lead_in = float(timing["lead_in_seconds"])
    hold_after = float(timing["hold_after_seconds"])
    minimum = float(timing["minimum_duration_seconds"])
    target_duration = max(video_duration, lead_in + audio_duration + hold_after, minimum)
    video_pad = max(target_duration - video_duration, 0.0)
    audio_pad = max(target_duration - lead_in - audio_duration, 0.0)
    delay_ms = max(int(round(lead_in * 1000)), 0)

    command = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-i",
        str(audio_path),
        "-filter_complex",
        (
            f"[0:v]tpad=stop_mode=clone:stop_duration={video_pad:.3f}[v];"
            f"[1:a]adelay={delay_ms}:all=1,apad=pad_dur={audio_pad:.3f}[a]"
        ),
        "-map",
        "[v]",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-t",
        f"{target_duration:.3f}",
        str(output_path),
    ]
    run_ffmpeg(command)
    return output_path.resolve()


def concat_scene_videos(segment_paths: list[Path], output_path: Path, *, with_audio: bool) -> Path:
    if not segment_paths:
        raise ValueError("At least one segment is required to build a lesson video.")
    ffmpeg = resolve_ffmpeg_tool("ffmpeg")
    ensure_directory(output_path.parent)

    concat_file = output_path.with_suffix(".segments.txt")
    concat_file.write_text(
        "\n".join(f"file '{path.resolve().as_posix()}'" for path in segment_paths) + "\n",
        encoding="utf-8",
    )
    command = [
        ffmpeg,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-c:v",
        "libx264",
        "-preset",
        "medium",
        "-pix_fmt",
        "yuv420p",
    ]
    if with_audio:
        command.extend(["-c:a", "aac", "-b:a", "192k"])
    command.append(str(output_path))
    run_ffmpeg(command)
    return output_path.resolve()
