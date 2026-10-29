#include <파일규약.h>
#include "호출경계.h"

int broj_greške;
int 호출결과(int KR) {
    if (KR < 0) { broj_greške = -KR; return -1; }
    return KR;
}
int open(const char *Datoteka_stavka_ime, int otvoren_Postavke, ...) {
    mode_t 허가 = 0;
    if (otvoren_Postavke & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, otvoren_Postavke);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)Datoteka_stavka_ime, otvoren_Postavke, 허가, 0, 0));
}
int creat(const char *Datoteka_stavka_ime, mode_t 허가) { return open(Datoteka_stavka_ime, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *podaci, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)podaci, bajt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *podaci, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)podaci, bajt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Pomak_VALUE, int radnja_koren) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Pomak_VALUE, radnja_koren, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Status_VALUE, 0, 0, 0)); }
int unlink(const char *Datoteka_stavka_ime) { return 호출결과(jkoros_syscall(38, (int)Datoteka_stavka_ime, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bajt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bajt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int komanda, ...) {
    int VALUE = 0;
    if (komanda == F_DUPFD || komanda == F_DUPFD_CLOEXEC || komanda == F_SETFD || komanda == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, komanda); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, komanda, VALUE, 0, 0));
}
