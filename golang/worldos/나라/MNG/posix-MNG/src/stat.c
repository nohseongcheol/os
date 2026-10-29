#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *path, struct stat *buf)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)path, (long)buf, 0, 0, 0, 0));
}

int lstat(const char *path, struct stat *buf)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)path, (long)buf, 0, 0, 0, 0));
}

int fstat(int fd, struct stat *buf)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, fd, (long)buf, 0, 0, 0, 0));
}

int uname(struct utsname *name)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)name, 0, 0, 0, 0, 0));
}
