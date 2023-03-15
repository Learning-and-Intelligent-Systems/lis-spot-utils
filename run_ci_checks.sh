#!/bin/bash
mypy . --config-file mypy.ini
pytest . --pylint -m pylint --pylint-rcfile=.spot_utils_pylintrc
./run_autoformat.sh
