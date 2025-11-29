# Virtual Try-On AI - Setup and Usage Guide

# دليل إعداد واستخدام تطبيق الملابس الافتراضية

## 📋 Project Overview / نظرة عامة على المشروع

Virtual Try-On AI is a complete pipeline for:

- Human parsing (clothes segmentation) / تحليل الملابس الإنسانية
- Pose estimation (body keypoints detection) / تقدير الموضع واستخراج نقاط الجسم
- Body measurements calculation / حساب قياسات الجسم

تطبيق الملابس الافتراضية هو خط أنابيب كامل لـ:

- تحليل الملابس وتقسيمها
- استخراج نقاط المفاصل الجسدية
- حساب قياسات الجسم تلقائياً

---

## 🗂️ Project Structure / بنية المشروع

```
virtual-tryon/
├── input/                    # User input images / صور المدخلات
├── output/                   # Final output results / نتائج المخرجات النهائية
├── models/
│   └── schp/                # SCHP model weights / أوزان نموذج SCHP
├── parsing/                 # Parsing results / نتائج تحليل الملابس
├── pose/                    # Pose estimation results / نتائج تقدير الموضع
├── masks/                   # Segmentation masks / أقنعة التقسيم
├── scripts/                 # Additional scripts / سكريبتات إضافية
├── setup.py                 # Environment setup script / سكريبت الإعداد
├── run_parsing.py          # Human parsing script / سكريبت تحليل الملابس
├── run_pose.py             # Pose estimation script / سكريبت تقدير الموضع
├── main.py                 # Main pipeline / السكريبت الرئيسي
├── requirements.txt        # Python dependencies / المكتبات المطلوبة
└── README.md              # This file / هذا الملف
```

---

## 🔧 Installation & Setup / التثبيت والإعداد

### Prerequisites / المتطلبات الأساسية

- **Python 3.8+**
- **CUDA 11.8** (للتسريع على RTX 3050Ti) - Optional but recommended
- **Git** (لاستنساخ المستودعات)
- **pip** (مدير الحزم)

### Step 1: Setup Environment / الخطوة 1: إعداد البيئة

```bash
# ملاحظة: إذا كنت تستخدم Windows PowerShell
cd d:\virtual-tryon
python setup.py
```

**ماذا يفعل الإعداد:**

- Creates all required folders / ينشئ جميع المجلدات المطلوبة
- Sets up Python virtual environment / ينشئ بيئة Python افتراضية
- Installs all dependencies / يثبت جميع المكتبات
- Downloads SCHP model / يحمل نموذج SCHP
- Clones SCHP repository / يستنسخ مستودع SCHP

### Step 2: Prepare Your Image / الخطوة 2: تحضير الصورة

Place your test image at: `input/test.jpg`

```bash
copy "your_image.jpg" "input/test.jpg"
```

**Requirements for input image:**

- Format: JPG, PNG, or other common image formats
- Size: Recommended 500x500 pixels or larger
- Content: Full-body human image for best results

---

## 🚀 Usage / طريقة الاستخدام

### Run Complete Pipeline / تشغيل المسار الكامل

```bash
python main.py
```

This will:

1. Run human parsing (clothes segmentation)
2. Run pose estimation (body keypoints)
3. Calculate body measurements
4. Display results summary

---

### Run Individual Scripts / تشغيل السكريبتات منفردة

#### Run Parsing Only / تشغيل التحليل فقط

```bash
python run_parsing.py
```

**Output files:**

- `parsing/test_visual.png` - Colored segmentation visualization
- `parsing/test_labels.npy` - Parsing labels array
- `parsing/test_overlay.png` - Overlay image
- `masks/body_mask.png` - Body segmentation mask
- `masks/cloth_mask.png` - Clothing segmentation mask
- `masks/skin_mask.png` - Skin segmentation mask

#### Run Pose Estimation / تشغيل تقدير الموضع

```bash
python run_pose.py
```

**Output files:**

- `pose/keypoints.json` - 33 body keypoints with coordinates
- `pose/body_measure.json` - Calculated body measurements
- `pose/skeleton.png` - Skeleton visualization

---

## 📊 Output Files Description / وصف ملفات المخرجات

### Parsing Outputs / مخرجات التحليل

| File               | Description                     | العربية                 |
| ------------------ | ------------------------------- | ----------------------- |
| `test_visual.png`  | Color-coded segmentation        | تصور ملون للتقسيم       |
| `test_labels.npy`  | Numeric label array             | مصفوفة التسميات الرقمية |
| `test_overlay.png` | Original + segmentation overlay | صورة مدمجة              |

### Masks / الأقنعة

| File                  | Content                            | المحتوى                  |
| --------------------- | ---------------------------------- | ------------------------ |
| `body_mask.png`       | All body parts (except background) | جميع أجزاء الجسم         |
| `cloth_mask.png`      | Upper clothes only                 | الملابس العلوية فقط      |
| `skin_mask.png`       | Face, arms, legs                   | الوجه والذراعان والساقان |
| `background_mask.png` | Background only                    | الخلفية فقط              |

### Pose Estimation / نتائج تقدير الموضع

#### keypoints.json Structure:

```json
{
  "nose": {"x": 0.5, "y": 0.3, "z": 0.1, "visibility": 0.99},
  "left_shoulder": {"x": 0.45, "y": 0.4, "z": 0.05, "visibility": 0.98},
  ...
}
```

#### body_measure.json Structure:

```json
{
  "shoulder_width": {
    "value": 150.5,
    "unit": "pixels",
    "ar_name": "عرض المنكبين"
  },
  "hip_width": {
    "value": 145.2,
    "unit": "pixels",
    "ar_name": "عرض الورك"
  },
  ...
}
```

---

## 📈 Extracted Body Measurements / القياسات المستخرجة

The system calculates:

| Measurement    | Definition                                   | التعريف بالعربية     |
| -------------- | -------------------------------------------- | -------------------- |
| Shoulder Width | Distance between shoulders (landmarks 11-12) | المسافة بين المنكبين |
| Hip Width      | Distance between hips (landmarks 23-24)      | المسافة بين الوركين  |
| Chest Width    | Approximate chest width                      | عرض الصدر التقريبي   |
| Body Height    | Head to ankle distance                       | ارتفاع الجسم         |
| Arm Length     | Shoulder to wrist distance                   | طول الذراع           |
| Leg Length     | Hip to ankle distance                        | طول الساق            |

---

## 🔑 MediaPipe Pose Landmarks / نقاط MediaPipe

33 landmarks are detected:

```
0: Nose               (الأنف)
1-10: Eye/Ear        (العيون والآذان)
11-16: Shoulders/Arms (المنكبان والذراعان)
17-22: Hands         (اليدان)
23-28: Hips/Legs     (الوركان والساقان)
29-32: Feet          (القدمان)
```

---

## 🎨 SCHP Segmentation Classes / فئات التقسيم

| ID    | Class      | العربية  |
| ----- | ---------- | -------- |
| 0     | Background | الخلفية  |
| 1-10  | Clothes    | الملابس  |
| 11    | Face       | الوجه    |
| 12-13 | Legs       | الساقان  |
| 14-15 | Arms       | الذراعان |
| 16    | Bag        | الحقيبة  |
| 17    | Scarf      | الوشاح   |
| 18-19 | Skin       | الجلد    |

---

## 🐛 Troubleshooting / استكشاف الأخطاء

### Issue: Module not found error

**Solution:**

```bash
# Reinstall requirements
pip install -r requirements.txt

# Or within virtual environment
venv\Scripts\pip install -r requirements.txt
```

### Issue: No person detected in image

**Solution:**

- Ensure image shows a full-body person
- Image should be clear with good lighting
- Try with a different image
- Ensure image is not too small

### Issue: CUDA errors

**Solution:**

```bash
# Install CPU version if GPU unavailable
pip install torch==1.13.1 torchvision==0.14.1
```

### Issue: Model download fails

**Solution:**

1. Download manually from Google Drive:
   `https://drive.google.com/file/d/1LBvbjRgGc0wJdvO65_ZVgnj0iB3pHMKqN/view`

2. Place in: `models/schp/lip_final.pth`

---

## 📝 Code Structure / بنية الكود

### setup.py

- Environment initialization
- Folder creation
- Virtual environment setup
- Dependency installation
- Model downloading

### run_parsing.py

- SCHP model loading
- Image parsing
- Mask generation (body, cloth, skin)
- Visualization creation

### run_pose.py

- MediaPipe pose detection
- Keypoint extraction (33 landmarks)
- Body measurements calculation
- Skeleton visualization

### main.py

- Pipeline orchestration
- All steps execution
- Results summary
- Error handling

---

## 🚀 Advanced Usage / الاستخدام المتقدم

### Skip specific steps:

```bash
# Skip parsing step
python main.py --skip-parsing

# Skip pose estimation
python main.py --skip-pose

# Use custom image
python main.py --image "path/to/your/image.jpg"
```

### Process multiple images:

```bash
for image in input/*.jpg; do
    python main.py --image "$image"
done
```

---

## 📚 Dependencies / المكتبات المستخدمة

| Package       | Version      | Purpose                 |
| ------------- | ------------ | ----------------------- |
| torch         | 1.13.1+cu118 | Deep learning framework |
| torchvision   | 0.14.1+cu118 | Computer vision models  |
| opencv-python | 4.8.0.74     | Image processing        |
| mediapipe     | 0.10.0       | Pose estimation         |
| pillow        | 10.0.0       | Image operations        |
| numpy         | 1.24.3       | Numerical computing     |
| gdown         | 4.7.1        | Google Drive downloads  |

---

## 💡 Tips & Best Practices / نصائح وأفضل الممارسات

1. **Image Quality**: High-quality, well-lit images produce better results
2. **Full Body**: Ensure the entire body is visible in the image
3. **Clothing**: Different clothing provides better segmentation
4. **Resolution**: Higher resolution images give more accurate measurements
5. **GPU**: Use GPU for faster processing (CUDA 11.8 recommended)

---

## 📞 Support / الدعم

For issues:

1. Check the troubleshooting section
2. Verify all installation steps
3. Check that input image meets requirements
4. Review error messages carefully

---

## 📄 License / الترخيص

This project uses:

- SCHP model from: https://github.com/PeikeLi/Self-Correction-Human-Parsing
- MediaPipe from: https://github.com/google/mediapipe

---

## 🔄 Version History / سجل الإصدارات

- **v1.0** (2025-11-29): Initial release
  - Complete setup script
  - Parsing and pose estimation
  - Body measurements calculation
  - Multi-language support (Arabic & English)

---

## خطوات البدء السريع / Quick Start Guide

```bash
# 1. تشغيل الإعداد
python setup.py

# 2. ضع صورتك
copy your_image.jpg input/test.jpg

# 3. شغل المسار الكامل
python main.py

# 4. شاهد النتائج في:
# - parsing/     (نتائج التحليل)
# - pose/        (نتائج الموضع)
# - masks/       (الأقنعة)
```

---

**Last Updated**: 2025-11-29
**Version**: 1.0
