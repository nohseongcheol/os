#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ಮಾಪನ) {
    if (ಮಾಪನ < 0) { 오류번호 = -ಮಾಪನ; return -1; }
    return ಮಾಪನ;
}
int open(const char *ಫೈಲ್_ನಮೂದು_ಹೆಸರು, int ರಚಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್, ...) {
    mode_t 허가 = 0;
    if (ರಚಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್ & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ರಚಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ಫೈಲ್_ನಮೂದು_ಹೆಸರು, ರಚಿಸು_ಸೆಟ್ಟಿಂಗ್ಸ್, 허가, 0, 0));
}
int creat(const char *ಫೈಲ್_ನಮೂದು_ಹೆಸರು, mode_t 허가) { return open(ಫೈಲ್_ನಮೂದು_ಹೆಸರು, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ಡೇಟಾ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ಡೇಟಾ, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ಡೇಟಾ, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ಡೇಟಾ, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ, int ಬಿಂಬಿಸು_ಮೂಲ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ಆಫ್_ಸೆಟ್_ಮೌಲ್ಯ, ಬಿಂಬಿಸು_ಮೂಲ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *ಸ್ಥಿತಿ_ಮೌಲ್ಯ) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)ಸ್ಥಿತಿ_ಮೌಲ್ಯ, 0, 0, 0)); }
int unlink(const char *ಫೈಲ್_ನಮೂದು_ಹೆಸರು) { return 호출결과(jkoros_syscall(38, (int)ಫೈಲ್_ನಮೂದು_ಹೆಸರು, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int ಆಜ್ಞೆ, ...) {
    int ಮೌಲ್ಯ = 0;
    if (ಆಜ್ಞೆ == F_DUPFD || ಆಜ್ಞೆ == F_DUPFD_CLOEXEC || ಆಜ್ಞೆ == F_SETFD || ಆಜ್ಞೆ == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ಆಜ್ಞೆ); ಮೌಲ್ಯ = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, ಆಜ್ಞೆ, ಮೌಲ್ಯ, 0, 0));
}
