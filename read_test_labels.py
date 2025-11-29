import numpy as np
import os

# مسار الملف
file_path = r"D:\virtual-tryon\parsing\test_labels.npy"

# التحقق من وجود الملف
if not os.path.exists(file_path):
    print("❌ الملف غير موجود!")
    exit()

# قراءة الملف
print("⏳ جاري تحميل الملف...")
labels = np.load(file_path)

# طباعة المعلومات
print("\n" + "="*60)
print("📊 معلومات الملف:")
print("="*60)
print(f"✓ حجم المصفوفة (الصورة): {labels.shape}")
print(f"✓ عدد البكسلات الكلي: {labels.size:,}")
print(f"✓ نوع البيانات: {labels.dtype}")
print(f"✓ الفئات الموجودة: {np.unique(labels)}")

# إحصائيات لكل فئة
print("\n" + "="*60)
print("📈 إحصائيات الفئات:")
print("="*60)

class_names = {
    0: "خلفية (Background)",
    1: "قبعة (Hat)",
    2: "شعر (Hair)",
    3: "نظارة (Sunglasses)",
    4: "ملابس علوية (Upper-clothes)",
    5: "تنورة (Skirt)",
    6: "بنطلون (Pants)",
    7: "فستان (Dress)",
    8: "حزام (Belt)",
    9: "حذاء يسار (Left-shoe)",
    10: "حذاء يمين (Right-shoe)",
    11: "وجه (Face)",
    12: "ساق يسرى (Left-leg)",
    13: "ساق يمنى (Right-leg)",
    14: "ذراع يسرى (Left-arm)",
    15: "ذراع يمنى (Right-arm)",
    16: "حقيبة (Bag)",
    17: "وشاح (Scarf)",
    18: "جلد - جذع (Skin-torso)",
    19: "جلد - رقبة (Skin-neck)"
}

for class_id in np.unique(labels):
    count = np.sum(labels == class_id)
    percentage = (count / labels.size) * 100
    class_name = class_names.get(class_id, f"فئة {class_id}")
    print(f"[{class_id:2d}] {class_name:<30} {count:>7} بكسل ({percentage:>5.2f}%)")

# عرض جزء صغير من المصفوفة
print("\n" + "="*60)
print("🔍 عينة من البيانات (أول 10×10 بكسل):")
print("="*60)
print(labels[:10, :10])

print("\n✅ تم القراءة بنجاح!")
