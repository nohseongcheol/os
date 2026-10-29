#include <errno.h>
#include <fcntl.h>
#include <system/stat.h>
#include <system/child_wait.h>
#include <unistd.h>
#include <system/syscall.h>

enum {
    SYS__exit = 1,
    SYS_fork = 2,
    SYS_read = 3,
    SYS_write = 4,
    SYS_close = 6,
    SYS_execve = 11,
    SYS_chdir = 12,
    SYS_lseek = 19,
    SYS_getpid = 20,
    SYS_getuid = 24,
    SYS_access = 33,
    SYS_sync = 36,
    SYS_dup = 41,
    SYS_brk = 45,
    SYS_getgid = 47,
    SYS_geteuid = 49,
    SYS_getegid = 50,
    SYS_dup2 = 63,
    SYS_getppid = 64,
    SYS_fsync = 118,
    SYS_getcwd = 183
};

#define syscall_without_arguments(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define syscall_with_one_argument(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define syscall_with_two_arguments(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define syscall_with_three_arguments(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void _exit(int status)
{
    syscall_with_one_argument(SYS__exit, status);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

signed_size_type read(int file_descriptor, void *transfer_buffer, object_size_type count)
{
    return (signed_size_type)__syscall_result(syscall_with_three_arguments(SYS_read, file_descriptor, transfer_buffer, count));
}

signed_size_type write(int file_descriptor, const void *transfer_buffer, object_size_type count)
{
    return (signed_size_type)__syscall_result(syscall_with_three_arguments(SYS_write, file_descriptor, transfer_buffer, count));
}

int close(int file_descriptor)
{
    return (int)__syscall_result(syscall_with_one_argument(SYS_close, file_descriptor));
}

file_offset_type lseek(int file_descriptor, file_offset_type offset, int whence)
{
    return (file_offset_type)__syscall_result(syscall_with_three_arguments(SYS_lseek, file_descriptor, offset, whence));
}

process_identifier_type fork(void)
{
    return (process_identifier_type)__syscall_result(syscall_without_arguments(SYS_fork));
}

int execve(const char *path, char *const arguments_2[], char *const envp[])
{
    return (int)__syscall_result(syscall_with_three_arguments(SYS_execve, path, arguments_2, envp));
}

process_identifier_type getpid(void) { return (process_identifier_type)syscall_without_arguments(SYS_getpid); }
process_identifier_type getppid(void) { return (process_identifier_type)syscall_without_arguments(SYS_getppid); }
user_identifier_type getuid(void) { return (user_identifier_type)syscall_without_arguments(SYS_getuid); }
user_identifier_type geteuid(void) { return (user_identifier_type)syscall_without_arguments(SYS_geteuid); }
group_identifier_type getgid(void) { return (group_identifier_type)syscall_without_arguments(SYS_getgid); }
group_identifier_type getegid(void) { return (group_identifier_type)syscall_without_arguments(SYS_getegid); }

int access(const char *path, int mode)
{
    return (int)__syscall_result(syscall_with_two_arguments(SYS_access, path, mode));
}

int chdir(const char *path)
{
    return (int)__syscall_result(syscall_with_one_argument(SYS_chdir, path));
}

char *getcwd(char *transfer_buffer, object_size_type digit_count)
{
    long result = __syscall_result(syscall_with_two_arguments(SYS_getcwd, transfer_buffer, digit_count));
    return result < 0 ? (char *)0 : transfer_buffer;
}

int dup(int file_descriptor)
{
    return (int)__syscall_result(syscall_with_one_argument(SYS_dup, file_descriptor));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(syscall_with_two_arguments(SYS_dup2, oldfd, newfd));
}

int fsync(int file_descriptor)
{
    return (int)__syscall_result(syscall_with_one_argument(SYS_fsync, file_descriptor));
}

void sync(void)
{
    syscall_without_arguments(SYS_sync);
}

int isatty(int file_descriptor)
{
    struct stat st;
    if (fstat(file_descriptor, &st) < 0)
        return 0;
    if (!is_character_device_mode(st.file_kind_and_permissions)) {
        errno = inappropriate_device_operation;
        return 0;
    }
    return 1;
}

int brk(void *address)
{
    long result = syscall_with_one_argument(SYS_brk, address);
    if (result != (long)address) {
        errno = insufficient_memory;
        return -1;
    }
    return 0;
}

void *sbrk(int increment)
{
    long current = syscall_with_one_argument(SYS_brk, 0);
    long requested = current + increment;
    if (increment != 0 && brk((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

process_identifier_type waitpid(process_identifier_type pid, int *status, int options)
{
    long result;
    do {
        result = syscall_with_three_arguments(7, pid, status, options);
    } while (result == -temporarily_unavailable && (options & do_not_wait_if_unready) == 0);
    return (process_identifier_type)__syscall_result(result);
}

process_identifier_type wait(int *status)
{
    return waitpid(-1, status, 0);
}
