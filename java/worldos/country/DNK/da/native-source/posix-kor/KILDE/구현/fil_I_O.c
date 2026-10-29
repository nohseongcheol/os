#include <파일규약.h>
#include "KALD_grænse.h"

int fejlnummer;
int 호출결과(int KR) {
    if (KR < 0) { fejlnummer = -KR; return -1; }
    return KR;
}
int open(const char *fil_post_navn, int åben_Indstillinger, ...) {
    mode_t 허가 = 0;
    if (åben_Indstillinger & O_CREAT) {
        __builtin_va_list Argumenter;
        __builtin_va_start(Argumenter, åben_Indstillinger);
        허가 = __builtin_va_arg(Argumenter, mode_t);
        __builtin_va_end(Argumenter);
    }
    return 호출결과(jkoros_syscall(30, (int)fil_post_navn, åben_Indstillinger, 허가, 0, 0));
}
int creat(const char *fil_post_navn, mode_t 허가) { return open(fil_post_navn, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t byte_TÆL) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, byte_TÆL, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t byte_TÆL) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, byte_TÆL, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t FORSKYDNING_VÆRDI, int To_do_rod) {
    return 호출결과(jkoros_syscall(34, 파일서술자, FORSKYDNING_VÆRDI, To_do_rod, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_VÆRDI) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_VÆRDI, 0, 0, 0)); }
int unlink(const char *fil_post_navn) { return 호출결과(jkoros_syscall(38, (int)fil_post_navn, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t byte_TÆL) { return 호출결과(jkoros_syscall(39, 파일서술자, byte_TÆL, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Kommando, ...) {
    int VÆRDI = 0;
    if (Kommando == F_DUPFD || Kommando == F_DUPFD_CLOEXEC || Kommando == F_SETFD || Kommando == F_SETFL) {
        __builtin_va_list Argumenter;
        __builtin_va_start(Argumenter, Kommando); VÆRDI = __builtin_va_arg(Argumenter, int); __builtin_va_end(Argumenter);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Kommando, VÆRDI, 0, 0));
}
