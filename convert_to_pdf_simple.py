"""
تحويل صفحات HTML إلى PDF باستخدام متصفح Chrome/Edge
"""

import os
import subprocess
from pathlib import Path
import shutil

# مسار المجلد
worksheets_dir = Path(r"C:\Users\memm2\Documents\programming\school\website\worksheets")

# ترتيب الملفات حسب المطلوب
file_order = [
    "cover-page.html",
    # Basic level (4 days)
    "basic-day1-worksheet.html",
    "basic-day2-worksheet.html",
    "basic-day3-worksheet.html",
    "basic-day4-worksheet.html",
    # Acceptable level (4 days)
    "acceptable-day1-worksheet.html",
    "acceptable-day2-worksheet.html",
    "acceptable-day3-worksheet.html",
    "acceptable-day4-worksheet.html",
    # Intermediate level (4 days)
    "intermediate-day1-worksheet.html",
    "intermediate-day2-worksheet.html",
    "intermediate-day3-worksheet.html",
    "intermediate-day4-worksheet.html",
    # Excellent level (4 days)
    "excellent-day1-worksheet.html",
    "excellent-day2-worksheet.html",
    "excellent-day3-worksheet.html",
    "excellent-day4-worksheet.html",
]

def find_chrome():
    """البحث عن متصفح Chrome أو Edge"""
    possible_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def convert_html_to_pdf_chrome(html_file, pdf_file, chrome_path):
    """تحويل HTML إلى PDF باستخدام Chrome/Edge headless"""
    try:
        # تحويل المسار إلى URL
        file_url = f"file:///{html_file}".replace("\\", "/")
        
        # أمر التحويل
        cmd = [
            chrome_path,
            "--headless",
            "--disable-gpu",
            "--print-to-pdf=" + str(pdf_file),
            "--no-margins",
            file_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(pdf_file):
            return True
        else:
            print(f"   ⚠️  خطأ في التحويل: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ⚠️  خطأ: {e}")
        return False

def merge_pdfs_simple(pdf_files, output_file):
    """دمج ملفات PDF باستخدام PyPDF2"""
    try:
        from PyPDF2 import PdfMerger
        
        merger = PdfMerger()
        for pdf_file in pdf_files:
            if os.path.exists(pdf_file):
                merger.append(str(pdf_file))
        
        merger.write(str(output_file))
        merger.close()
        return True
    except Exception as e:
        print(f"❌ خطأ في الدمج: {e}")
        return False

def convert_worksheets():
    """تحويل جميع ورقات العمل"""
    
    print("=" * 60)
    print("بدء عملية التحويل إلى PDF")
    print("=" * 60)
    
    # البحث عن المتصفح
    chrome_path = find_chrome()
    if not chrome_path:
        print("❌ خطأ: لم يتم العثور على Chrome أو Edge")
        print("الرجاء تثبيت أحدهما أولاً")
        return
    
    print(f"✓ تم العثور على المتصفح: {chrome_path}")
    
    # التحقق من وجود المجلد
    if not worksheets_dir.exists():
        print(f"❌ خطأ: المجلد غير موجود: {worksheets_dir}")
        return
    
    # قائمة لملفات PDF المؤقتة
    temp_pdfs = []
    temp_dir = worksheets_dir / "temp_pdfs"
    temp_dir.mkdir(exist_ok=True)
    
    # معالجة كل ملف
    print("\n📄 تحويل الملفات:")
    for i, filename in enumerate(file_order, 1):
        file_path = worksheets_dir / filename
        
        if file_path.exists():
            print(f"{i}. {filename}...", end=" ")
            temp_pdf = temp_dir / f"{i:02d}_{filename.replace('.html', '.pdf')}"
            
            if convert_html_to_pdf_chrome(file_path, temp_pdf, chrome_path):
                temp_pdfs.append(temp_pdf)
                print("✓")
            else:
                print("✗")
        else:
            print(f"{i}. ⚠️  الملف غير موجود: {filename}")
    
    if not temp_pdfs:
        print("\n❌ لم يتم تحويل أي ملفات")
        return
    
    # دمج الملفات
    output_pdf = worksheets_dir.parent / "all-worksheets-combined.pdf"
    
    print(f"\n⏳ دمج {len(temp_pdfs)} ملف PDF...")
    
    if merge_pdfs_simple(temp_pdfs, output_pdf):
        print("\n" + "=" * 60)
        print("✅ تم التحويل والدمج بنجاح!")
        print(f"📁 الملف: {output_pdf}")
        print(f"📄 عدد الصفحات: {len(temp_pdfs)}")
        print("=" * 60)
        
        # حذف الملفات المؤقتة
        print("\n🧹 تنظيف الملفات المؤقتة...")
        shutil.rmtree(temp_dir)
    else:
        print("\n❌ فشل في دمج الملفات")
        print(f"الملفات المؤقتة في: {temp_dir}")

if __name__ == "__main__":
    convert_worksheets()
