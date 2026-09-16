/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *cesta, struct stat *vyrovnávací_paměť_přenosu)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)cesta, (long)vyrovnávací_paměť_přenosu, 0, 0, 0, 0));
}

int lstat(const char *cesta, struct stat *vyrovnávací_paměť_přenosu)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)cesta, (long)vyrovnávací_paměť_přenosu, 0, 0, 0, 0));
}

int fstat(int deskriptor_souboru, struct stat *vyrovnávací_paměť_přenosu)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, deskriptor_souboru, (long)vyrovnávací_paměť_přenosu, 0, 0, 0, 0));
}

int uname(struct utsname *identita_systému)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)identita_systému, 0, 0, 0, 0, 0));
}
