@echo off
REM Quick Start Script for OCR Barcode Detector
REM This script sets up the environment and runs the application

echo.
echo ============================================================
echo   OCR Barcode Detector - Quick Start Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/3] Python found. Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/3] Dependencies installed successfully!
echo.
echo [3/3] Starting OCR Barcode Detector...
echo.

REM Start the GUI application
python main.py

pause
