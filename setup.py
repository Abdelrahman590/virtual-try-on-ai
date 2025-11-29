#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Virtual Try-On AI - Setup Script
سكريبت إعداد تطبيق الملابس الافتراضية - Virtual Try-On AI
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# إعدادات المشروع / Project Configuration
PROJECT_ROOT = Path(__file__).parent.absolute()
PYTHON_VERSION = "3.8"
VENV_NAME = "venv"
VENV_PATH = PROJECT_ROOT / VENV_NAME

# معرفات النماذج / Model Identifiers
SCHP_MODEL_ID = "1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN"  # Google Drive ID for lip_final.pth
SCHP_REPO_URL = "https://github.com/PeikeLi/Self-Correction-Human-Parsing.git"

# قائمة المجلدات المطلوبة / Required Folders
REQUIRED_FOLDERS = [
    "input",
    "output",
    "parsing",
    "pose",
    "masks",
    "models/schp",
    "scripts"
]

def print_header(msg):
    """طباعة رأس الرسالة / Print formatted header"""
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}\n")

def print_status(msg, status="INFO"):
    """طباعة رسالة الحالة / Print status message"""
    status_icon = "✓" if status == "SUCCESS" else "✗" if status == "ERROR" else "→"
    print(f"[{status_icon}] {msg}")

def create_folders():
    """إنشاء جميع المجلدات المطلوبة / Create all required folders"""
    print_header("Creating Project Folders")
    
    try:
        for folder in REQUIRED_FOLDERS:
            folder_path = PROJECT_ROOT / folder
            folder_path.mkdir(parents=True, exist_ok=True)
            print_status(f"Created folder: {folder}")
        
        print_status("All folders created successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error creating folders: {str(e)}", "ERROR")
        return False

def create_venv():
    """إنشاء بيئة افتراضية / Create Python virtual environment"""
    print_header("Creating Virtual Environment")
    
    try:
        if VENV_PATH.exists():
            print_status(f"Virtual environment already exists at {VENV_PATH}")
            return True
        
        print_status(f"Creating virtual environment with Python {PYTHON_VERSION}...")
        subprocess.run(
            [sys.executable, "-m", "venv", str(VENV_PATH)],
            check=True,
            capture_output=True
        )
        print_status("Virtual environment created successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error creating virtual environment: {str(e)}", "ERROR")
        return False

def get_pip_path():
    """الحصول على مسار pip / Get pip executable path"""
    if sys.platform == "win32":
        return VENV_PATH / "Scripts" / "pip.exe"
    else:
        return VENV_PATH / "bin" / "pip"

def get_python_path():
    """الحصول على مسار python / Get python executable path"""
    if sys.platform == "win32":
        return VENV_PATH / "Scripts" / "python.exe"
    else:
        return VENV_PATH / "bin" / "python"

def install_dependencies():
    """تثبيت جميع المكتبات المطلوبة / Install all required dependencies"""
    print_header("Installing Dependencies")
    
    try:
        pip_path = get_pip_path()
        
        # تحديث pip / Upgrade pip
        print_status("Upgrading pip...")
        subprocess.run(
            [str(pip_path), "install", "--upgrade", "pip"],
            check=True,
            capture_output=True
        )
        print_status("pip upgraded", "SUCCESS")
        
        # تثبيت المتطلبات / Install requirements
        print_status("Installing packages from requirements.txt...")
        requirements_file = PROJECT_ROOT / "requirements.txt"
        
        if not requirements_file.exists():
            print_status(f"requirements.txt not found at {requirements_file}", "ERROR")
            return False
        
        subprocess.run(
            [str(pip_path), "install", "-r", str(requirements_file)],
            check=True
        )
        print_status("All packages installed successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error installing dependencies: {str(e)}", "ERROR")
        return False

def clone_schp_repo():
    """استنساخ مستودع SCHP / Clone Self-Correction-Human-Parsing repository"""
    print_header("Cloning SCHP Repository")
    
    try:
        schp_path = PROJECT_ROOT / "models" / "schp" / "Self-Correction-Human-Parsing"
        
        if schp_path.exists():
            print_status("SCHP repository already exists")
            return True
        
        print_status("Cloning from GitHub...")
        subprocess.run(
            ["git", "clone", SCHP_REPO_URL, str(schp_path)],
            check=True,
            capture_output=True
        )
        print_status("Repository cloned successfully!", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error cloning repository: {str(e)}", "ERROR")
        print_status("Git might not be installed. Please install Git from https://git-scm.com/")
        return False

def download_schp_model():
    """تحميل نموذج SCHP / Download SCHP pretrained model"""
    print_header("Downloading SCHP Model")
    
    try:
        import gdown
        
        model_dir = PROJECT_ROOT / "models" / "schp"
        model_path = model_dir / "lip_final.pth"
        
        if model_path.exists():
            print_status("SCHP model already exists")
            return True
        
        print_status("Downloading lip_final.pth (this may take a few minutes)...")
        
        # Google Drive URL
        url = f"https://drive.google.com/uc?id={SCHP_MODEL_ID}"
        gdown.download(url, str(model_path), quiet=False)
        
        if model_path.exists():
            print_status(f"Model downloaded successfully to {model_path}!", "SUCCESS")
            return True
        else:
            print_status("Model download failed", "ERROR")
            return False
    except Exception as e:
        print_status(f"Error downloading model: {str(e)}", "ERROR")
        print_status("You can download the model manually from:")
        print_status("https://drive.google.com/file/d/1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN/view")
        return False

def verify_setup():
    """التحقق من إتمام الإعداد / Verify setup completion"""
    print_header("Verifying Setup")
    
    all_good = True
    
    # التحقق من المجلدات / Check folders
    for folder in REQUIRED_FOLDERS:
        folder_path = PROJECT_ROOT / folder
        if folder_path.exists():
            print_status(f"✓ {folder}")
        else:
            print_status(f"✗ {folder} - MISSING", "ERROR")
            all_good = False
    
    # التحقق من البيئة الافتراضية / Check virtual environment
    if VENV_PATH.exists():
        print_status("✓ Virtual environment")
    else:
        print_status("✗ Virtual environment - MISSING", "ERROR")
        all_good = False
    
    return all_good

def main():
    """الدالة الرئيسية / Main function"""
    print_header("Virtual Try-On AI - Project Setup")
    print("تطبيق الملابس الافتراضية - الإعداد الأولي")
    
    steps = [
        ("Creating folders", create_folders),
        ("Creating virtual environment", create_venv),
        ("Installing dependencies", install_dependencies),
        ("Cloning SCHP repository", clone_schp_repo),
        ("Downloading SCHP model", download_schp_model),
    ]
    
    completed = 0
    for step_name, step_func in steps:
        if step_func():
            completed += 1
        else:
            print_status(f"Setup incomplete at step: {step_name}", "ERROR")
            break
    
    # التحقق النهائي / Final verification
    print("\n")
    if verify_setup():
        print_header("Setup Completed Successfully! ✓")
        print("تم إكمال الإعداد بنجاح!")
        print(f"\nNext steps:")
        print(f"1. Copy your image to: {PROJECT_ROOT}/input/test.jpg")
        print(f"2. Run: python main.py")
        print(f"\nخطوات إضافية:")
        print(f"1. ضع صورتك في: {PROJECT_ROOT}/input/test.jpg")
        print(f"2. شغل: python main.py")
        return 0
    else:
        print_header("Setup Incomplete")
        print(f"Please resolve the issues above / رجاء حل المشاكل أعلاه")
        return 1

if __name__ == "__main__":
    sys.exit(main())
