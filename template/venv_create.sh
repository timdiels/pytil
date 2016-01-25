#!/bin/sh

# Create python virtual environment to develop in

set -e

rm -rf venv
python3.4 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install --upgrade setuptools
pip install --upgrade wheel
pip install -r requirements.txt
pip install -r extra_requirements.txt
pip install '.[test,dev]'
