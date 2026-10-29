#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int ukuran) {
    if (ukuran < 0) { 오류번호 = -ukuran; return -1; }
    return ukuran;
}
int open(const char *fail_pemasukan_nama, int buka_Seting, ...) {
    mode_t 허가 = 0;
    if (buka_Seting & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, buka_Seting);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)fail_pemasukan_nama, buka_Seting, 허가, 0, 0));
}
int creat(const char *fail_pemasukan_nama, mode_t 허가) { return open(fail_pemasukan_nama, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t bait_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, bait_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t bait_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, bait_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Ofset_VALUE, int projek_akar) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Ofset_VALUE, projek_akar, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_VALUE, 0, 0, 0)); }
int unlink(const char *fail_pemasukan_nama) { return 호출결과(jkoros_syscall(38, (int)fail_pemasukan_nama, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bait_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bait_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Perintah, ...) {
    int VALUE = 0;
    if (Perintah == F_DUPFD || Perintah == F_DUPFD_CLOEXEC || Perintah == F_SETFD || Perintah == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Perintah); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Perintah, VALUE, 0, 0));
}
