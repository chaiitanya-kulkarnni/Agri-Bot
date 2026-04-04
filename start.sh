#!/bin/bash

echo "================================================"
echo " Grape Plant Disease Detection System"
echo " Starting Application..."
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/Update dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if database exists
if [ ! -f "mydatabase.db" ]; then
    echo ""
    echo "WARNING: Database file 'mydatabase.db' not found!"
    echo "Please create the database or run the app to auto-create it."
    echo ""
fi

# Start the Flask application
echo ""
echo "================================================"
echo " Starting Flask Server..."
echo " Access the app at: http://localhost:5000"
echo " Press Ctrl+C to stop the server"
echo "================================================"
echo ""
python main.py
