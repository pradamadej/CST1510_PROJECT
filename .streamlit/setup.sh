#!/bin/bash

# Upgrade pip first
python -m pip install --upgrade pip

# Install requirements
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p .streamlit