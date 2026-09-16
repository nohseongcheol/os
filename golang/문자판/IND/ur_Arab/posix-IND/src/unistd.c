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
    SYS_پڑھنا = 3,
    SYS_لکھنا = 4,
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

void _exit(int حالت)
{
    SC1(SYS__exit, حالت);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t پڑھنا(int فائل_کا_وصف_کنندہ, void *منتقلی_کا_عارضی_ذخیرہ, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_پڑھنا, فائل_کا_وصف_کنندہ, منتقلی_کا_عارضی_ذخیرہ, count));
}

ssize_t لکھنا(int فائل_کا_وصف_کنندہ, const void *منتقلی_کا_عارضی_ذخیرہ, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_لکھنا, فائل_کا_وصف_کنندہ, منتقلی_کا_عارضی_ذخیرہ, count));
}

int close(int فائل_کا_وصف_کنندہ)
{
    return (int)__syscall_result(SC1(SYS_close, فائل_کا_وصف_کنندہ));
}

off_t lseek(int فائل_کا_وصف_کنندہ, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, فائل_کا_وصف_کنندہ, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *راستہ, char *const دلائل_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, راستہ, دلائل_2, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *راستہ, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, راستہ, mode));
}

int chdir(const char *راستہ)
{
    return (int)__syscall_result(SC1(SYS_chdir, راستہ));
}

char *getcwd(char *منتقلی_کا_عارضی_ذخیرہ, size_t ہندسوں_کی_تعداد)
{
    long result = __syscall_result(SC2(SYS_getcwd, منتقلی_کا_عارضی_ذخیرہ, ہندسوں_کی_تعداد));
    return result < 0 ? (char *)0 : منتقلی_کا_عارضی_ذخیرہ;
}

int dup(int فائل_کا_وصف_کنندہ)
{
    return (int)__syscall_result(SC1(SYS_dup, فائل_کا_وصف_کنندہ));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int فائل_کا_وصف_کنندہ)
{
    return (int)__syscall_result(SC1(SYS_fsync, فائل_کا_وصف_کنندہ));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int فائل_کا_وصف_کنندہ)
{
    struct stat st;
    if (fstat(فائل_کا_وصف_کنندہ, &st) < 0)
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

pid_t waitpid(pid_t pid, int *حالت, int options)
{
    long result;
    do {
        result = SC3(7, pid, حالت, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *حالت)
{
    return waitpid(-1, حالت, 0);
}
