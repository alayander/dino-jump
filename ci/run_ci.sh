#!/bin/bash

VENV_DIR="ci_venv"

path=${1:-.}

if [ ! -d $VENV_DIR ]; then
    ./ci/ci_venv.sh
else
    echo ===== USING EXISTING CI_VENV =====
fi

source "$VENV_DIR/bin/activate"

black $path --exclude "ci_venv/"

echo ===== BLACK AUTOFORMATER COMPLETE =====

find $path -name "*.py" -print0 | xargs -0 pylint --rcfile=ci/.pylintrc --disable=

echo ===== PYLINT COMPLETE =====

find $path -name '*.ino' -exec clang-format -i {} \;

echo ===== CLANG-FORMAT COMPLETE =====
