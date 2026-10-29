#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int maatreël) {
    if (maatreël < 0) { 오류번호 = -maatreël; return -1; }
    return maatreël;
}
int open(const char *lêer_inskrywing_naam, int skep_Instellings, ...) {
    mode_t 허가 = 0;
    if (skep_Instellings & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, skep_Instellings);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)lêer_inskrywing_naam, skep_Instellings, 허가, 0, 0));
}
int creat(const char *lêer_inskrywing_naam, mode_t 허가) { return open(lêer_inskrywing_naam, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *data, size_t greep_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)data, greep_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *data, size_t greep_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)data, greep_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_wortel) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_wortel, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *stand_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)stand_VALUE, 0, 0, 0)); }
int unlink(const char *lêer_inskrywing_naam) { return 호출결과(jkoros_syscall(38, (int)lêer_inskrywing_naam, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t greep_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, greep_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Opdrag, ...) {
    int VALUE = 0;
    if (Opdrag == F_DUPFD || Opdrag == F_DUPFD_CLOEXEC || Opdrag == F_SETFD || Opdrag == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Opdrag); VALUE = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Opdrag, VALUE, 0, 0));
}
