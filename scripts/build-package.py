#!/usr/bin/env python3
"""
Build script for you-down package
"""

import subprocess
import sys


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        sys.exit(1)


def main():
    """Main build function."""
    print("🚀 Building you-down package...")
    
    # Clean previous builds
    run_command("rm -rf build/ dist/ *.egg-info/", "Cleaning previous builds")
    
    # Build the package
    run_command("python -m build", "Building package")
    
    # Check the built package
    run_command("python -m twine check dist/*", "Checking package")
    
    print("\n🎉 Build completed successfully!")
    print("\n📦 Package files created in dist/ directory")
    print("\n📤 To upload to PyPI (test):")
    print("   python -m twine upload --repository testpypi dist/*")
    print("\n📤 To upload to PyPI (production):")
    print("   python -m twine upload dist/*")
    print("\n🧪 To install locally for testing:")
    print("   pip install dist/you-down-*.tar.gz")


if __name__ == "__main__":
    main() 