#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int tomhas) {
    if (tomhas < 0) { 오류번호 = -tomhas; return -1; }
    return tomhas;
}
int open(const char *faidhle_cur_a_steach_ainm, int fosgail_roghainnean, ...) {
    mode_t 허가 = 0;
    if (fosgail_roghainnean & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, fosgail_roghainnean);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)faidhle_cur_a_steach_ainm, fosgail_roghainnean, 허가, 0, 0));
}
int creat(const char *faidhle_cur_a_steach_ainm, mode_t 허가) { return open(faidhle_cur_a_steach_ainm, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *dàta, size_t baidht_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)dàta, baidht_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *dàta, size_t baidht_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)dàta, baidht_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int tilg_freumh) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, tilg_freumh, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *cor_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)cor_VALUE, 0, 0, 0)); }
int unlink(const char *faidhle_cur_a_steach_ainm) { return 호출결과(jkoros_syscall(38, (int)faidhle_cur_a_steach_ainm, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t baidht_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, baidht_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int àithne, ...) {
    int VALUE = 0;
    if (àithne == F_DUPFD || àithne == F_DUPFD_CLOEXEC || àithne == F_SETFD || àithne == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, àithne); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, àithne, VALUE, 0, 0));
}
