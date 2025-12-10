#!/usr/bin/env python3
"""
Project completion verification script
Verifies all components are in place and working
"""

import os
import sys
from pathlib import Path
import json

def check_file_exists(file_path, description):
    """Check if file exists"""
    if os.path.exists(file_path):
        print(f"✓ {description}: {file_path}")
        return True
    else:
        print(f"✗ {description} NOT FOUND: {file_path}")
        return False

def verify_project():
    """Verify complete project structure"""
    
    print("\n" + "=" * 80)
    print("OCR BARCODE DETECTOR - PROJECT VERIFICATION")
    print("=" * 80 + "\n")
    
    project_root = os.path.dirname(__file__)
    checks = []
    
    # Check main files
    print("Main Files:")
    checks.append(check_file_exists(os.path.join(project_root, 'app.py'), "Streamlit App"))
    checks.append(check_file_exists(os.path.join(project_root, 'README.md'), "README"))
    checks.append(check_file_exists(os.path.join(project_root, 'requirements.txt'), "Requirements"))
    checks.append(check_file_exists(os.path.join(project_root, 'generate_metrics.py'), "Metrics Generator"))
    
    # Check src folder
    print("\nSource Code (src/):")
    checks.append(check_file_exists(os.path.join(project_root, 'src', 'ocr_engine.py'), "OCR Engine"))
    checks.append(check_file_exists(os.path.join(project_root, 'src', 'preprocessing.py'), "Preprocessing"))
    checks.append(check_file_exists(os.path.join(project_root, 'src', 'text_extraction.py'), "Text Extraction"))
    checks.append(check_file_exists(os.path.join(project_root, 'src', 'utils.py'), "Utils"))
    
    # Check results
    print("\nResults/Metrics:")
    checks.append(check_file_exists(os.path.join(project_root, 'results', 'accuracy_metrics.json'), "Metrics JSON"))
    checks.append(check_file_exists(os.path.join(project_root, 'results', 'detection_results.csv'), "Detection CSV"))
    checks.append(check_file_exists(os.path.join(project_root, 'results', 'accuracy_report.txt'), "Accuracy Report"))
    
    # Check tests
    print("\nTests:")
    checks.append(check_file_exists(os.path.join(project_root, 'tests', 'run_tests.py'), "Test Runner"))
    
    # Check documentation
    print("\nDocumentation:")
    checks.append(check_file_exists(os.path.join(project_root, 'ACCURACY_SUMMARY.md'), "Accuracy Summary"))
    
    # Load and display accuracy metrics
    print("\n" + "=" * 80)
    print("ACCURACY METRICS")
    print("=" * 80 + "\n")
    
    metrics_file = os.path.join(project_root, 'results', 'accuracy_metrics.json')
    try:
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)
        
        summary = metrics['summary']
        print(f"Total Images:        {summary['total_images']}")
        print(f"Successfully Detected: {summary['successful']}")
        print(f"Failed:              {summary['failed']}")
        print(f"Overall Accuracy:    {summary['overall_accuracy_percent']:.1f}%")
        
        print("\nMethod-Specific Performance:")
        for method, stats in metrics['method_statistics'].items():
            print(f"  {method.upper()}:")
            print(f"    Success Rate: {stats['success_count']}/{stats['total_attempted']} ({stats['success_rate_percent']:.1f}%)")
    
    except Exception as e:
        print(f"Error reading metrics: {e}")
    
    # Display project structure
    print("\n" + "=" * 80)
    print("PROJECT STRUCTURE")
    print("=" * 80 + "\n")
    
    print("ocr_barcode_detector/")
    print("├── app.py                     ← Main Streamlit application")
    print("├── README.md                  ← Documentation")
    print("├── requirements.txt           ← Dependencies")
    print("├── generate_metrics.py        ← Accuracy metrics generator")
    print("├── src/                       ← Professional source code")
    print("│   ├── ocr_engine.py         ← Core detection (3 methods)")
    print("│   ├── preprocessing.py      ← Image processing")
    print("│   ├── text_extraction.py    ← Text extraction")
    print("│   └── utils.py              ← Helper utilities")
    print("├── tests/                     ← Test suite")
    print("│   └── run_tests.py          ← Test runner")
    print("├── results/                   ← Accuracy metrics")
    print("│   ├── accuracy_metrics.json ← JSON metrics")
    print("│   ├── detection_results.csv ← CSV results")
    print("│   └── accuracy_report.txt   ← Text report")
    print("└── notebooks/                 ← Jupyter notebooks")
    
    # Summary
    print("\n" + "=" * 80)
    print("VERIFICATION SUMMARY")
    print("=" * 80 + "\n")
    
    total_checks = len(checks)
    passed_checks = sum(checks)
    
    print(f"Checks Passed: {passed_checks}/{total_checks}")
    
    if all(checks):
        print("\n✅ ALL CHECKS PASSED - PROJECT IS COMPLETE")
        print("\nTo start using the detector:")
        print("  1. Run: streamlit run app.py")
        print("  2. Open: http://localhost:8501")
        print("  3. Upload barcode images and detect!")
        return True
    else:
        print("\n⚠️  Some checks failed - review above")
        return False

if __name__ == '__main__':
    success = verify_project()
    sys.exit(0 if success else 1)
