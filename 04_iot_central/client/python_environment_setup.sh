#!/bin/bash
# Setup Virtual Environment
echo "Python virtual environment creation script"
[[ ! -d .venv ]] \
&& python3 -m venv --prompt 04_iot_central ./.venv \
&& echo "Virtual environment created"

# Activate virtual env
source ./.venv/bin/activate
echo "Virtual environment activated"

# Install python dependencies
echo "Installing python dependencies..."
pip install -r requirements.txt
echo "Dependencies installed"

# Create .env file
[[ ! -e .env ]] && cat << EOF > .env
SCOPE_ID='PASTE-YOUR-SCOPE_ID-HERE'
GROUP_SYMMETRIC_KEY='PASTE-YOUR-GROUP_SYMMETRIC_KEY-HERE'
EOF

echo "Environment setup complete!"
sleep 5