# lis-spot-utils
A number of helpful utilities for doing cool things with the Boston Dynamics Spot Robot!

## Installation
(Note: Performing the installation in a separate virtualenv or conda environment is
recommended!)
Users should just be able to run `pip install -e .` 
Developers should run `pip install -e .[develop]`

## Contributing
- Run pip install -e .[develop] to install all dependencies for development.
- You can't push directly to master. Make a new branch in this repository (don't use a fork, since that will not properly trigger the checks when you make a PR). When your code is ready for review, make a PR and request reviews from the appropriate people.
- To merge a PR, you need at least one approval, and you have to pass the 2 checks defined in .github/workflows/ci.yml, which you can run automatically with `./run_ci_checks.sh`, or individually as follows:
- mypy . --config-file mypy.ini
- ./run_autoformat.sh
