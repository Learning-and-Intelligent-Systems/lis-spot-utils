#!/bin/bash
mypy . --config-file mypy.ini
./run_autoformat.sh
