#!/bin/bash

# Exit on any error
set -e
source ./scripts/activate_env.sh

# Build script for you-down package

run_command() {
  command="$1"
  description="$2"
  echo "🔄 $description..."
  if eval "$command"; then
    echo "✅ $description completed successfully"
  else
    echo "❌ $description failed:"
    echo "Error: See above"
    exit 1
  fi
}

main() {
  echo "🚀 Building you-down package..."

  # Clean previous builds
  run_command "rm -rf build/ dist/ *.egg-info/" "Cleaning previous builds"

  # Format the code with black
  run_command "sh ./scripts/format.sh" "Formatting code with black"

  # Check code quality
  run_command "sh ./scripts/quality.sh" "Checking code quality"

  # Build the package
  run_command "python -m build" "Building package"

  # Check the built package
  run_command "python -m twine check dist/*" "Checking package"

  echo ""
  echo "🎉 Build completed successfully!"
  echo ""
  echo "📦 Package files created in dist/ directory"
  echo ""
  echo "📤 To upload to PyPI (test):"
  echo "   python -m twine upload --repository testpypi dist/*"
  echo ""
  echo "📤 To upload to PyPI (production):"
  echo "   python -m twine upload dist/*"
  echo ""
  echo "🧪 To install locally for testing:"
  echo "   pip install dist/you-down-*.tar.gz"
}

main
