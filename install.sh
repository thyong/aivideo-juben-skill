#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skills_dir=${CODEX_HOME:-"$HOME/.codex"}/skills

mkdir -p "$skills_dir"

for skill_path in "$repo_dir"/skills/*; do
  [ -d "$skill_path" ] || continue
  skill_name=$(basename "$skill_path")
  target_path="$skills_dir/$skill_name"
  if [ -e "$target_path" ] || [ -L "$target_path" ]; then
    if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$skill_path" ]; then
      continue
    fi
    echo "Refusing to replace existing skill: $target_path" >&2
    exit 1
  fi
  ln -s "$skill_path" "$target_path"
done

echo "Installed skills from $repo_dir"
