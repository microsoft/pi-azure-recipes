#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
[ ! -d .venv ] \
    && python3 -m venv --prompt 02_c2d ./.venv \
    && echo "Virtual environment created"
source ./.venv/bin/activate
echo "Virtual environment activated"
pip install -r requirements.txt
echo "Dependencies installed"
sleep 5