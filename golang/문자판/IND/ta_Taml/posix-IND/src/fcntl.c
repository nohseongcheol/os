/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <fcntl.h>
#include <அமைப்பு/syscall.h>

enum { SYS_திற = 5, SYS_கோப்பை_உருவாக்கு = 8, SYS_கோப்பைக்_கட்டுப்படுத்து = 55 };

int திற(const char *பாதை, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_திற, (long)பாதை, oflag, mode, 0, 0, 0));
}

int கோப்பை_உருவாக்கு(const char *பாதை, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_கோப்பை_உருவாக்கு, (long)பாதை, mode, 0, 0, 0, 0));
}

int கோப்பைக்_கட்டுப்படுத்து(int கோப்பு_விவரிப்பி, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_கோப்பைக்_கட்டுப்படுத்து, கோப்பு_விவரிப்பி, cmd, argument, 0, 0, 0));
}
