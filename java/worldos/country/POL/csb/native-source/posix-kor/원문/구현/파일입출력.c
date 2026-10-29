#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int 결과) {
    if (결과 < 0) { 오류번호 = -결과; return -1; }
    return 결과;
}
int open(const char *파일이름, int 열기설정, ...) {
    mode_t 허가 = 0;
    if (열기설정 & O_CREAT) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, 열기설정);
        허가 = __builtin_va_arg(인수, mode_t);
        __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(30, (int)파일이름, 열기설정, 허가, 0, 0));
}
int creat(const char *파일이름, mode_t 허가) { return open(파일이름, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *자료, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)자료, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *자료, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)자료, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t 변위, int 기준) {
    return 호출결과(jkoros_syscall(34, 파일서술자, 변위, 기준, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *상태) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)상태, 0, 0, 0)); }
int unlink(const char *파일이름) { return 호출결과(jkoros_syscall(38, (int)파일이름, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Pòlét, ...) {
    int 값 = 0;
    if (Pòlét == F_DUPFD || Pòlét == F_DUPFD_CLOEXEC || Pòlét == F_SETFD || Pòlét == F_SETFL) {
        __builtin_va_list 인수;
        __builtin_va_start(인수, Pòlét); 값 = __builtin_va_arg(인수, int); __builtin_va_end(인수);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Pòlét, 값, 0, 0));
}
