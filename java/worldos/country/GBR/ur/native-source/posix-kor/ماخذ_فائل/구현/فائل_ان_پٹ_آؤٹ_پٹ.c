#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int پیمائش) {
    if (پیمائش < 0) { 오류번호 = -پیمائش; return -1; }
    return پیمائش;
}
int open(const char *فائل_اندراج_نام, int بنائیں_سیٹنگز, ...) {
    mode_t 허가 = 0;
    if (بنائیں_سیٹنگز & O_CREAT) {
        __builtin_va_list دلائل;
        __builtin_va_start(دلائل, بنائیں_سیٹنگز);
        허가 = __builtin_va_arg(دلائل, mode_t);
        __builtin_va_end(دلائل);
    }
    return 호출결과(jkoros_syscall(30, (int)فائل_اندراج_نام, بنائیں_سیٹنگز, 허가, 0, 0));
}
int creat(const char *فائل_اندراج_نام, mode_t 허가) { return open(فائل_اندراج_نام, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *کوائف, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)کوائف, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *کوائف, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)کوائف, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t آفسٹ_قدر, int عکس_ڈالنا_روٹ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, آفسٹ_قدر, عکس_ڈالنا_روٹ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *حالت_قدر) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)حالت_قدر, 0, 0, 0)); }
int unlink(const char *فائل_اندراج_نام) { return 호출결과(jkoros_syscall(38, (int)فائل_اندراج_نام, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int حکم, ...) {
    int قدر = 0;
    if (حکم == F_DUPFD || حکم == F_DUPFD_CLOEXEC || حکم == F_SETFD || حکم == F_SETFL) {
        __builtin_va_list دلائل;
        __builtin_va_start(دلائل, حکم); قدر = __builtin_va_arg(دلائل, int); __builtin_va_end(دلائل);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, حکم, قدر, 0, 0));
}
