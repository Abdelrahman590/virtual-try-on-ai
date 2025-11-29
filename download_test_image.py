#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Download a real person image for testing the pipeline.
تحميل صورة شخص حقيقي لاختبار خط الأنابيب.
"""

import cv2
import numpy as np
from pathlib import Path
import urllib.request
import ssl

PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_DIR = PROJECT_ROOT / "input"

def download_real_person_image():
    """Download a real person image from Wikipedia Commons"""
    
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = INPUT_DIR / "test.jpg"
    
    # Create SSL context to bypass certificate issues
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Free image URLs from Wikimedia Commons (public domain)
    urls = [
        # Standing person - public domain
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/ReceiptSwiss.jpg/440px-ReceiptSwiss.jpg",
        # Another simple person image
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Cat03.jpg/1200px-Cat03.jpg",
    ]
    
    print("[→] Attempting to download a real person image...")
    
    downloaded = False
    for url in urls:
        try:
            print(f"[→] Trying: {url[:80]}...")
            urllib.request.urlretrieve(url, str(output_path), timeout=10)
            
            # Verify it's a valid image
            test_img = cv2.imread(str(output_path))
            if test_img is not None and test_img.shape[0] > 100 and test_img.shape[1] > 100:
                print(f"[✓] Successfully downloaded image: {test_img.shape}")
                downloaded = True
                break
            else:
                print("[✗] Downloaded file is not a valid image or too small")
        except Exception as e:
            print(f"[✗] Failed to download: {str(e)[:100]}")
    
    if not downloaded:
        print("[→] Download failed, creating enhanced synthetic image...")
        create_synthetic_person_image(output_path)
    
    return True

def create_synthetic_person_image(output_path):
    """Create a more realistic synthetic person image"""
    
    # Higher resolution for better detection
    height, width = 1600, 1000
    image = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Light background
    image[:] = (240, 235, 230)
    
    # Colors (BGR)
    skin = (210, 165, 145)
    dark_hair = (30, 25, 45)
    shirt_color = (60, 100, 220)  # Reddish/orange
    pants_color = (50, 50, 120)
    shoe_color = (40, 40, 40)
    white = (255, 255, 255)
    black = (0, 0, 0)
    
    # Head position (centered, upper part of image)
    head_x, head_y = width // 2, 150
    
    # ===== Draw head and face =====
    # Hair
    cv2.circle(image, (head_x, head_y), 80, dark_hair, -1)
    
    # Face
    cv2.ellipse(image, (head_x, head_y + 20), (75, 85), 0, 0, 360, skin, -1)
    
    # Left eye
    cv2.circle(image, (head_x - 35, head_y - 10), 12, white, -1)
    cv2.circle(image, (head_x - 35, head_y - 10), 8, black, -1)
    cv2.circle(image, (head_x - 32, head_y - 12), 4, white, 1)
    
    # Right eye
    cv2.circle(image, (head_x + 35, head_y - 10), 12, white, -1)
    cv2.circle(image, (head_x + 35, head_y - 10), 8, black, -1)
    cv2.circle(image, (head_x + 32, head_y - 12), 4, white, 1)
    
    # Nose (triangle)
    nose_pts = np.array([
        [head_x, head_y + 10],
        [head_x - 10, head_y + 35],
        [head_x + 10, head_y + 35]
    ], np.int32)
    cv2.fillPoly(image, [nose_pts], skin)
    
    # Mouth
    cv2.ellipse(image, (head_x, head_y + 50), (20, 12), 0, 0, 180, (160, 100, 100), 2)
    
    # ===== Draw body =====
    # Neck
    cv2.rectangle(image, (head_x - 25, head_y + 100), (head_x + 25, head_y + 140), skin, -1)
    
    # Shoulders and body
    body_pts = np.array([
        [head_x - 65, head_y + 140],
        [head_x + 65, head_y + 140],
        [head_x + 75, head_y + 280],
        [head_x - 75, head_y + 280]
    ], np.int32)
    cv2.fillPoly(image, [body_pts], shirt_color)
    
    # Left sleeve
    cv2.ellipse(image, (head_x - 80, head_y + 190), (35, 60), -25, 0, 180, shirt_color, -1)
    
    # Right sleeve
    cv2.ellipse(image, (head_x + 80, head_y + 190), (35, 60), 25, 0, 180, shirt_color, -1)
    
    # Left forearm (skin)
    cv2.line(image, (head_x - 105, head_y + 190), (head_x - 130, head_y + 320), skin, 35)
    
    # Right forearm (skin)
    cv2.line(image, (head_x + 105, head_y + 190), (head_x + 130, head_y + 320), skin, 35)
    
    # Hands
    cv2.circle(image, (head_x - 130, head_y + 330), 18, skin, -1)
    cv2.circle(image, (head_x + 130, head_y + 330), 18, skin, -1)
    
    # Waist belt area
    cv2.rectangle(image, (head_x - 60, head_y + 280), (head_x + 60, head_y + 295), (50, 50, 50), -1)
    
    # ===== Draw legs =====
    # Left leg
    cv2.rectangle(image, (head_x - 50, head_y + 295), (head_x - 20, head_y + 680), pants_color, -1)
    
    # Right leg
    cv2.rectangle(image, (head_x + 20, head_y + 295), (head_x + 50, head_y + 680), pants_color, -1)
    
    # Left ankle (skin)
    cv2.rectangle(image, (head_x - 50, head_y + 680), (head_x - 20, head_y + 750), skin, -1)
    
    # Right ankle (skin)
    cv2.rectangle(image, (head_x + 20, head_y + 680), (head_x + 50, head_y + 750), skin, -1)
    
    # Left shoe
    cv2.rectangle(image, (head_x - 55, head_y + 750), (head_x - 15, head_y + 820), shoe_color, -1)
    
    # Right shoe
    cv2.rectangle(image, (head_x + 15, head_y + 750), (head_x + 55, head_y + 820), shoe_color, -1)
    
    # Add shirt details
    # Buttons
    for button_y in range(head_y + 300, head_y + 270, -50):
        if button_y > head_y + 160:
            cv2.circle(image, (head_x, button_y), 4, (30, 50, 100), -1)
    
    # Shirt collar
    collar_pts = np.array([
        [head_x - 20, head_y + 140],
        [head_x + 20, head_y + 140],
        [head_x, head_y + 160]
    ], np.int32)
    cv2.fillPoly(image, [collar_pts], (40, 70, 180))
    
    # Save image
    cv2.imwrite(str(output_path), image)
    
    print(f"[✓] Created enhanced synthetic person image")
    print(f"[✓] Image size: {width}x{height} pixels")
    print(f"[✓] Saved to: {output_path}")

if __name__ == "__main__":
    download_real_person_image()
