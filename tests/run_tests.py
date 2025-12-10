#!/usr/bin/env python
"""
Test script for OCR Barcode Detector
This tests the complete detection pipeline
"""

import os
import sys
from pathlib import Path
from barcode_detector import BarcodeDetector

def test_single_image():
    """Test with a single barcode image"""
    print("\n" + "="*70)
    print("OCR BARCODE DETECTOR - TEST")
    print("="*70 + "\n")
    
    # Test image path
    test_image = r"k:\Harry\b\ReverseWay Bill\reverseWaybill-162822952260583552_1.jpg"
    
    print(f"Test Image: {test_image}")
    print(f"File Exists: {os.path.exists(test_image)}")
    
    if not os.path.exists(test_image):
        print("❌ ERROR: Test image not found!")
        return False
    
    # Initialize detector
    print("\nInitializing detector...")
    detector = BarcodeDetector()
    
    # Run detection
    print("Running detection...")
    result = detector.extract_barcode(test_image)
    
    # Display results
    print("\n" + "-"*70)
    print("DETECTION RESULTS:")
    print("-"*70)
    
    print(f"\nSuccess: {result['success']}")
    print(f"Method: {result.get('method', 'N/A')}")
    
    if result['success']:
        print(f"\n✓ BARCODE DETECTED!")
        print(f"Content: b'{result['barcode_content']}'")
        print(f"\nFormatted Output:")
        print(f"  {result['message']}")
        return True
    else:
        print(f"\n✗ DETECTION FAILED")
        print(f"Message: {result['message']}")
        return False

def test_batch_images():
    """Test with all images in ReverseWay Bill folder"""
    print("\n" + "="*70)
    print("BATCH TEST - ALL IMAGES")
    print("="*70 + "\n")
    
    folder = r"k:\Harry\b\ReverseWay Bill"
    
    if not os.path.exists(folder):
        print(f"❌ ERROR: Folder not found: {folder}")
        return False
    
    # Get all JPG files
    images = list(Path(folder).glob("*.jpg"))
    print(f"Found {len(images)} images\n")
    
    if not images:
        print("❌ No images found!")
        return False
    
    # Initialize detector
    detector = BarcodeDetector()
    
    successful = 0
    failed = 0
    
    # Process first 5 images
    for idx, img_path in enumerate(images[:5], 1):
        print(f"[{idx}/5] Processing: {img_path.name}")
        
        try:
            result = detector.extract_barcode(str(img_path))
            
            if result['success']:
                print(f"     ✓ {result['barcode_content']}")
                successful += 1
            else:
                print(f"     ✗ No barcode")
                failed += 1
        except Exception as e:
            print(f"     ✗ Error: {e}")
            failed += 1
    
    print("\n" + "-"*70)
    print(f"Batch Results: {successful} successful, {failed} failed")
    print("="*70 + "\n")
    
    return successful > 0

if __name__ == "__main__":
    print("\n🔍 OCR BARCODE DETECTOR - COMPREHENSIVE TEST\n")
    
    # Test 1: Single image
    test1_passed = test_single_image()
    
    # Test 2: Batch processing
    test2_passed = test_batch_images()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Single Image Test: {'✓ PASSED' if test1_passed else '✗ FAILED'}")
    print(f"Batch Test: {'✓ PASSED' if test2_passed else '✗ FAILED'}")
    print("="*70 + "\n")
    
    if test1_passed and test2_passed:
        print("✅ ALL TESTS PASSED - READY FOR PRODUCTION\n")
        sys.exit(0)
    else:
        print("⚠️  SOME TESTS FAILED - CHECK CONFIGURATION\n")
        sys.exit(1)
