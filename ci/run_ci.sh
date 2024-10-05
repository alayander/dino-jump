#!/bin/bash

path=${1:-.}

source ci/ci_venv.sh

black $path --exclude "ci_venv/"

echo ===== BLACK AUTOFORMATER COMPLETE =====

find $path -name "*.py" -print0 | xargs -0 pylint --rcfile=ci/.pylintrc --disable=

echo ===== PYLINT COMPLETE =====

find $path -name '*.ino' -exec clang-format -i {} \;

echo ===== CLANG-FORMAT COMPLETE =====
