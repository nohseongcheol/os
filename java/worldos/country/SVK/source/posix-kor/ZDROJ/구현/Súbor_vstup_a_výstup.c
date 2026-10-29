#include <파일규약.h>
#include "호출경계.h"

int chybové_číslo;
int 호출결과(int KR) {
    if (KR < 0) { chybové_číslo = -KR; return -1; }
    return KR;
}
int open(const char *Súbor_položka_názov, int otvoriť_Nastavenia, ...) {
    mode_t 허가 = 0;
    if (otvoriť_Nastavenia & O_CREAT) {
        __builtin_va_list Argumenty;
        __builtin_va_start(Argumenty, otvoriť_Nastavenia);
        허가 = __builtin_va_arg(Argumenty, mode_t);
        __builtin_va_end(Argumenty);
    }
    return 호출결과(jkoros_syscall(30, (int)Súbor_položka_názov, otvoriť_Nastavenia, 허가, 0, 0));
}
int creat(const char *Súbor_položka_názov, mode_t 허가) { return open(Súbor_položka_názov, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *údaje, size_t Byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)údaje, Byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *údaje, size_t Byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)údaje, Byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Posun_VALUE, int akcia_koreň) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Posun_VALUE, akcia_koreň, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Stav_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Stav_VALUE, 0, 0, 0)); }
int unlink(const char *Súbor_položka_názov) { return 호출결과(jkoros_syscall(38, (int)Súbor_položka_názov, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t Byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, Byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Príkaz, ...) {
    int VALUE = 0;
    if (Príkaz == F_DUPFD || Príkaz == F_DUPFD_CLOEXEC || Príkaz == F_SETFD || Príkaz == F_SETFL) {
        __builtin_va_list Argumenty;
        __builtin_va_start(Argumenty, Príkaz); VALUE = __builtin_va_arg(Argumenty, int); __builtin_va_end(Argumenty);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Príkaz, VALUE, 0, 0));
}
