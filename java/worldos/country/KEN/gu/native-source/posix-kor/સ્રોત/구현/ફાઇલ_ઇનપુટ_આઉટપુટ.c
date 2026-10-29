#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int પરિમાણ) {
    if (પરિમાણ < 0) { 오류번호 = -પરિમાણ; return -1; }
    return પરિમાણ;
}
int open(const char *ફાઇલ_પ્રવેશ_નામ, int બનાવો_સેટિંગ્સ, ...) {
    mode_t 허가 = 0;
    if (બનાવો_સેટિંગ્સ & O_CREAT) {
        __builtin_va_list દલીલો;
        __builtin_va_start(દલીલો, બનાવો_સેટિંગ્સ);
        허가 = __builtin_va_arg(દલીલો, mode_t);
        __builtin_va_end(દલીલો);
    }
    return 호출결과(jkoros_syscall(30, (int)ફાઇલ_પ્રવેશ_નામ, બનાવો_સેટિંગ્સ, 허가, 0, 0));
}
int creat(const char *ફાઇલ_પ્રવેશ_નામ, mode_t 허가) { return open(ફાઇલ_પ્રવેશ_નામ, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ડેટા, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ડેટા, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *ડેટા, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ડેટા, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ઑફસેટ_મૂલ્ય, int પ્રોજેક્ટ_રૂટ) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ઑફસેટ_મૂલ્ય, પ્રોજેક્ટ_રૂટ, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *સ્થિતિ_મૂલ્ય_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)સ્થિતિ_મૂલ્ય_e10195a1, 0, 0, 0)); }
int unlink(const char *ફાઇલ_પ્રવેશ_નામ) { return 호출결과(jkoros_syscall(38, (int)ફાઇલ_પ્રવેશ_નામ, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int આદેશ, ...) {
    int મૂલ્ય = 0;
    if (આદેશ == F_DUPFD || આદેશ == F_DUPFD_CLOEXEC || આદેશ == F_SETFD || આદેશ == F_SETFL) {
        __builtin_va_list દલીલો;
        __builtin_va_start(દલીલો, આદેશ); મૂલ્ય = __builtin_va_arg(દલીલો, int); __builtin_va_end(દલીલો);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, આદેશ, મૂલ્ય, 0, 0));
}
