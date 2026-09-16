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
void _exit(int status) __attribute__((noreturn));
ssize_t Baca(int deskriptor_berkas, void *penyangga_transfer, size_t count);
ssize_t Tulis(int deskriptor_berkas, const void *penyangga_transfer, size_t count);
int Tutup(int deskriptor_berkas);
off_t lseek(int deskriptor_berkas, off_t offset, int whence);
pid_t fork(void);
int execve(const char *jalur, char *const argumen_2[], char *const envp[]);
pid_t getpid(void);
pid_t getppid(void);
uid_t getuid(void);
uid_t geteuid(void);
gid_t getgid(void);
gid_t getegid(void);
int access(const char *jalur, int mode);
int chdir(const char *jalur);
char *getcwd(char *penyangga_transfer, size_t jumlah_digit);
int dup(int deskriptor_berkas);
int dup2(int oldfd, int newfd);
int fsync(int deskriptor_berkas);
void sync(void);
int isatty(int deskriptor_berkas);
int brk(void *address);
void *sbrk(int increment);
#ifdef __cplusplus
}
#endif

#endif
