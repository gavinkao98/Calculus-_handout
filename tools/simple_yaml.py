from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SCALAR_NUMBER_RE = re.compile(r"^-?(?:0|[1-9]\d*)(?:\.\d+)?$")


class SimpleYamlError(ValueError):
    """Raised when a YAML document falls outside the supported subset."""


def load_yaml_path(path: Path) -> Any:
    return load_yaml(path.read_text(encoding="utf-8"))


def load_yaml(text: str) -> Any:
    lines = text.splitlines()

    def skip_blank_lines(position: int) -> int:
        while position < len(lines) and not lines[position].strip():
            position += 1
        return position

    def indentation_of(line: str) -> int:
        return len(line) - len(line.lstrip(" "))

    def parse_scalar(token: str) -> Any:
        token = token.strip()
        if token == "null":
            return None
        if token == "true":
            return True
        if token == "false":
            return False
        if token.startswith('"') or token.startswith("[") or token.startswith("{"):
            try:
                return json.loads(token)
            except json.JSONDecodeError as exc:
                raise SimpleYamlError(f"Could not parse scalar token: {token}") from exc
        if SCALAR_NUMBER_RE.match(token):
            return float(token) if "." in token else int(token)
        return token

    def parse_block(expected_indent: int, position: int) -> tuple[Any, int]:
        position = skip_blank_lines(position)
        if position >= len(lines):
            return None, position

        line = lines[position]
        current_indent = indentation_of(line)
        if current_indent < expected_indent:
            return None, position
        if current_indent > expected_indent:
            raise SimpleYamlError(
                f"Unexpected indentation at line {position + 1}: expected {expected_indent} spaces, "
                f"found {current_indent}."
            )

        stripped = line[current_indent:]
        if stripped.startswith("-"):
            return parse_list(expected_indent, position)
        return parse_mapping(expected_indent, position)

    def parse_mapping(expected_indent: int, position: int) -> tuple[dict[str, Any], int]:
        mapping: dict[str, Any] = {}

        while position < len(lines):
            position = skip_blank_lines(position)
            if position >= len(lines):
                break

            line = lines[position]
            current_indent = indentation_of(line)
            if current_indent < expected_indent:
                break
            if current_indent != expected_indent:
                raise SimpleYamlError(
                    f"Unexpected indentation at line {position + 1}: expected {expected_indent} spaces, "
                    f"found {current_indent}."
                )

            stripped = line[current_indent:]
            if stripped.startswith("-"):
                break

            if ":" not in stripped:
                raise SimpleYamlError(f"Expected a mapping entry at line {position + 1}: {line}")

            key, remainder = stripped.split(":", 1)
            key = key.strip()
            remainder = remainder.lstrip()
            if not key:
                raise SimpleYamlError(f"Missing key at line {position + 1}: {line}")

            if not remainder:
                position += 1
                value, position = parse_block(expected_indent + 2, position)
                if value is None:
                    value = {}
            else:
                value = parse_scalar(remainder)
                position += 1

            mapping[key] = value

        return mapping, position

    def parse_list(expected_indent: int, position: int) -> tuple[list[Any], int]:
        items: list[Any] = []

        while position < len(lines):
            position = skip_blank_lines(position)
            if position >= len(lines):
                break

            line = lines[position]
            current_indent = indentation_of(line)
            if current_indent < expected_indent:
                break
            if current_indent != expected_indent:
                raise SimpleYamlError(
                    f"Unexpected indentation at line {position + 1}: expected {expected_indent} spaces, "
                    f"found {current_indent}."
                )

            stripped = line[current_indent:]
            if not stripped.startswith("-"):
                break

            remainder = stripped[1:].lstrip()
            if not remainder:
                position += 1
                value, position = parse_block(expected_indent + 2, position)
                items.append(value)
                continue

            items.append(parse_scalar(remainder))
            position += 1

        return items, position

    parsed, index = parse_block(0, 0)
    index = skip_blank_lines(index)
    if index != len(lines):
        raise SimpleYamlError(f"Unexpected trailing content at line {index + 1}.")
    return parsed


def dump_yaml(value: Any) -> str:
    return render_yaml(value).rstrip() + "\n"


def render_yaml(value: Any, indent: int = 0) -> str:
    prefix = " " * indent
    if isinstance(value, dict):
        if not value:
            return prefix + "{}\n"
        parts: list[str] = []
        for key, item in value.items():
            if not isinstance(key, str):
                raise SimpleYamlError(f"Only string keys are supported, got {type(key)!r}.")
            if is_scalar(item):
                parts.append(f"{prefix}{key}: {render_scalar(item)}\n")
            else:
                parts.append(f"{prefix}{key}:\n{render_yaml(item, indent + 2)}")
        return "".join(parts)

    if isinstance(value, list):
        if not value:
            return prefix + "[]\n"
        parts = []
        for item in value:
            if is_scalar(item):
                parts.append(f"{prefix}- {render_scalar(item)}\n")
            else:
                parts.append(f"{prefix}-\n{render_yaml(item, indent + 2)}")
        return "".join(parts)

    return prefix + render_scalar(value) + "\n"


def is_scalar(value: Any) -> bool:
    if value is None or isinstance(value, (bool, int, float, str)):
        return True
    return value == [] or value == {}


def render_scalar(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, (int, float)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    raise SimpleYamlError(f"Unsupported scalar type: {type(value)!r}")
