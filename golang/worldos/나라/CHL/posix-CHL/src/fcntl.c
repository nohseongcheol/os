#include <fcntl.h>
#include <sistema/syscall.h>

enum { SYS_abrir = 5, SYS_crear_archivo = 8, SYS_controlar_archivo = 55 };

int abrir(const char *ruta, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_abrir, (long)ruta, oflag, mode, 0, 0, 0));
}

int crear_archivo(const char *ruta, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_crear_archivo, (long)ruta, mode, 0, 0, 0, 0));
}

int controlar_archivo(int descriptor_del_archivo, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_controlar_archivo, descriptor_del_archivo, cmd, argument, 0, 0, 0));
}
