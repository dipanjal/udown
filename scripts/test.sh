#!/bin/bash

# Exit on any error
set -e

echo "🧪 Running you-down tests..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run ./scripts/install.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Show Python version
echo "🐍 Python version:"
python --version

# Run linting checks
echo "🔍 Running linting checks..."
echo "   - flake8..."
flake8 ytdl/ --count --select=E9,F63,F7,F82 --show-source --statistics || echo "⚠️  flake8 found some issues"
flake8 ytdl/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

# Run formatting check
echo "   - black formatting check..."
black --check ytdl/ || echo "⚠️  black formatting issues found"

# Run type checking
echo "   - mypy type checking..."
mypy ytdl/ || echo "⚠️  mypy found type issues"

# Run tests
echo "🧪 Running pytest tests..."
python -m pytest -v

# Run CLI help test
echo "🔧 Testing CLI..."
you-down --help || echo "⚠️  CLI help test failed"

echo ""
echo "✅ All tests completed!"
echo ""