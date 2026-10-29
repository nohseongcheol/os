#ifndef JKOROS_FCNTL_H
#define JKOROS_FCNTL_H
#include <sys/types.h>
#define O_RDONLY 0
#define O_WRONLY 1
#define O_RDWR 2
#define O_ACCMODE 3
#define O_CREAT 64
#define O_EXCL 128
#define O_TRUNC 512
#define O_APPEND 1024
#define O_NONBLOCK 2048
#define O_CLOEXEC 524288
#define F_DUPFD 0
#define F_GETFD 1
#define F_SETFD 2
#define F_GETFL 3
#define F_SETFL 4
#define F_DUPFD_CLOEXEC 1030
#define FD_CLOEXEC 1
int open(const char *ファイル入口名前, int 設定値開放, ...);
int creat(const char *ファイル入口名前, mode_t 許可許可権);
int fcntl(int ファイル記述子, int 命令, ...);
#endif
