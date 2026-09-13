#ifndef _声明_文件控制
#define _声明_文件控制

#include <系统/数据类型.h>

#define 只读打开 0x0000
#define 只写打开 0x0001
#define 读写打开 0x0002
#define 访问模式掩码 0x0003
#define 不存在则创建 0x0040
#define 仅允许新文件 0x0080
#define 清空原有内容 0x0200
#define 在末尾追加 0x0400
#define 仅允许目录 0x10000

#define 复制描述编号 0
#define 取得描述编号标志 1
#define 设置描述编号标志 2
#define 取得文件状态标志 3
#define 设置文件状态标志 4
#define 替换程序时关闭 1

#ifdef __cplusplus
extern "C" {
#endif
int 打开(const char *路径, int 打开选项, ...);
int 创建文件(const char *路径, 文件模式类型 访问方式);
int 控制文件(int 文件描述编号, int 控制命令, ...);
#ifdef __cplusplus
}
#endif

#endif
