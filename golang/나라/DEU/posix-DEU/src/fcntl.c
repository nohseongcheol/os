/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <fcntl.h>
#include <System/syscall.h>

enum { SYS_öffnen = 5, SYS_Datei_anlegen = 8, SYS_Dateizugriff_steuern = 55 };

int öffnen(const char *Pfad, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_öffnen, (long)Pfad, oflag, mode, 0, 0, 0));
}

int Datei_anlegen(const char *Pfad, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_Datei_anlegen, (long)Pfad, mode, 0, 0, 0, 0));
}

int Dateizugriff_steuern(int Dateideskriptor, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_Dateizugriff_steuern, Dateideskriptor, cmd, argument, 0, 0, 0));
}
