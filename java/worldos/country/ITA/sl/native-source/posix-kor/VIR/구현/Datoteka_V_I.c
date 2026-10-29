#include <파일규약.h>
#include "호출경계.h"

int številka_napake;
int 호출결과(int REZULTAT) {
    if (REZULTAT < 0) { številka_napake = -REZULTAT; return -1; }
    return REZULTAT;
}
int open(const char *Datoteka_vnos_ime, int odprto_Nastavitve, ...) {
    mode_t 허가 = 0;
    if (odprto_Nastavitve & O_CREAT) {
        __builtin_va_list Argumenti;
        __builtin_va_start(Argumenti, odprto_Nastavitve);
        허가 = __builtin_va_arg(Argumenti, mode_t);
        __builtin_va_end(Argumenti);
    }
    return 호출결과(jkoros_syscall(30, (int)Datoteka_vnos_ime, odprto_Nastavitve, 허가, 0, 0));
}
int creat(const char *Datoteka_vnos_ime, mode_t 허가) { return open(Datoteka_vnos_ime, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *podatki, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)podatki, bajt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *podatki, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)podatki, bajt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t odmik_VALUE, int pobuda_koren) {
    return 호출결과(jkoros_syscall(34, 파일서술자, odmik_VALUE, pobuda_koren, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *stanje_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)stanje_VALUE, 0, 0, 0)); }
int unlink(const char *Datoteka_vnos_ime) { return 호출결과(jkoros_syscall(38, (int)Datoteka_vnos_ime, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bajt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bajt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Ukaz, ...) {
    int VALUE = 0;
    if (Ukaz == F_DUPFD || Ukaz == F_DUPFD_CLOEXEC || Ukaz == F_SETFD || Ukaz == F_SETFL) {
        __builtin_va_list Argumenti;
        __builtin_va_start(Argumenti, Ukaz); VALUE = __builtin_va_arg(Argumenti, int); __builtin_va_end(Argumenti);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Ukaz, VALUE, 0, 0));
}
