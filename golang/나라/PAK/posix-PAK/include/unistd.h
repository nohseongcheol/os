#ifndef _LIBC_UNISTD_H
#define _LIBC_UNISTD_H

#include <stddef.h>
#include <sys/types.h>

#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define F_OK 0
#define X_OK 1
#define W_OK 2
#define R_OK 4
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **environ;
void _exit(int حالت) __attribute__((noreturn));
ssize_t پڑھیں(int فائل_کا_وصف_کنندہ, void *منتقلی_کا_عارضی_ذخیرہ, size_t count);
ssize_t لکھیں(int فائل_کا_وصف_کنندہ, const void *منتقلی_کا_عارضی_ذخیرہ, size_t count);
int بندکریں(int فائل_کا_وصف_کنندہ);
off_t lseek(int فائل_کا_وصف_کنندہ, off_t offset, int whence);
pid_t fork(void);
int execve(const char *راستہ, char *const دلائل_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *راستہ, int mode);
int chdir(const char *راستہ);
char *getcwd(char *منتقلی_کا_عارضی_ذخیرہ, size_t ہندسوں_کی_تعداد);
int dup(int فائل_کا_وصف_کنندہ);
int dup2(int oldfd, int newfd);
int fsync(int فائل_کا_وصف_کنندہ);
void sync(void);
int isatty(int فائل_کا_وصف_کنندہ);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
