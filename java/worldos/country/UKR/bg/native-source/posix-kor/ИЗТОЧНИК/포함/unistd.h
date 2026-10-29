#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 파일서술자, void *данни, size_t 바이트수);
ssize_t write(int 파일서술자, const void *данни, size_t 바이트수);
int close(int 파일서술자);
off_t lseek(int 파일서술자, off_t Изместване_стойност, int проект_корен);
int dup(int 파일서술자);
int dup2(int 파일서술자, int 새서술자);
int unlink(const char *Файл_запис_препратка_към_клетка);
int ftruncate(int 파일서술자, off_t 바이트수);
int fsync(int 파일서술자);
void _exit(int Изход_код) __attribute__((noreturn));
#endif
