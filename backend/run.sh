#!/bin/bash

# AirLogger Backend Startup Script

echo "Starting AirLogger Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found!"
    echo "Please create .env from .env.example and add your FlightAware API key"
    exit 1
fi

# Run the application
echo "Starting Flask application..."
python app.py