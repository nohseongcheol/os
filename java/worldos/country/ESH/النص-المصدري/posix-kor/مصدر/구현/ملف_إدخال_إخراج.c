#include <파일규약.h>
#include "호출경계.h"

int رقم_الخطأ;
int 호출결과(int نتيجة) {
    if (نتيجة < 0) { رقم_الخطأ = -نتيجة; return -1; }
    return نتيجة;
}
int open(const char *ملف_إدخال_اسم, int فتح_إعدادات, ...) {
    mode_t 허가 = 0;
    if (فتح_إعدادات & O_CREAT) {
        __builtin_va_list وسائط;
        __builtin_va_start(وسائط, فتح_إعدادات);
        허가 = __builtin_va_arg(وسائط, mode_t);
        __builtin_va_end(وسائط);
    }
    return 호출결과(jkoros_syscall(30, (int)ملف_إدخال_اسم, فتح_إعدادات, 허가, 0, 0));
}
int creat(const char *ملف_إدخال_اسم, mode_t 허가) { return open(ملف_إدخال_اسم, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *بيانات, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)بيانات, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *بيانات, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)بيانات, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t إزاحة_قيمة, int يعرض_جذر) {
    return 호출결과(jkoros_syscall(34, 파일서술자, إزاحة_قيمة, يعرض_جذر, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *حالة_قيمة) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)حالة_قيمة, 0, 0, 0)); }
int unlink(const char *ملف_إدخال_اسم) { return 호출결과(jkoros_syscall(38, (int)ملف_إدخال_اسم, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int أمر, ...) {
    int قيمة = 0;
    if (أمر == F_DUPFD || أمر == F_DUPFD_CLOEXEC || أمر == F_SETFD || أمر == F_SETFL) {
        __builtin_va_list وسائط;
        __builtin_va_start(وسائط, أمر); قيمة = __builtin_va_arg(وسائط, int); __builtin_va_end(وسائط);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, أمر, قيمة, 0, 0));
}
