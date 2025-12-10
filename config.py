"""
Configuration file for OCR Barcode Detector
Customize detection behavior here
"""

# Detection Settings
DETECTION_CONFIG = {
    # Use GPU for EasyOCR (requires CUDA)
    'use_gpu': False,
    
    # Which detection methods to use (in order of preference)
    'methods': ['pyzbar', 'morphology', 'easyocr'],
    
    # Enable detailed logging
    'verbose': False,
    
    # Timeout for detection (seconds)
    'timeout': 300,
}

# Image Processing Settings
IMAGE_CONFIG = {
    # Maximum image width (pixels)
    'max_width': 2000,
    
    # Maximum image height (pixels)
    'max_height': 2000,
    
    # Image quality for display
    'display_quality': 85,
    
    # Supported image formats
    'supported_formats': ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'],
}

# PyZbar Settings
PYZBAR_CONFIG = {
    # Enable PyZbar detection
    'enabled': True,
}

# Morphology Settings
MORPHOLOGY_CONFIG = {
    'enabled': True,
    
    # Morphological kernel size
    'kernel_size': 5,
    
    # Morphological operations type
    'morph_operation': 'MORPH_CLOSE',
}

# EasyOCR Settings
EASYOCR_CONFIG = {
    'enabled': True,
    
    # Languages to recognize
    'languages': ['en'],
    
    # Detection confidence threshold (0.0 to 1.0)
    'confidence_threshold': 0.5,
    
    # Use GPU if available
    'gpu': False,
    
    # Model cache directory
    'model_dir': None,  # None = default cache location
}

# GUI Settings
GUI_CONFIG = {
    # Window size
    'window_width': 1000,
    'window_height': 750,
    
    # Theme colors
    'primary_color': '#3498db',
    'success_color': '#27ae60',
    'danger_color': '#e74c3c',
    'header_color': '#2c3e50',
    
    # Font settings
    'font_family': 'Arial',
    'font_size_title': 24,
    'font_size_label': 11,
    'font_size_content': 10,
    
    # Image preview size
    'preview_max_width': 350,
    'preview_max_height': 450,
    
    # Show loading indicator
    'show_loading': True,
}

# Output Settings
OUTPUT_CONFIG = {
    # Format for barcode output
    'format': "Barcode contents: b'{barcode}'",
    
    # Include detection method in output
    'include_method': True,
    
    # Include raw text in output
    'include_raw_text': False,
    
    # Save results to file
    'save_results': False,
    'results_file': 'barcode_results.txt',
}

# Logging Settings
LOGGING_CONFIG = {
    # Enable logging
    'enabled': True,
    
    # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    'level': 'INFO',
    
    # Log file path
    'log_file': 'barcode_detector.log',
    
    # Log format
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
}


def get_config(section):
    """Get configuration for a specific section"""
    configs = {
        'detection': DETECTION_CONFIG,
        'image': IMAGE_CONFIG,
        'pyzbar': PYZBAR_CONFIG,
        'morphology': MORPHOLOGY_CONFIG,
        'easyocr': EASYOCR_CONFIG,
        'gui': GUI_CONFIG,
        'output': OUTPUT_CONFIG,
        'logging': LOGGING_CONFIG,
    }
    return configs.get(section, {})


def get_all_config():
    """Get all configuration"""
    return {
        'detection': DETECTION_CONFIG,
        'image': IMAGE_CONFIG,
        'pyzbar': PYZBAR_CONFIG,
        'morphology': MORPHOLOGY_CONFIG,
        'easyocr': EASYOCR_CONFIG,
        'gui': GUI_CONFIG,
        'output': OUTPUT_CONFIG,
        'logging': LOGGING_CONFIG,
    }
