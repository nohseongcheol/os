/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *পথ, struct stat *স্থানান্তরের_অস্থায়ী_ভান্ডার)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)পথ, (long)স্থানান্তরের_অস্থায়ী_ভান্ডার, 0, 0, 0, 0));
}

int lstat(const char *পথ, struct stat *স্থানান্তরের_অস্থায়ী_ভান্ডার)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)পথ, (long)স্থানান্তরের_অস্থায়ী_ভান্ডার, 0, 0, 0, 0));
}

int fstat(int নথি_নির্দেশক, struct stat *স্থানান্তরের_অস্থায়ী_ভান্ডার)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, নথি_নির্দেশক, (long)স্থানান্তরের_অস্থায়ী_ভান্ডার, 0, 0, 0, 0));
}

int uname(struct utsname *ব্যবস্থার_পরিচয়)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)ব্যবস্থার_পরিচয়, 0, 0, 0, 0, 0));
}
