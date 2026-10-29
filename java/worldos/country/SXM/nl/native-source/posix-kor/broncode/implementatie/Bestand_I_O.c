#include <파일규약.h>
#include "Bellen_grens.h"

int foutnummer;
int 호출결과(int resultaat) {
    if (resultaat < 0) { foutnummer = -resultaat; return -1; }
    return resultaat;
}
int open(const char *Bestand_invoer_naam, int open_Instellingen, ...) {
    mode_t toekenning_machtiging = 0;
    if (open_Instellingen & O_CREAT) {
        __builtin_va_list argumenten;
        __builtin_va_start(argumenten, open_Instellingen);
        toekenning_machtiging = __builtin_va_arg(argumenten, mode_t);
        __builtin_va_end(argumenten);
    }
    return 호출결과(jkoros_syscall(30, (int)Bestand_invoer_naam, open_Instellingen, toekenning_machtiging, 0, 0));
}
int creat(const char *Bestand_invoer_naam, mode_t toekenning_machtiging) { return open(Bestand_invoer_naam, O_WRONLY | O_CREAT | O_TRUNC, toekenning_machtiging); }
ssize_t read(int 파일서술자, void *gegevens, size_t byte_AANTAL) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)gegevens, byte_AANTAL, 0, 0));
}
ssize_t write(int 파일서술자, const void *gegevens, size_t byte_AANTAL) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)gegevens, byte_AANTAL, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t VERSCHUIVING_WAARDE, int Taken_wortel) {
    return 호출결과(jkoros_syscall(34, 파일서술자, VERSCHUIVING_WAARDE, Taken_wortel, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Status_WAARDE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Status_WAARDE, 0, 0, 0)); }
int unlink(const char *Bestand_invoer_naam) { return 호출결과(jkoros_syscall(38, (int)Bestand_invoer_naam, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_AANTAL) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_AANTAL, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int opdracht, ...) {
    int WAARDE = 0;
    if (opdracht == F_DUPFD || opdracht == F_DUPFD_CLOEXEC || opdracht == F_SETFD || opdracht == F_SETFL) {
        __builtin_va_list argumenten;
        __builtin_va_start(argumenten, opdracht); WAARDE = __builtin_va_arg(argumenten, int); __builtin_va_end(argumenten);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, opdracht, WAARDE, 0, 0));
}
