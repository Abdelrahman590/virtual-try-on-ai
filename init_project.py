#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project Initialization Script
سكريبت تهيئة المشروع
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.absolute()

def initialize_project():
    """تهيئة هيكل المشروع / Initialize project structure"""
    
    directories = [
        "input",
        "output",
        "parsing",
        "pose", 
        "masks",
        "models/schp",
        "scripts",
    ]
    
    for directory in directories:
        dir_path = PROJECT_ROOT / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create .gitkeep files to preserve directories in git
        gitkeep = dir_path / ".gitkeep"
        gitkeep.touch()
    
    print("✓ Project structure initialized")
    return True

if __name__ == "__main__":
    initialize_project()
