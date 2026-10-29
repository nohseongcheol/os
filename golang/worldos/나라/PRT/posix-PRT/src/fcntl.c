#include <fcntl.h>
#include <sistema/syscall.h>

enum { SYS_abrir = 5, SYS_criar_ficheiro = 8, SYS_controlar_ficheiro = 55 };

int abrir(const char *caminho, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_abrir, (long)caminho, oflag, mode, 0, 0, 0));
}

int criar_ficheiro(const char *caminho, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_criar_ficheiro, (long)caminho, mode, 0, 0, 0, 0));
}

int controlar_ficheiro(int descritor_do_ficheiro, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_controlar_ficheiro, descritor_do_ficheiro, cmd, argument, 0, 0, 0));
}
