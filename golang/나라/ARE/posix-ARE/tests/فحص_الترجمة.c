/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <النظام/stat.h>
#include <النظام/هوية_النظام.h>
#include <النظام/انتظار_العمليات_الفرعية.h>
#include <unistd.h>

int posix_compile_test(void)
{
    char cwd[8];
    struct حالة_الملف st;
    struct utsname هوية_النظام;
    int واصف_الملف = فتح("/USER1", O_RDONLY);
    int copy = واصف_الملف >= 0 ? نسخ_مرجع_الملف_المفتوح(واصف_الملف) : -1;
    if (copy >= 0) إغلاق(copy);
    if (واصف_الملف >= 0) {
        جلب_حالة_الملف_المفتوح(واصف_الملف, &st);
        نقل_موضع_الملف(واصف_الملف, 0, SEEK_SET);
        إغلاق(واصف_الملف);
    }
    حالة_الملف("/", &st);
    جلب_معلومات_النظام(&هوية_النظام);
    جلب_مسار_دليل_العمل(cwd, sizeof(cwd));
    return errno + جلب_معرف_العملية() + جلب_معرف_العملية_الأم();
}
