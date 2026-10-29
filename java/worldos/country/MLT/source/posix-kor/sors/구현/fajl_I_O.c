#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int miżura) {
    if (miżura < 0) { 오류번호 = -miżura; return -1; }
    return miżura;
}
int open(const char *fajl_entrata_isem, int fetaħ_Settings, ...) {
    mode_t 허가 = 0;
    if (fetaħ_Settings & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, fetaħ_Settings);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)fajl_entrata_isem, fetaħ_Settings, 허가, 0, 0));
}
int creat(const char *fajl_entrata_isem, mode_t 허가) { return open(fajl_entrata_isem, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int pprojetta_għerq) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, pprojetta_għerq, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *stat_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)stat_VALUE, 0, 0, 0)); }
int unlink(const char *fajl_entrata_isem) { return 호출결과(jkoros_syscall(38, (int)fajl_entrata_isem, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int kmand, ...) {
    int VALUE = 0;
    if (kmand == F_DUPFD || kmand == F_DUPFD_CLOEXEC || kmand == F_SETFD || kmand == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, kmand); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, kmand, VALUE, 0, 0));
}
