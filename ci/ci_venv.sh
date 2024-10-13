#!/bin/bash

VENV_DIR="ci_venv"
PACKAGES=("pylint" "black" "clang-format")

# Run check if python installed
check_python_installed() {
    if ! command -v python3 &> /dev/null; then
        echo "Python is NOT installed."
        echo "Please install Python here: https://www.python.org/downloads/"
        exit 1
    fi
}

check_packages_installed() {
    for pkg in "${PACKAGES[@]}"; do
        pip show "$pkg" > /dev/null 2>&1
        if [ $? -ne 0 ]; then
            pip install "$pkg"
        fi
    done
}

activate_venv() {
    os_name=$(uname)
    if [[ "$os_name" == "Linux" || "$os_name" == "Darwin" ]]; then
        source "$VENV_DIR/bin/activate"
    elif [[ "$os_name" == "CYGWIN"* || "$os_name" == "MINGW"* ]]; then
        source "$VENV_DIR/Scripts/activate"
    else
        echo "Error reading back OS, complain to Alex to fix :("
        exit 1
    fi
}

check_python_installed

if [ ! -d $VENV_DIR ]; then
    echo ===== CREATING CI_VENV =====

    python3 -m venv "$VENV_DIR"

    activate_venv

    python3 -m pip install --upgrade pip
    pip install pylint
    pip install black
    pip install clang-format

    echo ===== SETUP AND INSTALLATION OF PACKAGES COMPLETE =====
else
    echo ===== USING EXISTING CI_VENV =====

    activate_venv
    check_packages_installed
fi
