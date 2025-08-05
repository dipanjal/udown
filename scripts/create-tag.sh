#!/bin/bash

# Script to create GitHub tag with current .app-version
# Usage: ./create-tag.sh

set -e

VERSION_FILE=".app-version"

# Check if .app-version exists
if [ ! -f "$VERSION_FILE" ]; then
    echo "❌ Error: $VERSION_FILE not found"
    exit 1
fi

# Read version from file
VERSION=$(cat "$VERSION_FILE" | tr -d '\n' | tr -d ' ')

# Validate version is not empty
if [ -z "$VERSION" ]; then
    echo "❌ Error: Version is empty in $VERSION_FILE"
    exit 1
fi

# Add 'v' prefix if not present
if [[ ! "$VERSION" =~ ^v ]]; then
    TAG_NAME="v$VERSION"
else
    TAG_NAME="$VERSION"
fi

echo "🏷️  Creating tag: $TAG_NAME"

# Check if tag already exists
if git tag -l | grep -q "^$TAG_NAME$"; then
    echo "⚠️  Tag $TAG_NAME already exists"
    read -p "Do you want to delete and recreate it? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git tag -d "$TAG_NAME"
        git push origin :refs/tags/"$TAG_NAME" 2>/dev/null || true
        echo "🗑️  Deleted existing tag"
    else
        echo "❌ Aborted"
        exit 1
    fi
fi

# Create annotated tag
git tag -a "$TAG_NAME" -m "Release $TAG_NAME"

# Push tag to remote
git push origin "$TAG_NAME"

echo "✅ Successfully created and pushed tag: $TAG_NAME"
echo "🔗 View release at: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/releases/tag/$TAG_NAME"