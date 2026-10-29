#include <파일규약.h>
#include "ring_gräns.h"

int felnummer;
int 호출결과(int RESULTAT) {
    if (RESULTAT < 0) { felnummer = -RESULTAT; return -1; }
    return RESULTAT;
}
int open(const char *fil_post_namn, int skapa_Inställningar, ...) {
    mode_t beviljande_behörighet = 0;
    if (skapa_Inställningar & O_CREAT) {
        __builtin_va_list argument;
        __builtin_va_start(argument, skapa_Inställningar);
        beviljande_behörighet = __builtin_va_arg(argument, mode_t);
        __builtin_va_end(argument);
    }
    return 호출결과(jkoros_syscall(30, (int)fil_post_namn, skapa_Inställningar, beviljande_behörighet, 0, 0));
}
int creat(const char *fil_post_namn, mode_t beviljande_behörighet) { return open(fil_post_namn, O_WRONLY | O_CREAT | O_TRUNC, beviljande_behörighet); }
ssize_t read(int 파일서술자, void *data, size_t byte_ANTAL) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_ANTAL, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_ANTAL) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_ANTAL, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t FÖRSKJUTNING_värde, int åtgärd_rot) {
    return 호출결과(jkoros_syscall(34, 파일서술자, FÖRSKJUTNING_värde, åtgärd_rot, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_värde) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_värde, 0, 0, 0)); }
int unlink(const char *fil_post_namn) { return 호출결과(jkoros_syscall(38, (int)fil_post_namn, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_ANTAL) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_ANTAL, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int kommando, ...) {
    int värde = 0;
    if (kommando == F_DUPFD || kommando == F_DUPFD_CLOEXEC || kommando == F_SETFD || kommando == F_SETFL) {
        __builtin_va_list argument;
        __builtin_va_start(argument, kommando); värde = __builtin_va_arg(argument, int); __builtin_va_end(argument);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, kommando, värde, 0, 0));
}
