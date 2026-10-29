#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int পৰিমাপ) {
    if (পৰিমাপ < 0) { 오류번호 = -পৰিমাপ; return -1; }
    return পৰিমাপ;
}
int open(const char *ফাইল_প্রবিষ্ট_নাম, int খোলক_ছেটিংছ, ...) {
    mode_t 허가 = 0;
    if (খোলক_ছেটিংছ & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, খোলক_ছেটিংছ);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ফাইল_প্রবিষ্ট_নাম, খোলক_ছেটিংছ, 허가, 0, 0));
}
int creat(const char *ফাইল_প্রবিষ্ট_নাম, mode_t 허가) { return open(ফাইল_প্রবিষ্ট_নাম, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ডাটা, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ডাটা, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ডাটা, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ডাটা, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t অফছেট_মান, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, অফছেট_মান, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *অৱস্থা_মান) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)অৱস্থা_মান, 0, 0, 0)); }
int unlink(const char *ফাইল_প্রবিষ্ট_নাম) { return 호출결과(jkoros_syscall(38, (int)ফাইল_প্রবিষ্ট_নাম, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int কমান্ড, ...) {
    int মান = 0;
    if (কমান্ড == F_DUPFD || কমান্ড == F_DUPFD_CLOEXEC || কমান্ড == F_SETFD || কমান্ড == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, কমান্ড); মান = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, কমান্ড, মান, 0, 0));
}
