#!/bin/bash
# SecureShare Startup Script for Unix/Linux/Mac

echo "========================================"
echo "SecureShare - Secure File Sharing Platform"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.12 or higher"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to create virtual environment"
        exit 1
    fi
    echo "Virtual environment created successfully"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Initialize database if it doesn't exist
if [ ! -f "instance/secureshare.db" ]; then
    echo "Initializing database..."
    python scripts/seed_data.py
    if [ $? -ne 0 ]; then
        echo "WARNING: Failed to seed database, but continuing..."
    fi
fi

# Start the application
echo ""
echo "Starting SecureShare..."
echo "Application will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""
python run.py
