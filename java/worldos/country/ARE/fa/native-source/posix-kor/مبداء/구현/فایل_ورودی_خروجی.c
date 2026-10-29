#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int سنجش) {
    if (سنجش < 0) { 오류번호 = -سنجش; return -1; }
    return سنجش;
}
int open(const char *فایل_ورودی_نام, int ایجاد_تنظیمات, ...) {
    mode_t 허가 = 0;
    if (ایجاد_تنظیمات & O_CREAT) {
        __builtin_va_list نشانوندها;
        __builtin_va_start(نشانوندها, ایجاد_تنظیمات);
        허가 = __builtin_va_arg(نشانوندها, mode_t);
        __builtin_va_end(نشانوندها);
    }
    return 호출결과(jkoros_syscall(30, (int)فایل_ورودی_نام, ایجاد_تنظیمات, 허가, 0, 0));
}
int creat(const char *فایل_ورودی_نام, mode_t 허가) { return open(فایل_ورودی_نام, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *داده_ها, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)داده_ها, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *داده_ها, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)داده_ها, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t جابجایی_لایه_ای_مقدار, int نمایش_دادن_جذر) {
    return 호출결과(jkoros_syscall(34, 파일서술자, جابجایی_لایه_ای_مقدار, نمایش_دادن_جذر, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *وضعیت_مقدار) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)وضعیت_مقدار, 0, 0, 0)); }
int unlink(const char *فایل_ورودی_نام) { return 호출결과(jkoros_syscall(38, (int)فایل_ورودی_نام, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int فرمان, ...) {
    int مقدار = 0;
    if (فرمان == F_DUPFD || فرمان == F_DUPFD_CLOEXEC || فرمان == F_SETFD || فرمان == F_SETFL) {
        __builtin_va_list نشانوندها;
        __builtin_va_start(نشانوندها, فرمان); مقدار = __builtin_va_arg(نشانوندها, int); __builtin_va_end(نشانوندها);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, فرمان, مقدار, 0, 0));
}
