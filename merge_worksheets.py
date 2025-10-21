"""
سكربت لدمج ملفات الأوراق التعليمية (Worksheets) لكل مستوى
يقوم بدمج 4 أيام في ملف واحد محسّن للطباعة

المستويات:
- Intermediate (18-24 درجة)
- Acceptable (10-17 درجة)
- Basic (0-9 درجة)

يقرأ القالب من excellent-alldays-worksheet.html للحصول على CSS والبنية
ثم يستخرج المحتوى الفعلي من ملفات كل مستوى
"""

from bs4 import BeautifulSoup
import os
import re

def read_file(filepath):
    """قراءة محتوى ملف HTML"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    """كتابة محتوى إلى ملف HTML"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_day_content(filepath):
    """
    استخراج محتوى يوم كامل من ملف HTML
    يستخرج كل المحتوى الموجود في body (ما عدا السكربتات والأزرار)
    """
    html_content = read_file(filepath)
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # البحث عن div الرئيسي الذي يحتوي على class يحتوي على 'worksheet'
    main_div = soup.find('div', class_=lambda x: x and 'worksheet' in str(x).lower() and 'day' not in str(x).lower())
    
    if main_div:
        return main_div
    
    # إذا لم نجد div رئيسي، استخرج محتوى body
    body = soup.find('body')
    if body:
        # إزالة الأزرار والسكربتات
        for tag in body.find_all(['script', 'button']):
            tag.decompose()
        
        # إنشاء div جديد لتغليف المحتوى
        content_wrapper = soup.new_tag('div')
        
        # نقل جميع عناصر body إلى wrapper
        for element in list(body.children):
            if element.name:  # تجاهل النصوص الفارغة
                content_wrapper.append(element.extract())
        
        return content_wrapper
    
    return None

def create_merged_worksheet(level_name, level_class, level_description):
    """
    إنشاء ملف مدمج لمستوى معين
    
    level_name: اسم المستوى (intermediate, acceptable, basic)
    level_class: اسم الـ CSS class للمستوى
    level_description: وصف المستوى بالعربية
    """
    
    base_dir = "worksheets"
    
    # 1. قراءة القالب للحصول على HEAD (CSS + structure) فقط
    template_path = os.path.join(base_dir, "excellent-alldays-worksheet.html")
    template_content = read_file(template_path)
    template_soup = BeautifulSoup(template_content, 'html.parser')
    
    # 2. استخراج head من القالب
    head_tag = template_soup.find('head')
    if not head_tag:
        print(f"  ❌ خطأ: لم يتم العثور على <head> في القالب")
        return None
    
    # تعديل العنوان
    title_tag = head_tag.find('title')
    if title_tag:
        title_tag.string = f"Remedial Plan - {level_name.title()} Level - All Days"
    
    # تعديل CSS classes
    css_style = head_tag.find('style')
    if css_style:
        css_text = css_style.string
        # استبدال excellent-worksheet بـ level_class الجديد
        css_text = css_text.replace('.excellent-worksheet', f'.{level_class}')
        css_style.string = css_text
    
    # 3. إنشاء HTML جديد من الصفر
    new_soup = BeautifulSoup('<!DOCTYPE html><html dir="rtl" lang="ar"></html>', 'html.parser')
    html_tag = new_soup.find('html')
    
    # إضافة head المعدّل
    html_tag.append(head_tag)
    
    # إنشاء body جديد
    body_tag = new_soup.new_tag('body')
    html_tag.append(body_tag)
    
    # إضافة زر الطباعة
    print_button = new_soup.new_tag('button', **{'class': 'print-button', 'onclick': 'window.print()'})
    print_button.string = '🖨️ طباعة جميع أوراق العمل (4 أيام)'
    body_tag.append(print_button)
    
    # 4. قراءة محتوى الأيام الأربعة من الملفات الصحيحة
    for day_num in range(1, 5):
        day_file = os.path.join(base_dir, f"{level_name}-day{day_num}-worksheet.html")
        
        if not os.path.exists(day_file):
            print(f"  ⚠️ تحذير: الملف غير موجود - {day_file}")
            continue
        
        print(f"  📖 قراءة: {day_file}")
        
        # استخراج محتوى اليوم الكامل
        day_content_div = extract_day_content(day_file)
        
        if not day_content_div:
            print(f"  ⚠️ تحذير: لم يتم استخراج محتوى من {day_file}")
            continue
        
        # إضافة فاصل صفحة قبل الأيام 2، 3، 4
        if day_num > 1:
            separator = new_soup.new_tag('div', **{'class': 'day-separator'})
            body_tag.append(separator)
        
        # تعديل class name في المحتوى المستخرج
        if day_content_div.has_attr('class'):
            # استبدال أي class يحتوي على 'worksheet' بـ level_class الجديد
            old_classes = day_content_div.get('class', [])
            new_classes = []
            for cls in old_classes:
                if 'worksheet' in cls:
                    new_classes.append(level_class)
                else:
                    new_classes.append(cls)
            day_content_div['class'] = new_classes
        
        # تحديث h1 في اليوم الأول فقط ليكون "جميع الأيام"
        if day_num == 1:
            h1_in_day = day_content_div.find('h1')
            if h1_in_day:
                h1_in_day.string = f"الخطة العلاجية - {level_description} - جميع الأيام"
        
        # إضافة المحتوى
        body_tag.append(day_content_div)
    
    # 5. حفظ الملف المدمج
    output_file = os.path.join(base_dir, f"{level_name}-alldays-worksheet.html")
    
    # تنسيق HTML
    final_html = new_soup.prettify()
    write_file(output_file, final_html)
    
    print(f"✅ تم إنشاء: {output_file}")
    return output_file

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("بدء عملية دمج الأوراق التعليمية")
    print("=" * 60)
    print()
    
    # المستويات المطلوب دمجها
    levels = [
        {
            'name': 'intermediate',
            'class': 'intermediate-worksheet',
            'description': 'المستوى المتوسط'
        },
        {
            'name': 'acceptable',
            'class': 'acceptable-worksheet',
            'description': 'المستوى المقبول'
        },
        {
            'name': 'basic',
            'class': 'basic-worksheet',
            'description': 'المستوى الأساسي'
        }
    ]
    
    created_files = []
    
    for level in levels:
        print(f"\n📝 معالجة المستوى: {level['description']} ({level['name']})")
        print("-" * 60)
        try:
            output = create_merged_worksheet(
                level['name'],
                level['class'],
                level['description']
            )
            created_files.append(output)
        except Exception as e:
            print(f"❌ خطأ في معالجة {level['name']}: {str(e)}")
    
    print("\n" + "=" * 60)
    print("اكتمل الدمج!")
    print("=" * 60)
    print(f"\nتم إنشاء {len(created_files)} ملف:")
    for f in created_files:
        print(f"  ✅ {f}")
    print("\n💡 يمكنك الآن فتح الملفات في المتصفح واختبار الطباعة")

if __name__ == "__main__":
    main()
