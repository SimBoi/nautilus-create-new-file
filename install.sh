#!/usr/bin/env bash
set -euo pipefail

ext_name=nautilus-create-new-file
repo_dir="$HOME/.local/share/nautilus-extensions/$ext_name"
ext_dir="$HOME/.local/share/nautilus-python/extensions"
repo_url="https://github.com/SimBoi/$ext_name"

mkdir -p "$ext_dir"
if [ -d "$repo_dir/.git" ]; then
  git -C "$repo_dir" pull --ff-only
else
  git clone --depth=1 "$repo_url" "$repo_dir"
fi

mkdir -p "$ext_dir"
ln -sf "$repo_dir/$ext_name.py" "$ext_dir/$ext_name.py"
ln -sfn "$repo_dir/po" "$ext_dir/$ext_name-translations"

echo "Create new file extension installed in $ext_dir, linking repo in $repo_dir."
echo "Restart nautilus with: nautilus -q"

