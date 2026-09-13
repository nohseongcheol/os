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
void _exit(int tillstånd) __attribute__((noreturn));
ssize_t Läs(int filbeskrivare, void *överföringsbuffert, size_t count);
ssize_t Skriv(int filbeskrivare, const void *överföringsbuffert, size_t count);
int Stäng(int filbeskrivare);
off_t lseek(int filbeskrivare, off_t offset, int whence);
pid_t fork(void);
int execve(const char *sökväg, char *const argument_3[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *sökväg, int mode);
int chdir(const char *sökväg);
char *getcwd(char *överföringsbuffert, size_t antal_siffror);
int dup(int filbeskrivare);
int dup2(int oldfd, int newfd);
int fsync(int filbeskrivare);
void sync(void);
int isatty(int filbeskrivare);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
