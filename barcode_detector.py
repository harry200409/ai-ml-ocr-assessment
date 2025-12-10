import cv2
import numpy as np
from pyzbar.pyzbar import decode
import os
from PIL import Image

try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False


class BarcodeDetector:
    """OCR Barcode Detector for extracting barcode contents from images"""
    
    def __init__(self):
        """Initialize the barcode detector"""
        self.reader = None  # Lazy load EasyOCR
    
    def detect_barcode_pyzbar(self, image_path):
        """
        Detect barcode using pyzbar library
        Returns: tuple (barcode_data, confidence)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None, "Error: Could not load image"
            
            # Decode barcodes
            barcodes = decode(image)
            
            if barcodes:
                results = []
                for barcode in barcodes:
                    barcode_data = barcode.data.decode('utf-8')
                    barcode_type = barcode.type
                    results.append({
                        'data': barcode_data,
                        'type': barcode_type,
                        'method': 'pyzbar'
                    })
                return results, "Success"
            
            return None, "No barcode detected with pyzbar"
        
        except Exception as e:
            return None, f"Error in pyzbar detection: {str(e)}"
    
    def _get_reader(self):
        """Lazy load EasyOCR reader on first use"""
        if self.reader is None and EASYOCR_AVAILABLE:
            try:
                self.reader = easyocr.Reader(['en'], gpu=False, verbose=False)
            except Exception as e:
                print(f"Warning: Could not load EasyOCR: {e}")
        return self.reader
    
    def detect_barcode_ocr(self, image_path):
        """
        Detect barcode using EasyOCR (fallback method)
        Returns: tuple (barcode_data, confidence)
        """
        try:
            reader = self._get_reader()
            if reader is None:
                return None, "EasyOCR not available"
            
            image = cv2.imread(image_path)
            if image is None:
                return None, "Error: Could not load image"
            
            # Use EasyOCR to extract text
            results = reader.readtext(image, detail=0)
            
            if results:
                ocr_text = ' '.join(results)
                # Filter out only numeric characters that look like barcodes
                barcode_candidates = ''.join(c for c in ocr_text if c.isdigit() or c.isalpha())
                
                if barcode_candidates:
                    return [{
                        'data': barcode_candidates,
                        'method': 'easyocr',
                        'raw_text': ocr_text
                    }], "Success"
            
            return None, "No barcode detected with OCR"
        
        except Exception as e:
            return None, f"Error in OCR detection: {str(e)}"
    
    def detect_barcode_morphology(self, image_path):
        """
        Detect barcode using morphological operations and contour detection
        Returns: tuple (barcode_data, confidence)
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return None, "Error: Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply thresholding
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Get the largest contour (likely the barcode)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Extract ROI
                x, y, w, h = cv2.boundingRect(largest_contour)
                roi = image[y:y+h, x:x+w]
                
                # Apply OCR to ROI
                reader = self._get_reader()
                if reader is not None:
                    result = reader.readtext(roi, detail=0)
                    if result:
                        ocr_text = ' '.join(result)
                        barcode_candidates = ''.join(c for c in ocr_text if c.isdigit() or c.isalpha())
                        
                        if barcode_candidates:
                            return [{
                                'data': barcode_candidates,
                                'method': 'morphology',
                                'raw_text': ocr_text
                            }], "Success"
            
            return None, "No barcode detected with morphology"
        
        except Exception as e:
            return None, f"Error in morphology detection: {str(e)}"
    
    def extract_barcode(self, image_path):
        """
        Main method to extract barcode from image
        Tries multiple detection methods
        Returns: dict with barcode data and method used
        """
        if not os.path.exists(image_path):
            return {
                'success': False,
                'barcode_content': None,
                'method': None,
                'message': f'File not found: {image_path}'
            }
        
        # Try pyzbar first (most reliable for actual barcodes)
        results, msg = self.detect_barcode_pyzbar(image_path)
        if results:
            return {
                'success': True,
                'barcode_content': results[0]['data'],
                'method': 'pyzbar',
                'message': f'Barcode contents: b\'{results[0]["data"]}\''
            }
        
        # Try morphological approach
        results, msg = self.detect_barcode_morphology(image_path)
        if results:
            return {
                'success': True,
                'barcode_content': results[0]['data'],
                'method': 'morphology',
                'message': f'Barcode contents: b\'{results[0]["data"]}\''
            }
        
        # Try EasyOCR as fallback
        results, msg = self.detect_barcode_ocr(image_path)
        if results:
            return {
                'success': True,
                'barcode_content': results[0]['data'],
                'method': 'easyocr',
                'message': f'Barcode contents: b\'{results[0]["data"]}\''
            }
        
        return {
            'success': False,
            'barcode_content': None,
            'method': None,
            'message': 'No barcode detected in image'
        }
