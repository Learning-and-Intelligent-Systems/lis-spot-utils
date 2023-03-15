#!/bin/bash
mypy . --config-file mypy.ini
pytest . --pylint -m pylint --pylint-rcfile=.pylintrc
./run_autoformat.sh
