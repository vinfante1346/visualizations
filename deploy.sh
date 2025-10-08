#!/bin/bash

# Simple deploy script for Val
# Usage: ./deploy.sh filename.html "Description"

# Check if filename provided
if [ -z "$1" ]; then
    echo "❌ Error: Please provide a filename"
    echo "Usage: ./deploy.sh filename.html \"Description\""
    exit 1
fi

# Check if file exists in artifacts
if [ ! -f "artifacts/$1" ]; then
    echo "❌ Error: File 'artifacts/$1' not found"
    echo "Make sure your HTML file is in the artifacts/ folder"
    exit 1
fi

# Get description or use default
DESCRIPTION="${2:-Update $1}"

echo "📦 Deploying $1..."
echo "📝 Commit message: $DESCRIPTION"
echo ""

# Git commands
git add .
git commit -m "$DESCRIPTION"
git push

echo ""
echo "✅ Deployed successfully!"
echo ""
echo "🌐 Your link will be ready in 1-2 minutes:"
echo "https://pwatson-mybambu.github.io/visualizations/artifacts/$1"
echo ""
