#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *راستہ, struct stat *منتقلی_کا_عارضی_ذخیرہ)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)راستہ, (long)منتقلی_کا_عارضی_ذخیرہ, 0, 0, 0, 0));
}

int lstat(const char *راستہ, struct stat *منتقلی_کا_عارضی_ذخیرہ)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)راستہ, (long)منتقلی_کا_عارضی_ذخیرہ, 0, 0, 0, 0));
}

int fstat(int فائل_کا_وصف_کنندہ, struct stat *منتقلی_کا_عارضی_ذخیرہ)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, فائل_کا_وصف_کنندہ, (long)منتقلی_کا_عارضی_ذخیرہ, 0, 0, 0, 0));
}

int uname(struct utsname *نظام_کی_شناخت)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)نظام_کی_شناخت, 0, 0, 0, 0, 0));
}
