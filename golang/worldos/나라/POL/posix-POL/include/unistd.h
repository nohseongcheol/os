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
void _exit(int stan) __attribute__((noreturn));
ssize_t Odczyt(int deskryptor_pliku, void *bufor_przesyłania, size_t count);
ssize_t Zapis(int deskryptor_pliku, const void *bufor_przesyłania, size_t count);
int Zamknij(int deskryptor_pliku);
off_t lseek(int deskryptor_pliku, off_t offset, int whence);
pid_t fork(void);
int execve(const char *ścieżka, char *const argumenty_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *ścieżka, int mode);
int chdir(const char *ścieżka);
char *getcwd(char *bufor_przesyłania, size_t liczba_cyfr);
int dup(int deskryptor_pliku);
int dup2(int oldfd, int newfd);
int fsync(int deskryptor_pliku);
void sync(void);
int isatty(int deskryptor_pliku);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
