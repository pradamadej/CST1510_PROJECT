#!/bin/bash

# Upgrade pip first
python -m pip install --upgrade pip

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Create default config if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    cat > .streamlit/config.toml << EOF
[server]
headless = true
port = \$PORT
enableCORS = false
enableXsrfProtection = false

[browser]
serverAddress = "0.0.0.0"
serverPort = 8501
EOF
fi