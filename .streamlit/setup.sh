#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p .streamlit

# Create default config if it doesn't exist
if [ ! -f .streamlit/config.toml ]; then
    echo "[server]" > .streamlit/config.toml
    echo "headless = true" >> .streamlit/config.toml
    echo "port = \$PORT" >> .streamlit/config.toml
    echo "enableCORS = false" >> .streamlit/config.toml
    echo "enableXsrfProtection = false" >> .streamlit/config.toml
fi