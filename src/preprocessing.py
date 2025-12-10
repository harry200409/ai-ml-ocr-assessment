import cv2
import numpy as np


def preprocess_image(image_path, target_size=None):
    """
    Preprocess image for barcode detection
    
    Args:
        image_path: Path to image file
        target_size: Optional target size (width, height)
    
    Returns:
        Preprocessed image
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not load image: {image_path}")
    
    # Resize if target size specified
    if target_size:
        image = cv2.resize(image, target_size)
    
    return image


def enhance_contrast(image):
    """
    Enhance image contrast using CLAHE
    
    Args:
        image: Input image
    
    Returns:
        Contrast-enhanced image
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(image)
    
    return enhanced


def denoise_image(image):
    """
    Denoise image using bilateral filter
    
    Args:
        image: Input image
    
    Returns:
        Denoised image
    """
    denoised = cv2.bilateralFilter(image, 9, 75, 75)
    return denoised


def get_binary_image(image):
    """
    Convert image to binary
    
    Args:
        image: Input image
    
    Returns:
        Binary image
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    _, binary = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary


def apply_morphology(image, operation='close', kernel_size=(5, 5)):
    """
    Apply morphological operations
    
    Args:
        image: Input image
        operation: 'close', 'open', 'gradient'
        kernel_size: Size of morphological kernel
    
    Returns:
        Processed image
    """
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    
    if operation == 'close':
        result = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    elif operation == 'open':
        result = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    elif operation == 'gradient':
        result = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    else:
        raise ValueError(f"Unknown operation: {operation}")
    
    return result
