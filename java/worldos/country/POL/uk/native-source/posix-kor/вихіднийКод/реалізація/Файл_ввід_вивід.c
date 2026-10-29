#include <파일규약.h>
#include "호출경계.h"

int номер_помилки;
int 호출결과(int результат) {
    if (результат < 0) { номер_помилки = -результат; return -1; }
    return результат;
}
int open(const char *Файл_запис_ім_я, int відкрито_Настройки, ...) {
    mode_t 허가 = 0;
    if (відкрито_Настройки & O_CREAT) {
        __builtin_va_list аргументи;
        __builtin_va_start(аргументи, відкрито_Настройки);
        허가 = __builtin_va_arg(аргументи, mode_t);
        __builtin_va_end(аргументи);
    }
    return 호출결과(jkoros_syscall(30, (int)Файл_запис_ім_я, відкрито_Настройки, 허가, 0, 0));
}
int creat(const char *Файл_запис_ім_я, mode_t 허가) { return open(Файл_запис_ім_я, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *дані, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)дані, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *дані, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)дані, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Зміщена_копія_значення, int Дії_корінь) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Зміщена_копія_значення, Дії_корінь, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Стан_значення) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Стан_значення, 0, 0, 0)); }
int unlink(const char *Файл_запис_ім_я) { return 호출결과(jkoros_syscall(38, (int)Файл_запис_ім_я, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int команда, ...) {
    int значення = 0;
    if (команда == F_DUPFD || команда == F_DUPFD_CLOEXEC || команда == F_SETFD || команда == F_SETFL) {
        __builtin_va_list аргументи;
        __builtin_va_start(аргументи, команда); значення = __builtin_va_arg(аргументи, int); __builtin_va_end(аргументи);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, команда, значення, 0, 0));
}
