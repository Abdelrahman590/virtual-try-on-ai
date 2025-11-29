#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pose Estimation Script using MediaPipe
"""

import os
import sys
import cv2
import json
import numpy as np
import mediapipe as mp
from pathlib import Path
from typing import Dict, Tuple

# Project Configuration
PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_PATH = PROJECT_ROOT / "input" / "test.jpg"
POSE_OUTPUT = PROJECT_ROOT / "pose"

# MediaPipe Pose Configuration
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Landmark indices for measurements (33 landmarks)
LANDMARKS_MAP = {
    "nose": 0,
    "left_eye_inner": 1,
    "left_eye": 2,
    "left_eye_outer": 3,
    "right_eye_inner": 4,
    "right_eye": 5,
    "right_eye_outer": 6,
    "left_ear": 7,
    "right_ear": 8,
    "mouth_left": 9,
    "mouth_right": 10,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_pinky": 17,
    "right_pinky": 18,
    "left_index": 19,
    "right_index": 20,
    "left_thumb": 21,
    "right_thumb": 22,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
    "left_heel": 29,
    "right_heel": 30,
    "left_foot_index": 31,
    "right_foot_index": 32,
}

def print_status(msg, status="INFO"):
    """Print status message"""
    status_icon = "✓" if status == "SUCCESS" else "✗" if status == "ERROR" else "→"
    print(f"[{status_icon}] {msg}")

def load_image(image_path):
    """Load image"""
    print_status(f"Loading image: {image_path}")
    
    try:
        if not Path(image_path).exists():
            print_status(f"Image not found: {image_path}", "ERROR")
            return None
        
        image = cv2.imread(str(image_path))
        if image is None:
            print_status(f"Failed to load image: {image_path}", "ERROR")
            return None
        
        print_status(f"Image loaded! Shape: {image.shape}", "SUCCESS")
        return image
    except Exception as e:
        print_status(f"Error loading image: {str(e)}", "ERROR")
        return None

def detect_pose(image):
    """Detect pose in image"""
    print_status("Detecting pose using MediaPipe...")
    
    try:
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, c = image.shape
        
        # Detect pose
        with mp_pose.Pose(
            static_image_mode=True,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5
        ) as pose:
            results = pose.process(image_rgb)
        
        if results.pose_landmarks is None:
            print_status("No person detected in image - trying with lower confidence", "ERROR")
            # Try again with lower confidence threshold
            with mp_pose.Pose(
                static_image_mode=True,
                model_complexity=1,
                enable_segmentation=False,
                min_detection_confidence=0.1
            ) as pose:
                results = pose.process(image_rgb)
            
            if results.pose_landmarks is None:
                print_status("Still no person detected even with lower threshold", "ERROR")
                return None
        
        try:
            num_landmarks = len(results.pose_landmarks.landmark)
        except:
            num_landmarks = len(results.pose_landmarks) if results.pose_landmarks else 0
        
        print_status(f"Detected {num_landmarks} landmarks", "SUCCESS")
        return results
    except Exception as e:
        print_status(f"Error detecting pose: {str(e)}", "ERROR")
        return None

def extract_keypoints(pose_results) -> Dict:
    """Extract keypoints from pose results"""
    print_status("Extracting keypoints...")
    
    try:
        keypoints = {}
        
        for landmark, index in LANDMARKS_MAP.items():
            try:
                # Handle both possible structures
                if hasattr(pose_results.pose_landmarks, 'landmark'):
                    lm = pose_results.pose_landmarks.landmark[index]
                else:
                    lm = pose_results.pose_landmarks[index]
                    
                keypoints[landmark] = {
                    "x": float(lm.x),
                    "y": float(lm.y),
                    "z": float(lm.z),
                    "visibility": float(lm.visibility)
                }
            except (IndexError, AttributeError) as e:
                print_status(f"Warning: Could not extract landmark {landmark}", "ERROR")
                continue
        
        if len(keypoints) > 0:
            print_status(f"Extracted {len(keypoints)} keypoints", "SUCCESS")
            return keypoints
        else:
            print_status("No keypoints extracted", "ERROR")
            return {}
    except Exception as e:
        print_status(f"Error extracting keypoints: {str(e)}", "ERROR")
        return {}

def calculate_distance(point1: Dict, point2: Dict, image_width: int, image_height: int) -> float:
    """
    حساب المسافة بين نقطتين / Calculate distance between two points
    Returns distance in pixels
    """
    # تحويل الإحداثيات المعايرة إلى بكسل / Convert normalized coordinates to pixels
    p1_x, p1_y = point1["x"] * image_width, point1["y"] * image_height
    p2_x, p2_y = point2["x"] * image_width, point2["y"] * image_height
    
    distance = np.sqrt((p2_x - p1_x)**2 + (p2_y - p1_y)**2)
    return distance

def calculate_body_measurements(keypoints: Dict, image_width: int, image_height: int) -> Dict:
    """
    حساب قياسات الجسم / Calculate body measurements
    
    قياسات الجسم:
    - Shoulder width: المسافة بين المنكبين (11 و 12)
    - Chest width: عرض الصدر (بين المنكبين)
    - Hip width: عرض الورك (بين الوركين 23 و 24)
    """
    print_status("Calculating body measurements...")
    
    try:
        measurements = {}
        
        # الحصول على النقاط المطلوبة / Get required landmarks
        left_shoulder = keypoints.get("left_shoulder")
        right_shoulder = keypoints.get("right_shoulder")
        left_hip = keypoints.get("left_hip")
        right_hip = keypoints.get("right_hip")
        left_ankle = keypoints.get("left_ankle")
        right_ankle = keypoints.get("right_ankle")
        
        # عرض المنكبين / Shoulder width
        if left_shoulder and right_shoulder:
            shoulder_width = calculate_distance(
                left_shoulder, right_shoulder, image_width, image_height
            )
            measurements["shoulder_width"] = {
                "value": float(shoulder_width),
                "unit": "pixels",
                "ar_name": "عرض المنكبين"
            }
        
        # عرض الورك / Hip width
        if left_hip and right_hip:
            hip_width = calculate_distance(
                left_hip, right_hip, image_width, image_height
            )
            measurements["hip_width"] = {
                "value": float(hip_width),
                "unit": "pixels",
                "ar_name": "عرض الورك"
            }
        
        # الارتفاع التقريبي (من المنكب إلى الكاحل) / Approximate height
        if right_shoulder and right_ankle:
            height = calculate_distance(
                right_shoulder, right_ankle, image_width, image_height
            )
            measurements["body_height"] = {
                "value": float(height),
                "unit": "pixels",
                "ar_name": "ارتفاع الجسم"
            }
        
        # عرض الصدر (تقريبي: مساحة بين المنكبين) / Chest width (approximate)
        if left_shoulder and right_shoulder:
            chest_width = calculate_distance(
                left_shoulder, right_shoulder, image_width, image_height
            ) * 0.95  # تقريب بسيط / Simple approximation
            measurements["chest_width"] = {
                "value": float(chest_width),
                "unit": "pixels",
                "ar_name": "عرض الصدر"
            }
        
        # طول الذراع / Arm length
        left_wrist = keypoints.get("left_wrist")
        if left_shoulder and left_wrist:
            left_arm_length = calculate_distance(
                left_shoulder, left_wrist, image_width, image_height
            )
            measurements["left_arm_length"] = {
                "value": float(left_arm_length),
                "unit": "pixels",
                "ar_name": "طول الذراع اليسرى"
            }
        
        # طول الساق / Leg length
        if left_hip and left_ankle:
            left_leg_length = calculate_distance(
                left_hip, left_ankle, image_width, image_height
            )
            measurements["left_leg_length"] = {
                "value": float(left_leg_length),
                "unit": "pixels",
                "ar_name": "طول الساق اليسرى"
            }
        
        print_status("Body measurements calculated", "SUCCESS")
        return measurements
    except Exception as e:
        print_status(f"Error calculating measurements: {str(e)}", "ERROR")
        return {}

def draw_skeleton(image, pose_results) -> np.ndarray:
    """Draw skeleton on image"""
    print_status("Drawing skeleton...")
    
    try:
        # نسخ الصورة الأصلية / Copy original image
        annotated_image = image.copy()
        
        # تحويل إلى RGB للرسم / Convert to RGB for drawing
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        
        # رسم الهيكل العظمي / Draw pose landmarks and connections
        mp_drawing.draw_landmarks(
            annotated_image,
            pose_results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        # تحويل مرة أخرى إلى BGR / Convert back to BGR
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
        
        print_status("Skeleton drawn", "SUCCESS")
        return annotated_image
    except Exception as e:
        print_status(f"Error drawing skeleton: {str(e)}", "ERROR")
        return image

def save_keypoints(keypoints: Dict):
    """Save keypoints to JSON"""
    print_status("Saving keypoints...")
    
    try:
        POSE_OUTPUT.mkdir(parents=True, exist_ok=True)
        
        keypoints_path = POSE_OUTPUT / "keypoints.json"
        with open(keypoints_path, "w", encoding="utf-8") as f:
            json.dump(keypoints, f, indent=2)
        
        print_status(f"Saved keypoints: {keypoints_path}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error saving keypoints: {str(e)}", "ERROR")
        return False

def save_measurements(measurements: Dict):
    """حفظ قياسات الجسم / Save body measurements to JSON"""
    print_status("Saving body measurements...")
    
    try:
        POSE_OUTPUT.mkdir(parents=True, exist_ok=True)
        
        measurements_path = POSE_OUTPUT / "body_measure.json"
        with open(measurements_path, "w", encoding="utf-8") as f:
            json.dump(measurements, f, indent=2, ensure_ascii=False)
        
        print_status(f"Saved measurements: {measurements_path}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error saving measurements: {str(e)}", "ERROR")
        return False

def save_skeleton_image(skeleton_image: np.ndarray):
    """حفظ صورة الهيكل العظمي / Save skeleton image"""
    print_status("Saving skeleton image...")
    
    try:
        POSE_OUTPUT.mkdir(parents=True, exist_ok=True)
        
        skeleton_path = POSE_OUTPUT / "skeleton.png"
        cv2.imwrite(str(skeleton_path), skeleton_image)
        
        print_status(f"Saved skeleton: {skeleton_path}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error saving skeleton image: {str(e)}", "ERROR")
        return False

def main():
    """الدالة الرئيسية / Main function"""
    print("="*60)
    print("  Pose Estimation - MediaPipe")
    print("  تقدير الموضع - MediaPipe")
    print("="*60 + "\n")
    
    # تحميل الصورة / Load image
    image = load_image(INPUT_PATH)
    if image is None:
        return 1
    
    h, w, c = image.shape
    
    # الكشف عن الموضع / Detect pose
    pose_results = detect_pose(image)
    if pose_results is None:
        return 1
    
    # استخراج نقاط المفاصل / Extract keypoints
    keypoints = extract_keypoints(pose_results)
    if not keypoints:
        return 1
    
    # حساب قياسات الجسم / Calculate body measurements
    measurements = calculate_body_measurements(keypoints, w, h)
    
    # رسم الهيكل العظمي / Draw skeleton
    skeleton_image = draw_skeleton(image, pose_results)
    
    # حفظ النتائج / Save results
    if not save_keypoints(keypoints):
        return 1
    
    if not save_measurements(measurements):
        return 1
    
    if not save_skeleton_image(skeleton_image):
        return 1
    
    # طباعة الملخص / Print summary
    print("\n" + "="*60)
    print("  Pose Estimation Completed! ✓")
    print("  تم إكمال تقدير الموضع!")
    print("="*60)
    print("\nBody Measurements / قياسات الجسم:")
    print("-" * 60)
    
    for key, value in measurements.items():
        ar_name = value.get("ar_name", key)
        measure_value = value.get("value", 0)
        unit = value.get("unit", "")
        print(f"  {ar_name:<30} {measure_value:>10.2f} {unit}")
    
    print("="*60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
