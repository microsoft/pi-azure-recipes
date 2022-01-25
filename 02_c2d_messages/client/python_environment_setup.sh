#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
[[ ! -d .venv ]] \
&& python3 -m venv --prompt 02_c2d ./.venv \
&& echo "Virtual environment created"

# Activate virtual environment
source ./.venv/bin/activate
echo "Virtual environment activated"

# Install dependencies
echo "Installing python dependencies..."
pip install -r requirements.txt
echo "Dependencies installed"

# Create .env file
[[ ! -e .env ]] && cat << EOF > .env
CONNECTION_STRING='YOUR-DEVICE-CONNECTION-STRING'
EOF
echo "Environment setup complete!"

sleep 5