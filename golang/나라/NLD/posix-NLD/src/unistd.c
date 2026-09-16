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
    SYS_Lezen = 3,
    SYS_Schrijven = 4,
    SYS_Sluiten = 6,
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

void _exit(int toestand)
{
    SC1(SYS__exit, toestand);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t Lezen(int bestandsdescriptor, void *overdrachtsbuffer, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Lezen, bestandsdescriptor, overdrachtsbuffer, count));
}

ssize_t Schrijven(int bestandsdescriptor, const void *overdrachtsbuffer, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Schrijven, bestandsdescriptor, overdrachtsbuffer, count));
}

int Sluiten(int bestandsdescriptor)
{
    return (int)__syscall_result(SC1(SYS_Sluiten, bestandsdescriptor));
}

off_t lseek(int bestandsdescriptor, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, bestandsdescriptor, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *pad, char *const argumenten_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, pad, argumenten_2, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *pad, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, pad, mode));
}

int chdir(const char *pad)
{
    return (int)__syscall_result(SC1(SYS_chdir, pad));
}

char *getcwd(char *overdrachtsbuffer, size_t aantal_cijfers)
{
    long result = __syscall_result(SC2(SYS_getcwd, overdrachtsbuffer, aantal_cijfers));
    return result < 0 ? (char *)0 : overdrachtsbuffer;
}

int dup(int bestandsdescriptor)
{
    return (int)__syscall_result(SC1(SYS_dup, bestandsdescriptor));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int bestandsdescriptor)
{
    return (int)__syscall_result(SC1(SYS_fsync, bestandsdescriptor));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int bestandsdescriptor)
{
    struct stat st;
    if (fstat(bestandsdescriptor, &st) < 0)
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

pid_t waitpid(pid_t pid, int *toestand, int options)
{
    long result;
    do {
        result = SC3(7, pid, toestand, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *toestand)
{
    return waitpid(-1, toestand, 0);
}
