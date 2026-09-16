#include <fcntl.h>
#include <प्रणाली/syscall.h>

enum { SYS_खोलना = 5, SYS_संचिका_बनाना = 8, SYS_संचिका_नियंत्रित_करना = 55 };

int खोलना(const char *पथ, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_खोलना, (long)पथ, oflag, mode, 0, 0, 0));
}

int संचिका_बनाना(const char *पथ, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_संचिका_बनाना, (long)पथ, mode, 0, 0, 0, 0));
}

int संचिका_नियंत्रित_करना(int संचिका_विवरणक, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_संचिका_नियंत्रित_करना, संचिका_विवरणक, cmd, argument, 0, 0, 0));
}
