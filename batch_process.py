#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Processing Script for Virtual Try-On AI
سكريبت المعالجة الجماعية لتطبيق الملابس الافتراضية
"""

import os
import sys
import argparse
import json
from pathlib import Path
from datetime import datetime
import shutil

PROJECT_ROOT = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import SUPPORTED_IMAGE_FORMATS

def print_header(msg):
    """طباعة رأس / Print header"""
    print(f"\n{'='*70}")
    print(f"  {msg}")
    print(f"{'='*70}\n")

def print_status(msg, status="INFO"):
    """طباعة الحالة / Print status"""
    icons = {"SUCCESS": "✓", "ERROR": "✗", "WARNING": "⚠", "INFO": "→"}
    print(f"[{icons.get(status, '→')}] {msg}")

def find_images(input_dir: Path) -> list:
    """البحث عن جميع الصور / Find all images in directory"""
    print_status(f"Searching for images in {input_dir}")
    
    images = []
    for ext in SUPPORTED_IMAGE_FORMATS:
        images.extend(input_dir.glob(f"*{ext}"))
    
    print_status(f"Found {len(images)} images", "SUCCESS")
    return sorted(images)

def create_batch_structure(output_dir: Path, num_images: int) -> dict:
    """إنشاء هيكل الإخراج الجماعي / Create batch output structure"""
    batch_dir = output_dir / f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    batch_dir.mkdir(parents=True, exist_ok=True)
    
    batch_info = {
        "batch_dir": str(batch_dir),
        "start_time": datetime.now().isoformat(),
        "total_images": num_images,
        "processed": 0,
        "successful": 0,
        "failed": 0,
        "results": []
    }
    
    print_status(f"Created batch directory: {batch_dir}", "SUCCESS")
    return batch_info

def process_image(image_path: Path, batch_dir: Path, batch_info: dict) -> bool:
    """معالجة صورة واحدة / Process single image"""
    try:
        image_name = image_path.stem
        image_output_dir = batch_dir / image_name
        image_output_dir.mkdir(parents=True, exist_ok=True)
        
        print_status(f"Processing: {image_path.name}")
        
        # Copy image to output directory
        import subprocess
        output_image = image_output_dir / "input.jpg"
        
        # Convert to standard format for processing
        import cv2
        img = cv2.imread(str(image_path))
        if img is None:
            print_status(f"Failed to load image: {image_path.name}", "ERROR")
            batch_info["failed"] += 1
            return False
        
        cv2.imwrite(str(output_image), img)
        
        # Run processing (placeholder - would integrate actual processing)
        result = {
            "image_name": image_path.name,
            "input_path": str(image_path),
            "output_dir": str(image_output_dir),
            "status": "processed",
            "timestamp": datetime.now().isoformat()
        }
        
        batch_info["processed"] += 1
        batch_info["successful"] += 1
        batch_info["results"].append(result)
        
        print_status(f"✓ {image_path.name}", "SUCCESS")
        return True
    except Exception as e:
        print_status(f"Error processing {image_path.name}: {str(e)}", "ERROR")
        batch_info["processed"] += 1
        batch_info["failed"] += 1
        return False

def generate_batch_report(batch_info: dict, output_dir: Path) -> None:
    """إنشاء تقرير المعالجة الجماعية / Generate batch processing report"""
    print_header("Generating Batch Report", )
    
    batch_info["end_time"] = datetime.now().isoformat()
    batch_info["success_rate"] = (batch_info["successful"] / max(batch_info["processed"], 1)) * 100
    
    report_path = Path(batch_info["batch_dir"]) / "batch_report.json"
    
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(batch_info, f, indent=2, ensure_ascii=False)
    
    print_status(f"Report saved: {report_path}", "SUCCESS")
    
    # Print summary
    print("\nBatch Processing Summary / ملخص المعالجة الجماعية:")
    print("-" * 70)
    print(f"  Total Images:     {batch_info['total_images']}")
    print(f"  Processed:        {batch_info['processed']}")
    print(f"  Successful:       {batch_info['successful']}")
    print(f"  Failed:           {batch_info['failed']}")
    print(f"  Success Rate:     {batch_info['success_rate']:.1f}%")
    print(f"  Output Directory: {batch_info['batch_dir']}")
    print("-" * 70)

def cleanup_temp_files(batch_dir: Path) -> None:
    """تنظيف الملفات المؤقتة / Clean up temporary files"""
    print_status("Cleaning up temporary files...")
    
    temp_patterns = ["*.tmp", "*.temp", ".*.swp"]
    
    for pattern in temp_patterns:
        for file in batch_dir.glob(f"**/{pattern}"):
            try:
                file.unlink()
            except:
                pass

def main():
    """الدالة الرئيسية / Main function"""
    parser = argparse.ArgumentParser(
        description="Batch process multiple images"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=str(PROJECT_ROOT / "input"),
        help="Input directory with images"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(PROJECT_ROOT / "output"),
        help="Output directory for results"
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search recursively in subdirectories"
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*",
        help="File pattern to match"
    )
    
    args = parser.parse_args()
    
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    
    print_header("Batch Image Processing - Virtual Try-On AI")
    print("معالجة الصور الجماعية - تطبيق الملابس الافتراضية")
    
    # Validate input directory
    if not input_dir.exists():
        print_status(f"Input directory not found: {input_dir}", "ERROR")
        return 1
    
    # Find images
    if args.recursive:
        images = list(input_dir.glob(f"**/{args.pattern}*"))
    else:
        images = list(input_dir.glob(f"{args.pattern}*"))
    
    images = [img for img in images if img.suffix.lower() in SUPPORTED_IMAGE_FORMATS]
    
    if not images:
        print_status("No images found!", "ERROR")
        return 1
    
    print_status(f"Found {len(images)} images to process")
    
    # Create batch structure
    batch_info = create_batch_structure(output_dir, len(images))
    batch_dir = Path(batch_info["batch_dir"])
    
    # Process images
    print_header("Processing Images", )
    for i, image_path in enumerate(images, 1):
        print(f"\n[{i}/{len(images)}] ", end="")
        process_image(image_path, batch_dir, batch_info)
    
    # Cleanup
    cleanup_temp_files(batch_dir)
    
    # Generate report
    generate_batch_report(batch_info, output_dir)
    
    print("\n" + "="*70)
    print("  Batch Processing Completed! ✓")
    print("  تم إكمال المعالجة الجماعية!")
    print("="*70 + "\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
