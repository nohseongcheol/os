#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int o_lchov) {
    if (o_lchov < 0) { 오류번호 = -o_lchov; return -1; }
    return o_lchov;
}
int open(const char *fayl_kiritish_nom, int ochmoq_Sozlamalar, ...) {
    mode_t 허가 = 0;
    if (ochmoq_Sozlamalar & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, ochmoq_Sozlamalar);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)fayl_kiritish_nom, ochmoq_Sozlamalar, 허가, 0, 0));
}
int creat(const char *fayl_kiritish_nom, mode_t 허가) { return open(fayl_kiritish_nom, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *ma_lumotlar, size_t bayt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)ma_lumotlar, bayt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *ma_lumotlar, size_t bayt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)ma_lumotlar, bayt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_ildiz) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_ildiz, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *holat_VALUE_e10195a1) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)holat_VALUE_e10195a1, 0, 0, 0)); }
int unlink(const char *fayl_kiritish_nom) { return 호출결과(jkoros_syscall(38, (int)fayl_kiritish_nom, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bayt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bayt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Buyruq, ...) {
    int VALUE = 0;
    if (Buyruq == F_DUPFD || Buyruq == F_DUPFD_CLOEXEC || Buyruq == F_SETFD || Buyruq == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Buyruq); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Buyruq, VALUE, 0, 0));
}
