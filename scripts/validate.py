#!/usr/bin/env python3
"""Validate the Copper KiroCrew theme without third-party dependencies."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
THEME_PATH = ROOT / "theme.json"
VARIABLES_PATH = ROOT / "variables.json"

EXPECTED_KEYS = {
    "--bg", "--bg-accent", "--bg-elevated", "--bg-hover", "--card",
    "--card-fg", "--card-hl", "--panel", "--panel-strong", "--chrome",
    "--text", "--text-strong", "--muted", "--muted-strong", "--muted-fg",
    "--border", "--border-strong", "--border-hover", "--accent",
    "--accent-fg", "--accent-hover", "--accent-subtle", "--accent-glow",
    "--ring", "--ok", "--ok-fg", "--ok-subtle", "--warn", "--warn-fg",
    "--warn-subtle", "--danger", "--danger-fg", "--danger-subtle", "--info",
    "--info-fg", "--aim", "--aim-fg", "--aim-subtle", "--clarify",
    "--clarify-subtle", "--json-key", "--json-str", "--json-num",
    "--json-bool", "--diff-add", "--diff-add-text", "--diff-del",
    "--diff-del-text", "--diff-hunk", "--diff-hunk-text", "--diff-meta-text",
    "--shadow-sm", "--shadow-md", "--shadow-lg",
}

HEX = re.compile(r"^#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?$")
SHADOW = re.compile(
    r"^0 (?:1px 2px|4px 12px|12px 32px) rgba\(\d{1,3},\d{1,3},\d{1,3},0\.\d+\)$"
)


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"cannot read valid JSON from {path.name}: {error}") from error


def rgb(value: str) -> tuple[float, float, float]:
    value = value.lstrip("#")[:6]
    return tuple(int(value[index:index + 2], 16) / 255 for index in (0, 2, 4))


def luminance(value: str) -> float:
    channels = []
    for channel in rgb(value):
        channels.append(channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4)
    return 0.2126 * channels[0] + 0.7152 * channels[1] + 0.0722 * channels[2]


def contrast(first: str, second: str) -> float:
    light, dark = sorted((luminance(first), luminance(second)), reverse=True)
    return (light + 0.05) / (dark + 0.05)


def validate() -> list[str]:
    errors: list[str] = []
    theme = load_json(THEME_PATH)
    variables = load_json(VARIABLES_PATH)

    expected_manifest = {
        "slug": "copper",
        "name": "Copper",
        "emoji": "◎",
        "level": 0,
        "formatVersion": 1,
    }
    if theme != expected_manifest:
        errors.append("theme.json does not match the expected Copper manifest")

    if set(variables) != {"dark", "light"}:
        errors.append("variables.json must contain exactly dark and light modes")
        return errors

    for mode in ("dark", "light"):
        palette = variables[mode]
        keys = set(palette)
        missing = sorted(EXPECTED_KEYS - keys)
        extra = sorted(keys - EXPECTED_KEYS)
        if missing:
            errors.append(f"{mode}: missing variables: {', '.join(missing)}")
        if extra:
            errors.append(f"{mode}: unexpected variables: {', '.join(extra)}")

        for key, value in palette.items():
            if not isinstance(value, str) or len(value) > 200:
                errors.append(f"{mode}: {key} must be a string of at most 200 characters")
                continue
            if key.startswith("--shadow-"):
                if not SHADOW.fullmatch(value):
                    errors.append(f"{mode}: {key} has an unsupported shadow value")
            elif not HEX.fullmatch(value):
                errors.append(f"{mode}: {key} must be a six- or eight-digit hex color")

        for foreground in ("--text", "--text-strong", "--muted-fg"):
            ratio = contrast(palette[foreground], palette["--bg"])
            if ratio < 4.5:
                errors.append(f"{mode}: {foreground} contrast is only {ratio:.2f}:1")

    if set(variables["dark"]) != set(variables["light"]):
        errors.append("dark and light modes must expose identical variable keys")

    return errors


def main() -> int:
    try:
        errors = validate()
    except ValueError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    print(f"PASS: Copper manifest and {len(EXPECTED_KEYS)} variables per mode are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
