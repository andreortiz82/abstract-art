#!/usr/bin/env bash
# Install the abstract-art Cursor agent skill to ~/.cursor/skills/
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.cursor/skills/abstract-art"

mkdir -p "$HOME/.cursor/skills"
rm -rf "$DEST"
cp -r "$REPO_ROOT/.cursor/skills/abstract-art" "$DEST"

echo "Installed abstract-art skill to $DEST"
echo "Restart Cursor or open a new agent chat to pick it up."
