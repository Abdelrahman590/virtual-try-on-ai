#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a test image by downloading a sample image from a free source.
إنشاء صورة اختبار من خلال تحميل صورة عينة من مصدر مجاني.
"""

import cv2
import numpy as np
from pathlib import Path
import urllib.request

PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_DIR = PROJECT_ROOT / "input"

def create_test_image_from_web():
    """Download a sample person image from web"""
    
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = INPUT_DIR / "test.jpg"
    
    # Try multiple free image sources
    urls = [
        # Wikimedia sample image
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ad/Camponotus_flavomarginatus_ant.jpg/640px-Camponotus_flavomarginatus_ant.jpg",
        # Simple sample
        "https://via.placeholder.com/600x800/87CEEB/000000?text=Person"
    ]
    
    # If web download fails, create synthetic image
    print("[→] Creating synthetic test image with improved human figure...")
    
    # Create image with better proportions and colors
    image = np.zeros((1200, 800, 3), dtype=np.uint8)
    
    # Background - realistic
    image[:] = (240, 235, 230)  # Light beige/gray background
    
    # Colors (BGR)
    skin = (200, 160, 130)
    dark_hair = (20, 20, 40)
    shirt_red = (50, 80, 220)  # Reddish
    pants_dark = (40, 40, 100)
    shoe_dark = (30, 30, 30)
    white = (255, 255, 255)
    black = (0, 0, 0)
    brown = (100, 80, 60)
    
    # Head positioned higher
    head_x, head_y = 400, 120
    
    # Draw hair/head
    cv2.circle(image, (head_x, head_y), 60, dark_hair, -1)
    
    # Draw face
    cv2.ellipse(image, (head_x, head_y + 10), (55, 65), 0, 0, 360, skin, -1)
    
    # Draw detailed face features
    # Eyes
    cv2.circle(image, (head_x - 25, head_y - 5), 8, white, -1)
    cv2.circle(image, (head_x + 25, head_y - 5), 8, white, -1)
    cv2.circle(image, (head_x - 25, head_y - 5), 5, black, -1)
    cv2.circle(image, (head_x + 25, head_y - 5), 5, black, -1)
    
    # Nose
    pts_nose = np.array([[head_x, head_y + 5], [head_x - 8, head_y + 20], [head_x + 8, head_y + 20]], np.int32)
    cv2.fillPoly(image, [pts_nose], skin)
    
    # Mouth
    cv2.ellipse(image, (head_x, head_y + 35), (18, 10), 0, 0, 180, (150, 100, 100), 2)
    
    # Neck
    cv2.rectangle(image, (head_x - 18, head_y + 70), (head_x + 18, head_y + 95), skin, -1)
    
    # Shoulders and body
    pts_body = np.array([
        [head_x - 50, head_y + 95],
        [head_x + 50, head_y + 95],
        [head_x + 60, head_y + 200],
        [head_x - 60, head_y + 200]
    ], np.int32)
    cv2.fillPoly(image, [pts_body], shirt_red)
    
    # Sleeves (arms)
    cv2.ellipse(image, (head_x - 65, head_y + 130), (30, 50), -20, 0, 180, shirt_red, -1)
    cv2.ellipse(image, (head_x + 65, head_y + 130), (30, 50), 20, 0, 180, shirt_red, -1)
    
    # Forearms
    cv2.line(image, (head_x - 80, head_y + 140), (head_x - 100, head_y + 230), skin, 25)
    cv2.line(image, (head_x + 80, head_y + 140), (head_x + 100, head_y + 230), skin, 25)
    
    # Hands
    cv2.circle(image, (head_x - 100, head_y + 240), 12, skin, -1)
    cv2.circle(image, (head_x + 100, head_y + 240), 12, skin, -1)
    
    # Waist (where shirt ends)
    cv2.rectangle(image, (head_x - 45, head_y + 200), (head_x + 45, head_y + 210), (180, 140, 100), -1)
    
    # Pants (two separate legs for realism)
    cv2.rectangle(image, (head_x - 35, head_y + 210), (head_x - 10, head_y + 480), pants_dark, -1)
    cv2.rectangle(image, (head_x + 10, head_y + 210), (head_x + 35, head_y + 480), pants_dark, -1)
    
    # Lower legs (skin visible)
    cv2.rectangle(image, (head_x - 35, head_y + 480), (head_x - 10, head_y + 540), skin, -1)
    cv2.rectangle(image, (head_x + 10, head_y + 480), (head_x + 35, head_y + 540), skin, -1)
    
    # Shoes
    cv2.rectangle(image, (head_x - 40, head_y + 540), (head_x - 5, head_y + 590), shoe_dark, -1)
    cv2.rectangle(image, (head_x + 5, head_y + 540), (head_x + 40, head_y + 590), shoe_dark, -1)
    
    # Add shirt buttons for detail
    for button_y in range(head_y + 220, head_y + 200, 40):
        if button_y < head_y + 200:
            cv2.circle(image, (head_x, button_y), 3, (30, 50, 100), -1)
    
    # Save image
    cv2.imwrite(str(output_path), image)
    
    print("[✓] Test image created successfully!")
    print(f"[✓] Image size: 800x1200 pixels")
    print(f"[✓] Features: Head, face, eyes, nose, mouth, neck, shirt, arms, pants, legs, shoes")
    print(f"[✓] Saved to: {output_path}")
    
    return True

if __name__ == "__main__":
    create_test_image_from_web()
