#include <файл_ABI.h>
#include "вызов_граница.h"

int номер_ошибки;
int 호출결과(int результат) {
    if (результат < 0) { номер_ошибки = -результат; return -1; }
    return результат;
}
int open(const char *файл_ввод_имя, int открыть_Настройки, ...) {
    mode_t предоставление_разрешения_Полномочие = 0;
    if (открыть_Настройки & O_CREAT) {
        __builtin_va_list аргументы;
        __builtin_va_start(аргументы, открыть_Настройки);
        предоставление_разрешения_Полномочие = __builtin_va_arg(аргументы, mode_t);
        __builtin_va_end(аргументы);
    }
    return 호출결과(jkoros_syscall(30, (int)файл_ввод_имя, открыть_Настройки, предоставление_разрешения_Полномочие, 0, 0));
}
int creat(const char *файл_ввод_имя, mode_t предоставление_разрешения_Полномочие) { return open(файл_ввод_имя, O_WRONLY | O_CREAT | O_TRUNC, предоставление_разрешения_Полномочие); }
ssize_t read(int файл_дескриптор, void *данные, size_t байт_СЧЁТ) {
    return 호출결과(jkoros_syscall(31, файл_дескриптор, (int)данные, байт_СЧЁТ, 0, 0));
}
ssize_t write(int файл_дескриптор, const void *данные, size_t байт_СЧЁТ) {
    return 호출결과(jkoros_syscall(32, файл_дескриптор, (int)данные, байт_СЧЁТ, 0, 0));
}
int close(int файл_дескриптор) { return 호출결과(jkoros_syscall(33, файл_дескриптор, 0, 0, 0, 0)); }
off_t lseek(int файл_дескриптор, off_t СМЕЩ_ЗНАЧЕН, int задача_корень) {
    return 호출결과(jkoros_syscall(34, файл_дескриптор, СМЕЩ_ЗНАЧЕН, задача_корень, 0, 0));
}
int dup(int файл_дескриптор) { return 호출결과(jkoros_syscall(35, файл_дескриптор, 0, 0, 0, 0)); }
int dup2(int файл_дескриптор, int 새서술자) { return 호출결과(jkoros_syscall(36, файл_дескриптор, 새서술자, 0, 0, 0)); }
int fstat(int файл_дескриптор, struct stat *Состояние_ЗНАЧЕН) { return 호출결과(jkoros_syscall(37, файл_дескриптор, (int)Состояние_ЗНАЧЕН, 0, 0, 0)); }
int unlink(const char *файл_ввод_имя) { return 호출결과(jkoros_syscall(38, (int)файл_ввод_имя, 0, 0, 0, 0)); }
int ftruncate(int файл_дескриптор, off_t байт_СЧЁТ) { return 호출결과(jkoros_syscall(39, файл_дескриптор, байт_СЧЁТ, 0, 0, 0)); }
int fsync(int файл_дескриптор) { return 호출결과(jkoros_syscall(47, файл_дескриптор, 0, 0, 0, 0)); }
int fcntl(int файл_дескриптор, int команда, ...) {
    int ЗНАЧЕН = 0;
    if (команда == F_DUPFD || команда == F_DUPFD_CLOEXEC || команда == F_SETFD || команда == F_SETFL) {
        __builtin_va_list аргументы;
        __builtin_va_start(аргументы, команда); ЗНАЧЕН = __builtin_va_arg(аргументы, int); __builtin_va_end(аргументы);
    }
    return 호출결과(jkoros_syscall(40, файл_дескриптор, команда, ЗНАЧЕН, 0, 0));
}
