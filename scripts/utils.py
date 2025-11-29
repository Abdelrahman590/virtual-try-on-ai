#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility Functions for Virtual Try-On AI
دوال مساعدة لتطبيق الملابس الافتراضية
"""

import os
import cv2
import numpy as np
from pathlib import Path
from typing import Tuple, List, Dict

def resize_image(image: np.ndarray, max_width: int = 1024, max_height: int = 1024) -> np.ndarray:
    """
    إعادة تحجيم الصورة / Resize image while maintaining aspect ratio
    
    Args:
        image: Input image
        max_width: Maximum width
        max_height: Maximum height
    
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    scale = min(max_width / w, max_height / h, 1.0)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    if scale < 1.0:
        image = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)
    
    return image

def normalize_image(image: np.ndarray) -> np.ndarray:
    """تطبيع الصورة / Normalize image to [0, 1]"""
    return image.astype(np.float32) / 255.0

def denormalize_image(image: np.ndarray) -> np.ndarray:
    """إلغاء تطبيع الصورة / Denormalize image from [0, 1] to [0, 255]"""
    return (image * 255.0).astype(np.uint8)

def apply_mask(image: np.ndarray, mask: np.ndarray, alpha: float = 0.3) -> np.ndarray:
    """تطبيق قناع على الصورة / Apply mask to image"""
    mask_3ch = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    mask_normalized = mask_3ch.astype(np.float32) / 255.0
    
    result = (image.astype(np.float32) * (1 - alpha) + 
              mask_3ch.astype(np.float32) * alpha).astype(np.uint8)
    
    return result

def get_bounding_box(mask: np.ndarray) -> Tuple[int, int, int, int]:
    """الحصول على صندوق محيط / Get bounding box from mask"""
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return 0, 0, mask.shape[1], mask.shape[0]
    
    x_min, y_min = mask.shape[1], mask.shape[0]
    x_max, y_max = 0, 0
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x + w)
        y_max = max(y_max, y + h)
    
    return x_min, y_min, x_max, y_max

def crop_to_mask(image: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """قص الصورة إلى حدود القناع / Crop image to mask bounds"""
    x_min, y_min, x_max, y_max = get_bounding_box(mask)
    return image[y_min:y_max, x_min:x_max]

def enhance_contrast(image: np.ndarray, clip_limit: float = 2.0) -> np.ndarray:
    """تحسين التباين / Enhance image contrast using CLAHE"""
    if len(image.shape) == 3:
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        lab = cv2.merge([l, a, b])
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    else:
        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))
        return clahe.apply(image)

def smooth_mask(mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """تنعيم القناع / Smooth mask edges"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
    return mask

def calculate_mask_area(mask: np.ndarray) -> float:
    """حساب مساحة القناع / Calculate mask area in pixels"""
    return np.sum(mask > 127)

def get_mask_stats(mask: np.ndarray) -> Dict:
    """الحصول على إحصائيات القناع / Get mask statistics"""
    area = calculate_mask_area(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    percentage = (area / total_pixels) * 100
    
    x_min, y_min, x_max, y_max = get_bounding_box(mask)
    bbox_width = x_max - x_min
    bbox_height = y_max - y_min
    
    return {
        "area": area,
        "percentage": percentage,
        "bbox_width": bbox_width,
        "bbox_height": bbox_height,
        "centroid_x": (x_min + x_max) / 2,
        "centroid_y": (y_min + y_max) / 2,
    }

def combine_masks(masks: List[np.ndarray], weights: List[float] = None) -> np.ndarray:
    """دمج عدة أقنعة / Combine multiple masks"""
    if weights is None:
        weights = [1.0 / len(masks)] * len(masks)
    
    result = np.zeros_like(masks[0], dtype=np.float32)
    
    for mask, weight in zip(masks, weights):
        result += mask.astype(np.float32) * weight
    
    return (result).astype(np.uint8)

def dilate_mask(mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """توسيع القناع / Dilate mask"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.dilate(mask, kernel, iterations=1)

def erode_mask(mask: np.ndarray, kernel_size: int = 5) -> np.ndarray:
    """تقليل القناع / Erode mask"""
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.erode(mask, kernel, iterations=1)

def distance_transform(mask: np.ndarray) -> np.ndarray:
    """حساب تحويل المسافة / Calculate distance transform"""
    return cv2.distanceTransform(mask, cv2.DIST_L2, cv2.DIST_MASK_PRECISE)

def create_heatmap(image: np.ndarray, intensity: np.ndarray) -> np.ndarray:
    """إنشاء خريطة حرارية / Create heatmap overlay"""
    heatmap = cv2.applyColorMap((intensity * 255).astype(np.uint8), cv2.COLORMAP_JET)
    result = cv2.addWeighted(image, 0.7, heatmap, 0.3, 0)
    return result

class ImageProcessor:
    """فئة معالجة الصور / Image processor utility class"""
    
    def __init__(self, image_path: str):
        """تهيئة معالج الصور / Initialize image processor"""
        self.image_path = Path(image_path)
        self.image = None
        self.original = None
        self.masks = {}
        
        if self.image_path.exists():
            self.load_image()
    
    def load_image(self):
        """تحميل الصورة / Load image"""
        self.image = cv2.imread(str(self.image_path))
        self.original = self.image.copy()
        return self
    
    def resize(self, max_width: int = 1024, max_height: int = 1024):
        """إعادة تحجيم الصورة / Resize image"""
        self.image = resize_image(self.image, max_width, max_height)
        return self
    
    def enhance_contrast(self, clip_limit: float = 2.0):
        """تحسين التباين / Enhance contrast"""
        self.image = enhance_contrast(self.image, clip_limit)
        return self
    
    def add_mask(self, name: str, mask: np.ndarray):
        """إضافة قناع / Add mask"""
        self.masks[name] = mask
        return self
    
    def apply_mask(self, mask_name: str, alpha: float = 0.3):
        """تطبيق القناع / Apply mask to image"""
        if mask_name in self.masks:
            mask = self.masks[mask_name]
            self.image = apply_mask(self.image, mask, alpha)
        return self
    
    def save(self, output_path: str):
        """حفظ الصورة / Save image"""
        cv2.imwrite(output_path, self.image)
        return self
    
    def reset(self):
        """إعادة تعيين إلى الأصلي / Reset to original"""
        self.image = self.original.copy()
        return self

def print_version():
    """طباعة معلومات الإصدار / Print version information"""
    print("Virtual Try-On AI - Utilities v1.0")
    print("تطبيق الملابس الافتراضية - المرافق")

if __name__ == "__main__":
    print_version()
