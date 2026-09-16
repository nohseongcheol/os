/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <fcntl.h>
#include <sys/syscall.h>

enum { SYS_Mở = 5, SYS_creat = 8, SYS_fcntl = 55 };

int Mở(const char *đường_dẫn, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_Mở, (long)đường_dẫn, oflag, mode, 0, 0, 0));
}

int creat(const char *đường_dẫn, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_creat, (long)đường_dẫn, mode, 0, 0, 0, 0));
}

int fcntl(int bộ_mô_tả_tệp, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_fcntl, bộ_mô_tả_tệp, cmd, argument, 0, 0, 0));
}
