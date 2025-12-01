#!/bin/bash

# Force Python 3.9 if available
python --version

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install requirements
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p .streamlit