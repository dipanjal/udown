#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "   - mypy type checking..."
mypy ytdl/ tests/ || echo "⚠️  mypy found type issues"
