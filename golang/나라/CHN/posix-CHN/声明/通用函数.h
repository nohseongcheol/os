/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_通用函数
#define _声明_通用函数
#include <基本定义.h>
typedef struct { int 商值; int 余数; } 整数除法结果类型;
typedef struct { long 商值; long 余数; } 长整数除法结果类型;
#define 成功退出 0
#define 失败退出 1
void *分配内存空间(大小类型 大小);
void *分配清零数组空间(大小类型 数量, 大小类型 元素大小);
void *调整内存空间大小(void *地址, 大小类型 大小);
void 释放内存空间(void *地址);
long 将字符串读为长整数(const char *字符串, char **转换末端地址, int 基数);
unsigned long 将字符串读为无符号长整数(const char *字符串, char **转换末端地址, int 基数);
int 将十进字符串读为整数(const char *字符串);
long 将十进字符串读为长整数(const char *字符串);
int 取得整数绝对值(int 值);
long 取得长整数绝对值(long 值);
整数除法结果类型 取得整数商余数(int 左值, int 右值);
长整数除法结果类型 取得长整数商余数(long 左值, long 右值);
void 按比较规则排序(void *元素数组, 大小类型 数量, 大小类型 元素大小,
           int (*比较函数)(const void *, const void *));
void *在有序数组中二分查找(const void *来源位置, const void *元素数组, 大小类型 数量,
              大小类型 元素大小, int (*比较函数)(const void *, const void *));
char *取得环境变量值(const char *系统资料);
#endif
