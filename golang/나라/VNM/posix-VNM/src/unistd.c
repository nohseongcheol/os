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
    SYS_Đọc = 3,
    SYS_Ghi = 4,
    SYS_Đóng = 6,
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

void _exit(int trạng_thái)
{
    SC1(SYS__exit, trạng_thái);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t Đọc(int bộ_mô_tả_tệp, void *bộ_đệm_truyền, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Đọc, bộ_mô_tả_tệp, bộ_đệm_truyền, count));
}

ssize_t Ghi(int bộ_mô_tả_tệp, const void *bộ_đệm_truyền, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Ghi, bộ_mô_tả_tệp, bộ_đệm_truyền, count));
}

int Đóng(int bộ_mô_tả_tệp)
{
    return (int)__syscall_result(SC1(SYS_Đóng, bộ_mô_tả_tệp));
}

off_t lseek(int bộ_mô_tả_tệp, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, bộ_mô_tả_tệp, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *đường_dẫn, char *const đối_số_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, đường_dẫn, đối_số_2, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *đường_dẫn, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, đường_dẫn, mode));
}

int chdir(const char *đường_dẫn)
{
    return (int)__syscall_result(SC1(SYS_chdir, đường_dẫn));
}

char *getcwd(char *bộ_đệm_truyền, size_t số_chữ_số)
{
    long result = __syscall_result(SC2(SYS_getcwd, bộ_đệm_truyền, số_chữ_số));
    return result < 0 ? (char *)0 : bộ_đệm_truyền;
}

int dup(int bộ_mô_tả_tệp)
{
    return (int)__syscall_result(SC1(SYS_dup, bộ_mô_tả_tệp));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int bộ_mô_tả_tệp)
{
    return (int)__syscall_result(SC1(SYS_fsync, bộ_mô_tả_tệp));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int bộ_mô_tả_tệp)
{
    struct stat st;
    if (fstat(bộ_mô_tả_tệp, &st) < 0)
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

pid_t waitpid(pid_t pid, int *trạng_thái, int options)
{
    long result;
    do {
        result = SC3(7, pid, trạng_thái, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *trạng_thái)
{
    return waitpid(-1, trạng_thái, 0);
}
