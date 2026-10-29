#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int tomhas) {
    if (tomhas < 0) { 오류번호 = -tomhas; return -1; }
    return tomhas;
}
int open(const char *comhad_iontráil_ainm, int oscail_Socruithe, ...) {
    mode_t 허가 = 0;
    if (oscail_Socruithe & O_CREAT) {
        __builtin_va_list Argóintí;
        __builtin_va_start(Argóintí, oscail_Socruithe);
        허가 = __builtin_va_arg(Argóintí, mode_t);
        __builtin_va_end(Argóintí);
    }
    return 호출결과(jkoros_syscall(30, (int)comhad_iontráil_ainm, oscail_Socruithe, 허가, 0, 0));
}
int creat(const char *comhad_iontráil_ainm, mode_t 허가) { return open(comhad_iontráil_ainm, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *sonraí, size_t beart_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)sonraí, beart_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *sonraí, size_t beart_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)sonraí, beart_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int teilgean_fréamh) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, teilgean_fréamh, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *staid_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)staid_VALUE, 0, 0, 0)); }
int unlink(const char *comhad_iontráil_ainm) { return 호출결과(jkoros_syscall(38, (int)comhad_iontráil_ainm, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t beart_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, beart_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Ordú, ...) {
    int VALUE = 0;
    if (Ordú == F_DUPFD || Ordú == F_DUPFD_CLOEXEC || Ordú == F_SETFD || Ordú == F_SETFL) {
        __builtin_va_list Argóintí;
        __builtin_va_start(Argóintí, Ordú); VALUE = __builtin_va_arg(Argóintí, int); __builtin_va_end(Argóintí);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Ordú, VALUE, 0, 0));
}
