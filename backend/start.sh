#!/bin/bash
"""
Django Backend Startup Script
"""

set -e

echo "🚀 Starting Healthcare Portal Django Backend..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Run migrations (if using Django ORM)
echo "🗄️  Running database setup..."
# For MongoDB with MongoEngine, migrations are not needed

# Initialize sample doctors
echo "👨‍⚕️  Initializing sample doctors..."
python database/init_doctors.py

# Start Django development server
echo "✅ Starting Django development server on 0.0.0.0:8000..."
python manage.py runserver 0.0.0.0:8000
