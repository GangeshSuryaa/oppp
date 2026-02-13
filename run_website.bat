@echo off
echo ========================================
echo  Pulmonologist Website Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet

REM Create necessary directories
if not exist "data" mkdir data
if not exist "static\images" mkdir static\images

REM Run the Flask application
echo.
echo Starting Flask server...
echo.
python app.py

REM Deactivate when done
deactivate
