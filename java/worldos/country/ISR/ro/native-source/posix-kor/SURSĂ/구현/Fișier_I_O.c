#include <파일규약.h>
#include "호출경계.h"

int număr_de_eroare;
int 호출결과(int KR) {
    if (KR < 0) { număr_de_eroare = -KR; return -1; }
    return KR;
}
int open(const char *Fișier_intrare_nume, int crea_Setări, ...) {
    mode_t 허가 = 0;
    if (crea_Setări & O_CREAT) {
        __builtin_va_list Argumente;
        __builtin_va_start(Argumente, crea_Setări);
        허가 = __builtin_va_arg(Argumente, mode_t);
        __builtin_va_end(Argumente);
    }
    return 호출결과(jkoros_syscall(30, (int)Fișier_intrare_nume, crea_Setări, 허가, 0, 0));
}
int creat(const char *Fișier_intrare_nume, mode_t 허가) { return open(Fișier_intrare_nume, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *date, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)date, byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *date, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)date, byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_rădăcină) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_rădăcină, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Stare_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Stare_VALUE, 0, 0, 0)); }
int unlink(const char *Fișier_intrare_nume) { return 호출결과(jkoros_syscall(38, (int)Fișier_intrare_nume, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Comandă, ...) {
    int VALUE = 0;
    if (Comandă == F_DUPFD || Comandă == F_DUPFD_CLOEXEC || Comandă == F_SETFD || Comandă == F_SETFL) {
        __builtin_va_list Argumente;
        __builtin_va_start(Argumente, Comandă); VALUE = __builtin_va_arg(Argumente, int); __builtin_va_end(Argumente);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Comandă, VALUE, 0, 0));
}
