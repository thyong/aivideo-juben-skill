#!/usr/bin/env python3
"""Inspect and enforce exact, approved animal-character substitutions."""

from __future__ import annotations

import argparse
import codecs
import json
import re
import sys
from pathlib import Path


SHOT_RE = re.compile(r"<<<分镜开始>>>(.*?)<<<分镜结束>>>", re.S)
SEQ_RE = re.compile(r"^序号：\s*(\d+)\s*$", re.M)
ROLE_RE = re.compile(r'"source"\s*:\s*"([^"]+)"')
USED_ROLES_RE = re.compile(r"^对应角色：\s*(\[[^\n\r]*\])\s*$", re.M)


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(codecs.BOM_UTF8)
    if bom:
        raw = raw[len(codecs.BOM_UTF8):]
    return raw.decode("utf-8"), bom


def shots(text: str) -> list[tuple[int, str]]:
    result: list[tuple[int, str]] = []
    for match in SHOT_RE.finditer(text):
        seq = SEQ_RE.search(match.group(1))
        if not seq:
            raise ValueError("Malformed shot: missing 序号")
        result.append((int(seq.group(1)), match.group(1)))
    if not result:
        raise ValueError("No TKDRAMA shot blocks found")
    return result


def inspect_source(path: Path) -> dict[str, object]:
    text, bom = read_text(path)
    parsed = shots(text)
    used: list[dict[str, object]] = []
    for seq, body in parsed:
        match = USED_ROLES_RE.search(body)
        value = json.loads(match.group(1)) if match else []
        used.append({"shot": seq, "corresponding_roles": value})
    return {
        "utf8_bom": bom,
        "shot_count": len(parsed),
        "declared_role_names": sorted(set(ROLE_RE.findall(text))),
        "shots": used,
    }


def load_plan(path: Path) -> dict[str, object]:
    plan = json.loads(path.read_text(encoding="utf-8-sig"))
    approval = plan.get("approval")
    if not isinstance(approval, dict) or approval.get("mapping_confirmed") is not True:
        raise ValueError("Role mapping is not recorded as confirmed")
    count = plan.get("source_shot_count")
    if not isinstance(count, int) or count <= 0:
        raise ValueError("source_shot_count must be a positive integer")
    mappings = plan.get("role_mappings")
    if not isinstance(mappings, list) or not mappings:
        raise ValueError("role_mappings must be a non-empty array")
    seen: set[str] = set()
    for item in mappings:
        if not isinstance(item, dict):
            raise ValueError("Each role mapping must be an object")
        source, target = item.get("source"), item.get("target")
        if not isinstance(source, str) or not source or not isinstance(target, str) or not target:
            raise ValueError("Each role mapping needs non-empty source and target strings")
        if source == target:
            raise ValueError(f"Redundant role mapping: {source}")
        if source in seen:
            raise ValueError(f"Duplicate role mapping source: {source}")
        seen.add(source)
    replacements = plan.get("approved_replacements", [])
    if not isinstance(replacements, list):
        raise ValueError("approved_replacements must be an array")
    for item in replacements:
        if not isinstance(item, dict):
            raise ValueError("Each approved replacement must be an object")
        source, target = item.get("source"), item.get("target")
        if not isinstance(source, str) or not source or not isinstance(target, str):
            raise ValueError("Each approved replacement needs exact source and target strings")
        if source == target:
            raise ValueError("Approved replacement source and target must differ")
        if "count" in item and (not isinstance(item["count"], int) or item["count"] <= 0):
            raise ValueError("Approved replacement count must be a positive integer")
    return plan


def apply_plan(source_text: str, plan: dict[str, object]) -> str:
    mapping = {item["source"]: item["target"] for item in plan["role_mappings"]}
    missing = [source for source in mapping if source not in source_text]
    if missing:
        raise ValueError(f"Mapped source literals not found: {', '.join(missing)}")
    pattern = re.compile("|".join(re.escape(key) for key in sorted(mapping, key=len, reverse=True)))
    expected = pattern.sub(lambda match: mapping[match.group(0)], source_text)
    for item in plan.get("approved_replacements", []):
        actual_count = expected.count(item["source"])
        requested_count = item.get("count", actual_count)
        if actual_count != requested_count:
            raise ValueError(
                f"Approved literal occurrence mismatch: expected {requested_count}, found {actual_count}"
            )
        expected = expected.replace(item["source"], item["target"])
    return expected


def write_output(source: Path, output: Path, plan_path: Path) -> int:
    if source.resolve() == output.resolve():
        raise ValueError("Output must not overwrite the source")
    if output.exists():
        raise ValueError("Output already exists")
    source_text, source_bom = read_text(source)
    plan = load_plan(plan_path)
    source_shots = shots(source_text)
    if plan["source_shot_count"] != len(source_shots):
        raise ValueError("Plan source_shot_count does not match source")
    output_text = apply_plan(source_text, plan)
    payload = output_text.encode("utf-8")
    if source_bom:
        payload = codecs.BOM_UTF8 + payload
    output.write_bytes(payload)
    print(f"Created exact-conversion output: {output}")
    return 0


def validate(source: Path, output: Path, plan_path: Path) -> int:
    if source.resolve() == output.resolve():
        raise ValueError("Output must not overwrite the source")
    source_text, source_bom = read_text(source)
    output_text, output_bom = read_text(output)
    plan = load_plan(plan_path)
    source_shots = shots(source_text)
    if plan["source_shot_count"] != len(source_shots):
        raise ValueError("Plan source_shot_count does not match source")
    if source_bom != output_bom:
        raise ValueError("UTF-8 BOM state changed")
    expected = apply_plan(source_text, plan)
    if output_text != expected:
        raise ValueError("Output contains a change outside the confirmed exact replacements")
    output_shots = shots(output_text)
    if [seq for seq, _ in source_shots] != [seq for seq, _ in output_shots]:
        raise ValueError("Shot count or sequence changed")
    print(
        f"Validation passed: {len(output_shots)} shots; output contains only confirmed exact replacements"
    )
    return 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser()
    commands = root.add_subparsers(dest="command", required=True)
    inspect_cmd = commands.add_parser("inspect")
    inspect_cmd.add_argument("source", type=Path)
    apply_cmd = commands.add_parser("apply")
    apply_cmd.add_argument("source", type=Path)
    apply_cmd.add_argument("output", type=Path)
    apply_cmd.add_argument("plan", type=Path)
    validate_cmd = commands.add_parser("validate")
    validate_cmd.add_argument("source", type=Path)
    validate_cmd.add_argument("output", type=Path)
    validate_cmd.add_argument("plan", type=Path)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        if args.command == "inspect":
            print(json.dumps(inspect_source(args.source), ensure_ascii=False, indent=2))
            return 0
        if args.command == "apply":
            return write_output(args.source, args.output, args.plan)
        return validate(args.source, args.output, args.plan)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
