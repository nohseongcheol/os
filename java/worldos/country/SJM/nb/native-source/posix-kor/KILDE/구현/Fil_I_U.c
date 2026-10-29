#include <파일규약.h>
#include "Ring_grense.h"

int feilnummer;
int 호출결과(int KR) {
    if (KR < 0) { feilnummer = -KR; return -1; }
    return KR;
}
int open(const char *Fil_oppføring_navn, int åpen_Innstillinger, ...) {
    mode_t 허가 = 0;
    if (åpen_Innstillinger & O_CREAT) {
        __builtin_va_list Argumenter;
        __builtin_va_start(Argumenter, åpen_Innstillinger);
        허가 = __builtin_va_arg(Argumenter, mode_t);
        __builtin_va_end(Argumenter);
    }
    return 호출결과(jkoros_syscall(30, (int)Fil_oppføring_navn, åpen_Innstillinger, 허가, 0, 0));
}
int creat(const char *Fil_oppføring_navn, mode_t 허가) { return open(Fil_oppføring_navn, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t byte_ANTALL) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_ANTALL, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_ANTALL) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_ANTALL, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t FORSKYVNING_VERDI, int speile_rot) {
    return 호출결과(jkoros_syscall(34, 파일서술자, FORSKYVNING_VERDI, speile_rot, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_VERDI) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_VERDI, 0, 0, 0)); }
int unlink(const char *Fil_oppføring_navn) { return 호출결과(jkoros_syscall(38, (int)Fil_oppføring_navn, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_ANTALL) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_ANTALL, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Kommando, ...) {
    int VERDI = 0;
    if (Kommando == F_DUPFD || Kommando == F_DUPFD_CLOEXEC || Kommando == F_SETFD || Kommando == F_SETFL) {
        __builtin_va_list Argumenter;
        __builtin_va_start(Argumenter, Kommando); VERDI = __builtin_va_arg(Argumenter, int); __builtin_va_end(Argumenter);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Kommando, VERDI, 0, 0));
}
