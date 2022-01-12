#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
[ ! -d .venv ] \
    && python3 -m venv --prompt 04_iot_central ./.venv \
    && echo "Virtual environment created"

source ./.venv/bin/activate
echo "Virtual environment activated"
pip install -r requirements.txt
echo SCOPE_ID= >> .env
echo GROUP_SYMMETRIC_KEY= >> .env
echo "Dependencies installed"
sleep 5