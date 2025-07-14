#!/bin/bash

# Setup script for Tool Recommendation Container
# This script copies the necessary files from the main project

set -e

echo "🔧 Setting up Tool Recommendation Container..."

# Define source and destination paths
SOURCE_DIR="/workspaces/Docy_Search_GitHub"
CONTAINER_DIR="/workspaces/Docy_Search_GitHub/tool_recommendation_container"

# Create directory structure
echo "📁 Creating directory structure..."
mkdir -p "$CONTAINER_DIR/tool_recommendation"
mkdir -p "$CONTAINER_DIR/config"
mkdir -p "$CONTAINER_DIR/data"
mkdir -p "$CONTAINER_DIR/logs"

# Copy tool recommendation files
echo "📋 Copying tool recommendation files..."
cp -r "$SOURCE_DIR/docy_search/tool_recommendation/"* "$CONTAINER_DIR/tool_recommendation/"

# Copy config files
echo "⚙️ Copying configuration files..."
cp -r "$SOURCE_DIR/config/"* "$CONTAINER_DIR/config/"

# Create __init__.py files
echo "🐍 Creating Python module files..."
touch "$CONTAINER_DIR/tool_recommendation/__init__.py"
touch "$CONTAINER_DIR/config/__init__.py"

# Make setup script executable
chmod +x "$CONTAINER_DIR/setup.sh"

# Create a simple test script
cat > "$CONTAINER_DIR/test_container.py" << 'EOF'
#!/usr/bin/env python3
"""
Simple test script for the Tool Recommendation Container
"""

import sys
import time
from client import ToolRecommendationClient

def test_container():
    """Test the container functionality."""
    print("🧪 Testing Tool Recommendation Container...")
    
    # Initialize client
    client = ToolRecommendationClient("http://localhost:8000")
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    for i in range(30):
        if client.health_check():
            print("✅ Server is healthy!")
            break
        time.sleep(1)
        print(f"   Waiting... ({i+1}/30)")
    else:
        print("❌ Server failed to start")
        return False
    
    # Test basic functionality
    print("\n🔍 Testing tool search...")
    result = client.search_tools("python web framework")
    if result and "error" not in result.lower():
        print("✅ Tool search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ Tool search failed: {result}")
        return False
    
    # Test web search
    print("\n🌐 Testing web search...")
    result = client.search_web("streamlit tutorial")
    if result and "error" not in result.lower():
        print("✅ Web search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ Web search failed: {result}")
    
    # Test GitHub search
    print("\n🐙 Testing GitHub search...")
    result = client.search_github("streamlit components")
    if result and "error" not in result.lower():
        print("✅ GitHub search works!")
        print(f"   Result preview: {result[:100]}...")
    else:
        print(f"❌ GitHub search failed: {result}")
    
    # Test Python execution
    print("\n🐍 Testing Python execution...")
    result = client.execute_python("print('Hello from container!')")
    if result and "Hello from container!" in result:
        print("✅ Python execution works!")
        print(f"   Result: {result.strip()}")
    else:
        print(f"❌ Python execution failed: {result}")
    
    print("\n🎉 Container test completed!")
    return True

if __name__ == "__main__":
    success = test_container()
    sys.exit(0 if success else 1)
EOF

chmod +x "$CONTAINER_DIR/test_container.py"

# Create a makefile for easy commands
cat > "$CONTAINER_DIR/Makefile" << 'EOF'
.PHONY: build run stop test clean logs health

# Build the container
build:
	@echo "🔨 Building Tool Recommendation Container..."
	docker-compose build

# Run the container
run:
	@echo "🚀 Starting Tool Recommendation Container..."
	docker-compose up -d
	@echo "✅ Container started! Access at http://localhost:8000"

# Stop the container
stop:
	@echo "🛑 Stopping Tool Recommendation Container..."
	docker-compose down

# Test the container
test:
	@echo "🧪 Testing Tool Recommendation Container..."
	python test_container.py

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	docker-compose down -v
	docker system prune -f

# View logs
logs:
	@echo "📋 Viewing container logs..."
	docker-compose logs -f

# Health check
health:
	@echo "🏥 Checking container health..."
	curl -f http://localhost:8000/health || echo "❌ Container not healthy"

# Full setup and test
setup: build run
	@echo "⏳ Waiting for container to start..."
	@sleep 10
	@make test

# Development mode (with live reload)
dev:
	@echo "🔧 Starting in development mode..."
	uvicorn server:app --host 0.0.0.0 --port 8000 --reload
EOF

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
