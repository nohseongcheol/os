/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

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
void _exit(int stav) __attribute__((noreturn));
ssize_t Čtení(int deskriptor_souboru, void *vyrovnávací_paměť_přenosu, size_t count);
ssize_t Zápis(int deskriptor_souboru, const void *vyrovnávací_paměť_přenosu, size_t count);
int Zavřít(int deskriptor_souboru);
off_t lseek(int deskriptor_souboru, off_t offset, int whence);
pid_t fork(void);
int execve(const char *cesta, char *const argumenty_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *cesta, int mode);
int chdir(const char *cesta);
char *getcwd(char *vyrovnávací_paměť_přenosu, size_t počet_číslic);
int dup(int deskriptor_souboru);
int dup2(int oldfd, int newfd);
int fsync(int deskriptor_souboru);
void sync(void);
int isatty(int deskriptor_souboru);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
