import os
from pathlib import Path
from datetime import datetime
import json
import csv


def get_project_root():
    """Get project root directory"""
    return Path(__file__).parent.parent


def ensure_directory(directory_path):
    """
    Create directory if it doesn't exist
    
    Args:
        directory_path: Path to directory
    """
    Path(directory_path).mkdir(parents=True, exist_ok=True)


def load_config(config_path):
    """
    Load configuration from JSON file
    
    Args:
        config_path: Path to config file
    
    Returns:
        Configuration dict
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    return config


def save_results_csv(results, output_path):
    """
    Save detection results to CSV
    
    Args:
        results: List of detection results
        output_path: Output file path
    """
    if not results:
        return
    
    keys = results[0].keys()
    
    with open(output_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(results)


def save_results_json(results, output_path):
    """
    Save detection results to JSON
    
    Args:
        results: Results to save
        output_path: Output file path
    """
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)


def load_results_json(input_path):
    """
    Load detection results from JSON
    
    Args:
        input_path: Input file path
    
    Returns:
        Loaded results
    """
    with open(input_path, 'r') as f:
        results = json.load(f)
    
    return results


def timestamp():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def format_barcode_output(barcode_content):
    """
    Format barcode output to required format
    
    Args:
        barcode_content: Raw barcode content
    
    Returns:
        Formatted output (b'content')
    """
    return f"b'{barcode_content}'"


def get_image_files(directory_path, extensions=None):
    """
    Get all image files from directory
    
    Args:
        directory_path: Path to directory
        extensions: List of file extensions (e.g., ['.jpg', '.png'])
    
    Returns:
        List of image file paths
    """
    if extensions is None:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    
    if not os.path.exists(directory_path):
        return []
    
    image_files = []
    for ext in extensions:
        image_files.extend(Path(directory_path).glob(f'*{ext}'))
        image_files.extend(Path(directory_path).glob(f'*{ext.upper()}'))
    
    return sorted(list(set(image_files)))
