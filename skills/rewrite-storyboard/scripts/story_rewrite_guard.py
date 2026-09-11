#!/usr/bin/env python3
"""Inspect and structurally validate confirmed TKDRAMA story rewrites."""

from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
from pathlib import Path


SHOT_RE = re.compile(r"<<<分镜开始>>>(.*?)<<<分镜结束>>>", re.S)
SEQ_RE = re.compile(r"^序号：\s*(\d+)\s*$", re.M)
FILE_RE = re.compile(r"^文件名：\s*(.*?)\s*$", re.M)
ROLE_LINE_RE = re.compile(r'^-\s*\{.*?"source"\s*:\s*"([^"]+)".*?\}\s*$', re.M)
USED_ROLES_RE = re.compile(r"^对应角色：\s*(\[[^\n\r]*\])\s*$", re.M)
STORY_RE = re.compile(r"<<<故事概述>>>\s*(.*?)\s*<<<故事概述结束>>>", re.S)
CHARACTERS_RE = re.compile(r"<<<故事角色>>>\s*(.*?)\s*<<<故事角色结束>>>", re.S)
IMAGE_RE = re.compile(r"<<<图片提示词>>>\s*(.*?)\s*<<<图片提示词结束>>>", re.S)
VIDEO_RE = re.compile(r"<<<视频提示词>>>\s*(.*?)\s*<<<视频提示词结束>>>", re.S)


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(codecs.BOM_UTF8)
    if bom:
        raw = raw[len(codecs.BOM_UTF8):]
    return raw.decode("utf-8"), bom


def parse_shots(text: str) -> list[dict[str, object]]:
    result: list[dict[str, object]] = []
    for match in SHOT_RE.finditer(text):
        body = match.group(1)
        seq_match = SEQ_RE.search(body)
        if not seq_match:
            raise ValueError("Malformed shot: missing 序号")
        used_match = USED_ROLES_RE.search(body)
        if not used_match:
            raise ValueError(f"Shot {seq_match.group(1)} missing 对应角色")
        try:
            used_roles = json.loads(used_match.group(1))
        except json.JSONDecodeError as exc:
            raise ValueError(f"Shot {seq_match.group(1)} has invalid 对应角色 JSON") from exc
        if not isinstance(used_roles, list) or not all(isinstance(item, str) for item in used_roles):
            raise ValueError(f"Shot {seq_match.group(1)} 对应角色 must be a string array")
        image_match = IMAGE_RE.search(body)
        video_match = VIDEO_RE.search(body)
        result.append({
            "seq": seq_match.group(1),
            "filename": FILE_RE.search(body).group(1) if FILE_RE.search(body) else "",
            "roles": used_roles,
            "image_prompt": image_match.group(1).strip() if image_match else None,
            "video_prompt": video_match.group(1).strip() if video_match else None,
        })
    if not result:
        raise ValueError("No TKDRAMA shot blocks found")
    return result


def declared_roles(text: str) -> list[str]:
    match = CHARACTERS_RE.search(text)
    if not match:
        raise ValueError("Missing 故事角色 block")
    roles = ROLE_LINE_RE.findall(match.group(1))
    if not roles:
        raise ValueError("No valid source roles found in 故事角色 block")
    return roles


def source_inventory(path: Path) -> dict[str, object]:
    text, bom = read_text(path)
    story_match = STORY_RE.search(text)
    if not story_match or not story_match.group(1).strip():
        raise ValueError("Missing or empty 故事概述 block")
    items = parse_shots(text)
    return {
        "utf8_bom": bom,
        "shot_count": len(items),
        "story_characters": declared_roles(text),
        "shots": [{
            "seq": item["seq"],
            "filename": item["filename"],
            "roles": item["roles"],
            "has_image_prompt": bool(item["image_prompt"]),
            "has_video_prompt": bool(item["video_prompt"]),
        } for item in items],
    }


def load_plan(path: Path) -> dict[str, object]:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    approval = data.get("approval")
    if not isinstance(approval, dict):
        raise ValueError("Plan missing approval object")
    if approval.get("direction_confirmed") is not True:
        raise ValueError("Direction is not recorded as confirmed")
    if approval.get("shot_plan_confirmed") is not True:
        raise ValueError("Shot plan is not recorded as confirmed")
    for key in ("source_shot_count", "output_shot_count"):
        if not isinstance(data.get(key), int) or data[key] <= 0:
            raise ValueError(f"Plan field {key} must be a positive integer")
    if not isinstance(data.get("direction"), str) or not data["direction"].strip():
        raise ValueError("Plan must record the confirmed direction")
    changes = data.get("changed_shots")
    if not isinstance(changes, dict) or not changes:
        raise ValueError("Plan must contain non-empty changed_shots")
    for key, value in changes.items():
        if not str(key).isdigit() or not isinstance(value, str) or not value.strip():
            raise ValueError("Each changed_shots entry needs a numeric shot and concise change")
    for key in ("required_terms", "forbidden_residue"):
        value = data.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ValueError(f"Plan field {key} must be an array of non-empty strings")
    return data


def command_inspect(source: Path) -> int:
    print(json.dumps(source_inventory(source), ensure_ascii=False, indent=2))
    return 0


def command_validate(source: Path, output: Path, plan_path: Path) -> int:
    if source.resolve() == output.resolve():
        raise ValueError("Output must not overwrite the source")
    plan = load_plan(plan_path)
    source_text, source_bom = read_text(source)
    output_text, output_bom = read_text(output)
    source_shots = parse_shots(source_text)
    output_shots = parse_shots(output_text)
    errors: list[str] = []

    if plan["source_shot_count"] != len(source_shots):
        errors.append("Plan source_shot_count does not match source")
    if plan["output_shot_count"] != len(output_shots):
        errors.append("Plan output_shot_count does not match output")
    if source_bom != output_bom:
        errors.append("UTF-8 BOM preservation mismatch")
    if output_text == source_text:
        errors.append("Output is identical to source")

    output_sequences = [int(item["seq"]) for item in output_shots]
    if len(output_sequences) != len(set(output_sequences)):
        errors.append("Output contains duplicate shot numbers")
    if output_sequences != list(range(1, len(output_shots) + 1)):
        errors.append("Output shot numbers are not continuous from 1")

    if len(source_shots) == len(output_shots):
        for before, after in zip(source_shots, output_shots):
            if before["filename"] != after["filename"]:
                errors.append(f"Image filename changed at shot {after['seq']}")

    story_match = STORY_RE.search(output_text)
    if not story_match or not story_match.group(1).strip():
        errors.append("Output story overview is missing or empty")

    try:
        roles = set(declared_roles(output_text))
    except ValueError as exc:
        roles = set()
        errors.append(str(exc))
    used_roles = {role for item in output_shots for role in item["roles"]}
    undefined = sorted(used_roles - roles)
    if undefined:
        errors.append(f"Undefined roles in shots: {', '.join(undefined)}")

    for item in output_shots:
        if item["image_prompt"] is None:
            errors.append(f"Shot {item['seq']} missing 图片提示词 block")
        elif not item["image_prompt"]:
            errors.append(f"Shot {item['seq']} has empty 图片提示词")
        if item["video_prompt"] is None:
            errors.append(f"Shot {item['seq']} missing 视频提示词 block")

    output_seq_strings = {item["seq"] for item in output_shots}
    unknown_changes = sorted(set(plan["changed_shots"]) - output_seq_strings, key=int)
    if unknown_changes:
        errors.append(f"Plan references missing output shots: {', '.join(unknown_changes)}")

    for term in plan.get("required_terms", []):
        if term not in output_text:
            errors.append(f"Required approved term missing: {term}")
    for term in plan.get("forbidden_residue", []):
        if term in output_text:
            errors.append(f"Obsolete residue remains: {term}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"Validation passed: {len(output_shots)} shots, approvals recorded, "
        "roles resolved, structure and literal continuity checks passed"
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    inspect_cmd = sub.add_parser("inspect")
    inspect_cmd.add_argument("source", type=Path)
    validate_cmd = sub.add_parser("validate")
    validate_cmd.add_argument("source", type=Path)
    validate_cmd.add_argument("output", type=Path)
    validate_cmd.add_argument("plan", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "inspect":
            return command_inspect(args.source)
        return command_validate(args.source, args.output, args.plan)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
