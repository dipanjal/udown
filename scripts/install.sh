#!/bin/bash

# Exit on any error
set -e

echo "🚀 Setting up you-down development environment..."

# Install Python version if pyenv is available
if command -v pyenv &> /dev/null; then
    echo "📦 Installing Python version with pyenv..."
    pyenv install -s
else
    echo "⚠️  pyenv not found, using system Python"
fi

DIRECTORY=".venv"

# Remove existing virtual environment if it exists
if [ -d "$DIRECTORY" ]; then
    echo "🗑️  Removing existing $DIRECTORY"
    rm -rf $DIRECTORY
fi

echo "🔧 Creating new virtual environment..."
python -m venv $DIRECTORY

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source $DIRECTORY/bin/activate

# Show Python version and location
echo "🐍 Python version and location:"
which python
python --version

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install the package in development mode with all dependencies
echo "📦 Installing you-down in development mode..."
pip install -e ".[dev]"

# Verify installation
echo "✅ Verifying installation..."
python -c "import ytdl; print('✅ ytdl package imported successfully')"
python -c "import pytest; print('✅ pytest available for testing')"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "📋 Next steps:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Run tests: make test"
echo ""