#!/bin/bash

VENV_DIR="ci_venv"

path=${1:-.}

if [ ! -d $VENV_DIR ]; then
    ./ci/ci_venv.sh
else
    echo ===== USING EXISTING CI_VENV =====
fi

os_name=$(uname)
if [[ "$os_name" == "Linux" || "$os_name" == "Darwin" ]]; then
    source "$VENV_DIR/bin/activate"
elif [[ "$os_name" == "CYGWIN"* || "$os_name" == "MINGW"* ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo "Error reading back OS, complain to Alex to fix :("
fi

black $path --exclude "ci_venv/"

echo ===== BLACK AUTOFORMATER COMPLETE =====

find $path -name "*.py" -print0 | xargs -0 pylint --rcfile=ci/.pylintrc --disable=

echo ===== PYLINT COMPLETE =====

find $path -name '*.ino' -exec clang-format -i {} \;

echo ===== CLANG-FORMAT COMPLETE =====
