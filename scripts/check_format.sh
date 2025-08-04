#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "   - black formatting check..."
black --check ytdl/ || echo "⚠️  black formatting issues found"

# # Find all unformatted python files and format them using black
# find . -name "*.py" -print0 | xargs -0 black
