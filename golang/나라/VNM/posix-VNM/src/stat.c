/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *đường_dẫn, struct stat *bộ_đệm_truyền)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)đường_dẫn, (long)bộ_đệm_truyền, 0, 0, 0, 0));
}

int lstat(const char *đường_dẫn, struct stat *bộ_đệm_truyền)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)đường_dẫn, (long)bộ_đệm_truyền, 0, 0, 0, 0));
}

int fstat(int bộ_mô_tả_tệp, struct stat *bộ_đệm_truyền)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, bộ_mô_tả_tệp, (long)bộ_đệm_truyền, 0, 0, 0, 0));
}

int uname(struct utsname *thông_tin_hệ_thống)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)thông_tin_hệ_thống, 0, 0, 0, 0, 0));
}
