#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
python3 -m venv ./.venv --system-site-packages
echo "Virtual evnironment created"
source ./.venv/bin/activate
echo "Virtual enviornment activated"
pip install -r requirements.txt
echo CONNECTION_STRING= >> .env
echo "Dependencies installed"
sleep 5