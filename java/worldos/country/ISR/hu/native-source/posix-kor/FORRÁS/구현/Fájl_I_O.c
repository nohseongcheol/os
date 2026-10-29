#include <파일규약.h>
#include "hív_határ.h"

int hibaszám;
int 호출결과(int KR) {
    if (KR < 0) { hibaszám = -KR; return -1; }
    return KR;
}
int open(const char *Fájl_bejegyzés_név, int készít_Gépház, ...) {
    mode_t engedély_engedély = 0;
    if (készít_Gépház & O_CREAT) {
        __builtin_va_list Argumentumok;
        __builtin_va_start(Argumentumok, készít_Gépház);
        engedély_engedély = __builtin_va_arg(Argumentumok, mode_t);
        __builtin_va_end(Argumentumok);
    }
    return 호출결과(jkoros_syscall(30, (int)Fájl_bejegyzés_név, készít_Gépház, engedély_engedély, 0, 0));
}
int creat(const char *Fájl_bejegyzés_név, mode_t engedély_engedély) { return open(Fájl_bejegyzés_név, O_WRONLY | O_CREAT | O_TRUNC, engedély_engedély); }
ssize_t read(int 파일서술자, void *adat, size_t bájt_DARAB) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)adat, bájt_DARAB, 0, 0));
}
ssize_t write(int 파일서술자, const void *adat, size_t bájt_DARAB) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)adat, bájt_DARAB, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Ofszet_ÉRTÉK, int teendő_gyök) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Ofszet_ÉRTÉK, teendő_gyök, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Állapot_ÉRTÉK) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Állapot_ÉRTÉK, 0, 0, 0)); }
int unlink(const char *Fájl_bejegyzés_név) { return 호출결과(jkoros_syscall(38, (int)Fájl_bejegyzés_név, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bájt_DARAB) { return 호출결과(jkoros_syscall(39, 파일서술자, bájt_DARAB, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Parancs, ...) {
    int ÉRTÉK = 0;
    if (Parancs == F_DUPFD || Parancs == F_DUPFD_CLOEXEC || Parancs == F_SETFD || Parancs == F_SETFL) {
        __builtin_va_list Argumentumok;
        __builtin_va_start(Argumentumok, Parancs); ÉRTÉK = __builtin_va_arg(Argumentumok, int); __builtin_va_end(Argumentumok);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Parancs, ÉRTÉK, 0, 0));
}
