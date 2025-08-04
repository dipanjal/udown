#!/bin/bash

# Exit on any error
set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found"
    echo "Create Virtual Environment and install dependencies"
    
    # need to exit if installation fails
    echo "Running installation script..."
    ./scripts/install.sh
    INSTALL_STATUS=$?

    echo "Installation script completed with status: $INSTALL_STATUS"

    if [ $INSTALL_STATUS -ne 0 ]; then
        echo "❌ Installation failed. Please check the installation script."
        exit 1
    fi
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Show Python version
echo "🐍 Python version:"
python --version
