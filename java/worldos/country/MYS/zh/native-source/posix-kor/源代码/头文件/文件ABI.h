#ifndef JKOROS_KOREAN_FILE_H
#define JKOROS_KOREAN_FILE_H
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/stat.h>
#define 打开文件 open
#define 创建文件 creat
#define 读取文件数据 read
#define 写入文件数据 write
#define 关闭文件 close
#define 寻道文件 lseek
#define 复制副本文件描述符 dup
#define 复制副本文件描述符位置 dup2
#define 移除文件条目名称 unlink
#define 设定文件长度 ftruncate
#define 提交文件存储装置 fsync
#define 读取文件运行状态 fstat
#define 控制文件描述符 fcntl
#define 读取仅用值 O_RDONLY
#define 写入仅用值 O_WRONLY
#define 读取写入 O_RDWR
#define 创建条件缺失 O_CREAT
#define 创建新建文件 (O_CREAT | O_EXCL)
#define 截断内容 O_TRUNC
#define 追加位置结束 O_APPEND
#define 执行行为非判断等待状态 O_NONBLOCK
#define 起点开头 SEEK_SET
#define 当前根 SEEK_CUR
#define 结束原点 SEEK_END
#define 文件运行状态 stat
typedef size_t 字节个数类型;
typedef ssize_t 输入输出结果类型;
typedef off_t 文件偏移类型;
#endif
