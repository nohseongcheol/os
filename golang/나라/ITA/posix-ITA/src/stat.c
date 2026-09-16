/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *percorso, struct stat *memoria_intermedia_di_trasferimento)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)percorso, (long)memoria_intermedia_di_trasferimento, 0, 0, 0, 0));
}

int lstat(const char *percorso, struct stat *memoria_intermedia_di_trasferimento)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)percorso, (long)memoria_intermedia_di_trasferimento, 0, 0, 0, 0));
}

int fstat(int descrittore_del_file, struct stat *memoria_intermedia_di_trasferimento)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, descrittore_del_file, (long)memoria_intermedia_di_trasferimento, 0, 0, 0, 0));
}

int uname(struct utsname *identità_del_sistema)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)identità_del_sistema, 0, 0, 0, 0, 0));
}
