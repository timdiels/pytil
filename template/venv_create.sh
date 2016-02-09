#!/bin/sh

# Create python virtual environment to develop in

set -e

[ -d venv ] || python -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade wheel
pip install -r requirements.txt
pip install -r extra_requirements.txt
pip install '.[test,dev]'