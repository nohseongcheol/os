#include <fcntl.h>
#include <sys/syscall.h>

enum { SYS_Otevřít = 5, SYS_creat = 8, SYS_fcntl = 55 };

int Otevřít(const char *cesta, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_Otevřít, (long)cesta, oflag, mode, 0, 0, 0));
}

int creat(const char *cesta, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_creat, (long)cesta, mode, 0, 0, 0, 0));
}

int fcntl(int deskriptor_souboru, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_fcntl, deskriptor_souboru, cmd, argument, 0, 0, 0));
}
