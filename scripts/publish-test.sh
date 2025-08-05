#!/bin/bash
# Publish script for you-down package to TestPyPI

# Exit on any error
set -e

source ./scripts/activate_env.sh

echo "🚀 Publishing you-down package to TestPyPI..."

# Check if twine is available
if ! command -v twine &> /dev/null; then
    echo "❌ twine is not installed. Please install it with: pip install twine"
    exit 1
fi

# Check if dist directory exists and has files
echo "🔍 Checking build directory..."
if [ ! -d "dist" ] || [ -z "$(ls -A dist)" ]; then
    echo "❌ No package files found in dist/ directory"
    echo "Build the package first"
    ./scripts/build-package.sh
    if [ $? -ne 0 ]; then
        echo "❌ Failed to build the package. Please fix the issues before publishing."
        exit 1
    fi
    echo "✅ Package built successfully. Now you can publish it."
else
    echo "✅ Found package files in dist/ directory"
fi


# Ensure the package is built
echo "🔍 Ensuring package is built..."
if [ ! -f "dist/you-down-*.tar.gz" ] && [ !-f "dist/you_down-*.whl" ]; then
    echo "❌ No package files found in dist/ directory"
    echo "Please build the package first using ./scripts/build-package.sh"
    exit 1
fi


# echo "   Proceeding to publish..."
#     do you want to continue? (y/n)"
#     read -r answer
#     if [[ ! "$answer" =~ ^[Yy]$ ]]; then
#         echo "❌ Publishing aborted by user."
#         exit 0
#     fi

# Take confirmation before publishing
echo ""
echo "Are you sure you want to publish these files to TestPyPI?"
echo "do you want to continue? (y/n)"
read -r answer
if [[ -z "$answer" ]]; then
    echo "❌ No input provided. Publishing aborted."
    exit 1
fi
if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    echo "❌ Publishing aborted by user."
    exit 0
fi

# Ensure the package version is set correctly
echo "🔍 Checking package version..."
if [ ! -f ".app-version" ]; then
    echo "❌ .app-version file not found."
    echo "Please create a .app-version file with the version number before publishing."
    exit 1
fi

# Check package before uploading
echo "🔍 Checking package integrity..."
python -m twine check dist/*

if [ $? -ne 0 ]; then
    echo "❌ Package check failed. Please fix the issues before publishing."
    exit 1
fi

# Upload to TestPyPI
echo "📤 Uploading to TestPyPI..."
python -m twine upload --repository testpypi dist/* --verbose

if [ $? -eq 0 ]; then
   echo "✅ Package successfully published to TestPyPI!"
   echo ""
   echo "🔗 You can view your package at:"
   echo "   https://test.pypi.org/project/you-down/"
   echo ""
   echo "🧪 To install from TestPyPI:"
   echo "   pip install --index-url https://test.pypi.org/simple/ you-down"
else
   echo "❌ Failed to publish to TestPyPI"
   exit 1
fi