#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int পরিমাপ) {
    if (পরিমাপ < 0) { 오류번호 = -পরিমাপ; return -1; }
    return পরিমাপ;
}
int open(const char *ফাইল_ভুক্তি_নাম, int খোলা_সেটিংস, ...) {
    mode_t 허가 = 0;
    if (খোলা_সেটিংস & O_CREAT) {
        __builtin_va_list আর্গুমেন্ট_তালিকা;
        __builtin_va_start(আর্গুমেন্ট_তালিকা, খোলা_সেটিংস);
        허가 = __builtin_va_arg(আর্গুমেন্ট_তালিকা, mode_t);
        __builtin_va_end(আর্গুমেন্ট_তালিকা);
    }
    return 호출결과(jkoros_syscall(30, (int)ফাইল_ভুক্তি_নাম, খোলা_সেটিংস, 허가, 0, 0));
}
int creat(const char *ফাইল_ভুক্তি_নাম, mode_t 허가) { return open(ফাইল_ভুক্তি_নাম, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ডাটা, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ডাটা, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ডাটা, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ডাটা, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t অফসেট_মান, int প্রকল্প_মূল) {
    return 호출결과(jkoros_syscall(34, 파일서술자, অফসেট_মান, প্রকল্প_মূল, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *অবস্হা_মান) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)অবস্হা_মান, 0, 0, 0)); }
int unlink(const char *ফাইল_ভুক্তি_নাম) { return 호출결과(jkoros_syscall(38, (int)ফাইল_ভুক্তি_নাম, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int আদেশ, ...) {
    int মান = 0;
    if (আদেশ == F_DUPFD || আদেশ == F_DUPFD_CLOEXEC || আদেশ == F_SETFD || আদেশ == F_SETFL) {
        __builtin_va_list আর্গুমেন্ট_তালিকা;
        __builtin_va_start(আর্গুমেন্ট_তালিকা, আদেশ); মান = __builtin_va_arg(আর্গুমেন্ট_তালিকা, int); __builtin_va_end(আর্গুমেন্ট_তালিকা);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, আদেশ, মান, 0, 0));
}
