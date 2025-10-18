/* ============================================
   📚 الخطة العلاجية للغة الإنجليزية - JavaScript
   ============================================ */

// ===========================================
// وظيفة فتح جميع أوراق العمل للطباعة
// ===========================================
function printAllWorksheets(level) {
    const files = [
        `worksheets/${level}-day1-worksheet.html`,
        `worksheets/${level}-day2-worksheet.html`,
        `worksheets/${level}-day3-worksheet.html`,
        `worksheets/${level}-day4-worksheet.html`
    ];
    
    // فتح كل ملف في تبويب جديد
    files.forEach((file, index) => {
        setTimeout(() => {
            window.open(file, '_blank');
        }, index * 200); // تأخير بسيط بين كل تبويب
    });
}

// ===========================================
// وظيفة فتح جميع الاختبارات للطباعة
// ===========================================
function printAllTests(level) {
    const files = [
        `tests/${level}-day1-test.html`,
        `tests/${level}-day2-test.html`,
        `tests/${level}-day3-test.html`,
        `tests/${level}-day4-test.html`
    ];
    
    // فتح كل ملف في تبويب جديد
    files.forEach((file, index) => {
        setTimeout(() => {
            window.open(file, '_blank');
        }, index * 200); // تأخير بسيط بين كل تبويب
    });
}

// ===========================================
// تأثير Smooth Scrolling
// ===========================================
document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll للروابط الداخلية
    const links = document.querySelectorAll('a[href^="#"]');
    
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// ===========================================
// تأثير Fade In للعناصر عند التحميل
// ===========================================
window.addEventListener('load', function() {
    const cards = document.querySelectorAll('.card, .day-card');
    
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 50);
        }, index * 100);
    });
});

// ===========================================
// عرض رسالة تأكيد عند فتح الملفات
// ===========================================
function showConfirmation(message) {
    // يمكن إضافة رسالة تأكيد بسيطة
    console.log(message);
}

// ===========================================
// التحقق من دعم المتصفح
// ===========================================
if (typeof window.open === 'undefined') {
    console.warn('المتصفح لا يدعم فتح نوافذ جديدة');
}
