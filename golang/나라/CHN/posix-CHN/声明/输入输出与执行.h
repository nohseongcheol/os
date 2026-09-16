/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_输入输出与执行
#define _声明_输入输出与执行

#include <基本定义.h>
#include <系统/数据类型.h>

#define 标准输入编号 0
#define 标准输出编号 1
#define 标准错误输出编号 2
#define 检查存在 0
#define 检查执行权限 1
#define 检查写权限 2
#define 检查读权限 4
#define 从起点定位 0
#define 从当前位置定位 1
#define 从末尾定位 2

#ifdef __cplusplus
extern "C" {
#endif
extern char **环境变量列表;
void 立即结束(int 结束状态) __attribute__((noreturn));
有符号大小类型 读取(int 文件描述编号, void *缓冲区域, 大小类型 数量);
有符号大小类型 写入(int 文件描述编号, const void *缓冲区域, 大小类型 数量);
int 关闭(int 文件描述编号);
文件位置类型 移动读写位置(int 文件描述编号, 文件位置类型 位移, int 位置基准);
进程编号类型 分出子进程(void);
int 替换执行内容(const char *路径, char *const 参数列表[], char *const 环境列表[]);
进程编号类型 取得进程编号(void);
进程编号类型 取得父进程编号(void);
用户编号类型 取得用户编号(void);
用户编号类型 取得有效用户编号(void);
组编号类型 取得组编号(void);
组编号类型 取得有效组编号(void);
int 检查访问权限(const char *路径, int 访问方式);
int 切换工作目录(const char *路径);
char *取得工作目录路径(char *缓冲区域, 大小类型 大小);
int 复制打开文件引用(int 文件描述编号);
int 按指定编号复制文件引用(int 原描述编号, int 新描述编号);
int 同步文件记录(int 文件描述编号);
void 同步全部记录(void);
int 检查是否终端(int 文件描述编号);
int 设定动态存储末端(void *地址);
void *移动动态存储末端(int 增量);
#ifdef __cplusplus
}
#endif

#endif
