#!/bin/bash

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "🔧 Testing CLI..."
you-down --help || echo "⚠️  CLI help test failed"
