@echo off
REM SecureShare Startup Script for Windows
echo ========================================
echo SecureShare - Secure File Sharing Platform
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12 or higher
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created successfully
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Initialize database if it doesn't exist
if not exist "instance\secureshare.db" (
    echo Initializing database...
    python scripts\seed_data.py
    if errorlevel 1 (
        echo WARNING: Failed to seed database, but continuing...
    )
)

REM Start the application
echo.
echo Starting SecureShare...
echo Application will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.
python run.py

pause
