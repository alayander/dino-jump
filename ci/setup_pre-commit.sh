#!/bin/bash

LOCAL_SCRIPT_PATH="ci/pre-commit"
HOOKS_DIR=".git/hooks"
HOOK_FILE="pre-commit"

cp "$LOCAL_SCRIPT_PATH" "$HOOKS_DIR/$HOOK_FILE"

chmod +x "$HOOKS_DIR/$HOOK_FILE"

echo "Hook installed successfully."
