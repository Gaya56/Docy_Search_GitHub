#!/bin/bash

# Setup script for Tool Recommendation Container
# This script initializes the container environment

set -e

echo "🔧 Setting up Tool Recommendation Container..."

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p data
mkdir -p logs

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the container"
else
    echo "✅ .env file already exists"
fi

# Make scripts executable
echo "🔧 Making scripts executable..."
chmod +x test_container.py

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Edit .env file with your API keys"
echo "   2. Run: make build"
echo "   3. Run: make run"
echo "   4. Test: make test"
echo ""
echo "🔗 Useful commands:"
echo "   make build  - Build the container"
echo "   make run    - Start the container"
echo "   make test   - Test the container"
echo "   make logs   - View logs"
echo "   make stop   - Stop the container"
echo "   make clean  - Clean up everything"
echo ""
