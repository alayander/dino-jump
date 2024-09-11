#!/bin/bash

GIST_RAW_URL="https://gist.githubusercontent.com/alayander/c7481150e7c2daf0a38dfa05dfd4d982/raw/dinojump_pre-commit"
HOOKS_DIR=".git/hooks"
HOOK_FILE="pre-commit"

curl -s -o "$HOOKS_DIR/$HOOK_FILE" "$GIST_RAW_URL"

chmod +x "$HOOKS_DIR/$HOOK_FILE"

echo "Hook installed successfully."
