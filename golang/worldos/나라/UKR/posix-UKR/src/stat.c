#include <sys/stat.h>
#include <sys/utsname.h>
#include <sys/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *шлях, struct stat *буфер_передавання)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)шлях, (long)буфер_передавання, 0, 0, 0, 0));
}

int lstat(const char *шлях, struct stat *буфер_передавання)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)шлях, (long)буфер_передавання, 0, 0, 0, 0));
}

int fstat(int дескриптор_файла, struct stat *буфер_передавання)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, дескриптор_файла, (long)буфер_передавання, 0, 0, 0, 0));
}

int uname(struct utsname *відомості_про_систему)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)відомості_про_систему, 0, 0, 0, 0, 0));
}
