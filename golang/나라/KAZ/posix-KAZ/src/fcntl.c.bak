#include <fcntl.h>
#include <система/syscall.h>

enum { SYS_открыть = 5, SYS_создать_файл = 8, SYS_управлять_файлом = 55 };

int открыть(const char *путь, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_открыть, (long)путь, oflag, mode, 0, 0, 0));
}

int создать_файл(const char *путь, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_создать_файл, (long)путь, mode, 0, 0, 0, 0));
}

int управлять_файлом(int дескриптор_файла, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_управлять_файлом, дескриптор_файла, cmd, argument, 0, 0, 0));
}
