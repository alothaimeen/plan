"""
تحويل صفحات HTML إلى PDF
يقوم هذا السكريبت بتحويل جميع ورقات العمل إلى ملف PDF واحد بالترتيب المحدد
"""

import os
import asyncio
from pathlib import Path

try:
    from playwright.async_api import async_playwright
    from PyPDF2 import PdfMerger
    print("✓ تم تحميل المكتبات بنجاح")
except ImportError as e:
    print(f"❌ خطأ: مكتبة مفقودة - {e}")
    print("الرجاء تثبيت المكتبات باستخدام:")
    print("pip install playwright PyPDF2")
    print("playwright install chromium")
    exit(1)

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

async def convert_html_to_pdf(html_file, pdf_file):
    """تحويل ملف HTML واحد إلى PDF"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # فتح ملف HTML
        file_url = f"file:///{html_file}".replace("\\", "/")
        await page.goto(file_url)
        
        # الانتظار قليلاً للتأكد من تحميل المحتوى
        await page.wait_for_load_state('networkidle')
        
        # حفظ كـ PDF
        await page.pdf(path=pdf_file, format='A4', print_background=True)
        await browser.close()

async def convert_worksheets_to_pdf():
    """تحويل جميع ورقات العمل إلى ملف PDF واحد"""
    
    print("=" * 60)
    print("بدء عملية التحويل إلى PDF")
    print("=" * 60)
    
    # التحقق من وجود المجلد
    if not worksheets_dir.exists():
        print(f"❌ خطأ: المجلد غير موجود: {worksheets_dir}")
        return
    
    # قائمة لملفات PDF المؤقتة
    temp_pdfs = []
    
    # معالجة كل ملف حسب الترتيب
    for i, filename in enumerate(file_order, 1):
        file_path = worksheets_dir / filename
        
        if file_path.exists():
            print(f"{i}. معالجة: {filename}")
            try:
                # إنشاء ملف PDF مؤقت
                temp_pdf = worksheets_dir / f"temp_{i}.pdf"
                await convert_html_to_pdf(str(file_path), str(temp_pdf))
                temp_pdfs.append(temp_pdf)
                print(f"   ✓ تم التحويل")
            except Exception as e:
                print(f"   ⚠️  تحذير: خطأ في معالجة {filename}: {e}")
        else:
            print(f"   ⚠️  تحذير: الملف غير موجود: {filename}")
    
    if not temp_pdfs:
        print("\n❌ لم يتم العثور على أي ملفات HTML للتحويل")
        return
    
    # اسم ملف PDF الناتج
    output_pdf = worksheets_dir.parent / "all-worksheets-combined.pdf"
    
    print(f"\n📄 عدد الصفحات المراد دمجها: {len(temp_pdfs)}")
    print(f"💾 مسار الملف الناتج: {output_pdf}")
    print("\n⏳ جاري دمج ملفات PDF...")
    
    try:
        # دمج جميع ملفات PDF
        merger = PdfMerger()
        
        for temp_pdf in temp_pdfs:
            merger.append(str(temp_pdf))
        
        # حفظ الملف المدمج
        merger.write(str(output_pdf))
        merger.close()
        
        # حذف الملفات المؤقتة
        print("🧹 تنظيف الملفات المؤقتة...")
        for temp_pdf in temp_pdfs:
            temp_pdf.unlink()
        
        print("\n" + "=" * 60)
        print("✅ تم التحويل والدمج بنجاح!")
        print(f"📁 الملف: {output_pdf}")
        print(f"📄 عدد الصفحات المدمجة: {len(temp_pdfs)}")
        print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ خطأ أثناء الدمج: {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(convert_worksheets_to_pdf())
