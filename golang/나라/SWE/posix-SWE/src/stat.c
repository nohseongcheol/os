/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *sökväg, struct stat *överföringsbuffert)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)sökväg, (long)överföringsbuffert, 0, 0, 0, 0));
}

int lstat(const char *sökväg, struct stat *överföringsbuffert)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)sökväg, (long)överföringsbuffert, 0, 0, 0, 0));
}

int fstat(int filbeskrivare, struct stat *överföringsbuffert)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, filbeskrivare, (long)överföringsbuffert, 0, 0, 0, 0));
}

int uname(struct utsname *systemidentitet)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)systemidentitet, 0, 0, 0, 0, 0));
}
