#include <Soubor_ABI.h>
#include "VOLAT_mez.h"

int číslo_chyby;
int 호출결과(int VÝSLEDEK) {
    if (VÝSLEDEK < 0) { číslo_chyby = -VÝSLEDEK; return -1; }
    return VÝSLEDEK;
}
int open(const char *Soubor_položka_název, int otevřít_Nastavení, ...) {
    mode_t oprávnění_oprávnění = 0;
    if (otevřít_Nastavení & O_CREAT) {
        __builtin_va_list argumenty;
        __builtin_va_start(argumenty, otevřít_Nastavení);
        oprávnění_oprávnění = __builtin_va_arg(argumenty, mode_t);
        __builtin_va_end(argumenty);
    }
    return 호출결과(jkoros_syscall(30, (int)Soubor_položka_název, otevřít_Nastavení, oprávnění_oprávnění, 0, 0));
}
int creat(const char *Soubor_položka_název, mode_t oprávnění_oprávnění) { return open(Soubor_položka_název, O_WRONLY | O_CREAT | O_TRUNC, oprávnění_oprávnění); }
ssize_t read(int Soubor_popisovač, void *data, size_t bajt_POČET) {
    return 호출결과(jkoros_syscall(31, Soubor_popisovač, (int)data, bajt_POČET, 0, 0));
}
ssize_t write(int Soubor_popisovač, const void *data, size_t bajt_POČET) {
    return 호출결과(jkoros_syscall(32, Soubor_popisovač, (int)data, bajt_POČET, 0, 0));
}
int close(int Soubor_popisovač) { return 호출결과(jkoros_syscall(33, Soubor_popisovač, 0, 0, 0, 0)); }
off_t lseek(int Soubor_popisovač, off_t POSUN_HODNOTA, int akce_kořen) {
    return 호출결과(jkoros_syscall(34, Soubor_popisovač, POSUN_HODNOTA, akce_kořen, 0, 0));
}
int dup(int Soubor_popisovač) { return 호출결과(jkoros_syscall(35, Soubor_popisovač, 0, 0, 0, 0)); }
int dup2(int Soubor_popisovač, int 새서술자) { return 호출결과(jkoros_syscall(36, Soubor_popisovač, 새서술자, 0, 0, 0)); }
int fstat(int Soubor_popisovač, struct stat *Stav_HODNOTA) { return 호출결과(jkoros_syscall(37, Soubor_popisovač, (int)Stav_HODNOTA, 0, 0, 0)); }
int unlink(const char *Soubor_položka_název) { return 호출결과(jkoros_syscall(38, (int)Soubor_položka_název, 0, 0, 0, 0)); }
int ftruncate(int Soubor_popisovač, off_t bajt_POČET) { return 호출결과(jkoros_syscall(39, Soubor_popisovač, bajt_POČET, 0, 0, 0)); }
int fsync(int Soubor_popisovač) { return 호출결과(jkoros_syscall(47, Soubor_popisovač, 0, 0, 0, 0)); }
int fcntl(int Soubor_popisovač, int příkaz, ...) {
    int HODNOTA = 0;
    if (příkaz == F_DUPFD || příkaz == F_DUPFD_CLOEXEC || příkaz == F_SETFD || příkaz == F_SETFL) {
        __builtin_va_list argumenty;
        __builtin_va_start(argumenty, příkaz); HODNOTA = __builtin_va_arg(argumenty, int); __builtin_va_end(argumenty);
    }
    return 호출결과(jkoros_syscall(40, Soubor_popisovač, příkaz, HODNOTA, 0, 0));
}
