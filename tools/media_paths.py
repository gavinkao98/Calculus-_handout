from __future__ import annotations

from pathlib import Path


DEFAULT_DECK_ID = "ch01_inverse_functions"


def deck_json_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slide_spec" / f"{deck_id}.json"


def slide_tex_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slides" / f"{deck_id}.tex"


def slide_pdf_path(repo_root: Path, deck_id: str) -> Path:
    return repo_root / "artifacts" / "slides" / f"{deck_id}.pdf"


def audio_dir_path(repo_root: Path, deck_id: str, suffix: str = "") -> Path:
    stem = deck_id if not suffix else f"{deck_id}_{suffix}"
    return repo_root / "artifacts" / "audio" / stem


def audio_manifest_path(repo_root: Path, deck_id: str, suffix: str = "") -> Path:
    return audio_dir_path(repo_root, deck_id, suffix) / "manifest.json"


def video_output_path(repo_root: Path, stem: str) -> Path:
    return repo_root / "artifacts" / "video" / f"{stem}.mp4"
