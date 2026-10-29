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
void _exit(int toestand) __attribute__((noreturn));
ssize_t Lezen(int bestandsdescriptor, void *overdrachtsbuffer, size_t count);
ssize_t Schrijven(int bestandsdescriptor, const void *overdrachtsbuffer, size_t count);
int Sluiten(int bestandsdescriptor);
off_t lseek(int bestandsdescriptor, off_t offset, int whence);
pid_t fork(void);
int execve(const char *pad, char *const argumenten_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *pad, int mode);
int chdir(const char *pad);
char *getcwd(char *overdrachtsbuffer, size_t aantal_cijfers);
int dup(int bestandsdescriptor);
int dup2(int oldfd, int newfd);
int fsync(int bestandsdescriptor);
void sync(void);
int isatty(int bestandsdescriptor);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
