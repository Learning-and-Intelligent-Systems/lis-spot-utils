#!/bin/bash
mypy . --config-file mypy.ini
<<<<<<< HEAD
pytest . --pylint -m pylint --pylint-rcfile=.spot_utils_pylintrc
=======
pytest . --pylint -m pylint --pylint-rcfile=.pylint_rc
>>>>>>> fn issues
./run_autoformat.sh
