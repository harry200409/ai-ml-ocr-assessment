# OCR Barcode Detector

A professional-grade optical character recognition (OCR) barcode detection system with multiple detection methods, camera support, auto-rotation, web interface, and comprehensive testing capabilities.

##  Key Features

- **Camera Capture**: Real-time barcode detection via webcam
- **Auto-Rotation**: Automatically detects barcodes at multiple angles (tilted/rotated codes)
- **Multiple Detection Methods**: PyZbar (primary), Morphology + OCR (secondary), Pure OCR (fallback)
- **Web Interface**: Streamlit-based UI with single detection, batch processing, and history tracking
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Lazy Loading**: EasyOCR loads only when needed for fast startup
- **Batch Processing**: Process multiple images simultaneously with progress tracking
- **Professional Structure**: Clean src/ organization with separate modular components

## Installation

### Prerequisites
- Python 3.11+
- pip
- Webcam (for camera features)

### Quick Start

```bash
# Clone/download the project
cd ocr_barcode_detector

# Install dependencies
pip install -r requirements.txt

# Run the web interface
streamlit run app.py

The application will open at http://localhost:8501

```
## Poject structure

```text
ocr_barcode_detector/
├── README.md                 # Documentation
├── requirements.txt          # Python dependencies
├── app.py                    # Main Streamlit application (✨ UPDATED with camera)
├── barcode_detector.py       # Standalone detector class
├── generate_metrics.py       # Accuracy metrics generator
├── src/
│   ├── ocr_engine.py        # Core barcode detection engine (✨ NEW: rotation support)
│   ├── preprocessing.py     # Image preprocessing utilities
│   ├── text_extraction.py   # Text extraction methods
│   └── utils.py             # Helper functions
├── tests/
│   ├── test_detector.py     # Unit tests
│   └── run_tests.py         # Test runner script
├── results/
│   ├── accuracy_metrics.json # Detailed accuracy report
│   ├── detection_results.csv # Detection results per image
│   └── accuracy_report.txt   # Human-readable report
└── .gitignore               # Git ignore configuration

```
## Usage

- Web Interface (Streamlit)
- Single Detection with Camera or Upload

1. Open the app at http://localhost:8501
2. Navigate to "🔍 Detect Barcode" tab
3. Choose input mode:
- Upload image: Select a barcode image file (JPG, PNG, BMP, GIF, TIFF)
- Camera capture: Use your webcam to capture barcode
4. Click "🔍 Detect Barcode" button
- View results showing:
- Barcode content: b'M00968429135'
- Detection method: PyZbar, Morphology, or EasyOCR

## Batch Processing

1. Select "📊 Batch Processing" mode
2. Upload multiple images at once
3. Click "🚀 Process All Images" button
4. View results table with success/failure status

## View Detection History
1. Select "📜 History" mode
2. See all previous detections with timestamps
3. View statistics (total, successful, accuracy)

## Dependencies
- Package Version Purpose
pyzbar|	≥0.1.9|	Primary barcode detection
easyocr| ≥1.7.0|	Fallback OCR
opencv-python|	≥4.8.0|	Image processing
streamlit|	≥1.28.0|	Web interface
Pillow|	≥10.0.0|	Image I/O
numpy|	≥1.24.0|	Numerical operations


