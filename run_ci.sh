#!/bin/bash

# Run check if python installed
check_python_installed() {
    if ! command -v python3 &> /dev/null; then
        echo "Python is NOT installed."
        echo "Please install Python here: https://www.python.org/downloads/"
        exit 1
    fi
}

check_python_installed

VENV_DIR="ci_venv"

if [ ! -d $VENV_DIR ]; then
    echo ===== CREATING CI_VENV =====

    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"

    python3 -m pip install --upgrade pip
    pip install pylint
    pip install black
    
    echo ===== SETUP AND INSTALLATION OF PACKAGES COMPLETE =====
else
    echo ===== USING EXISTING CI_VENV =====
    source "$VENV_DIR/bin/activate"
fi

black . --exclude "ci_venv/"

echo ===== BLACK AUTOFORMATER COMPLETE =====

find . -name "*.py" -print0 | xargs -0 pylint --disable=

echo ===== PYLINT COMPLETE =====
