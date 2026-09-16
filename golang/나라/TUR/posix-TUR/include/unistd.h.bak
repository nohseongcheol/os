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
void _exit(int durum) __attribute__((noreturn));
ssize_t Okuma(int dosya_tanımlayıcısı, void *aktarım_ara_belleği, size_t count);
ssize_t Yazma(int dosya_tanımlayıcısı, const void *aktarım_ara_belleği, size_t count);
int Kapat(int dosya_tanımlayıcısı);
off_t lseek(int dosya_tanımlayıcısı, off_t offset, int whence);
pid_t fork(void);
int execve(const char *yol, char *const bağımsız_değişkenler_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *yol, int mode);
int chdir(const char *yol);
char *getcwd(char *aktarım_ara_belleği, size_t rakam_sayısı);
int dup(int dosya_tanımlayıcısı);
int dup2(int oldfd, int newfd);
int fsync(int dosya_tanımlayıcısı);
void sync(void);
int isatty(int dosya_tanımlayıcısı);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
