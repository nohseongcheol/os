#include <파일규약.h>
#include "호출경계.h"

int Номер_на_грешка;
int 호출결과(int РЕЗУЛТАТ) {
    if (РЕЗУЛТАТ < 0) { Номер_на_грешка = -РЕЗУЛТАТ; return -1; }
    return РЕЗУЛТАТ;
}
int open(const char *Файл_запис_препратка_към_клетка, int отварям_Настройки, ...) {
    mode_t 허가 = 0;
    if (отварям_Настройки & O_CREAT) {
        __builtin_va_list Параметри;
        __builtin_va_start(Параметри, отварям_Настройки);
        허가 = __builtin_va_arg(Параметри, mode_t);
        __builtin_va_end(Параметри);
    }
    return 호출결과(jkoros_syscall(30, (int)Файл_запис_препратка_към_клетка, отварям_Настройки, 허가, 0, 0));
}
int creat(const char *Файл_запис_препратка_към_клетка, mode_t 허가) { return open(Файл_запис_препратка_към_клетка, O_WRONLY | O_CREAT | O_TRUNC, 허가); }
ssize_t read(int 파일서술자, void *данни, size_t 바이트수) {
    return 호출결과(jkoros_syscall(31, 파일서술자, (int)данни, 바이트수, 0, 0));
}
ssize_t write(int 파일서술자, const void *данни, size_t 바이트수) {
    return 호출결과(jkoros_syscall(32, 파일서술자, (int)данни, 바이트수, 0, 0));
}
int close(int 파일서술자) { return 호출결과(jkoros_syscall(33, 파일서술자, 0, 0, 0, 0)); }
off_t lseek(int 파일서술자, off_t Изместване_стойност, int проект_корен) {
    return 호출결과(jkoros_syscall(34, 파일서술자, Изместване_стойност, проект_корен, 0, 0));
}
int dup(int 파일서술자) { return 호출결과(jkoros_syscall(35, 파일서술자, 0, 0, 0, 0)); }
int dup2(int 파일서술자, int 새서술자) { return 호출결과(jkoros_syscall(36, 파일서술자, 새서술자, 0, 0, 0)); }
int fstat(int 파일서술자, struct stat *Състояние_стойност) { return 호출결과(jkoros_syscall(37, 파일서술자, (int)Състояние_стойност, 0, 0, 0)); }
int unlink(const char *Файл_запис_препратка_към_клетка) { return 호출결과(jkoros_syscall(38, (int)Файл_запис_препратка_към_клетка, 0, 0, 0, 0)); }
int ftruncate(int 파일서술자, off_t 바이트수) { return 호출결과(jkoros_syscall(39, 파일서술자, 바이트수, 0, 0, 0)); }
int fsync(int 파일서술자) { return 호출결과(jkoros_syscall(47, 파일서술자, 0, 0, 0, 0)); }
int fcntl(int 파일서술자, int Команда, ...) {
    int стойност = 0;
    if (Команда == F_DUPFD || Команда == F_DUPFD_CLOEXEC || Команда == F_SETFD || Команда == F_SETFL) {
        __builtin_va_list Параметри;
        __builtin_va_start(Параметри, Команда); стойност = __builtin_va_arg(Параметри, int); __builtin_va_end(Параметри);
    }
    return 호출결과(jkoros_syscall(40, 파일서술자, Команда, стойност, 0, 0));
}
