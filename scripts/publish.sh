#!/bin/bash
# Publish script for udown package to TestPyPI

# Exit on any error
set -e

source ./scripts/activate_env.sh

PUBLISH_TEST="${PUBLISH_TEST:-false}"

check_dependencies() {
    # Check if twine is available
    if ! command -v twine &> /dev/null; then
        echo "❌ twine is not installed. Please install it with: pip install twine"
        exit 1
    fi
}

check_app_version() {
    # Ensure the package version is set correctly
    echo "🔍 Checking package version..."
    if [ ! -f ".app-version" ]; then
        echo "❌ .app-version file not found."
        echo "Please create a .app-version file with the version number before publishing."
        exit 1
    fi
}

check_tag_exists_in_origin() {
    # Check if corresponding tag exists on origin
    echo "🏷️  Checking if tag exists on origin..."
    VERSION=$(cat ".app-version" | tr -d '\n' | tr -d ' ')
    if [[ ! "$VERSION" =~ ^v ]]; then
        TAG_NAME="v$VERSION"
    else
        TAG_NAME="$VERSION"
    fi

    # Fetch tags from origin
    git fetch origin --tags > /dev/null || { echo "❌ Can't fetch from origin"; exit 1; }

    # Check if tag exists on origin
    if ! git ls-remote --tags origin | grep -q "refs/tags/$TAG_NAME$"; then
        echo "❌ Tag $TAG_NAME does not exist on origin."
        echo "Please create a tag first using 'make create-tag'"
        exit 1
    fi

    echo "✅ Tag $TAG_NAME exists on origin"
}

check_build() {
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
    echo "🔍 Ensuring package is built correctly..."
#    if ! [ -e "dist/udown-*.tar.gz" ] && ! [ -e "dist/you_down-*.whl" ]; then
    if ! compgen -G "dist/udown-*.tar.gz" > /dev/null && ! compgen -G "dist/you_down-*.whl" > /dev/null; then
        echo "❌ No package files found in dist/ directory"
        echo "Please build the package first using ./scripts/build-package.sh"
        exit 1
    fi
}

take_confirmation() {
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
}


publish_to_test_pypi() {
    echo "📤 Uploading to TestPyPI..."
    python -m twine upload --repository testpypi dist/* --verbose

    if [ $? -eq 0 ]; then
       echo "✅ Package successfully published to TestPyPI!"
       echo ""
       echo "🔗 You can view your package at:"
       echo "   https://test.pypi.org/project/udown/"
       echo ""
       echo "🧪 To install from TestPyPI:"
       echo "   pip install --index-url https://test.pypi.org/simple/ udown"
    else
       echo "❌ Failed to publish to TestPyPI"
       exit 1
    fi

}

publish_to_pypi() {
    echo "📤 Uploading to PyPI..."
    python -m twine upload --repository pypi dist/* --verbose

    if [ $? -eq 0 ]; then
       echo "✅ Package successfully published to PyPI!"
       echo ""
       echo "🔗 You can view your package at:"
       echo "   https://pypi.org/project/udown/"
       echo ""
       echo "🧪 To install from PyPI:"
       echo "   pip install udown"
    else
       echo "❌ Failed to publish to PyPI"
       exit 1
    fi
}

publish_package() {
    # Check package before uploading
    echo "🔍 Checking package integrity..."
    python -m twine check dist/*

    if [ $? -ne 0 ]; then
        echo "❌ Package check failed. Please fix the issues before publishing."
        exit 1
    fi

    if [[ "$PUBLISH_TEST" == "true" ]]; then
        publish_to_test_pypi
    else
        publish_to_pypi
    fi
}

check_prerequisites() {
    check_dependencies
    check_app_version
    check_tag_exists_in_origin
    check_build
}

main() {
    echo "🚀 Publishing udown package to PyPI..."
    check_prerequisites
    take_confirmation
    publish_package
}

main "$@"
