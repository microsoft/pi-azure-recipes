#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
python -m venv ./.venv
echo "Virtual evnironment created"
source ./.venv/Scripts/activate
echo "Virtual enviornment activated"
pip install -r requirements.txt
echo CONNECTION_STRING= >> .env
echo "Dependencies installed"
sleep 5