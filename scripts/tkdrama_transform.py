#!/usr/bin/env python3
"""Inspect, apply field replacements to, and validate TKDRAMA text exports."""

from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
from pathlib import Path


FIELDS = ("描述", "主体角色", "镜头", "光线", "场景环境", "画面风格", "生成要求")
FIELD_RE = re.compile(r"(" + "|".join(map(re.escape, FIELDS)) + r")：")
SHOT_RE = re.compile(r"<<<分镜开始>>>(.*?)<<<分镜结束>>>", re.S)
IMAGE_RE = re.compile(r"(<<<图片提示词>>>\s*)(.*?)(\s*<<<图片提示词结束>>>)", re.S)
SEQ_RE = re.compile(r"^序号：\s*(\d+)\s*$", re.M)
FILE_RE = re.compile(r"^文件名：\s*(.*?)\s*$", re.M)


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(codecs.BOM_UTF8)
    if bom:
        raw = raw[len(codecs.BOM_UTF8):]
    return raw.decode("utf-8"), bom


def write_text(path: Path, text: str, bom: bool) -> None:
    raw = text.encode("utf-8")
    if bom:
        raw = codecs.BOM_UTF8 + raw
    path.write_bytes(raw)


def parse_fields(prompt: str) -> tuple[dict[str, str], list[str]]:
    matches = list(FIELD_RE.finditer(prompt))
    values: dict[str, str] = {}
    order: list[str] = []
    for index, match in enumerate(matches):
        name = match.group(1)
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        values[name] = prompt[start:end].strip()
        order.append(name)
    return values, order


def shots(text: str) -> list[dict[str, object]]:
    result = []
    for match in SHOT_RE.finditer(text):
        body = match.group(1)
        seq_match = SEQ_RE.search(body)
        image_match = IMAGE_RE.search(body)
        if not seq_match or not image_match:
            raise ValueError("Malformed shot: missing 序号 or 图片提示词 block")
        seq = seq_match.group(1)
        filename_match = FILE_RE.search(body)
        prompt = image_match.group(2).strip()
        field_values, order = parse_fields(prompt)
        result.append({
            "seq": seq,
            "filename": filename_match.group(1) if filename_match else "",
            "body": body,
            "prompt": prompt,
            "fields": field_values,
            "order": order,
        })
    return result


def replace_prompt_fields(prompt: str, replacements: dict[str, str]) -> str:
    unknown = set(replacements) - set(FIELDS)
    if unknown:
        raise ValueError(f"Unknown fields: {sorted(unknown)}")
    matches = list(FIELD_RE.finditer(prompt))
    present = {m.group(1) for m in matches}
    missing = set(replacements) - present
    if missing:
        raise ValueError(f"Fields absent from prompt: {sorted(missing)}")
    pieces: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        name = match.group(1)
        value_start = match.end()
        value_end = matches[index + 1].start() if index + 1 < len(matches) else len(prompt)
        pieces.append(prompt[cursor:value_start])
        if name in replacements:
            old_value = prompt[value_start:value_end]
            trailing = old_value[len(old_value.rstrip()):]
            preserved_suffix = ""
            if name == "画面风格":
                suffix_markers = ("[反推后生成的图片将用于", "反推后生成的图片将用于")
                positions = [old_value.find(marker) for marker in suffix_markers]
                positions = [position for position in positions if position >= 0]
                if positions:
                    suffix_start = min(positions)
                    preserved_suffix = old_value[suffix_start:].rstrip()
            pieces.append(str(replacements[name]).strip() + preserved_suffix + trailing)
        else:
            pieces.append(prompt[value_start:value_end])
        cursor = value_end
    pieces.append(prompt[cursor:])
    return "".join(pieces)


def load_plan(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data.get("shots"), dict):
        raise ValueError("Plan must contain an object named 'shots'")
    global_fields = data.get("global_fields", {})
    if not isinstance(global_fields, dict):
        raise ValueError("'global_fields' must be an object when present")
    unknown = set(global_fields) - set(FIELDS)
    if unknown:
        raise ValueError(f"Unknown global fields: {sorted(unknown)}")
    return data


def command_inspect(source: Path) -> int:
    text, bom = read_text(source)
    inventory = []
    for shot in shots(text):
        inventory.append({
            "seq": shot["seq"],
            "filename": shot["filename"],
            "fields": shot["order"],
            "scene": shot["fields"].get("场景环境", ""),
            "light": shot["fields"].get("光线", ""),
        })
    print(json.dumps({"utf8_bom": bom, "shot_count": len(inventory), "shots": inventory}, ensure_ascii=False, indent=2))
    return 0


def apply_plan(text: str, plan: dict) -> str:
    requested = set(plan["shots"])
    global_fields = plan.get("global_fields", {})
    seen: set[str] = set()

    def replace_shot(match: re.Match[str]) -> str:
        body = match.group(1)
        seq_match = SEQ_RE.search(body)
        if not seq_match:
            raise ValueError("Shot missing sequence")
        seq = seq_match.group(1)
        if seq not in requested and not global_fields:
            return match.group(0)
        item = plan["shots"].get(seq, {})
        local_fields = item.get("fields", {})
        if not isinstance(local_fields, dict):
            raise ValueError(f"Shot {seq} fields must be an object")
        replacements = {**global_fields, **local_fields}
        if not replacements:
            raise ValueError(f"Shot {seq} has no field replacements")
        image_match = IMAGE_RE.search(body)
        if not image_match:
            raise ValueError(f"Shot {seq} missing image prompt")
        new_prompt = replace_prompt_fields(image_match.group(2), replacements)
        new_body = body[:image_match.start(2)] + new_prompt + body[image_match.end(2):]
        if seq in requested:
            seen.add(seq)
        return "<<<分镜开始>>>" + new_body + "<<<分镜结束>>>"

    output = SHOT_RE.sub(replace_shot, text)
    missing = requested - seen
    if missing:
        raise ValueError(f"Plan references missing shots: {sorted(missing)}")
    return output


def write_summary(path: Path, source: Path, output: Path, plan: dict) -> None:
    global_fields = list(plan.get("global_fields", {}).keys())
    lines = [
        "# 海洋风格转换修改总结",
        "",
        f"- 原文件：`{source.name}`",
        f"- 转换文件：`{output.name}`",
        f"- 全局统一字段：{'、'.join(global_fields) if global_fields else '无'}",
        f"- 单独调整分镜数：{len(plan['shots'])}",
        "",
        "| 分镜 | 修改字段 | 原场景 | 转换后场景 | 修改原因 | 叙事保持检查 |",
        "|---:|---|---|---|---|---|",
    ]
    for seq in sorted(plan["shots"], key=lambda value: int(value)):
        item = plan["shots"][seq]
        fields = "、".join(item.get("fields", {}).keys())
        summary = item.get("summary", {})
        cells = [
            seq,
            fields,
            summary.get("scene_before", "未说明"),
            summary.get("scene_after", "未说明"),
            summary.get("reason", "未说明"),
            summary.get("narrative_check", "未说明"),
        ]
        cells = [str(cell).replace("|", "\\|").replace("\n", " ") for cell in cells]
        lines.append("| " + " | ".join(cells) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def command_apply(source: Path, plan_path: Path, output: Path, summary: Path | None) -> int:
    text, bom = read_text(source)
    plan = load_plan(plan_path)
    converted = apply_plan(text, plan)
    write_text(output, converted, bom)
    if summary:
        write_summary(summary, source, output, plan)
    global_count = len(shots(text)) if plan.get("global_fields") else 0
    print(f"Applied global fields to {global_count} shots and local replacements to {len(plan['shots'])} shots: {output}")
    return 0


def command_validate(source: Path, output: Path, plan_path: Path) -> int:
    original_text, original_bom = read_text(source)
    output_text, output_bom = read_text(output)
    plan = load_plan(plan_path)
    expected = apply_plan(original_text, plan)
    errors: list[str] = []
    if original_bom != output_bom:
        errors.append("UTF-8 BOM preservation mismatch")
    if output_text != expected:
        errors.append("Output contains changes not represented by the replacement plan")
    original_shots = shots(original_text)
    output_shots = shots(output_text)
    if len(original_shots) != len(output_shots):
        errors.append("Shot count changed")
    for before, after in zip(original_shots, output_shots):
        if before["seq"] != after["seq"] or before["filename"] != after["filename"]:
            errors.append(f"Shot identity changed near {before['seq']}")
        if before["order"] != after["order"]:
            errors.append(f"Field order changed in shot {before['seq']}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Validation passed: {len(original_shots)} shots, structure preserved")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("source", type=Path)
    apply = sub.add_parser("apply")
    apply.add_argument("source", type=Path)
    apply.add_argument("plan", type=Path)
    apply.add_argument("output", type=Path)
    apply.add_argument("--summary", type=Path)
    validate = sub.add_parser("validate")
    validate.add_argument("source", type=Path)
    validate.add_argument("output", type=Path)
    validate.add_argument("plan", type=Path)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        if args.command == "inspect":
            return command_inspect(args.source)
        if args.command == "apply":
            return command_apply(args.source, args.plan, args.output, args.summary)
        return command_validate(args.source, args.output, args.plan)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
