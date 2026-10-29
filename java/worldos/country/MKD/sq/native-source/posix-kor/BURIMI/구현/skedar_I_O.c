#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int llogaritje) {
    if (llogaritje < 0) { 오류번호 = -llogaritje; return -1; }
    return llogaritje;
}
int open(const char *skedar_futje_emër, int hap_cilësimet, ...) {
    mode_t 허가 = 0;
    if (hap_cilësimet & O_CREAT) {
        __builtin_va_list Argumente;
        __builtin_va_start(Argumente, hap_cilësimet);
        허가 = __builtin_va_arg(Argumente, mode_t);
        __builtin_va_end(Argumente);
    }
    return 호출결과(jkoros_syscall(30, (int)skedar_futje_emër, hap_cilësimet, 허가, 0, 0));
}
int creat(const char *skedar_futje_emër, mode_t 허가) { return open(skedar_futje_emër, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *të_dhëna, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)të_dhëna, bajt_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *të_dhëna, size_t bajt_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)të_dhëna, bajt_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_rrënjë) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_rrënjë, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *status_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)status_VALUE, 0, 0, 0)); }
int unlink(const char *skedar_futje_emër) { return 호출결과(jkoros_syscall(38, (int)skedar_futje_emër, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t bajt_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, bajt_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Komanda, ...) {
    int VALUE = 0;
    if (Komanda == F_DUPFD || Komanda == F_DUPFD_CLOEXEC || Komanda == F_SETFD || Komanda == F_SETFL) {
        __builtin_va_list Argumente;
        __builtin_va_start(Argumente, Komanda); VALUE = __builtin_va_arg(Argumente, int); __builtin_va_end(Argumente);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Komanda, VALUE, 0, 0));
}
