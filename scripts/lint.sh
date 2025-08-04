#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "🔍 Running linting checks..."
echo "   - flake8..."
flake8 ytdl/ --count --select=E9,F63,F7,F82 --show-source --statistics || echo "⚠️  flake8 found some issues"
flake8 ytdl/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
