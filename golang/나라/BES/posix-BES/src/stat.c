/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *pad, struct stat *overdrachtsbuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)pad, (long)overdrachtsbuffer, 0, 0, 0, 0));
}

int lstat(const char *pad, struct stat *overdrachtsbuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)pad, (long)overdrachtsbuffer, 0, 0, 0, 0));
}

int fstat(int bestandsdescriptor, struct stat *overdrachtsbuffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, bestandsdescriptor, (long)overdrachtsbuffer, 0, 0, 0, 0));
}

int uname(struct utsname *systeemidentiteit)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)systeemidentiteit, 0, 0, 0, 0, 0));
}
