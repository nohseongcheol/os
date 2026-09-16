/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>

enum {
    SYS__exit = 1,
    SYS_fork = 2,
    SYS_faitau = 3,
    SYS_tusi = 4,
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

#define SC0(n) __syscall6((n), 0, 0, 0, 0, 0, 0)
#define SC1(n,a) __syscall6((n), (long)(a), 0, 0, 0, 0, 0)
#define SC2(n,a,b) __syscall6((n), (long)(a), (long)(b), 0, 0, 0, 0)
#define SC3(n,a,b,c) __syscall6((n), (long)(a), (long)(b), (long)(c), 0, 0, 0)

void _exit(int status)
{
    SC1(SYS__exit, status);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t faitau(int fd, void *buf, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_faitau, fd, buf, count));
}

ssize_t tusi(int fd, const void *buf, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_tusi, fd, buf, count));
}

int close(int fd)
{
    return (int)__syscall_result(SC1(SYS_close, fd));
}

off_t lseek(int fd, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, fd, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *path, char *const argv[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, path, argv, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *path, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, path, mode));
}

int chdir(const char *path)
{
    return (int)__syscall_result(SC1(SYS_chdir, path));
}

char *getcwd(char *buf, size_t size)
{
    long result = __syscall_result(SC2(SYS_getcwd, buf, size));
    return result < 0 ? (char *)0 : buf;
}

int dup(int fd)
{
    return (int)__syscall_result(SC1(SYS_dup, fd));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int fd)
{
    return (int)__syscall_result(SC1(SYS_fsync, fd));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int fd)
{
    struct stat st;
    if (fstat(fd, &st) < 0)
        return 0;
    if (!S_ISCHR(st.st_mode)) {
        errno = ENOTTY;
        return 0;
    }
    return 1;
}

int brk(void *address)
{
    long result = SC1(SYS_brk, address);
    if (result != (long)address) {
        errno = ENOMEM;
        return -1;
    }
    return 0;
}

void *sbrk(int increment)
{
    long current = SC1(SYS_brk, 0);
    long requested = current + increment;
    if (increment != 0 && brk((void *)requested) < 0)
        return (void *)-1;
    return (void *)current;
}

pid_t waitpid(pid_t pid, int *status, int options)
{
    long result;
    do {
        result = SC3(7, pid, status, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *status)
{
    return waitpid(-1, status, 0);
}
