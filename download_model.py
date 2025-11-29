#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download SCHP Model
تحميل نموذج SCHP
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()
MODELS_DIR = PROJECT_ROOT / "models" / "schp"

def download_model():
    """تحميل نموذج SCHP / Download SCHP model"""
    print("="*70)
    print("  Downloading SCHP Model")
    print("  تحميل نموذج SCHP")
    print("="*70 + "\n")
    
    try:
        import gdown
        
        # Check if model already exists with any known name
        possible_names = [
            "exp-schp-201908261155-lip.pth",
            "lip_final.pth",
            "schp_model.pth"
        ]
        
        for name in possible_names:
            model_path = MODELS_DIR / name
            if model_path.exists():
                size = model_path.stat().st_size / (1024**3)
                print(f"[✓] Model already exists: {name}")
                print(f"[✓] Size: {size:.2f} GB")
                return True
        
        # If no model found, download
        model_path = MODELS_DIR / "lip_final.pth"
        
        # Google Drive URL
        url = "https://drive.google.com/uc?id=1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN"
        
        print("[→] Downloading lip_final.pth...")
        print(f"[→] Saving to: {model_path}")
        print("[→] This may take 5-10 minutes depending on connection...\n")
        
        gdown.download(url, str(model_path), quiet=False)
        
        if model_path.exists():
            size = model_path.stat().st_size / (1024**3)
            print(f"\n[✓] Model downloaded successfully! ({size:.2f} GB)")
            return True
        else:
            print("[✗] Download failed!")
            return False
    except Exception as e:
        print(f"[✗] Error: {str(e)}")
        print("\n[→] Alternative: Download manually from:")
        print("    https://drive.google.com/file/d/1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN/view")
        print(f"\n[→] Then place it at: {MODELS_DIR}")
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
