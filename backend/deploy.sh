#!/bin/bash

# Backend Deployment Script
# This script helps deploy the backend to a VPS

echo "🚀 Starting backend deployment..."

# Check if virtual environment exists
if [ ! -d "app_env" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv app_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source app_env/bin/activate

# Install/update dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your configuration:"
    echo "OPENAI_API_KEY=your_api_key_here"
    echo "DATABASE_URL=sqlite:///./qa_system.db"
    exit 1
fi

# Create database tables
echo "🗄️  Setting up database..."
python -c "from app.database import create_tables; create_tables()"

# Test the application
echo "🧪 Testing application..."
python -c "from app.main import app; print('✅ Application imports successfully')"

echo "✅ Backend deployment completed!"
echo ""
echo "To run the application:"
echo "1. Activate virtual environment: source app_env/bin/activate"
echo "2. Run development server: uvicorn app.main:app --reload"
echo "3. Run production server: gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000"
echo ""
echo "API Documentation will be available at:"
echo "- Swagger UI: http://localhost:8000/docs"
echo "- ReDoc: http://localhost:8000/redoc" 