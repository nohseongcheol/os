#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int 결과) {
    if (결과 < 0) { 오류번호 = -결과; return -1; }
    return 결과;
}
int open(const char *ගොනුව_පිවිසුම_නම, int සාදන්න_පසුතල, ...) {
    mode_t 허가 = 0;
    if (සාදන්න_පසුතල & O_CREAT) {
        __builtin_va_list විස්තාරක;
        __builtin_va_start(විස්තාරක, සාදන්න_පසුතල);
        허가 = __builtin_va_arg(විස්තාරක, mode_t);
        __builtin_va_end(විස්තාරක);
    }
    return 호출결과(jkoros_syscall(30, (int)ගොනුව_පිවිසුම_නම, සාදන්න_පසුතල, 허가, 0, 0));
}
int creat(const char *ගොනුව_පිවිසුම_නම, mode_t 허가) { return open(ගොනුව_පිවිසුම_නම, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *දත්ත, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)දත්ත, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *දත්ත, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)දත්ත, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t ඕෆ්සෙට්_අගය, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, ඕෆ්සෙට්_අගය, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *තත්වය_අගය) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)තත්වය_අගය, 0, 0, 0)); }
int unlink(const char *ගොනුව_පිවිසුම_නම) { return 호출결과(jkoros_syscall(38, (int)ගොනුව_පිවිසුම_නම, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int විධානය, ...) {
    int අගය = 0;
    if (විධානය == F_DUPFD || විධානය == F_DUPFD_CLOEXEC || විධානය == F_SETFD || විධානය == F_SETFL) {
        __builtin_va_list විස්තාරක;
        __builtin_va_start(විස්තාරක, විධානය); අගය = __builtin_va_arg(විස්තාරක, int); __builtin_va_end(විස්තාරක);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, විධානය, අගය, 0, 0));
}
