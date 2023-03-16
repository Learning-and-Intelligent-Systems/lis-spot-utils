#!/bin/bash
python -m black .
docformatter -i -r . --exclude venv
isort . --split-on-trailing-comma
