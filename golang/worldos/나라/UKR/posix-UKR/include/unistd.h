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
void _exit(int стан) __attribute__((noreturn));
ssize_t Читання(int дескриптор_файла, void *буфер_передавання, size_t count);
ssize_t Запис(int дескриптор_файла, const void *буфер_передавання, size_t count);
int Закрити(int дескриптор_файла);
off_t lseek(int дескриптор_файла, off_t offset, int whence);
pid_t fork(void);
int execve(const char *шлях, char *const аргументи_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *шлях, int mode);
int chdir(const char *шлях);
char *getcwd(char *буфер_передавання, size_t кількість_цифр);
int dup(int дескриптор_файла);
int dup2(int oldfd, int newfd);
int fsync(int дескриптор_файла);
void sync(void);
int isatty(int дескриптор_файла);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
