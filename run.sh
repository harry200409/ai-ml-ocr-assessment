#!/bin/bash
# Quick Start Script for OCR Barcode Detector
# For macOS/Linux

echo ""
echo "============================================================"
echo "   OCR Barcode Detector - Quick Start Setup"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.7+ from https://www.python.org"
    exit 1
fi

echo "[1/3] Python found. Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[2/3] Dependencies installed successfully!"
echo ""
echo "[3/3] Starting OCR Barcode Detector..."
echo ""

# Start the GUI application
python3 main.py

