#include <파일규약.h>
#include "호출경계.h"

int број_грешке;
int 호출결과(int ИСХОД) {
    if (ИСХОД < 0) { број_грешке = -ИСХОД; return -1; }
    return ИСХОД;
}
int open(const char *фајл_унос_име, int креирати_Поставке, ...) {
    mode_t 허가 = 0;
    if (креирати_Поставке & O_CREAT) {
        __builtin_va_list Аргументи;
        __builtin_va_start(Аргументи, креирати_Поставке);
        허가 = __builtin_va_arg(Аргументи, mode_t);
        __builtin_va_end(Аргументи);
    }
    return 호출결과(jkoros_syscall(30, (int)фајл_унос_име, креирати_Поставке, 허가, 0, 0));
}
int creat(const char *фајл_унос_име, mode_t 허가) { return open(фајл_унос_име, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *подаци, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)подаци, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *подаци, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)подаци, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Помак_вриједност, int пројектовати_корен) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Помак_вриједност, пројектовати_корен, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *стање_вриједност) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)стање_вриједност, 0, 0, 0)); }
int unlink(const char *фајл_унос_име) { return 호출결과(jkoros_syscall(38, (int)фајл_унос_име, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Наредба, ...) {
    int вриједност = 0;
    if (Наредба == F_DUPFD || Наредба == F_DUPFD_CLOEXEC || Наредба == F_SETFD || Наредба == F_SETFL) {
        __builtin_va_list Аргументи;
        __builtin_va_start(Аргументи, Наредба); вриједност = __builtin_va_arg(Аргументи, int); __builtin_va_end(Аргументи);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Наредба, вриједност, 0, 0));
}
