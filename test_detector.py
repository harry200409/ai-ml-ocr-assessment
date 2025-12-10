"""
Test script to verify the barcode detector with the provided sample image
Run this to test with: k:\Harry\b\ReverseWay Bill\reverseWaybill-162822952260583552_1.jpg
Expected output: Barcode contents: b'M00968429135'
"""

from barcode_detector import BarcodeDetector
import os


def test_sample_image():
    """Test detection with the provided sample image"""
    
    # Path to your sample image
    sample_image = r"k:\Harry\b\ReverseWay Bill\reverseWaybill-162822952260583552_1.jpg"
    
    print("\n" + "="*70)
    print("OCR BARCODE DETECTOR - TEST")
    print("="*70)
    print(f"\nImage: {sample_image}")
    print(f"Exists: {os.path.exists(sample_image)}\n")
    
    if not os.path.exists(sample_image):
        print("ERROR: Sample image not found!")
        print(f"Expected location: {sample_image}")
        return
    
    # Initialize detector
    print("Initializing barcode detector...")
    detector = BarcodeDetector()
    
    # Extract barcode
    print("Processing image...")
    result = detector.extract_barcode(sample_image)
    
    # Display results
    print("\n" + "-"*70)
    print("RESULTS:")
    print("-"*70)
    print(f"Success: {result['success']}")
    print(f"Status: {result['message']}")
    print(f"Method: {result['method']}")
    
    if result['success']:
        print(f"\nBarcode Content: {result['barcode_content']}")
        print(f"\nFormatted Output: {result['message']}")
    
    print("\n" + "="*70)


def test_all_images():
    """Test detection with all images in the ReverseWay Bill folder"""
    
    folder_path = r"k:\Harry\b\ReverseWay Bill"
    
    print("\n" + "="*70)
    print("OCR BARCODE DETECTOR - BATCH TEST")
    print("="*70)
    print(f"\nFolder: {folder_path}\n")
    
    if not os.path.exists(folder_path):
        print("ERROR: Folder not found!")
        return
    
    # Get all jpg files
    images = [f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')]
    
    if not images:
        print("No JPG images found in folder!")
        return
    
    print(f"Found {len(images)} images\n")
    
    # Initialize detector
    detector = BarcodeDetector()
    
    successful = 0
    failed = 0
    
    # Process each image
    for i, image_file in enumerate(images[:5], 1):  # Test first 5 images
        image_path = os.path.join(folder_path, image_file)
        
        print(f"[{i}/{min(5, len(images))}] Processing: {image_file}")
        
        result = detector.extract_barcode(image_path)
        
        if result['success']:
            print(f"     ✓ Barcode: b'{result['barcode_content']}'")
            successful += 1
        else:
            print(f"     ✗ {result['message']}")
            failed += 1
    
    print("\n" + "-"*70)
    print(f"Results: {successful} successful, {failed} failed")
    print("="*70 + "\n")


if __name__ == "__main__":
    # Test single image
    test_sample_image()
    
    # Uncomment to test all images
    # test_all_images()
