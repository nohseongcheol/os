/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <fcntl.h>
#include <النظام/syscall.h>

enum { SYS_فتح = 5, SYS_إنشاء_ملف = 8, SYS_التحكم_في_الملف = 55 };

int فتح(const char *المسار, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_فتح, (long)المسار, oflag, mode, 0, 0, 0));
}

int إنشاء_ملف(const char *المسار, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_إنشاء_ملف, (long)المسار, mode, 0, 0, 0, 0));
}

int التحكم_في_الملف(int واصف_الملف, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_التحكم_في_الملف, واصف_الملف, cmd, argument, 0, 0, 0));
}
