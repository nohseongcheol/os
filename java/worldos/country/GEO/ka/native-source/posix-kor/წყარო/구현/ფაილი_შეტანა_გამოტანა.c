#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int გაზომვა) {
    if (გაზომვა < 0) { 오류번호 = -გაზომვა; return -1; }
    return გაზომვა;
}
int open(const char *ფაილი_შენატანი_სახელი, int გახსნა_პარამეტრები, ...) {
    mode_t 허가 = 0;
    if (გახსნა_პარამეტრები & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, გახსნა_პარამეტრები);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ფაილი_შენატანი_სახელი, გახსნა_პარამეტრები, 허가, 0, 0));
}
int creat(const char *ფაილი_შენატანი_სახელი, mode_t 허가) { return open(ფაილი_შენატანი_სახელი, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *მონაცემები, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)მონაცემები, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *მონაცემები, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)მონაცემები, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ოფსეტი_მნიშვნელობა, int პროეცირება_ფესვი) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ოფსეტი_მნიშვნელობა, პროეცირება_ფესვი, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *სტატუსი_მნიშვნელობა) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)სტატუსი_მნიშვნელობა, 0, 0, 0)); }
int unlink(const char *ფაილი_შენატანი_სახელი) { return 호출결과(jkoros_syscall(38, (int)ფაილი_შენატანი_სახელი, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ბრძანება, ...) {
    int მნიშვნელობა = 0;
    if (ბრძანება == F_DUPFD || ბრძანება == F_DUPFD_CLOEXEC || ბრძანება == F_SETFD || ბრძანება == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ბრძანება); მნიშვნელობა = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ბრძანება, მნიშვნელობა, 0, 0));
}
