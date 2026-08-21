#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skills_dir=${CODEX_HOME:-"$HOME/.codex"}/skills
failed=0

check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "OK command: $1"
  else
    echo "MISSING command: $1" >&2
    failed=1
  fi
}

check_command git
check_command python3

for skill_path in "$repo_dir"/skills/*; do
  [ -d "$skill_path" ] || continue
  skill_name=$(basename "$skill_path")
  target_path="$skills_dir/$skill_name"

  if [ ! -f "$skill_path/SKILL.md" ]; then
    echo "INVALID skill, missing SKILL.md: $skill_name" >&2
    failed=1
    continue
  fi

  if [ ! -L "$target_path" ]; then
    echo "NOT INSTALLED: $skill_name" >&2
    failed=1
    continue
  fi

  if [ "$(readlink "$target_path")" != "$skill_path" ]; then
    echo "WRONG LINK: $target_path -> $(readlink "$target_path")" >&2
    failed=1
    continue
  fi

  echo "OK skill: $skill_name"
done

if [ "$failed" -ne 0 ]; then
  echo "Skill deployment check failed." >&2
  exit 1
fi

echo "Skill deployment check passed."
