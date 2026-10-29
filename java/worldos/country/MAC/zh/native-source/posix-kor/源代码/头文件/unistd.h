#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int 文件描述符, void *数据, size_t 字节个数);
ssize_t write(int 文件描述符, const void *数据, size_t 字节个数);
int close(int 文件描述符);
off_t lseek(int 文件描述符, off_t 偏移值, int 项目根);
int dup(int 文件描述符);
int dup2(int 文件描述符, int 新建描述符);
int unlink(const char *文件条目名称);
int ftruncate(int 文件描述符, off_t 字节个数);
int fsync(int 文件描述符);
void _exit(int 退出代码) __attribute__((noreturn));
#endif
