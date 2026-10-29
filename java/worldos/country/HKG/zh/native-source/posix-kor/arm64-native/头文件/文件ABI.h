#ifndef JKOROS_ARM64_NATIVE_FILE_H
#define JKOROS_ARM64_NATIVE_FILE_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
// 독립된 bare-metal ABI. Linux/i386의 헤더나 libc와 혼합하지 않는다.
typedef intptr_t 输入输出结果类型;
typedef size_t 字节个数类型;
typedef int64_t 文件偏移类型;
int *pk_errno_location(void);
int pk_open(const char *path, int flags, ...);
输入输出结果类型 pk_read(int fd, void *buffer, size_t count);
输入输出结果类型 pk_write(int fd, const void *buffer, size_t count);
int pk_close(int fd);
文件偏移类型 pk_lseek(int fd, 文件偏移类型 offset, int origin);
int pk_unlink(const char *path);
int pk_ftruncate(int fd, 文件偏移类型 size);
int pk_fsync(int fd);
int pk_size(int fd);
int 打开文件(const char *路径, int 方法模式, ...);
输入输出结果类型 读取文件数据(int 文件, void *数据, size_t 项目个数);
输入输出结果类型 写入文件数据(int 文件, const void *数据, size_t 项目个数);
int 关闭文件(int 文件);
文件偏移类型 寻道文件(int 文件, 文件偏移类型 距离值, int 项目根);
int 移除文件条目名称(const char *路径);
int 设定文件长度(int 文件, 文件偏移类型 大小);
int 提交文件存储装置(int 文件);
int 文件大小(int 文件);
#ifdef __cplusplus
}
#endif
#define 错误编号 (*pk_errno_location())
#define 读取仅用值 0
#define 写入仅用值 1
#define 读取写入 2
#define 创建条件缺失 0x40
#define 创建新建文件 0xc0
#define 截断内容 0x200
#define 追加位置结束 0x400
#define 起点开头 0
#define 当前根 1
#define 结束原点 2
#endif
