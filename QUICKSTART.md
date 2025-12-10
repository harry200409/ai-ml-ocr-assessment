# OCR Barcode Detector - Quick Start Guide

## What You Got

A complete **OCR Barcode Detector** application with:
- ✅ Graphical User Interface (GUI)
- ✅ Command-line Interface (CLI)
- ✅ Multiple detection methods
- ✅ Full source code
- ✅ Test script included

## Quick Setup (2 minutes)

### Windows Users

1. **Open PowerShell or Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter

2. **Navigate to the project**
   ```
   cd k:\Harry\ocr_barcode_detector
   ```

3. **Run the setup script**
   ```
   run.bat
   ```

   Or manually:
   ```
   pip install -r requirements.txt
   python main.py
   ```

### macOS/Linux Users

1. **Open Terminal**

2. **Navigate to the project**
   ```
   cd k:/Harry/ocr_barcode_detector
   ```

3. **Run the setup script**
   ```
   chmod +x run.sh
   ./run.sh
   ```

   Or manually:
   ```
   pip3 install -r requirements.txt
   python3 main.py
   ```

## Using the Application

### GUI Mode (Easiest)

1. **Click "📁 Browse Image"**
   - Select: `k:\Harry\b\ReverseWay Bill\reverseWaybill-162822952260583552_1.jpg`

2. **Click "🔍 Detect Barcode"**
   - Wait for processing

3. **View Results**
   - See the barcode content: `b'M00968429135'`

### CLI Mode (For Batch Processing)

**Single Image:**
```
python main.py -i "k:\Harry\b\ReverseWay Bill\reverseWaybill-162822952260583552_1.jpg"
```

**Multiple Images:**
```
python main.py -i image1.jpg image2.jpg image3.jpg
```

## Expected Output

When processing `reverseWaybill-162822952260583552_1.jpg`:

```
Barcode contents: b'M00968429135'
Detection Method: PYZBAR (or MORPHOLOGY or EASYOCR as fallback)
```

## Project Structure

```
k:/Harry/ocr_barcode_detector/
├── main.py                    # Start here! (GUI & CLI)
├── ui.py                      # GUI interface
├── barcode_detector.py        # Core detection logic
├── test_detector.py           # Test with sample images
├── requirements.txt           # Dependencies
├── run.bat                    # Windows quick start
├── run.sh                     # macOS/Linux quick start
└── README.md                  # Full documentation
```

## Files Explained

| File | Purpose |
|------|---------|
| `main.py` | Entry point - handles GUI and CLI |
| `ui.py` | Beautiful Tkinter GUI with image preview |
| `barcode_detector.py` | Core detection logic (3 methods) |
| `test_detector.py` | Test script with your images |
| `requirements.txt` | Python package dependencies |
| `README.md` | Complete documentation |

## Detection Methods

The detector tries 3 methods in order:

1. **PyZbar** - Best for standard barcodes
2. **Morphology + OCR** - For complex/obscured barcodes
3. **EasyOCR** - General-purpose fallback

## First Run Tips

⚠️ **First run will be slow (30-60 seconds)**
- EasyOCR downloads ML models (~500MB)
- Models are cached after first run
- Subsequent runs are fast

## Test Your Setup

Before using with your images, test the detector:

```
python test_detector.py
```

This will verify everything is working with your sample image.

## Supported Barcode Types

- Code128, Code39
- EAN (8, 13)
- UPC-A, UPC-E
- QR Codes
- DataMatrix
- PDF417
- And more!

## Troubleshooting

### Problem: "No barcode detected"
- ✓ Check image quality
- ✓ Try different detection method
- ✓ Ensure barcode is clearly visible

### Problem: Module not found
- Run: `pip install -r requirements.txt`

### Problem: GUI won't start
- Try: `python -m tkinter` (tests Tkinter)
- If fails, reinstall Python with Tkinter option

### Problem: Slow processing
- First run loads ML models (normal)
- Crop image to barcode area for speed
- Use CLI for batch processing

## Getting Help

1. Check **README.md** for detailed documentation
2. Review **test_detector.py** for usage examples
3. Check the comments in **barcode_detector.py** for method details

## Next Steps

1. ✅ Run `python main.py`
2. ✅ Load your first barcode image
3. ✅ Click "Detect Barcode"
4. ✅ See results!

## Performance Tips

- **GUI**: Best for single images with visual feedback
- **CLI**: Best for batch processing multiple images
- **Test script**: Verify setup before using with real data

## Customization Ideas

Want to enhance it? Consider:
- [ ] Add image preprocessing (rotation, contrast adjustment)
- [ ] Save results to CSV/JSON
- [ ] Batch processing in GUI
- [ ] Integration with databases
- [ ] Custom barcode training

## Version Info

- **Version**: 1.0.0
- **Python**: 3.7+
- **Created**: December 2025
- **Status**: Production Ready

---

**Ready to detect some barcodes? Run `python main.py` now!** 🚀
