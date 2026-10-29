#include <파일규약.h>
#include <stdio.h>
int main(int 개수, char **إدخال_قائمة_f07b3200) {
    (void)개수; (void)إدخال_قائمة_f07b3200;
    int ملف = فتح_ملف("stored.txt", مقروء_مكتوب | 없으면만들기 | يقتطع_المحتويات, 0600);
    if (ملف < 0 || كتابة_ملف_بيانات(ملف, "saved-from-C", 12) != 12) return 1;
    if (تثبيت_تخزين_الملفات(ملف) < 0) return 2;
    if (يغلق_ملف(ملف) < 0) return 3;
    puts("POSIX FSYNC PASS");
    return 0;
}
