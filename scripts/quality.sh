#!/bin/bash

# Exit on any error
set -e

echo "🧪 Running udown quality check..."

source ./scripts/activate_env.sh

echo "🔍 Running tests..."
./scripts/lint.sh
./scripts/check_format.sh
./scripts/typecheck.sh
./scripts/test.sh
./scripts/show_cli_help.sh

echo ""
echo "✅ All tests completed!"
echo ""
