#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int mesur) {
    if (mesur < 0) { 오류번호 = -mesur; return -1; }
    return mesur;
}
int open(const char *ffeil_cofnod_enw, int agor_Gosodiadau, ...) {
    mode_t 허가 = 0;
    if (agor_Gosodiadau & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, agor_Gosodiadau);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)ffeil_cofnod_enw, agor_Gosodiadau, 허가, 0, 0));
}
int creat(const char *ffeil_cofnod_enw, mode_t 허가) { return open(ffeil_cofnod_enw, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t beit_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, beit_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t beit_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, beit_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int prosiect_gwraidd) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, prosiect_gwraidd, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *cyflwr_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)cyflwr_VALUE, 0, 0, 0)); }
int unlink(const char *ffeil_cofnod_enw) { return 호출결과(jkoros_syscall(38, (int)ffeil_cofnod_enw, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t beit_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, beit_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Gorchymyn, ...) {
    int VALUE = 0;
    if (Gorchymyn == F_DUPFD || Gorchymyn == F_DUPFD_CLOEXEC || Gorchymyn == F_SETFD || Gorchymyn == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Gorchymyn); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Gorchymyn, VALUE, 0, 0));
}
