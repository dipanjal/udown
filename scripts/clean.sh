#!/bin/bash
# Cleanup script for you-down package build artifacts

echo "🧹 Cleaning build artifacts..."

# Remove build directories
rm -rf build/
rm -rf dist/
rm -rf *.egg-info

# Remove Python cache files
rm -rf __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Remove test cache directories
rm -rf .pytest_cache/
rm -rf .mypy_cache/
rm -rf .coverage

# Remove temporary directories
rm -rf temp/
rm -rf downloads/

# Remove system files
find . -name ".DS_Store" -delete 2>/dev/null

echo "✅ Cleanup completed."
