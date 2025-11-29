#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Installation Verification Script
سكريبت التحقق من التثبيت
"""

import sys
import importlib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()

def print_header(msg):
    """طباعة رأس / Print header"""
    print(f"\n{'='*70}")
    print(f"  {msg}")
    print(f"{'='*70}\n")

def print_status(msg, status="INFO"):
    """طباعة الحالة / Print status"""
    icons = {"SUCCESS": "✓", "ERROR": "✗", "WARNING": "⚠", "INFO": "→"}
    print(f"[{icons.get(status, '→')}] {msg}")

def check_python_version():
    """التحقق من إصدار Python / Check Python version"""
    print_header("Python Version")
    
    version = sys.version_info
    required = (3, 8)
    
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version >= required:
        print_status(f"Python {required[0]}.{required[1]}+ ✓", "SUCCESS")
        return True
    else:
        print_status(f"Python {required[0]}.{required[1]}+ required", "ERROR")
        return False

def check_packages():
    """التحقق من المكتبات / Check required packages"""
    print_header("Required Packages")
    
    packages = {
        "numpy": "Data processing",
        "cv2": "Image processing",
        "torch": "Deep learning",
        "torchvision": "Vision models",
        "mediapipe": "Pose estimation",
        "PIL": "Image library",
        "gdown": "File download",
    }
    
    all_installed = True
    
    for package, description in packages.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, "__version__", "unknown")
            print_status(f"{package:<20} {description:<30} v{version}", "SUCCESS")
        except ImportError:
            print_status(f"{package:<20} {description:<30} NOT FOUND", "ERROR")
            all_installed = False
    
    return all_installed

def check_folders():
    """التحقق من المجلدات / Check required folders"""
    print_header("Project Folders")
    
    folders = [
        "input",
        "output",
        "models/schp",
        "parsing",
        "pose",
        "masks",
        "scripts",
    ]
    
    all_exist = True
    
    for folder in folders:
        folder_path = PROJECT_ROOT / folder
        if folder_path.exists():
            print_status(f"{folder:<30} ✓", "SUCCESS")
        else:
            print_status(f"{folder:<30} Missing", "ERROR")
            all_exist = False
    
    return all_exist

def check_scripts():
    """التحقق من السكريبتات / Check required scripts"""
    print_header("Required Scripts")
    
    scripts = [
        "setup.py",
        "main.py",
        "run_parsing.py",
        "run_pose.py",
        "batch_process.py",
        "scripts/utils.py",
        "scripts/config.py",
    ]
    
    all_exist = True
    
    for script in scripts:
        script_path = PROJECT_ROOT / script
        if script_path.exists():
            print_status(f"{script:<30} ✓", "SUCCESS")
        else:
            print_status(f"{script:<30} Missing", "ERROR")
            all_exist = False
    
    return all_exist

def check_cuda():
    """التحقق من CUDA / Check CUDA availability"""
    print_header("GPU Support (CUDA)")
    
    try:
        import torch
        
        if torch.cuda.is_available():
            print_status(f"CUDA Available", "SUCCESS")
            print_status(f"Device: {torch.cuda.get_device_name(0)}", "SUCCESS")
            print_status(f"CUDA Version: {torch.version.cuda}", "SUCCESS")
            return True
        else:
            print_status("CUDA Not Available (CPU will be used)", "WARNING")
            return False
    except Exception as e:
        print_status(f"Error checking CUDA: {str(e)}", "ERROR")
        return False

def check_model_files():
    """التحقق من ملفات النموذج / Check model files"""
    print_header("Model Files")
    
    model_files = {
        "models/schp/lip_final.pth": "SCHP Model",
    }
    
    all_exist = True
    
    for file, description in model_files.items():
        file_path = PROJECT_ROOT / file
        if file_path.exists():
            size = file_path.stat().st_size / (1024 * 1024)  # Convert to MB
            print_status(f"{description:<30} {size:.1f} MB", "SUCCESS")
        else:
            print_status(f"{description:<30} Not Downloaded", "WARNING")
            all_exist = False
    
    return all_exist

def check_requirements_txt():
    """التحقق من ملف requirements.txt / Check requirements file"""
    print_header("Requirements File")
    
    req_file = PROJECT_ROOT / "requirements.txt"
    
    if req_file.exists():
        with open(req_file, "r") as f:
            lines = f.readlines()
        print_status(f"Found {len(lines)} dependencies", "SUCCESS")
        return True
    else:
        print_status("requirements.txt not found", "ERROR")
        return False

def print_summary(results):
    """طباعة ملخص التحقق / Print verification summary"""
    print_header("Verification Summary / ملخص التحقق")
    
    total = len(results)
    passed = sum(1 for r in results.values() if r)
    
    print(f"Checks Passed: {passed}/{total}")
    print(f"Status: {'✓ READY' if passed == total else '⚠ INCOMPLETE' if passed >= total * 0.8 else '✗ ISSUES FOUND'}")
    
    if passed < total:
        print("\nFailed Checks:")
        for check, result in results.items():
            if not result:
                print(f"  - {check}")

def main():
    """الدالة الرئيسية / Main function"""
    print("="*70)
    print("  Virtual Try-On AI - Installation Verification")
    print("  تحقق من تثبيت تطبيق الملابس الافتراضية")
    print("="*70)
    
    results = {
        "Python Version": check_python_version(),
        "Required Packages": check_packages(),
        "Project Folders": check_folders(),
        "Required Scripts": check_scripts(),
        "Model Files": check_model_files(),
        "Requirements File": check_requirements_txt(),
        "CUDA Support": check_cuda(),
    }
    
    print_summary(results)
    
    print("\n" + "="*70)
    
    if all(results.values()):
        print("  ✓ Installation Complete - Ready to Use!")
        print("  ✓ الإعداد كامل - جاهز للاستخدام!")
        print("="*70)
        print("\nNext Steps:")
        print("  1. Place your image in: input/test.jpg")
        print("  2. Run: python main.py")
        print("\nخطوات إضافية:")
        print("  1. ضع صورتك في: input/test.jpg")
        print("  2. شغل: python main.py")
        return 0
    else:
        print("  ⚠ Some checks failed - Review issues above")
        print("  ⚠ بعض الفحوصات فشلت - راجع المشاكل أعلاه")
        print("="*70)
        print("\nTo fix issues:")
        print("  1. Run: python setup.py")
        print("  2. Ensure all dependencies are installed")
        print("  3. Check that all folders exist")
        return 1

if __name__ == "__main__":
    sys.exit(main())
