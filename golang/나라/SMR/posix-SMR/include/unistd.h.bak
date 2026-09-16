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
void _exit(int stato) __attribute__((noreturn));
ssize_t Lettura(int descrittore_del_file, void *memoria_intermedia_di_trasferimento, size_t count);
ssize_t Scrittura(int descrittore_del_file, const void *memoria_intermedia_di_trasferimento, size_t count);
int Chiudi(int descrittore_del_file);
off_t lseek(int descrittore_del_file, off_t offset, int whence);
pid_t fork(void);
int execve(const char *percorso, char *const argomenti_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *percorso, int mode);
int chdir(const char *percorso);
char *getcwd(char *memoria_intermedia_di_trasferimento, size_t numero_di_cifre);
int dup(int descrittore_del_file);
int dup2(int oldfd, int newfd);
int fsync(int descrittore_del_file);
void sync(void);
int isatty(int descrittore_del_file);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
