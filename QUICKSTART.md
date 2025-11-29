# Quick Start Guide - Virtual Try-On AI

# دليل البدء السريع - تطبيق الملابس الافتراضية

## 🚀 Quick Start / البدء السريع

### Windows (PowerShell):

```powershell
# 1. الانتقال إلى المجلد / Go to project directory
cd d:\virtual-tryon

# 2. تشغيل الإعداد / Run setup
python setup.py

# 3. ضع صورتك / Place your image
copy "C:\path\to\your\image.jpg" "input\test.jpg"

# 4. تشغيل المسار الكامل / Run the complete pipeline
python main.py

# النتائج ستكون في / Results will be in:
# - parsing\  (تحليل الملابس)
# - pose\     (نقاط الجسم)
# - masks\    (الأقنعة)
```

---

## 📦 Project Structure / بنية المشروع

```
virtual-tryon/
├── input/          ← ضع صورتك هنا / Put your image here
├── output/         ← المخرجات النهائية
├── models/         ← نماذج التعلم الآلي
├── parsing/        ← نتائج تحليل الملابس
├── pose/           ← نقاط الجسم والقياسات
├── masks/          ← أقنعة التقسيم
├── scripts/        ← سكريبتات إضافية
├── setup.py        ← سكريبت الإعداد الأولي
├── main.py         ← السكريبت الرئيسي
├── run_parsing.py  ← سكريبت تحليل الملابس
├── run_pose.py     ← سكريبت تقدير الموضع
└── README.md       ← التوثيق الكامل
```

---

## ⚙️ Setup Steps / خطوات الإعداد

### Step 1: Install Python

- Download Python 3.8+ from https://www.python.org/

### Step 2: Run Setup

```bash
python setup.py
```

This will:

- ✓ Create all folders
- ✓ Setup virtual environment
- ✓ Install all packages
- ✓ Download SCHP model
- ✓ Clone SCHP repository

### Step 3: Prepare Image

- Copy your image to `input/test.jpg`
- Image should show full body
- JPEG or PNG format

---

## ▶️ Usage / طريقة الاستخدام

### Full Pipeline:

```bash
python main.py
```

### Individual Scripts:

```bash
# Parsing only / التحليل فقط
python run_parsing.py

# Pose only / الموضع فقط
python run_pose.py
```

### Batch Processing:

```bash
python batch_process.py --input-dir input --output-dir output
```

---

## 📊 Output Files / ملفات المخرجات

| File                      | Description            |
| ------------------------- | ---------------------- |
| `parsing/test_visual.png` | Colored segmentation   |
| `parsing/test_labels.npy` | Parsing labels         |
| `masks/body_mask.png`     | Body segmentation      |
| `masks/cloth_mask.png`    | Clothing segmentation  |
| `masks/skin_mask.png`     | Skin segmentation      |
| `pose/keypoints.json`     | 33 body keypoints      |
| `pose/body_measure.json`  | Body measurements      |
| `pose/skeleton.png`       | Skeleton visualization |

---

## 🔧 Requirements / المتطلبات

- Python 3.8+
- 4GB+ RAM
- 2GB+ disk space for models
- GPU optional (faster processing)

---

## 🐛 Troubleshooting / استكشاف الأخطاء

### Issue: ModuleNotFoundError

```bash
# Solution / الحل:
pip install -r requirements.txt
```

### Issue: Model not found

```bash
# Solution / الحل:
# Re-run setup or download manually from:
# https://drive.google.com/file/d/1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN/view
```

### Issue: No person detected

- Use a clearer image
- Ensure full body is visible
- Try a different image

---

## 📚 Main Functions / الوظائف الرئيسية

### setup.py

- Environment initialization
- Dependency installation
- Model downloading

### run_parsing.py

- Human body segmentation
- Clothing detection
- Mask generation

### run_pose.py

- Pose estimation (MediaPipe)
- 33 landmark detection
- Body measurement calculation

### main.py

- Full pipeline orchestration
- Results summary
- Error handling

---

## 💡 Tips / نصائح

1. **Image Quality**: Use high-resolution, well-lit images
2. **Full Body**: Show entire body in frame
3. **GPU**: Enable CUDA for faster processing
4. **Multiple Images**: Use batch_process.py

---

## 📞 Support / الدعم

For detailed documentation, see: **README.md**

For issues:

1. Check troubleshooting section in README.md
2. Verify setup.py completed successfully
3. Check input image requirements

---

## ✅ Verification Checklist / قائمة التحقق

- [ ] Python 3.8+ installed
- [ ] setup.py executed successfully
- [ ] Image placed in input/test.jpg
- [ ] All folders created
- [ ] Models downloaded
- [ ] Dependencies installed

---

**Version**: 1.0
**Last Updated**: 2025-11-29
