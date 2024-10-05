#!/bin/bash

VENV_DIR="ci_venv"

# Run check if python installed
check_python_installed() {
    if ! command -v python3 &> /dev/null; then
        echo "Python is NOT installed."
        echo "Please install Python here: https://www.python.org/downloads/"
        exit 1
    fi
}

check_python_installed

echo ===== CREATING CI_VENV =====

python3 -m venv "$VENV_DIR"

os_name=$(uname)
if [[ "$os_name" == "Linux" || "$os_name" == "Darwin" ]]; then
    source "$VENV_DIR/bin/activate"
elif [[ "$os_name" == "CYGWIN"* || "$os_name" == "MINGW"* ]]; then
    source "$VENV_DIR/Scripts/activate"
else
    echo "Error reading back OS, complain to Alex to fix :("
    exit 1
fi

python3 -m pip install --upgrade pip
pip install pylint
pip install black
pip install clang-format

echo ===== SETUP AND INSTALLATION OF PACKAGES COMPLETE =====
