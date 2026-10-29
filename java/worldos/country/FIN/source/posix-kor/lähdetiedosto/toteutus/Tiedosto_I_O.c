#include <파일규약.h>
#include "KUTSU_rajattu_alue.h"

int virhenumero;
int 호출결과(int TULOS) {
    if (TULOS < 0) { virhenumero = -TULOS; return -1; }
    return TULOS;
}
int open(const char *Tiedosto_merkintä_nimi, int avata_Asetukset, ...) {
    mode_t 허가 = 0;
    if (avata_Asetukset & O_CREAT) {
        __builtin_va_list argumentit;
        __builtin_va_start(argumentit, avata_Asetukset);
        허가 = __builtin_va_arg(argumentit, mode_t);
        __builtin_va_end(argumentit);
    }
    return 호출결과(jkoros_syscall(30, (int)Tiedosto_merkintä_nimi, avata_Asetukset, 허가, 0, 0));
}
int creat(const char *Tiedosto_merkintä_nimi, mode_t 허가) { return open(Tiedosto_merkintä_nimi, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t tavu_LASKE) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, tavu_LASKE, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t tavu_LASKE) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, tavu_LASKE, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t SIIRTYMÄ_ARVO, int aloite_juuri) {
    return 호출결과(jkoros_syscall(34, 파일서술자, SIIRTYMÄ_ARVO, aloite_juuri, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Tila_ARVO) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Tila_ARVO, 0, 0, 0)); }
int unlink(const char *Tiedosto_merkintä_nimi) { return 호출결과(jkoros_syscall(38, (int)Tiedosto_merkintä_nimi, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t tavu_LASKE) { return 호출결과(jkoros_syscall(39, 파일서술자, tavu_LASKE, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int komento, ...) {
    int ARVO = 0;
    if (komento == F_DUPFD || komento == F_DUPFD_CLOEXEC || komento == F_SETFD || komento == F_SETFL) {
        __builtin_va_list argumentit;
        __builtin_va_start(argumentit, komento); ARVO = __builtin_va_arg(argumentit, int); __builtin_va_end(argumentit);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, komento, ARVO, 0, 0));
}
