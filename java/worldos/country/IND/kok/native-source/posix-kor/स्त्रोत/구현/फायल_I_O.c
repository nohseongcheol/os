#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int मेजप) {
    if (मेजप < 0) { 오류번호 = -मेजप; return -1; }
    return मेजप;
}
int open(const char *फायल_प्रवेश_नांव, int उगडचें_मांडावळी, ...) {
    mode_t 허가 = 0;
    if (उगडचें_मांडावळी & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, उगडचें_मांडावळी);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)फायल_प्रवेश_नांव, उगडचें_मांडावळी, 허가, 0, 0));
}
int creat(const char *फायल_प्रवेश_नांव, mode_t 허가) { return open(फायल_प्रवेश_नांव, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *डेटा, size_t बायट_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)डेटा, बायट_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *डेटा, size_t बायट_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)डेटा, बायट_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ऑफसॅट_मोल, int प्रॉजॅक्ट_रूट) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ऑफसॅट_मोल, प्रॉजॅक्ट_रूट, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *स्थिती_मोल_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)स्थिती_मोल_e10195a1, 0, 0, 0)); }
int unlink(const char *फायल_प्रवेश_नांव) { return 호출결과(jkoros_syscall(38, (int)फायल_प्रवेश_नांव, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t बायट_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, बायट_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int आदेश, ...) {
    int मोल = 0;
    if (आदेश == F_DUPFD || आदेश == F_DUPFD_CLOEXEC || आदेश == F_SETFD || आदेश == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, आदेश); मोल = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, आदेश, मोल, 0, 0));
}
