#include <errno.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sys/syscall.h>

enum {
    SYS__exit = 1,
    SYS_fork = 2,
    SYS_Okuma = 3,
    SYS_Yazma = 4,
    SYS_Kapat = 6,
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

void _exit(int durum)
{
    SC1(SYS__exit, durum);
    for (;;) {
        __asm__ __volatile__("hlt");
    }
}

ssize_t Okuma(int dosya_tanımlayıcısı, void *aktarım_ara_belleği, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Okuma, dosya_tanımlayıcısı, aktarım_ara_belleği, count));
}

ssize_t Yazma(int dosya_tanımlayıcısı, const void *aktarım_ara_belleği, size_t count)
{
    return (ssize_t)__syscall_result(SC3(SYS_Yazma, dosya_tanımlayıcısı, aktarım_ara_belleği, count));
}

int Kapat(int dosya_tanımlayıcısı)
{
    return (int)__syscall_result(SC1(SYS_Kapat, dosya_tanımlayıcısı));
}

off_t lseek(int dosya_tanımlayıcısı, off_t offset, int whence)
{
    return (off_t)__syscall_result(SC3(SYS_lseek, dosya_tanımlayıcısı, offset, whence));
}

pid_t fork(void)
{
    return (pid_t)__syscall_result(SC0(SYS_fork));
}

int execve(const char *yol, char *const bağımsız_değişkenler_2[], char *const envp[])
{
    return (int)__syscall_result(SC3(SYS_execve, yol, bağımsız_değişkenler_2, envp));
}

pid_t getpid(void) { return (pid_t)SC0(SYS_getpid); }
pid_t getppid(void) { return (pid_t)SC0(SYS_getppid); }
uid_t getuid(void) { return (uid_t)SC0(SYS_getuid); }
uid_t geteuid(void) { return (uid_t)SC0(SYS_geteuid); }
gid_t getgid(void) { return (gid_t)SC0(SYS_getgid); }
gid_t getegid(void) { return (gid_t)SC0(SYS_getegid); }

int access(const char *yol, int mode)
{
    return (int)__syscall_result(SC2(SYS_access, yol, mode));
}

int chdir(const char *yol)
{
    return (int)__syscall_result(SC1(SYS_chdir, yol));
}

char *getcwd(char *aktarım_ara_belleği, size_t rakam_sayısı)
{
    long result = __syscall_result(SC2(SYS_getcwd, aktarım_ara_belleği, rakam_sayısı));
    return result < 0 ? (char *)0 : aktarım_ara_belleği;
}

int dup(int dosya_tanımlayıcısı)
{
    return (int)__syscall_result(SC1(SYS_dup, dosya_tanımlayıcısı));
}

int dup2(int oldfd, int newfd)
{
    return (int)__syscall_result(SC2(SYS_dup2, oldfd, newfd));
}

int fsync(int dosya_tanımlayıcısı)
{
    return (int)__syscall_result(SC1(SYS_fsync, dosya_tanımlayıcısı));
}

void sync(void)
{
    SC0(SYS_sync);
}

int isatty(int dosya_tanımlayıcısı)
{
    struct stat st;
    if (fstat(dosya_tanımlayıcısı, &st) < 0)
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

pid_t waitpid(pid_t pid, int *durum, int options)
{
    long result;
    do {
        result = SC3(7, pid, durum, options);
    } while (result == -EAGAIN && (options & WNOHANG) == 0);
    return (pid_t)__syscall_result(result);
}

pid_t wait(int *durum)
{
    return waitpid(-1, durum, 0);
}
