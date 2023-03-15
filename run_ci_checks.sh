#!/bin/bash
mypy . --config-file mypy.ini
pytest . --pylint -m pylint --pylint-rcfile=.pylint_rc
./run_autoformat.sh
