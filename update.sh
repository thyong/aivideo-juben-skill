#!/bin/sh
set -eu

repo_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

if [ ! -d "$repo_dir/.git" ]; then
  echo "Not a Git checkout: $repo_dir" >&2
  exit 1
fi

if [ -n "$(git -C "$repo_dir" status --porcelain)" ]; then
  echo "Repository has local changes; commit or discard them before updating:" >&2
  git -C "$repo_dir" status --short >&2
  exit 1
fi

git -C "$repo_dir" pull --ff-only
"$repo_dir/install.sh"
"$repo_dir/doctor.sh"

echo "Skills updated successfully. Start a new Codex task to use the refreshed versions."
