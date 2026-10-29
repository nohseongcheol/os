#ifndef 原生捆绑头部
#define 原生捆绑头部
#include <stddef.h>
int JAR打开(const char *文件条目名称);
int JAR读取(const char *名称, unsigned char *结果数据, unsigned 缓冲容量);
const char *JAR主操作(void);
#endif
