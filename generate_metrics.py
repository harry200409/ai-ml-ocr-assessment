#!/usr/bin/env python3
"""
Accuracy metrics generator for OCR Barcode Detector
Processes all training images and generates comprehensive accuracy report
"""

import os
import sys
import json
import csv
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from ocr_engine import BarcodeDetector
from utils import get_image_files, ensure_directory, save_results_json, save_results_csv


def generate_accuracy_metrics():
    """Generate accuracy metrics for all training images"""
    
    print("=" * 80)
    print("OCR BARCODE DETECTOR - ACCURACY METRICS GENERATOR")
    print("=" * 80)
    
    # Initialize detector
    detector = BarcodeDetector()
    
    # Get training images
    training_dir = r"k:\Harry\b\ReverseWay Bill"
    
    if not os.path.exists(training_dir):
        print(f"Error: Training directory not found: {training_dir}")
        return
    
    image_files = get_image_files(training_dir)
    print(f"\nFound {len(image_files)} training images")
    
    if not image_files:
        print("No images found to process!")
        return
    
    # Process each image
    results = []
    method_stats = {
        'pyzbar': {'success': 0, 'total': 0, 'barcodes': []},
        'morphology': {'success': 0, 'total': 0, 'barcodes': []},
        'easyocr': {'success': 0, 'total': 0, 'barcodes': []},
        'failed': {'count': 0}
    }
    
    print("\nProcessing images...")
    print("-" * 80)
    
    for idx, image_path in enumerate(image_files, 1):
        image_name = os.path.basename(image_path)
        print(f"[{idx}/{len(image_files)}] {image_name}...", end=" ", flush=True)
        
        try:
            result = detector.extract_barcode(str(image_path))
            
            detection_result = {
                'image': image_name,
                'image_path': str(image_path),
                'detected': result['success'],
                'barcode': result['barcode_content'] if result['success'] else 'N/A',
                'method': result['method'] if result['success'] else 'None',
                'message': result['message'],
                'timestamp': datetime.now().isoformat()
            }
            
            results.append(detection_result)
            
            if result['success']:
                method = result['method']
                method_stats[method]['success'] += 1
                method_stats[method]['total'] += 1
                method_stats[method]['barcodes'].append(result['barcode_content'])
                print(f"✓ [{method.upper()}] {result['barcode_content']}")
            else:
                for method in ['pyzbar', 'morphology', 'easyocr']:
                    method_stats[method]['total'] += 1
                method_stats['failed']['count'] += 1
                print(f"✗ FAILED")
        
        except Exception as e:
            detection_result = {
                'image': image_name,
                'image_path': str(image_path),
                'detected': False,
                'barcode': 'N/A',
                'method': 'None',
                'message': f"Error: {str(e)}",
                'timestamp': datetime.now().isoformat()
            }
            results.append(detection_result)
            
            for method in ['pyzbar', 'morphology', 'easyocr']:
                method_stats[method]['total'] += 1
            method_stats['failed']['count'] += 1
            print(f"✗ ERROR: {str(e)}")
    
    # Calculate metrics
    print("\n" + "=" * 80)
    print("ACCURACY METRICS")
    print("=" * 80)
    
    total_images = len(image_files)
    successful = sum(1 for r in results if r['detected'])
    failed = total_images - successful
    overall_accuracy = (successful / total_images * 100) if total_images > 0 else 0
    
    print(f"\nOVERALL STATISTICS:")
    print(f"  Total Images:     {total_images}")
    print(f"  Successful:       {successful}")
    print(f"  Failed:           {failed}")
    print(f"  Overall Accuracy: {overall_accuracy:.2f}%")
    
    print(f"\nMETHOD-SPECIFIC STATISTICS:")
    for method in ['pyzbar', 'morphology', 'easyocr']:
        stats = method_stats[method]
        if stats['total'] > 0:
            accuracy = (stats['success'] / stats['total'] * 100)
            print(f"  {method.upper()}:")
            print(f"    Success Rate: {stats['success']}/{stats['total']} ({accuracy:.2f}%)")
    
    # Save results
    print(f"\n" + "=" * 80)
    print("SAVING RESULTS")
    print("=" * 80)
    
    # Ensure results directory
    results_dir = os.path.join(os.path.dirname(__file__), 'results')
    ensure_directory(results_dir)
    
    # Save JSON results
    json_path = os.path.join(results_dir, 'accuracy_metrics.json')
    json_results = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_images': total_images,
            'successful': successful,
            'failed': failed,
            'overall_accuracy_percent': round(overall_accuracy, 2)
        },
        'method_statistics': {
            method: {
                'success_count': stats['success'],
                'total_attempted': stats['total'],
                'success_rate_percent': round(
                    (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0, 2
                ),
                'detected_barcodes': stats['barcodes']
            }
            for method in ['pyzbar', 'morphology', 'easyocr']
        },
        'detection_results': results
    }
    
    with open(json_path, 'w') as f:
        json.dump(json_results, f, indent=2)
    print(f"✓ JSON Results: {json_path}")
    
    # Save CSV results
    csv_path = os.path.join(results_dir, 'detection_results.csv')
    save_results_csv(results, csv_path)
    print(f"✓ CSV Results:  {csv_path}")
    
    # Create summary report
    report_path = os.path.join(results_dir, 'accuracy_report.txt')
    with open(report_path, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("OCR BARCODE DETECTOR - ACCURACY REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("OVERALL STATISTICS:\n")
        f.write(f"  Total Images:     {total_images}\n")
        f.write(f"  Successful:       {successful}\n")
        f.write(f"  Failed:           {failed}\n")
        f.write(f"  Overall Accuracy: {overall_accuracy:.2f}%\n\n")
        
        f.write("METHOD-SPECIFIC STATISTICS:\n")
        for method in ['pyzbar', 'morphology', 'easyocr']:
            stats = method_stats[method]
            if stats['total'] > 0:
                accuracy = (stats['success'] / stats['total'] * 100)
                f.write(f"  {method.upper()}:\n")
                f.write(f"    Success Rate: {stats['success']}/{stats['total']} ({accuracy:.2f}%)\n")
                f.write(f"    Detected Barcodes: {len(stats['barcodes'])}\n\n")
        
        f.write("DETAILED RESULTS:\n")
        f.write("-" * 80 + "\n")
        for result in results:
            f.write(f"File: {result['image']}\n")
            f.write(f"  Status:   {'DETECTED' if result['detected'] else 'FAILED'}\n")
            f.write(f"  Barcode:  {result['barcode']}\n")
            f.write(f"  Method:   {result['method']}\n")
            f.write(f"  Message:  {result['message']}\n\n")
    
    print(f"✓ Report:       {report_path}")
    
    print("\n" + "=" * 80)
    print("ACCURACY METRICS GENERATION COMPLETE")
    print("=" * 80)
    
    return {
        'total_images': total_images,
        'successful': successful,
        'failed': failed,
        'overall_accuracy': overall_accuracy,
        'results': results
    }


if __name__ == '__main__':
    generate_accuracy_metrics()
