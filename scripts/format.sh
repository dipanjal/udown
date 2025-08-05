#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "   - black formatting..."
isort ytdl/
black ytdl/ --line-length 127 || echo "⚠️  black formatting failed"
