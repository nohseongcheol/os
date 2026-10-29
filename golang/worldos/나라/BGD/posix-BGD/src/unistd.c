#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>

enum {
    SYS__exit = 1,
    SYS_fork = 2,
    SYS_pora = 3,
    SYS_lekha = 4,
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

void _exit(int অবস্থা)
{
    SC1(SYS__exit, অবস্থা);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t pora(int নথি_নির্দেশক, void *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_pora, নথি_নির্দেশক, স্থানান্তরের_অস্থায়ী_ভান্ডার, count));
}

ssize_t lekha(int নথি_নির্দেশক, const void *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_lekha, নথি_নির্দেশক, স্থানান্তরের_অস্থায়ী_ভান্ডার, count));
}

int close(int নথি_নির্দেশক)
{
    return (int)__syscall_result(SC1(SYS_close, নথি_নির্দেশক));
}

off_t lseek(int নথি_নির্দেশক, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, নথি_নির্দেশক, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *পথ, char *const আর্গুমেন্ট_তালিকা_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, পথ, আর্গুমেন্ট_তালিকা_2, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *পথ, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, পথ, mode));
}

int chdir(const char *পথ)
{
    return (int)__syscall_result(SC1(SYS_chdir, পথ));
}

char *getcwd(char *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t অঙ্কের_সংখ্যা)
{
    long result = __syscall_result(SC2(SYS_getcwd, স্থানান্তরের_অস্থায়ী_ভান্ডার, অঙ্কের_সংখ্যা));
    return result < 0 ? (char *)0 : স্থানান্তরের_অস্থায়ী_ভান্ডার;
}

int dup(int নথি_নির্দেশক)
{
    return (int)__syscall_result(SC1(SYS_dup, নথি_নির্দেশক));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int নথি_নির্দেশক)
{
    return (int)__syscall_result(SC1(SYS_fsync, নথি_নির্দেশক));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int নথি_নির্দেশক)
{
    struct stat st;
    if (fstat(নথি_নির্দেশক, &st) < 0)
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

pid_t waitpid(pid_t pid, int *অবস্থা, int options)
{
    long result;
    do {
        result = SC3(7, pid, অবস্থা, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *অবস্থা)
{
    return waitpid(-1, অবস্থা, 0);
}
