/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <fcntl.h>
#include <système/syscall.h>

enum { SYS_ouvrir = 5, SYS_créer_un_fichier = 8, SYS_contrôler_le_fichier = 55 };

int ouvrir(const char *chemin, int oflag, ...)
{
    mode_t mode = 0;
    if ((oflag & O_CREAT) != 0) {
        __builtin_va_list args;
        __builtin_va_start(args, oflag);
        mode = __builtin_va_arg(args, mode_t);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_ouvrir, (long)chemin, oflag, mode, 0, 0, 0));
}

int créer_un_fichier(const char *chemin, mode_t mode)
{
    return (int)__syscall_result(
        __syscall6(SYS_créer_un_fichier, (long)chemin, mode, 0, 0, 0, 0));
}

int contrôler_le_fichier(int descripteur_de_fichier, int cmd, ...)
{
    long argument = 0;
    if (cmd == F_DUPFD || cmd == F_SETFD || cmd == F_SETFL) {
        __builtin_va_list args;
        __builtin_va_start(args, cmd);
        argument = __builtin_va_arg(args, long);
        __builtin_va_end(args);
    }
    return (int)__syscall_result(
        __syscall6(SYS_contrôler_le_fichier, descripteur_de_fichier, cmd, argument, 0, 0, 0));
}
