#include <文件ABI.h>
#include "调用边界位置.h"

int 错误编号;
int 调用状态结果(int 结果) {
    if (结果 < 0) { 错误编号 = -结果; return -1; }
    return 结果;
}
int open(const char *文件条目名称, int 打开设置, ...) {
    mode_t 授权权限 = 0;
    if (打开设置 & O_CREAT) {
        __builtin_va_list 实参;
        __builtin_va_start(实参, 打开设置);
        授权权限 = __builtin_va_arg(实参, mode_t);
        __builtin_va_end(实参);
    }
    return 调用状态结果(jkoros_syscall(30, (int)文件条目名称, 打开设置, 授权权限, 0, 0));
}
int creat(const char *文件条目名称, mode_t 授权权限) { return open(文件条目名称, O_WRONLY | O_CREAT | O_TRUNC, 授权权限); }
ssize_t read(int 文件描述符, void *数据, size_t 字节个数) {
    return 调用状态结果(jkoros_syscall(31, 文件描述符, (int)数据, 字节个数, 0, 0));
}
ssize_t write(int 文件描述符, const void *数据, size_t 字节个数) {
    return 调用状态结果(jkoros_syscall(32, 文件描述符, (int)数据, 字节个数, 0, 0));
}
int close(int 文件描述符) { return 调用状态结果(jkoros_syscall(33, 文件描述符, 0, 0, 0, 0)); }
off_t lseek(int 文件描述符, off_t 偏移值, int 项目根) {
    return 调用状态结果(jkoros_syscall(34, 文件描述符, 偏移值, 项目根, 0, 0));
}
int dup(int 文件描述符) { return 调用状态结果(jkoros_syscall(35, 文件描述符, 0, 0, 0, 0)); }
int dup2(int 文件描述符, int 新建描述符) { return 调用状态结果(jkoros_syscall(36, 文件描述符, 新建描述符, 0, 0, 0)); }
int fstat(int 文件描述符, struct stat *状态值) { return 调用状态结果(jkoros_syscall(37, 文件描述符, (int)状态值, 0, 0, 0)); }
int unlink(const char *文件条目名称) { return 调用状态结果(jkoros_syscall(38, (int)文件条目名称, 0, 0, 0, 0)); }
int ftruncate(int 文件描述符, off_t 字节个数) { return 调用状态结果(jkoros_syscall(39, 文件描述符, 字节个数, 0, 0, 0)); }
int fsync(int 文件描述符) { return 调用状态结果(jkoros_syscall(47, 文件描述符, 0, 0, 0, 0)); }
int fcntl(int 文件描述符, int 命令, ...) {
    int 值 = 0;
    if (命令 == F_DUPFD || 命令 == F_DUPFD_CLOEXEC || 命令 == F_SETFD || 命令 == F_SETFL) {
        __builtin_va_list 实参;
        __builtin_va_start(实参, 命令); 值 = __builtin_va_arg(实参, int); __builtin_va_end(实参);
    }
    return 调用状态结果(jkoros_syscall(40, 文件描述符, 命令, 值, 0, 0));
}
