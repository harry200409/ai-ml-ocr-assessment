@echo off
cd /d k:\Harry\ocr_barcode_detector
echo Starting OCR Barcode Detector Web UI...
echo.
echo Opening in browser at: http://localhost:8501
echo.
timeout /t 2
streamlit run app.py
pause
