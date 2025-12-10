#!/usr/bin/env python3
"""
OCR Barcode Detector - Main Entry Point
Provides both CLI and GUI interfaces for barcode detection
"""

import sys
import argparse
from barcode_detector import BarcodeDetector


def main():
    """Main function - handle CLI arguments"""
    parser = argparse.ArgumentParser(
        description='OCR Barcode Detector - Extract barcode contents from images',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # GUI Mode (default)
  python main.py

  # CLI Mode - Detect barcode in image
  python main.py -i path/to/image.jpg

  # CLI Mode - Process multiple images
  python main.py -i image1.jpg image2.jpg image3.jpg

  # GUI Mode with custom title
  python main.py --gui
        """
    )
    
    parser.add_argument('-i', '--image', nargs='+', help='Image file path(s) for CLI mode')
    parser.add_argument('--gui', action='store_true', help='Start GUI mode (default)')
    
    args = parser.parse_args()
    
    # If images provided, run in CLI mode
    if args.image:
        run_cli(args.image)
    else:
        # Default to GUI mode
        run_gui()


def run_cli(image_paths):
    """Run barcode detection in CLI mode"""
    detector = BarcodeDetector()
    
    print("\n" + "="*60)
    print("OCR BARCODE DETECTOR - CLI Mode")
    print("="*60 + "\n")
    
    for image_path in image_paths:
        print(f"\nProcessing: {image_path}")
        print("-" * 60)
        
        result = detector.extract_barcode(image_path)
        
        if result['success']:
            print(f"✓ Status: {result['message']}")
            print(f"  Detection Method: {result['method'].upper()}")
            print(f"  Barcode Content: b'{result['barcode_content']}'")
        else:
            print(f"✗ Status: {result['message']}")
            print(f"  Detection Method: {result['method']}")
        
        print("-" * 60)
    
    print("\n" + "="*60)
    print("Detection Complete")
    print("="*60 + "\n")


def run_gui():
    """Run barcode detection in GUI mode"""
    try:
        from ui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Error: Could not import UI module: {e}")
        print("Make sure ui.py is in the same directory as main.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
