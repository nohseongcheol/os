#include <파일규약.h>
#include "호출경계.h"

int tõrke_number;
int 호출결과(int TULEMUS) {
    if (TULEMUS < 0) { tõrke_number = -TULEMUS; return -1; }
    return TULEMUS;
}
int open(const char *Fail_kirje_nimetus, int avama_Sätted, ...) {
    mode_t 허가 = 0;
    if (avama_Sätted & O_CREAT) {
        __builtin_va_list Argumendid;
        __builtin_va_start(Argumendid, avama_Sätted);
        허가 = __builtin_va_arg(Argumendid, mode_t);
        __builtin_va_end(Argumendid);
    }
    return 호출결과(jkoros_syscall(30, (int)Fail_kirje_nimetus, avama_Sätted, 허가, 0, 0));
}
int creat(const char *Fail_kirje_nimetus, mode_t 허가) { return open(Fail_kirje_nimetus, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *andmed, size_t bait_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)andmed, bait_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *andmed, size_t bait_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)andmed, bait_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t nihe_VALUE, int Project_juur) {
    return 호출결과(jkoros_syscall(34, 파일서술자, nihe_VALUE, Project_juur, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Olek_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Olek_VALUE, 0, 0, 0)); }
int unlink(const char *Fail_kirje_nimetus) { return 호출결과(jkoros_syscall(38, (int)Fail_kirje_nimetus, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bait_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bait_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Käsk, ...) {
    int VALUE = 0;
    if (Käsk == F_DUPFD || Käsk == F_DUPFD_CLOEXEC || Käsk == F_SETFD || Käsk == F_SETFL) {
        __builtin_va_list Argumendid;
        __builtin_va_start(Argumendid, Käsk); VALUE = __builtin_va_arg(Argumendid, int); __builtin_va_end(Argumendid);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Käsk, VALUE, 0, 0));
}
