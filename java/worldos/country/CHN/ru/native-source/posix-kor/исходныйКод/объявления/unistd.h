#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int файл_дескриптор, void *данные, size_t байт_СЧЁТ);
ssize_t write(int файл_дескриптор, const void *данные, size_t байт_СЧЁТ);
int close(int файл_дескриптор);
off_t lseek(int файл_дескриптор, off_t СМЕЩ_ЗНАЧЕН, int задача_корень);
int dup(int файл_дескриптор);
int dup2(int файл_дескриптор, int 새서술자);
int unlink(const char *файл_ввод_имя);
int ftruncate(int файл_дескриптор, off_t байт_СЧЁТ);
int fsync(int файл_дескриптор);
void _exit(int код_выхода) __attribute__((noreturn));
#endif
