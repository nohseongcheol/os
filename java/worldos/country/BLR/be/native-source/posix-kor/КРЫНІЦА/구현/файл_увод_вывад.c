#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int 결과) {
    if (결과 < 0) { 오류번호 = -결과; return -1; }
    return 결과;
}
int open(const char *файл_увядзенне_імя, int адкрыць_Налады, ...) {
    mode_t 허가 = 0;
    if (адкрыць_Налады & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, адкрыць_Налады);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)файл_увядзенне_імя, адкрыць_Налады, 허가, 0, 0));
}
int creat(const char *файл_увядзенне_імя, mode_t 허가) { return open(файл_увядзенне_імя, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *дадзеныя, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)дадзеныя, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *дадзеныя, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)дадзеныя, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Зрух_значэнне, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Зрух_значэнне, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *стан_значэнне) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)стан_значэнне, 0, 0, 0)); }
int unlink(const char *файл_увядзенне_імя) { return 호출결과(jkoros_syscall(38, (int)файл_увядзенне_імя, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Загад, ...) {
    int значэнне = 0;
    if (Загад == F_DUPFD || Загад == F_DUPFD_CLOEXEC || Загад == F_SETFD || Загад == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Загад); значэнне = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Загад, значэнне, 0, 0));
}
