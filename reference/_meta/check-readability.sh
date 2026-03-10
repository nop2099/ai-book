#!/bin/bash
# Check reading level and vocabulary of reference pages
# Thin wrapper — activates venv and runs the Python script.
# Usage: bash reference/_meta/check-readability.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Create venv + install textstat if needed
if [ ! -d "$SCRIPT_DIR/.venv" ]; then
  echo "Setting up readability checker..."
  uv venv "$SCRIPT_DIR/.venv" --quiet
  source "$SCRIPT_DIR/.venv/bin/activate"
  uv pip install textstat --quiet
else
  source "$SCRIPT_DIR/.venv/bin/activate"
fi

python3 "$SCRIPT_DIR/check-readability.py" "$@"
