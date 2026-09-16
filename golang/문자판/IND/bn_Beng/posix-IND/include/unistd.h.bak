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
void _exit(int অবস্থা) __attribute__((noreturn));
ssize_t পড়া(int নথি_নির্দেশক, void *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t count);
ssize_t লেখা(int নথি_নির্দেশক, const void *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t count);
int close(int নথি_নির্দেশক);
off_t lseek(int নথি_নির্দেশক, off_t offset, int whence);
pid_t fork(void);
int execve(const char *পথ, char *const আর্গুমেন্ট_তালিকা_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *পথ, int mode);
int chdir(const char *পথ);
char *getcwd(char *স্থানান্তরের_অস্থায়ী_ভান্ডার, size_t অঙ্কের_সংখ্যা);
int dup(int নথি_নির্দেশক);
int dup2(int oldfd, int newfd);
int fsync(int নথি_নির্দেশক);
void sync(void);
int isatty(int নথি_নির্দেশক);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
