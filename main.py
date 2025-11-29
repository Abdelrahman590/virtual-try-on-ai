#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Pipeline Script - Virtual Try-On AI
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime

# Add project paths
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

def print_header(msg, level=1):
    """Print formatted header"""
    if level == 1:
        print(f"\n{'='*70}")
        print(f"  {msg}")
        print(f"{'='*70}\n")
    else:
        print(f"\n{'-'*70}")
        print(f"  {msg}")
        print(f"{'-'*70}\n")

def print_status(msg, status="INFO"):
    """Print status message"""
    status_icons = {
        "SUCCESS": "✓",
        "ERROR": "✗",
        "WARNING": "⚠",
        "INFO": "→"
    }
    icon = status_icons.get(status, "→")
    print(f"[{icon}] {msg}")

def check_environment():
    """Check environment and required files"""
    print_header("Checking Environment", 2)
    
    all_good = True
    
    # Check required files
    required_files = [
        "requirements.txt",
        "run_parsing.py",
        "run_pose.py",
    ]
    
    for file in required_files:
        file_path = PROJECT_ROOT / file
        if file_path.exists():
            print_status(f"Found: {file}")
        else:
            print_status(f"Missing: {file}", "ERROR")
            all_good = False
    
    # Check folders
    required_folders = ["input", "parsing", "pose", "masks", "models/schp"]
    for folder in required_folders:
        folder_path = PROJECT_ROOT / folder
        if folder_path.exists():
            print_status(f"Folder exists: {folder}")
        else:
            print_status(f"Folder missing: {folder}", "ERROR")
            all_good = False
    
    return all_good

def check_input_image(image_path):
    """Check if input image exists"""
    print_header("Checking Input Image", 2)
    
    if not Path(image_path).exists():
        print_status(f"Input image not found: {image_path}", "ERROR")
        print_status("Please place an image at: input/test.jpg", "WARNING")
        return False
    
    print_status(f"Input image found: {image_path}", "SUCCESS")
    return True

def run_parsing():
    """Run human parsing script"""
    print_header("Step 1: Running Human Parsing", 2)
    
    try:
        import subprocess
        
        # Use Python 3.10 where mediapipe is installed
        python_exe = r"C:\Users\NUMBER 1\AppData\Local\Programs\Python\Python310\python.exe"
        if not Path(python_exe).exists():
            python_exe = sys.executable  # Fallback to current Python
        
        parsing_script = PROJECT_ROOT / "run_parsing.py"
        
        print_status("Executing parsing script...")
        result = subprocess.run(
            [str(python_exe), str(parsing_script)],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_status("Parsing completed successfully!", "SUCCESS")
            return True
        else:
            print_status("Parsing failed!", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error running parsing: {str(e)}", "ERROR")
        return False

def run_pose_estimation():
    """Run pose estimation script"""
    print_header("Step 2: Running Pose Estimation", 2)
    
    try:
        import subprocess
        
        # Use Python 3.10 where mediapipe is installed
        python_exe = r"C:\Users\NUMBER 1\AppData\Local\Programs\Python\Python310\python.exe"
        if not Path(python_exe).exists():
            python_exe = sys.executable  # Fallback to current Python
        
        pose_script = PROJECT_ROOT / "run_pose.py"
        
        print_status("Executing pose estimation script...")
        result = subprocess.run(
            [str(python_exe), str(pose_script)],
            capture_output=False,
            text=True
        )
        
        if result.returncode == 0:
            print_status("Pose estimation completed successfully!", "SUCCESS")
            return True
        else:
            print_status("Pose estimation failed!", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error running pose estimation: {str(e)}", "ERROR")
        return False

def load_measurements():
    """Load body measurements"""
    print_header("Step 3: Loading Results", 2)
    
    try:
        measurements_path = PROJECT_ROOT / "pose" / "body_measure.json"
        
        if not measurements_path.exists():
            print_status("Body measurements file not found", "WARNING")
            return {}
        
        with open(measurements_path, "r", encoding="utf-8") as f:
            measurements = json.load(f)
        
        print_status("Body measurements loaded successfully!", "SUCCESS")
        return measurements
    except Exception as e:
        print_status(f"Error loading measurements: {str(e)}", "ERROR")
        return {}

def check_output_files():
    """Check output files"""
    print_header("Verifying Output Files", 2)
    
    output_files = {
        "parsing/test_visual.png": "تصور التحليل",
        "parsing/test_labels.npy": "تسميات التحليل",
        "masks/body_mask.png": "قناع الجسم",
        "masks/cloth_mask.png": "قناع الملابس",
        "masks/skin_mask.png": "قناع الجلد",
        "pose/keypoints.json": "نقاط المفاصل",
        "pose/body_measure.json": "قياسات الجسم",
        "pose/skeleton.png": "صورة الهيكل العظمي",
    }
    
    found_files = 0
    for file_path, description in output_files.items():
        full_path = PROJECT_ROOT / file_path
        if full_path.exists():
            print_status(f"✓ {description:<30} ({file_path})")
            found_files += 1
        else:
            print_status(f"✗ {description:<30} ({file_path})", "WARNING")
    
    return found_files

def print_summary(measurements):
    """Print results summary"""
    print_header("Pipeline Execution Summary / ملخص تنفيذ المسار", 1)
    
    print("\n" + "="*70)
    print("BODY MEASUREMENTS / قياسات الجسم")
    print("="*70)
    
    if measurements:
        for key, value in measurements.items():
            ar_name = value.get("ar_name", key)
            measure_value = value.get("value", 0)
            unit = value.get("unit", "")
            
            # تنسيق الطباعة / Format printing
            print(f"  {ar_name:<35} {measure_value:>12.2f} {unit}")
    else:
        print("  No measurements available / لا توجد قياسات متاحة")
    
    print("\n" + "="*70)
    print("OUTPUT FILES LOCATION / موقع ملفات الإخراج")
    print("="*70)
    print(f"  Parsing Results:  {PROJECT_ROOT / 'parsing'}")
    print(f"  Segmentation Masks: {PROJECT_ROOT / 'masks'}")
    print(f"  Pose Estimation:  {PROJECT_ROOT / 'pose'}")
    print("\n" + "="*70)
    
    # طباعة التاريخ والوقت / Print timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"  Execution Time: {timestamp}")
    print("="*70 + "\n")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Virtual Try-On AI - Complete Pipeline"
    )
    parser.add_argument(
        "--image",
        type=str,
        default="input/test.jpg",
        help="Path to input image (default: input/test.jpg)"
    )
    parser.add_argument(
        "--skip-parsing",
        action="store_true",
        help="Skip parsing step"
    )
    parser.add_argument(
        "--skip-pose",
        action="store_true",
        help="Skip pose estimation step"
    )
    
    args = parser.parse_args()
    input_image = PROJECT_ROOT / args.image
    
    # Print start message
    print_header("Virtual Try-On AI - Complete Pipeline", 1)
    
    # Check environment
    if not check_environment():
        print_status("Environment check failed", "ERROR")
        return 1
    
    # Check input image
    if not check_input_image(input_image):
        return 1
    
    # تشغيل خطوات المسار / Run pipeline steps
    steps_completed = 0
    
    if not args.skip_parsing:
        if run_parsing():
            steps_completed += 1
        else:
            print_status("Pipeline aborted due to parsing failure", "ERROR")
            return 1
    
    if not args.skip_pose:
        if run_pose_estimation():
            steps_completed += 1
        else:
            print_status("Pipeline aborted due to pose estimation failure", "ERROR")
            return 1
    
    # التحقق من ملفات الإخراج / Check output files
    output_count = check_output_files()
    
    # تحميل وطباعة النتائج / Load and print results
    measurements = load_measurements()
    print_summary(measurements)
    
    print_status(f"Pipeline execution completed: {steps_completed}/{2-int(args.skip_parsing)-int(args.skip_pose)} steps", "SUCCESS")
    print_status(f"Output files created: {output_count}", "SUCCESS")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
