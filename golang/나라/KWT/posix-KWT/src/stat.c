/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <النظام/stat.h>
#include <النظام/هوية_النظام.h>
#include <النظام/syscall.h>

enum { SYS_حالة_الملف = 106, SYS_جلب_حالة_الرابط_نفسه = 107, SYS_جلب_حالة_الملف_المفتوح = 108, SYS_جلب_معلومات_النظام = 122 };

int حالة_الملف(const char *المسار, struct حالة_الملف *مخزن_النقل_المؤقت)
{
    return (int)__syscall_result(
        __syscall6(SYS_حالة_الملف, (long)المسار, (long)مخزن_النقل_المؤقت, 0, 0, 0, 0));
}

int جلب_حالة_الرابط_نفسه(const char *المسار, struct حالة_الملف *مخزن_النقل_المؤقت)
{
    return (int)__syscall_result(
        __syscall6(SYS_جلب_حالة_الرابط_نفسه, (long)المسار, (long)مخزن_النقل_المؤقت, 0, 0, 0, 0));
}

int جلب_حالة_الملف_المفتوح(int واصف_الملف, struct حالة_الملف *مخزن_النقل_المؤقت)
{
    return (int)__syscall_result(
        __syscall6(SYS_جلب_حالة_الملف_المفتوح, واصف_الملف, (long)مخزن_النقل_المؤقت, 0, 0, 0, 0));
}

int جلب_معلومات_النظام(struct utsname *هوية_النظام)
{
    return (int)__syscall_result(
        __syscall6(SYS_جلب_معلومات_النظام, (long)هوية_النظام, 0, 0, 0, 0, 0));
}
