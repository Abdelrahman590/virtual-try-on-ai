#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Test Image
توليد صورة اختبار
"""

import cv2
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_DIR = PROJECT_ROOT / "input"

def create_test_image():
    """Create a test image with a person-like figure"""
    
    img = np.ones((600, 600, 3), dtype=np.uint8) * 240  # Light gray background
    
    # Skin color / لون البشرة
    skin = (200, 170, 140)
    
    # Head / الرأس
    cv2.circle(img, (300, 100), 40, skin, -1)
    
    # Neck / الرقبة
    cv2.rectangle(img, (285, 135), (315, 160), skin, -1)
    
    # Body / الجسم (shirt)
    cv2.rectangle(img, (250, 160), (350, 300), (30, 70, 200), -1)  # Blue shirt
    
    # Arms / الذراعان
    cv2.line(img, (250, 180), (150, 220), skin, 25)
    cv2.line(img, (350, 180), (450, 220), skin, 25)
    
    # Pants / البنطال
    cv2.rectangle(img, (260, 300), (340, 480), (50, 50, 100), -1)
    
    # Legs / الساقان
    cv2.line(img, (280, 480), (280, 560), skin, 25)
    cv2.line(img, (320, 480), (320, 560), skin, 25)
    
    # Feet / القدمان
    cv2.circle(img, (280, 570), 20, (60, 50, 40), -1)
    cv2.circle(img, (320, 570), 20, (60, 50, 40), -1)
    
    # Eyes / العيون
    cv2.circle(img, (285, 90), 5, (0, 0, 0), -1)
    cv2.circle(img, (315, 90), 5, (0, 0, 0), -1)
    
    # Mouth / الفم
    cv2.line(img, (290, 110), (310, 110), (139, 69, 69), 2)
    
    output_path = INPUT_DIR / "test.jpg"
    cv2.imwrite(str(output_path), img)
    
    print("[✓] Test image created successfully!")
    print(f"[✓] Saved to: {output_path}")
    return True

if __name__ == "__main__":
    create_test_image()
