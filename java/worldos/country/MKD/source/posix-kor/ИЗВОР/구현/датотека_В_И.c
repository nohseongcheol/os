#include <파일규약.h>
#include "호출경계.h"

int 오류번호;
int 호출결과(int мерка) {
    if (мерка < 0) { 오류번호 = -мерка; return -1; }
    return мерка;
}
int open(const char *датотека_внес_име, int отвори_Параметри, ...) {
    mode_t 허가 = 0;
    if (отвори_Параметри & O_CREAT) {
        __builtin_va_list Аргументи;
        __builtin_va_start(Аргументи, отвори_Параметри);
        허가 = __builtin_va_arg(Аргументи, mode_t);
        __builtin_va_end(Аргументи);
    }
    return 호출결과(jkoros_syscall(30, (int)датотека_внес_име, отвори_Параметри, 허가, 0, 0));
}
int creat(const char *датотека_внес_име, mode_t 허가) { return open(датотека_внес_име, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *податоци, size_t бајт_COUNT) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)податоци, бајт_COUNT, 0, 0));
}
ssize_t write(int 파일서술자, const void *податоци, size_t бајт_COUNT) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)податоци, бајт_COUNT, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t OFFSET_VALUE, int Project_корен) {
    return 호출결과(jkoros_syscall(34, 파일서술자, OFFSET_VALUE, Project_корен, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *статус_VALUE) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)статус_VALUE, 0, 0, 0)); }
int unlink(const char *датотека_внес_име) { return 호출결과(jkoros_syscall(38, (int)датотека_внес_име, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t бајт_COUNT) { return 호출결과(jkoros_syscall(39, 파일서술자, бајт_COUNT, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Команда, ...) {
    int VALUE = 0;
    if (Команда == F_DUPFD || Команда == F_DUPFD_CLOEXEC || Команда == F_SETFD || Команда == F_SETFL) {
        __builtin_va_list Аргументи;
        __builtin_va_start(Аргументи, Команда); VALUE = __builtin_va_arg(Аргументи, int); __builtin_va_end(Аргументи);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Команда, VALUE, 0, 0));
}
