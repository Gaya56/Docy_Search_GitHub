#!/bin/bash
"""
Quick Start Script for AI Tool Recommendation System
This script helps you get the system up and running quickly.
"""

echo "🤖 AI Tool Recommendation System - Quick Start"
echo "=============================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run:"
    echo "   uv venv"
    echo "   source .venv/bin/activate"
    echo "   uv pip install -r requirements.txt"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Created .env file. Please edit it with your API keys."
    else
        echo "❌ .env.example not found. Please create .env manually."
    fi
fi

# Activate virtual environment
source .venv/bin/activate

echo ""
echo "🚀 Starting services..."
echo ""

# Check if Docker container is running
if ! curl -sf http://localhost:8947/health > /dev/null 2>&1; then
    echo "📦 Starting Docker container..."
    make run
    echo "⏳ Waiting for container to start..."
    sleep 10
else
    echo "✅ Docker container already running"
fi

# Start Streamlit app
echo "🌐 Starting Streamlit app..."
echo "📍 App will be available at: http://localhost:8501"
echo "📍 API server available at: http://localhost:8947"
echo ""
echo "💡 Tips:"
echo "   - Configure your API keys in the sidebar"
echo "   - Try different modes: Tool Discovery, Notion, or Combined"
echo "   - Use quick action buttons for common tasks"
echo ""

streamlit run app.py --server.port 8501
