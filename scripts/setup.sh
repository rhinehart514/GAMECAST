#!/bin/bash

echo "================================"
echo "NHL Simulation Game - Setup"
echo "================================"
echo ""

# Check if in correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: Please run from nhl-simulation-game/ directory"
    exit 1
fi

echo "📦 Setting up Intelligence Service..."
cd intelligence-service
python -m venv venv
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
pip install -r requirements.txt
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the intelligence service:"
echo "  cd intelligence-service"
echo "  source venv/bin/activate  # or venv\Scripts\activate on Windows"
echo "  python src/main.py"
echo ""
echo "API docs will be at: http://localhost:8000/docs"

