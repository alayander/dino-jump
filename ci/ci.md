The scripts in this directory are meant to be run from the root directory of the repository: `./ci/{script}`

- run_ci.sh
    - This script runs a python linter and autoformatter
- setup_pre-commit.sh
    - This script sets up a pre-commit git hook using the `pre-commit` file in this directory
- ci_venv.sh
    - This script is a helper script to set up the virtual environment and install the necessary packages
