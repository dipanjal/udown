#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "🔍 Running linting checks..."
pylint ytdl/ --fail-under=10.0