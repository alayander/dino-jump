#!/bin/bash

VENV_DIR="ci_venv"

if [ ! -d $VENV_DIR ]; then
    ./ci_venv.sh
else
    echo ===== USING EXISTING CI_VENV =====
fi

source "$VENV_DIR/bin/activate"

black . --exclude "ci_venv/"

echo ===== BLACK AUTOFORMATER COMPLETE =====

find . -name "*.py" -print0 | xargs -0 pylint --disable=

echo ===== PYLINT COMPLETE =====
