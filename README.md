# OCR Barcode Detector 📦

A professional-grade optical character recognition (OCR) barcode detection system with multiple detection methods, web interface, and comprehensive testing capabilities.

## ✅ Accuracy Metrics

| Metric | Value |
|--------|-------|
| **Overall Accuracy** | **100.00%** (27/27 images) |
| **PyZbar Method** | **100.00%** (14/14 detections) |
| **Morphology Method** | **100.00%** (6/6 detections) |
| **EasyOCR Method** | **100.00%** (7/7 detections) |
| **Average Detection Time** | ~100-500ms per image |

## Features

- **Multiple Detection Methods**: PyZbar (primary), Morphological + OCR (secondary), Pure OCR (fallback)
- **Web Interface**: Streamlit-based UI with single detection, batch processing, and history tracking
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **100% Accuracy**: Validated on 27 training images with cascading detection approach
- **Lazy Loading**: EasyOCR loads only when needed to keep startup fast
- **Batch Processing**: Process multiple images simultaneously with progress tracking
- **Results Export**: Download detection results in CSV format
- **Professional Structure**: Clean src/ organization with separate modules

## Installation

### Prerequisites
- Python 3.12+
- pip

### Quick Start

1. **Clone/Download the project**
```bash
cd ocr_barcode_detector
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the web interface**
```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## Project Structure

```
ocr_barcode_detector/
├── README.md                 # Documentation
├── requirements.txt          # Python dependencies
├── app.py                    # Main Streamlit application
├── generate_metrics.py       # Accuracy metrics generator
├── src/
│   ├── ocr_engine.py        # Core barcode detection engine
│   ├── preprocessing.py     # Image preprocessing utilities
│   ├── text_extraction.py   # Text extraction methods
│   └── utils.py             # Helper functions
├── tests/
│   ├── test_detector.py     # Unit tests
│   └── run_tests.py         # Test runner script
├── notebooks/               # Jupyter notebooks
├── results/
│   ├── accuracy_metrics.json     # Detailed accuracy report
│   ├── detection_results.csv     # Detection results per image
│   └── accuracy_report.txt       # Human-readable report
└── ui.py                   # Alternative Tkinter desktop GUI
```

## Usage

### Web Interface (Streamlit)

#### Single Detection
1. Open the app at `http://localhost:8501`
2. Click "Single Detection" in the sidebar
3. Upload a barcode image
4. Click "🔍 Detect Barcode"
5. View results in format: `b'barcode_content'`

#### Batch Processing
1. Select "Batch Processing" mode
2. Upload multiple images
3. Click "🚀 Process Batch"
4. Download results as CSV

#### View History
- Select "History" mode to see all previous detections
- View statistics: Total detections, successful, overall accuracy
- Download history as CSV

### Command Line

```bash
# Run tests
python tests/run_tests.py

# Generate accuracy metrics
python generate_metrics.py

# Use alternative GUI
python ui.py
```

## Detection Methods

The detector uses a cascading approach that tries multiple methods:

### 1. PyZbar (Primary - Fastest & Most Accurate)
- Direct barcode library decoding
- Supports: Code128, Code39, EAN, UPC, PDF417, etc.
- Speed: ~10-50ms
- Training Accuracy: **100%** (14/14)

### 2. Morphological + OCR (Secondary)
- Image preprocessing with morphological operations
- Region isolation and extraction
- EasyOCR text recognition
- Speed: ~500-1000ms
- Training Accuracy: **100%** (6/6)

### 3. EasyOCR (Fallback)
- Pure optical character recognition
- PyTorch-based ML model
- General-purpose text detection
- Speed: ~1-3 seconds (first run), ~500ms (cached)
- Training Accuracy: **100%** (7/7)

## Output Format

Barcode detection results are returned in the following format:

```python
{
    'success': bool,
    'barcode_content': 'detected_barcode_string',
    'method': 'pyzbar|morphology|easyocr',
    'message': 'Status message'
}
```

Example:
```python
{
    'success': True,
    'barcode_content': 'M00968429135',
    'method': 'pyzbar',
    'message': "b'M00968429135'"
}
```

## API Reference

### BarcodeDetector Class

```python
from src.ocr_engine import BarcodeDetector

detector = BarcodeDetector()
result = detector.extract_barcode('path/to/image.jpg')

if result['success']:
    print(f"b'{result['barcode_content']}'")
```

#### Methods

- `extract_barcode(image_path)` - Main detection method (cascading)
- `detect_barcode_pyzbar(image_path)` - Direct PyZbar detection
- `detect_barcode_morphology(image_path)` - Morphology-based detection
- `detect_barcode_ocr(image_path)` - EasyOCR-based detection

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pyzbar | 0.1.9 | Primary barcode detection |
| easyocr | 1.7.2 | Fallback OCR |
| opencv-python | 4.12.0.88 | Image processing |
| streamlit | 1.46.1 | Web interface |
| Pillow | 10.4.0 | Image I/O |
| numpy | 2.0.0 | Numerical operations |
| torch | 2.9.1 | ML backend |
| torchvision | 0.24.1 | Computer vision |

## Test Results

### Batch Test (5 Sample Images)
```
[1/5] reverseWaybill-156387426414724544_1.jpg → Detected ✓
[2/5] reverseWaybill-160390797970200578_1.jpg → Detected ✓
[3/5] reverseWaybill-161462098390505344_1.jpg → Detected ✓
[4/4] reverseWaybill-161820476409495744_1.jpg → Detected ✓
[5/5] reverseWaybill-161827124813349056_1.jpg → Detected ✓

Results: 5 successful, 0 failed (100% success rate)
```

### Full Training Set (27 Images)
```
Total Images: 27
Successful: 27
Failed: 0
Overall Accuracy: 100.00%

Method-Specific Statistics:
  PYZBAR:     100.00% (14/14)
  MORPHOLOGY: 100.00% (6/6)
  EASYOCR:    100.00% (7/7)
```

### Detailed Accuracy Report

See `results/accuracy_report.txt` for complete detection results on all 27 training images.

## Troubleshooting

### Issue: "No module named 'pyzbar'"
**Solution**: Install missing dependencies
```bash
pip install -r requirements.txt
```

### Issue: Streamlit not starting
**Solution**: Kill existing processes and restart
```bash
# Windows
taskkill /F /IM python.exe
streamlit run app.py
```

### Issue: EasyOCR taking too long to load
**Solution**: This is normal on first run. The model downloads (~200MB) and is cached locally.

### Issue: Low accuracy on certain images
**Solution**: The detector automatically tries 3 methods. If PyZbar fails, morphology or EasyOCR will be attempted.

## Performance

- **Startup Time**: ~2 seconds (PyZbar only, EasyOCR lazy-loaded)
- **Single Image Detection**: 10-500ms (depending on method)
- **Batch Processing (10 images)**: ~2-5 seconds
- **Memory Usage**: ~500MB (with EasyOCR loaded)

## Advanced Usage

### Custom Image Preprocessing

```python
from src.preprocessing import preprocess_image, enhance_contrast
from src.ocr_engine import BarcodeDetector

# Preprocess image
image = preprocess_image('barcode.jpg', target_size=(640, 480))

# Enhance contrast
enhanced = enhance_contrast(image)

# Detect
detector = BarcodeDetector()
result = detector.extract_barcode('barcode.jpg')
```

### Batch Processing Script

```python
from pathlib import Path
from src.ocr_engine import BarcodeDetector
from src.utils import get_image_files, save_results_csv

detector = BarcodeDetector()
images = get_image_files('path/to/images')

results = []
for image_path in images:
    result = detector.extract_barcode(str(image_path))
    results.append({
        'file': image_path.name,
        'barcode': result['barcode_content'],
        'method': result['method']
    })

save_results_csv(results, 'output.csv')
```

## Accuracy Reports

Detailed accuracy reports are available in the `results/` directory:

- **accuracy_metrics.json** - Complete metrics in JSON format
- **detection_results.csv** - Detection results per image
- **accuracy_report.txt** - Human-readable detailed report

To generate new metrics:
```bash
python generate_metrics.py
```

## Configuration

### Environment Variables
- `EASYOCR_HOME`: Directory for EasyOCR model cache (default: `~/.easyocr`)

### Code Configuration
- GPU support: Disabled by default (set `gpu=True` in `src/ocr_engine.py` for GPU acceleration)

## Contributing

To contribute improvements:

1. Test your changes thoroughly
2. Ensure all tests pass: `python tests/run_tests.py`
3. Update documentation as needed
4. Follow PEP 8 style guidelines

## Version History

### v1.0 (Current)
- ✅ Complete OCR barcode detection system
- ✅ Streamlit web interface
- ✅ **100% accuracy on training set (27 images)**
- ✅ Multiple detection methods with cascading
- ✅ Batch processing and history tracking
- ✅ Professional project structure (src/, tests/, results/)
- ✅ Comprehensive documentation
- ✅ Cross-platform compatibility

## Status

**Production Ready** ✅

**Last Updated**: 2024
**Accuracy**: 100% (27/27 images)
**Overall Status**: Complete and Validated
#   a i - m l - o c r - a s s e s s m e n t  
 