#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration File for Virtual Try-On AI
ملف الإعدادات لتطبيق الملابس الافتراضية
"""

import os
from pathlib import Path

# ============================================
# PROJECT PATHS / مسارات المشروع
# ============================================

PROJECT_ROOT = Path(__file__).parent.parent.absolute()

# Input/Output Paths
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"
PARSING_DIR = PROJECT_ROOT / "parsing"
POSE_DIR = PROJECT_ROOT / "pose"
MASKS_DIR = PROJECT_ROOT / "masks"
MODELS_DIR = PROJECT_ROOT / "models"
SCHP_DIR = MODELS_DIR / "schp"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# ============================================
# IMAGE SETTINGS / إعدادات الصورة
# ============================================

# Default input image / صورة الإدخال الافتراضية
DEFAULT_INPUT_IMAGE = "input/test.jpg"

# Image processing parameters
IMAGE_MAX_WIDTH = 1024
IMAGE_MAX_HEIGHT = 1024
IMAGE_QUALITY = 95

# ============================================
# PARSING SETTINGS / إعدادات التحليل
# ============================================

# SCHP Model configuration
SCHP_MODEL_NAME = "lip_final.pth"
SCHP_REPO_URL = "https://github.com/PeikeLi/Self-Correction-Human-Parsing.git"
SCHP_GOOGLE_DRIVE_ID = "1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN"

# Parsing classes / فئات التحليل
PARSING_CLASSES = {
    0: "Background",
    1: "Hat",
    2: "Hair",
    3: "Sunglasses",
    4: "Upper-clothes",
    5: "Skirt",
    6: "Pants",
    7: "Dress",
    8: "Belt",
    9: "Left-shoe",
    10: "Right-shoe",
    11: "Face",
    12: "Left-leg",
    13: "Right-leg",
    14: "Left-arm",
    15: "Right-arm",
    16: "Bag",
    17: "Scarf",
    18: "Torso-skin",
    19: "Neck-skin",
}

# Color palette for visualization (BGR format)
PARSING_PALETTE = [
    [0, 0, 0],           # 0: Background
    [0, 0, 128],         # 1: Hat
    [0, 0, 255],         # 2: Hair
    [0, 85, 0],          # 3: Sunglasses
    [51, 0, 170],        # 4: Upper-clothes
    [0, 85, 255],        # 5: Skirt
    [85, 0, 0],          # 6: Pants
    [221, 119, 0],       # 7: Dress
    [0, 85, 85],         # 8: Belt
    [85, 0, 0],          # 9: Left-shoe
    [0, 51, 85],         # 10: Right-shoe
    [128, 86, 52],       # 11: Face
    [0, 128, 0],         # 12: Left-leg
    [128, 0, 128],       # 13: Right-leg
    [128, 0, 0],         # 14: Left-arm
    [0, 128, 128],       # 15: Right-arm
    [0, 0, 128],         # 16: Bag
    [0, 64, 192],        # 17: Scarf
    [128, 128, 0],       # 18: Torso-skin
    [0, 128, 64],        # 19: Neck-skin
]

# Mask generation classes
BODY_PARTS = {
    "body": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
    "cloth": [4, 5, 6, 7, 8, 16, 17],  # Upper clothes, skirt, pants, dress, belt, bag, scarf
    "skin": [11, 12, 13, 14, 15, 18, 19],  # Face, legs, arms, skin
    "background": [0],
}

# ============================================
# POSE ESTIMATION SETTINGS / إعدادات تقدير الموضع
# ============================================

# MediaPipe configuration
MEDIAPIPE_MIN_DETECTION_CONFIDENCE = 0.5
MEDIAPIPE_MODEL_COMPLEXITY = 2
MEDIAPIPE_ENABLE_SEGMENTATION = False

# Number of landmarks
NUM_LANDMARKS = 33

# Landmark names
LANDMARK_NAMES = [
    "nose", "left_eye_inner", "left_eye", "left_eye_outer",
    "right_eye_inner", "right_eye", "right_eye_outer",
    "left_ear", "right_ear", "mouth_left", "mouth_right",
    "left_shoulder", "right_shoulder",
    "left_elbow", "right_elbow",
    "left_wrist", "right_wrist",
    "left_pinky", "right_pinky", "left_index", "right_index",
    "left_thumb", "right_thumb",
    "left_hip", "right_hip",
    "left_knee", "right_knee",
    "left_ankle", "right_ankle",
    "left_heel", "right_heel", "left_foot_index", "right_foot_index"
]

# Landmark indices for key measurements
LANDMARK_INDICES = {
    "nose": 0,
    "left_eye": 2,
    "right_eye": 5,
    "left_ear": 7,
    "right_ear": 8,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

# ============================================
# DEVICE SETTINGS / إعدادات الجهاز
# ============================================

# GPU configuration
USE_CUDA = True
CUDA_DEVICE_ID = 0

# Processing options
BATCH_SIZE = 1
NUM_WORKERS = 0

# ============================================
# LOGGING & DEBUG / تسجيل والتصحيح
# ============================================

# Logging level
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Debug mode
DEBUG_MODE = False

# Save intermediate results
SAVE_INTERMEDIATE = True

# ============================================
# DISPLAY & VISUALIZATION / العرض والتصور
# ============================================

# Visualization settings
DRAW_CONFIDENCE = True
DRAW_LANDMARKS = True
SKELETON_COLOR = (0, 255, 0)  # Green in BGR
KEYPOINT_COLOR = (0, 0, 255)  # Red in BGR
KEYPOINT_RADIUS = 3
CONNECTION_THICKNESS = 2

# ============================================
# DATA FORMATS / تنسيقات البيانات
# ============================================

# Supported image formats
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

# Output formats
OUTPUT_FORMATS = {
    "image": ".png",
    "numpy": ".npy",
    "json": ".json",
    "csv": ".csv",
}

# ============================================
# MEASUREMENT SETTINGS / إعدادات القياسات
# ============================================

# Unit system
MEASUREMENT_UNIT = "pixels"  # pixels, cm, inches

# Pixel to real-world conversion (example - adjust based on camera)
PIXELS_PER_CM = 0.5  # Approximate

# Minimum confidence for measurement
MIN_MEASUREMENT_CONFIDENCE = 0.5

# ============================================
# PERFORMANCE / الأداء
# ============================================

# Model precision
MODEL_PRECISION = "float32"  # float32, float16

# Multi-threading
USE_THREADING = True
MAX_THREADS = 4

# ============================================
# VALIDATION / التحقق
# ============================================

# Image validation
MIN_IMAGE_SIZE = 100
MIN_IMAGE_AREA = 10000

# Pose validation
MIN_PERSON_HEIGHT = 50  # pixels
MIN_VISIBLE_LANDMARKS = 10

# ============================================
# PATHS CONFIGURATION / تكوين المسارات
# ============================================

PATHS = {
    "input": INPUT_DIR,
    "output": OUTPUT_DIR,
    "parsing": PARSING_DIR,
    "pose": POSE_DIR,
    "masks": MASKS_DIR,
    "models": MODELS_DIR,
    "schp": SCHP_DIR,
    "scripts": SCRIPTS_DIR,
}

# Create all required directories
def ensure_directories():
    """تأكد من وجود جميع المجلدات المطلوبة / Ensure all required directories exist"""
    for path in PATHS.values():
        path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    # Print configuration
    print("Virtual Try-On AI Configuration")
    print("="*50)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Input Directory: {INPUT_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print("\nPaths:")
    for name, path in PATHS.items():
        print(f"  {name}: {path}")
