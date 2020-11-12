#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
python -m venv ./.venv --system-site-packages
echo "Virtual evnironment created"
source ./.venv/bin/activate
echo "Virtual enviornment activated"
pip install -r requirements.txt
echo SUBSCRIPTION_KEY= >> .env
echo ENDPOINT= >>> .env
echo "Dependencies installed"
sleep 5