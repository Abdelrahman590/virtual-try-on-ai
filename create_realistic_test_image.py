#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create a more realistic test image with a human figure for testing the pipeline.
إنشاء صورة اختبار واقعية برسم شخصي لاختبار خط الأنابيب.
"""

import cv2
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_DIR = PROJECT_ROOT / "input"

def create_realistic_test_image():
    """Create a realistic test image with human figure"""
    
    # Create image (1000x800 with gradient background)
    image = np.zeros((1000, 800, 3), dtype=np.uint8)
    
    # Create background gradient (light gray)
    for i in range(1000):
        color_value = int(200 + (i / 1000) * 55)
        image[i, :] = [color_value, color_value, color_value]
    
    # Colors (BGR format for OpenCV)
    skin_color = (180, 160, 145)      # Natural skin tone
    neck_color = (180, 160, 145)
    shirt_color = (40, 80, 200)       # Red/reddish shirt (B=40, G=80, R=200)
    pants_color = (40, 40, 100)       # Dark blue jeans
    shoe_color = (30, 30, 30)         # Black shoes
    white = (255, 255, 255)
    black = (0, 0, 0)
    hair_color = (20, 20, 40)         # Dark brown/black hair
    
    # Human figure position (centered)
    center_x, center_y = 400, 150
    
    # Draw hair (head)
    cv2.circle(image, (center_x, center_y), 55, hair_color, -1)
    
    # Draw face (skin)
    cv2.circle(image, (center_x, center_y + 5), 50, skin_color, -1)
    
    # Draw neck
    cv2.rectangle(image, (center_x - 15, center_y + 45), (center_x + 15, center_y + 65), neck_color, -1)
    
    # Draw left eye
    cv2.circle(image, (center_x - 20, center_y), 6, white, -1)
    cv2.circle(image, (center_x - 20, center_y), 3, black, -1)
    
    # Draw right eye
    cv2.circle(image, (center_x + 20, center_y), 6, white, -1)
    cv2.circle(image, (center_x + 20, center_y), 3, black, -1)
    
    # Draw nose
    cv2.line(image, (center_x, center_y + 5), (center_x, center_y + 15), skin_color, 3)
    
    # Draw mouth
    cv2.ellipse(image, (center_x, center_y + 25), (15, 8), 0, 0, 180, (160, 140, 140), 2)
    
    # Draw shirt/torso (more voluminous)
    pts = np.array([
        [center_x - 45, center_y + 65],      # Left shoulder
        [center_x + 45, center_y + 65],      # Right shoulder
        [center_x + 50, center_y + 140],     # Right side
        [center_x - 50, center_y + 140],     # Left side
    ], np.int32)
    cv2.fillPoly(image, [pts], shirt_color)
    
    # Draw left sleeve
    cv2.ellipse(image, (center_x - 50, center_y + 85), (25, 35), 15, 0, 180, shirt_color, -1)
    
    # Draw right sleeve
    cv2.ellipse(image, (center_x + 50, center_y + 85), (25, 35), -15, 0, 180, shirt_color, -1)
    
    # Draw left arm (below sleeve)
    cv2.line(image, (center_x - 70, center_y + 100), (center_x - 90, center_y + 160), skin_color, 20)
    
    # Draw right arm (below sleeve)
    cv2.line(image, (center_x + 70, center_y + 100), (center_x + 90, center_y + 160), skin_color, 20)
    
    # Draw hands
    cv2.circle(image, (center_x - 90, center_y + 165), 10, skin_color, -1)
    cv2.circle(image, (center_x + 90, center_y + 165), 10, skin_color, -1)
    
    # Draw pants (two legs)
    cv2.rectangle(image, (center_x - 25, center_y + 140), (center_x - 5, center_y + 320), pants_color, -1)
    cv2.rectangle(image, (center_x + 5, center_y + 140), (center_x + 25, center_y + 320), pants_color, -1)
    
    # Draw legs (below pants - skin visible at ankles)
    cv2.rectangle(image, (center_x - 25, center_y + 320), (center_x - 5, center_y + 360), skin_color, -1)
    cv2.rectangle(image, (center_x + 5, center_y + 320), (center_x + 25, center_y + 360), skin_color, -1)
    
    # Draw shoes
    cv2.rectangle(image, (center_x - 28, center_y + 360), (center_x - 2, center_y + 395), shoe_color, -1)
    cv2.rectangle(image, (center_x + 2, center_y + 360), (center_x + 28, center_y + 395), shoe_color, -1)
    
    # Add some clothing details
    # Shirt collar
    cv2.rectangle(image, (center_x - 15, center_y + 65), (center_x + 15, center_y + 75), shirt_color, -1)
    
    # Add subtle shading on shirt
    for x in range(center_x - 45, center_x + 45, 8):
        shade_value = 5 if (x // 8) % 2 == 0 else 0
        cv2.line(image, (x, center_y + 65), (x, center_y + 140), 
                 tuple(max(0, c - shade_value) for c in shirt_color), 1)
    
    # Save image
    output_path = INPUT_DIR / "test.jpg"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), image)
    
    print("[✓] Realistic test image created!")
    print(f"[✓] Image size: 800x1000 pixels with human figure")
    print(f"[✓] Saved to: {output_path}")
    return True

if __name__ == "__main__":
    create_realistic_test_image()
