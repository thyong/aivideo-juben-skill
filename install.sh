#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
skills_dir=${CODEX_HOME:-"$HOME/.codex"}/skills
repair=0

if [ "${1:-}" = "--repair" ]; then
  repair=1
elif [ "$#" -gt 0 ]; then
  echo "Usage: $0 [--repair]" >&2
  exit 2
fi

mkdir -p "$skills_dir"

installed=0
for skill_path in "$repo_dir"/skills/*; do
  [ -d "$skill_path" ] || continue
  skill_name=$(basename "$skill_path")
  target_path="$skills_dir/$skill_name"
  if [ ! -f "$skill_path/SKILL.md" ]; then
    echo "Invalid skill, missing SKILL.md: $skill_path" >&2
    exit 1
  fi
  if [ -e "$target_path" ] || [ -L "$target_path" ]; then
    if [ -L "$target_path" ] && [ "$(readlink "$target_path")" = "$skill_path" ]; then
      echo "Already installed: $skill_name"
      continue
    fi
    if [ -L "$target_path" ] && [ "$repair" -eq 1 ]; then
      rm "$target_path"
    else
      echo "Refusing to replace existing skill: $target_path" >&2
      echo "If it is an outdated symlink, rerun with --repair." >&2
      exit 1
    fi
  fi
  ln -s "$skill_path" "$target_path"
  installed=$((installed + 1))
  echo "Installed: $skill_name"
done

echo "Skill repository: $repo_dir"
echo "Codex skill directory: $skills_dir"
echo "New links created: $installed"
echo "Run $repo_dir/doctor.sh to verify the installation."
echo "Then start a new Codex task so the skill list refreshes."
