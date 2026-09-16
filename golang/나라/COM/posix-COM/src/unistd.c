/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <النظام/stat.h>
#include <النظام/انتظار_العمليات_الفرعية.h>
#include <unistd.h>
#include <النظام/syscall.h>

enum {
    SYS_إنهاء_فوري = 1,
    SYS_إنشاء_عملية_فرعية = 2,
    SYS_قراءة = 3,
    SYS_كتابة = 4,
    SYS_إغلاق = 6,
    SYS_استبدال_البرنامج_الجاري = 11,
    SYS_تغيير_دليل_العمل = 12,
    SYS_نقل_موضع_الملف = 19,
    SYS_جلب_معرف_العملية = 20,
    SYS_جلب_معرف_المستخدم = 24,
    SYS_فحص_صلاحيات_الوصول = 33,
    SYS_مزامنة_جميع_البيانات = 36,
    SYS_نسخ_مرجع_الملف_المفتوح = 41,
    SYS_تعيين_نهاية_الذاكرة_المتغيرة = 45,
    SYS_جلب_معرف_المجموعة = 47,
    SYS_جلب_معرف_المستخدم_الفعلي = 49,
    SYS_جلب_معرف_المجموعة_الفعلي = 50,
    SYS_نسخ_مرجع_الملف_إلى_رقم_محدد = 63,
    SYS_جلب_معرف_العملية_الأم = 64,
    SYS_مزامنة_بيانات_الملف = 118,
    SYS_جلب_مسار_دليل_العمل = 183
};

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void إنهاء_فوري(int الحالة)
{
    SC1(SYS_إنهاء_فوري, الحالة);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t قراءة(int واصف_الملف, void *مخزن_النقل_المؤقت, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_قراءة, واصف_الملف, مخزن_النقل_المؤقت, count));
}

ssize_t كتابة(int واصف_الملف, const void *مخزن_النقل_المؤقت, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_كتابة, واصف_الملف, مخزن_النقل_المؤقت, count));
}

int إغلاق(int واصف_الملف)
{
    return (int)__syscall_result(SC1(SYS_إغلاق, واصف_الملف));
}

off_t نقل_موضع_الملف(int واصف_الملف, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_نقل_موضع_الملف, واصف_الملف, offset, whence));
}

pid_t إنشاء_عملية_فرعية(void)
{
    return (pid_t)__syscall_result(SC0(SYS_إنشاء_عملية_فرعية));
}

int استبدال_البرنامج_الجاري(const char *المسار, char *const المعاملات_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_استبدال_البرنامج_الجاري, المسار, المعاملات_2, envp));
}

pid_t جلب_معرف_العملية(void) { return (pid_t)SC0(SYS_جلب_معرف_العملية); }
pid_t جلب_معرف_العملية_الأم(void) { return (pid_t)SC0(SYS_جلب_معرف_العملية_الأم); }
uid_t جلب_معرف_المستخدم(void) { return (uid_t)SC0(SYS_جلب_معرف_المستخدم); }
uid_t جلب_معرف_المستخدم_الفعلي(void) { return (uid_t)SC0(SYS_جلب_معرف_المستخدم_الفعلي); }
gid_t جلب_معرف_المجموعة(void) { return (gid_t)SC0(SYS_جلب_معرف_المجموعة); }
gid_t جلب_معرف_المجموعة_الفعلي(void) { return (gid_t)SC0(SYS_جلب_معرف_المجموعة_الفعلي); }

int فحص_صلاحيات_الوصول(const char *المسار, int mode)
{
    return (int)__syscall_result(SC2(SYS_فحص_صلاحيات_الوصول, المسار, mode));
}

int تغيير_دليل_العمل(const char *المسار)
{
    return (int)__syscall_result(SC1(SYS_تغيير_دليل_العمل, المسار));
}

char *جلب_مسار_دليل_العمل(char *مخزن_النقل_المؤقت, size_t عدد_الخانات)
{
    long result = __syscall_result(SC2(SYS_جلب_مسار_دليل_العمل, مخزن_النقل_المؤقت, عدد_الخانات));
    return result < 0 ? (char *)0 : مخزن_النقل_المؤقت;
}

int نسخ_مرجع_الملف_المفتوح(int واصف_الملف)
{
    return (int)__syscall_result(SC1(SYS_نسخ_مرجع_الملف_المفتوح, واصف_الملف));
}

int نسخ_مرجع_الملف_إلى_رقم_محدد(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_نسخ_مرجع_الملف_إلى_رقم_محدد, oldfd, newfd));
}

int مزامنة_بيانات_الملف(int واصف_الملف)
{
    return (int)__syscall_result(SC1(SYS_مزامنة_بيانات_الملف, واصف_الملف));
}

void مزامنة_جميع_البيانات(void)
{
    SC0(SYS_مزامنة_جميع_البيانات);
}

int فحص_كون_الوصف_طرفية(int واصف_الملف)
{
    struct حالة_الملف st;
    if (جلب_حالة_الملف_المفتوح(واصف_الملف, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int تعيين_نهاية_الذاكرة_المتغيرة(void *address)
{
    long result = SC1(SYS_تعيين_نهاية_الذاكرة_المتغيرة, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *نقل_نهاية_الذاكرة_المتغيرة(int increment)
{
    long current = SC1(SYS_تعيين_نهاية_الذاكرة_المتغيرة, 0);
    long requested = current + increment;
    if (increment != 0 && تعيين_نهاية_الذاكرة_المتغيرة((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t انتظار_العملية_الفرعية_المحددة(pid_t pid, int *الحالة, int options)
{
    long result;
    do {
        result = SC3(7, pid, الحالة, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t انتظار_عملية_فرعية(int *الحالة)
{
    return انتظار_العملية_الفرعية_المحددة(-1, الحالة, 0);
}
