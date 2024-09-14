The scripts in this directory are meant to be run from the root directory of the repository: `./ci/{script}`

- run_ci.sh {path}
    - This script runs a python linter and autoformatter
    - {path} can be supplied to run the ci suite on a specific directory
- setup_pre-commit.sh
    - This script sets up a pre-commit git hook using the `pre-commit` file in this directory
- ci_venv.sh
    - This script is a helper script to set up the virtual environment and install the necessary packages

**After setting the pre-commit, it can be bypassed by adding `--no-verify` to git commit command**
