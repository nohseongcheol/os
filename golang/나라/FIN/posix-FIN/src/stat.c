/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *polku, struct stat *siirtopuskuri)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)polku, (long)siirtopuskuri, 0, 0, 0, 0));
}

int lstat(const char *polku, struct stat *siirtopuskuri)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)polku, (long)siirtopuskuri, 0, 0, 0, 0));
}

int fstat(int tiedostokuvaaja, struct stat *siirtopuskuri)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, tiedostokuvaaja, (long)siirtopuskuri, 0, 0, 0, 0));
}

int uname(struct utsname *järjestelmätiedot)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)järjestelmätiedot, 0, 0, 0, 0, 0));
}
