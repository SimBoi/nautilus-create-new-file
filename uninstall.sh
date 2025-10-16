#!/usr/bin/env bash
set -euo pipefail

ext_name=nautilus-create-new-file
repo_dir="$HOME/.local/share/nautilus-extensions/$ext_name"
ext_dir="$HOME/.local/share/nautilus-python/extensions"
repo_url="https://github.com/SimBoi/$ext_name"

rm -f "$ext_dir/$ext_name.py"
rm -f "$ext_dir/$ext_name-translations" #symlink
rm -rf "$repo_dir"

echo "Create new file extension uninstalled from $ext_dir, removed linked repo from $repo_dir."
echo "Restart nautilus with: nautilus -q"

