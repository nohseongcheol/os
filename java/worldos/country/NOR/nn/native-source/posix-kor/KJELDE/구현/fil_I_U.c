#include <파일규약.h>
#include "호출경계.h"

int feilnummer;
int 호출결과(int forretningsmål) {
    if (forretningsmål < 0) { feilnummer = -forretningsmål; return -1; }
    return forretningsmål;
}
int open(const char *fil_oppføring_namn, int opne_Innstillingar, ...) {
    mode_t 허가 = 0;
    if (opne_Innstillingar & O_CREAT) {
        __builtin_va_list Argument;
        __builtin_va_start(Argument, opne_Innstillingar);
        허가 = __builtin_va_arg(Argument, mode_t);
        __builtin_va_end(Argument);
    }
    return 호출결과(jkoros_syscall(30, (int)fil_oppføring_namn, opne_Innstillingar, 허가, 0, 0));
}
int creat(const char *fil_oppføring_namn, mode_t 허가) { return open(fil_oppføring_namn, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int spegle_rot) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, spegle_rot, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_VALUE, 0, 0, 0)); }
int unlink(const char *fil_oppføring_namn) { return 호출결과(jkoros_syscall(38, (int)fil_oppføring_namn, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Kommando, ...) {
    int VALUE = 0;
    if (Kommando == F_DUPFD || Kommando == F_DUPFD_CLOEXEC || Kommando == F_SETFD || Kommando == F_SETFL) {
        __builtin_va_list Argument;
        __builtin_va_start(Argument, Kommando); VALUE = __builtin_va_arg(Argument, int); __builtin_va_end(Argument);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Kommando, VALUE, 0, 0));
}
