#!/usr/bin/env python3
"""Validate a standalone TKDRAMA original-story export."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_GLOBAL_MARKERS = (
    "TKDRAMA 剧本导出文件",
    "<<<故事概述>>>",
    "<<<故事概述结束>>>",
    "<<<故事角色>>>",
    "<<<故事角色结束>>>",
)

REQUIRED_PROMPT_FIELDS = (
    "描述：",
    "主体角色：",
    "镜头：",
    "光线：",
    "场景环境：",
    "画面风格：",
    "生成要求：",
)

FORBIDDEN_DEPENDENCIES = (
    "承接上一镜",
    "动作无缝衔接",
    "保持上一镜位置",
    "延续上一镜动作",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--min-shots", type=int)
    parser.add_argument("--max-shots", type=int)
    return parser.parse_args()


def fail(errors: list[str]) -> int:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    return 1


def main() -> int:
    args = parse_args()
    if not args.file.is_file():
        return fail([f"file not found: {args.file}"])

    text = args.file.read_text(encoding="utf-8-sig").replace("\r\n", "\n").replace("\r", "\n")
    errors: list[str] = []

    for marker in REQUIRED_GLOBAL_MARKERS:
        if marker not in text:
            errors.append(f"missing global marker: {marker}")

    blocks = re.findall(r"<<<分镜开始>>>\n(.*?)\n<<<分镜结束>>>", text, re.S)
    starts = text.count("<<<分镜开始>>>")
    ends = text.count("<<<分镜结束>>>")
    if starts != ends or len(blocks) != starts:
        errors.append(f"shot markers do not balance: starts={starts}, ends={ends}, parsed={len(blocks)}")

    if args.min_shots is not None and len(blocks) < args.min_shots:
        errors.append(f"shot count {len(blocks)} is below minimum {args.min_shots}")
    if args.max_shots is not None and len(blocks) > args.max_shots:
        errors.append(f"shot count {len(blocks)} exceeds maximum {args.max_shots}")

    numbers: list[int] = []
    filenames: list[str] = []
    for index, block in enumerate(blocks, start=1):
        number_match = re.search(r"^序号：(\d+)\s*$", block, re.M)
        filename_match = re.search(r"^文件名：(.+?)\s*$", block, re.M)
        roles_match = re.search(r"^对应角色：(\[.*\])\s*$", block, re.M)
        prompt_match = re.search(r"<<<图片提示词>>>\n(.*?)\n<<<图片提示词结束>>>", block, re.S)

        if not number_match:
            errors.append(f"shot {index}: missing numeric 序号")
        else:
            numbers.append(int(number_match.group(1)))

        if not filename_match:
            errors.append(f"shot {index}: missing 文件名")
        else:
            filenames.append(filename_match.group(1).strip())

        if not roles_match:
            errors.append(f"shot {index}: missing JSON 对应角色 list")
        else:
            try:
                roles = json.loads(roles_match.group(1))
                if not isinstance(roles, list):
                    raise ValueError("not a list")
            except (json.JSONDecodeError, ValueError) as exc:
                errors.append(f"shot {index}: invalid 对应角色 JSON: {exc}")

        if not prompt_match:
            errors.append(f"shot {index}: missing image-prompt block")
        else:
            prompt = prompt_match.group(1)
            for field in REQUIRED_PROMPT_FIELDS:
                if field not in prompt:
                    errors.append(f"shot {index}: missing prompt field {field}")

        if "<<<视频提示词>>>" not in block or "<<<视频提示词结束>>>" not in block:
            errors.append(f"shot {index}: missing video-prompt markers")

    expected_numbers = list(range(1, len(blocks) + 1))
    if numbers != expected_numbers:
        errors.append(f"shot numbers are not sequential: {numbers}")

    expected_filenames = [f"{number}.jpg" for number in expected_numbers]
    if filenames != expected_filenames:
        errors.append(f"filenames must follow shot order: {filenames}")

    for phrase in FORBIDDEN_DEPENDENCIES:
        if phrase in text:
            errors.append(f"explicit cross-clip dependency found: {phrase}")

    if errors:
        return fail(errors)

    print(f"TKDRAMA original-story validation passed: {args.file} ({len(blocks)} shots)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
