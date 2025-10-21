# برومبت لإصلاح سكربت دمج الأوراق التعليمية

## المشكلة الحالية

السكربت الحالي `merge_worksheets.py` يحتوي على أخطاء خطيرة:

### 1. **محتوى مكرر من ملف القالب**
- السكربت يقرأ ملف `excellent-alldays-worksheet.html` كقالب
- لكنه **لا يستخرج محتوى الأيام الأربعة من الملفات الجديدة بشكل صحيح**
- النتيجة: الملفات الثلاثة المُنشأة (intermediate, acceptable, basic) تحتوي على **نفس محتوى excellent** بدلاً من محتواها الخاص
- الفرق الوحيد: اسم الملف والعنوان العلوي فقط!

### 2. **تكرار عبارة "إعداد أ. محمد العثيمين"**
- السكربت يضيف العبارة `<div class="subtitle">إعداد أ. محمد العثيمين - أبي بكر بن العربي الثانوية</div>` بشكل مكرر
- هذه العبارة يجب أن تظهر **مرة واحدة فقط** في header الصفحة
- لكن السكربت يضيفها مع كل يوم مما يسبب تكراراً

### 3. **مشكلة في استخراج المحتوى**
- دالة `extract_day_content()` لا تعمل بشكل صحيح
- تستخرج المحتوى من القالب بدلاً من الملفات الفعلية للمستوى المطلوب

---

## المطلوب بالضبط

### البنية الصحيحة للملف المدمج

يجب أن يكون الملف المدمج بهذه البنية:

```html
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="utf-8"/>
    <title>Remedial Plan - [LEVEL] - All Days</title>
    <link href="../css/style.css" rel="stylesheet"/>
    <style>
        /* نفس CSS من القالب لكن مع تعديل اسم class */
        .[level-class] { ... }
        .day-separator { page-break-before: always; }
        .day3-bonus-pagebreak { page-break-before: always; }
    </style>
</head>
<body>
    <button class="print-button" onclick="window.print()">
        🖨️ طباعة جميع أوراق العمل (4 أيام)
    </button>
    
    <!-- اليوم الأول -->
    <div class="[level-class]">
        <div class="worksheet-header">
            <h1>الخطة العلاجية - [LEVEL_AR] - جميع الأيام</h1>
            <div class="subtitle">إعداد أ. محمد العثيمين - أبي بكر بن العربي الثانوية</div>
        </div>
        
        <!-- محتوى اليوم الأول من ملف [level]-day1-worksheet.html -->
        [CONTENT FROM day1-worksheet.html]
    </div>
    
    <!-- فاصل صفحة -->
    <div class="day-separator"></div>
    
    <!-- اليوم الثاني -->
    <div class="[level-class]">
        <!-- محتوى اليوم الثاني من ملف [level]-day2-worksheet.html -->
        [CONTENT FROM day2-worksheet.html]
    </div>
    
    <!-- فاصل صفحة -->
    <div class="day-separator"></div>
    
    <!-- اليوم الثالث -->
    <div class="[level-class]">
        <!-- محتوى اليوم الثالث من ملف [level]-day3-worksheet.html -->
        [CONTENT FROM day3-worksheet.html]
    </div>
    
    <!-- فاصل صفحة -->
    <div class="day-separator"></div>
    
    <!-- اليوم الرابع -->
    <div class="[level-class]">
        <!-- محتوى اليوم الرابع من ملف [level]-day4-worksheet.html -->
        [CONTENT FROM day4-worksheet.html]
    </div>
</body>
</html>
```

---

## الخطوات الصحيحة

### 1. **قراءة القالب للحصول على البنية والـ CSS فقط**
```python
# قراءة excellent-alldays-worksheet.html
# استخراج: <head> (title, style, link)
# تعديل: اسم class في CSS من .excellent-worksheet إلى .[level]-worksheet
```

### 2. **قراءة محتوى كل يوم من الملفات الصحيحة**
```python
# لكل مستوى (intermediate, acceptable, basic):
#   اقرأ: [level]-day1-worksheet.html
#   استخرج المحتوى الموجود داخل <div class="[level]-worksheet">
#   (كل شيء من بداية div إلى نهايته، ما عدا <head> و <html>)
```

### 3. **دمج المحتوى بشكل صحيح**
```python
# أنشئ ملف HTML جديد:
#   - <head> من القالب (مع تعديل class names)
#   - <body> يحتوي على:
#       * زر الطباعة
#       * محتوى اليوم 1 كامل داخل div.[level]-worksheet
#       * <div class="day-separator"></div>
#       * محتوى اليوم 2 كامل داخل div.[level]-worksheet
#       * <div class="day-separator"></div>
#       * محتوى اليوم 3 كامل داخل div.[level]-worksheet
#       * <div class="day-separator"></div>
#       * محتوى اليوم 4 كامل داخل div.[level]-worksheet
```

---

## ملفات المدخلات (Inputs)

```
worksheets/
├── intermediate-day1-worksheet.html  # محتوى اليوم 1 للمستوى المتوسط
├── intermediate-day2-worksheet.html  # محتوى اليوم 2 للمستوى المتوسط
├── intermediate-day3-worksheet.html  # محتوى اليوم 3 للمستوى المتوسط
├── intermediate-day4-worksheet.html  # محتوى اليوم 4 للمستوى المتوسط
├── acceptable-day1-worksheet.html    # محتوى اليوم 1 للمستوى المقبول
├── acceptable-day2-worksheet.html    # محتوى اليوم 2 للمستوى المقبول
├── acceptable-day3-worksheet.html    # محتوى اليوم 3 للمستوى المقبول
├── acceptable-day4-worksheet.html    # محتوى اليوم 4 للمستوى المقبول
├── basic-day1-worksheet.html         # محتوى اليوم 1 للمستوى الأساسي
├── basic-day2-worksheet.html         # محتوى اليوم 2 للمستوى الأساسي
├── basic-day3-worksheet.html         # محتوى اليوم 3 للمستوى الأساسي
└── basic-day4-worksheet.html         # محتوى اليوم 4 للمستوى الأساسي
```

## ملفات المخرجات (Outputs)

```
worksheets/
├── intermediate-alldays-worksheet.html  # دمج 4 أيام المستوى المتوسط
├── acceptable-alldays-worksheet.html    # دمج 4 أيام المستوى المقبول
└── basic-alldays-worksheet.html         # دمج 4 أيام المستوى الأساسي
```

---

## المستويات الثلاثة

| المستوى | level_name | level_class | level_description_ar |
|---------|------------|-------------|---------------------|
| المتوسط | intermediate | intermediate-worksheet | المستوى المتوسط |
| المقبول | acceptable | acceptable-worksheet | المستوى المقبول |
| الأساسي | basic | basic-worksheet | المستوى الأساسي |

---

## ملاحظات مهمة

1. **كل ملف day*.html يحتوي على HTML كامل** (<!DOCTYPE>, <html>, <head>, <body>)
2. **المحتوى المطلوب** موجود داخل `<div class="[level]-worksheet">...</div>`
3. **لا تنسخ القالب 4 مرات!** اقرأ كل ملف day*.html واستخرج محتواه الفعلي
4. **العبارة "إعداد أ. محمد العثيمين"** يجب أن تظهر مرة واحدة فقط في الـ worksheet-header
5. **استخدم BeautifulSoup** لاستخراج المحتوى بشكل صحيح

---

## مثال على استخراج المحتوى الصحيح

```python
from bs4 import BeautifulSoup

def extract_day_content_correctly(filepath, level_class):
    """استخراج محتوى يوم من ملف HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    # ابحث عن div الرئيسي الذي يحتوي على المحتوى
    # قد يكون class="[level]-worksheet" أو "excellent-worksheet" أو غيره
    main_div = soup.find('div', class_=lambda x: x and 'worksheet' in x and 'day' not in x)
    
    if not main_div:
        # إذا لم نجد، ابحث عن أي div رئيسي في body
        body = soup.find('body')
        if body:
            # استخرج كل المحتوى ما عدا الأزرار والسكربتات
            main_div = body
    
    return main_div
```

---

## الكود المطلوب

اكتب سكربت Python جديد كامل يقوم بـ:

1. ✅ قراءة القالب (excellent-alldays-worksheet.html) للحصول على البنية والـ CSS
2. ✅ لكل مستوى من الثلاثة (intermediate, acceptable, basic):
   - قراءة 4 ملفات (day1, day2, day3, day4)
   - استخراج المحتوى الفعلي لكل يوم (ليس من القالب!)
   - دمج المحتوى في ملف واحد بالبنية الصحيحة
   - حفظ الملف باسم [level]-alldays-worksheet.html
3. ✅ التأكد من عدم تكرار العبارات أو المحتوى
4. ✅ إضافة page breaks بشكل صحيح بين الأيام

---

## التنفيذ

يرجى كتابة السكربت الصحيح وتنفيذه.
