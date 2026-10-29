#ifndef JKOROS_UNISTD_H
#define JKOROS_UNISTD_H
#include <sys/types.h>
#define STDIN_FILENO 0
#define STDOUT_FILENO 1
#define STDERR_FILENO 2
#define SEEK_SET 0
#define SEEK_CUR 1
#define SEEK_END 2
ssize_t read(int ファイル記述子, void *データ, size_t バイト個数);
ssize_t write(int ファイル記述子, const void *データ, size_t バイト個数);
int close(int ファイル記述子);
off_t lseek(int ファイル記述子, off_t 変位量値, int 計画根);
int dup(int ファイル記述子);
int dup2(int ファイル記述子, int 新規記述子);
int unlink(const char *ファイル入口名前);
int ftruncate(int ファイル記述子, off_t バイト個数);
int fsync(int ファイル記述子);
void _exit(int 終了点コード) __attribute__((noreturn));
#endif
