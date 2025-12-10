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

    def _load_image(self, image_path):
        """Load image as numpy array"""
        image = cv2.imread(image_path)
        return image
    
    def _get_reader(self):
        """Lazy load EasyOCR reader to avoid startup delays"""
        if self.reader is None and EASYOCR_AVAILABLE:
            self.reader = easyocr.Reader(
                ['en'], 
                gpu=False,
                verbose=False,
                model_storage_directory=os.path.expanduser('~/.easyocr')
            )
        return self.reader
    
    def _rotate_image(self, image, angle):
        """Rotate image by given angle while keeping full frame"""
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        cos = np.abs(matrix[0, 0])
        sin = np.abs(matrix[0, 1])
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))
        matrix[0, 2] += (nW / 2) - center[0]
        matrix[1, 2] += (nH / 2) - center[1]
        rotated = cv2.warpAffine(image, matrix, (nW, nH), borderMode=cv2.BORDER_REPLICATE)
        return rotated

    def _try_rotations(self, image, detector_fn, angles=None):
        """Try detection on multiple rotations to handle tilted codes"""
        if angles is None:
            angles = [0, -15, 15, -30, 30, -45, 45]
        last_msg = "No result"
        for angle in angles:
            rotated = image if angle == 0 else self._rotate_image(image, angle)
            result, msg = detector_fn(rotated)
            if result:
                if angle != 0:
                    msg = f"{msg} (angle {angle}°)"
                return result, msg
            last_msg = msg
        return None, last_msg

    def detect_barcode_pyzbar(self, image_path=None, image=None):
        """
        Detect barcode using pyzbar library
        Returns: tuple (barcode_data, confidence)
        """
        try:
            if image is None:
                image = self._load_image(image_path)
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
    
    def detect_barcode_morphology(self, image_path=None, image=None):
        """
        Detect barcode using morphological operations + OCR
        """
        try:
            reader = self._get_reader()
            if reader is None:
                return None, "EasyOCR not available"
            
            if image is None:
                image = self._load_image(image_path)
            if image is None:
                return None, "Error: Could not load image"
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            grad = cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel)
            
            # Threshold
            _, thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Find contours
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                return None, "No contours found"
            
            # Get largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Extract region
            roi = image[y:y+h, x:x+w]
            
            # OCR on extracted region
            result = reader.readtext(roi)
            
            if result:
                text = ''.join([text[1] for text in result])
                return [{'data': text, 'method': 'morphology'}], "Success"
            
            return None, "No text found in extracted region"
        
        except Exception as e:
            return None, f"Error in morphology detection: {str(e)}"
    
    def detect_barcode_ocr(self, image_path=None, image=None):
        """
        Detect barcode using EasyOCR
        """
        try:
            reader = self._get_reader()
            if reader is None:
                return None, "EasyOCR not available"
            
            if image is None:
                image = self._load_image(image_path)
            if image is None:
                return None, "Error: Could not load image"
            
            # Direct OCR
            result = reader.readtext(image)
            
            if result:
                text = ''.join([text[1] for text in result])
                return [{'data': text, 'method': 'easyocr'}], "Success"
            
            return None, "No text found with EasyOCR"
        
        except Exception as e:
            return None, f"Error in OCR detection: {str(e)}"
    
    def extract_barcode(self, image_path):
        """
        Extract barcode content using cascading approach
        Returns: dict with success status and barcode content
        """
        image = self._load_image(image_path)
        if image is None:
            return {
                'success': False,
                'barcode_content': None,
                'method': None,
                'message': 'Failed to load image'
            }

        # Try pyzbar first (fastest and most accurate) with rotations
        result, msg = self._try_rotations(image, lambda img: self.detect_barcode_pyzbar(image=img))
        if result:
            return {
                'success': True,
                'barcode_content': result[0]['data'],
                'method': 'pyzbar',
                'message': msg
            }

        # Try morphology approach with rotations
        result, msg = self._try_rotations(image, lambda img: self.detect_barcode_morphology(image=img))
        if result:
            return {
                'success': True,
                'barcode_content': result[0]['data'],
                'method': 'morphology',
                'message': msg
            }

        # Try pure OCR with rotations
        result, msg = self._try_rotations(image, lambda img: self.detect_barcode_ocr(image=img))
        if result:
            return {
                'success': True,
                'barcode_content': result[0]['data'],
                'method': 'easyocr',
                'message': msg
            }

        # All methods failed
        return {
            'success': False,
            'barcode_content': None,
            'method': None,
            'message': f'Failed to detect barcode. Last error: {msg}'
        }
