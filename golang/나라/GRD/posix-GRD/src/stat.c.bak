#include <system/stat.h>
#include <system/system_identity.h>
#include <system/syscall.h>

enum { SYS_stat = 106, SYS_lstat = 107, SYS_fstat = 108, SYS_uname = 122 };

int stat(const char *path, struct stat *transfer_buffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_stat, (long)path, (long)transfer_buffer, 0, 0, 0, 0));
}

int lstat(const char *path, struct stat *transfer_buffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_lstat, (long)path, (long)transfer_buffer, 0, 0, 0, 0));
}

int fstat(int file_descriptor, struct stat *transfer_buffer)
{
    return (int)__syscall_result(
        __syscall6(SYS_fstat, file_descriptor, (long)transfer_buffer, 0, 0, 0, 0));
}

int uname(struct system_identity_2 *system_identity)
{
    return (int)__syscall_result(
        __syscall6(SYS_uname, (long)system_identity, 0, 0, 0, 0, 0));
}
