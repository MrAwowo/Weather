#!/bin/bash

# Weather Prediction App Startup Script

echo "🌤️  Starting Weather Prediction App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create .env file if it doesn't exist (optional, for Supabase)
if [ ! -f ".env" ]; then
    echo "ℹ️  No .env file found (this is optional)"
    echo "ℹ️  The app will work without it!"
    echo "ℹ️  To setup Supabase later, run: cp .env.example .env"
fi

# Run the app
echo "🚀 Launching Streamlit app..."
echo "✅ No API keys required - using Open-Meteo!"
streamlit run app.py
