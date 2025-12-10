import cv2
import numpy as np
from PIL import Image


def extract_text_region(image, bounding_box):
    """
    Extract text region from image using bounding box
    
    Args:
        image: Input image
        bounding_box: (x, y, width, height)
    
    Returns:
        Extracted region
    """
    x, y, w, h = bounding_box
    roi = image[y:y+h, x:x+w]
    return roi


def get_contour_region(image):
    """
    Extract region of interest using contour detection
    
    Args:
        image: Input image (binary)
    
    Returns:
        Extracted ROI and bounding box
    """
    contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None
    
    # Get largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    return (x, y, w, h), largest_contour


def detect_edges(image, method='canny'):
    """
    Detect edges in image
    
    Args:
        image: Input image
        method: 'canny' or 'sobel'
    
    Returns:
        Edge map
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if method == 'canny':
        edges = cv2.Canny(image, 50, 150)
    elif method == 'sobel':
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=5)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=5)
        edges = np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return edges


def clean_text(text):
    """
    Clean extracted text
    
    Args:
        text: Raw extracted text
    
    Returns:
        Cleaned text
    """
    # Remove whitespace and special characters
    cleaned = ''.join(text.split())
    return cleaned


def filter_numeric(text):
    """
    Filter only numeric characters
    
    Args:
        text: Input text
    
    Returns:
        Numeric characters only
    """
    return ''.join(c for c in text if c.isdigit())


def validate_barcode_format(barcode_content):
    """
    Validate barcode format
    
    Args:
        barcode_content: Barcode string
    
    Returns:
        tuple (is_valid, confidence_score)
    """
    # Check if all digits
    if not barcode_content.replace(' ', '').isdigit():
        return False, 0.5
    
    # Check length (typical barcodes are 12-128 characters)
    if len(barcode_content) < 8 or len(barcode_content) > 128:
        return False, 0.6
    
    return True, 1.0
