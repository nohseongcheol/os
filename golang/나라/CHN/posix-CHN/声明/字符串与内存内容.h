/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _声明_字符串与内存内容
#define _声明_字符串与内存内容
#include <基本定义.h>
void *复制内存内容(void *目标位置, const void *来源位置, 大小类型 长度);
void *允许重叠移动内存内容(void *目标位置, const void *来源位置, 大小类型 长度);
void *用值填充内存区域(void *目标位置, int 字符值, 大小类型 长度);
int 比较内存内容(const void *左值, const void *右值, 大小类型 长度);
void *在内存中查找值(const void *来源位置, int 字符值, 大小类型 长度);
大小类型 取得字符串字节数(const char *字符串);
大小类型 取得限长字符串字节数(const char *字符串, 大小类型 上限);
char *复制字符串(char *目标位置, const char *来源位置);
char *定长填充复制字符串(char *目标位置, const char *来源位置, 大小类型 上限);
char *复制字符串并取得末端(char *目标位置, const char *来源位置);
char *定长填充复制并取得末端(char *目标位置, const char *来源位置, 大小类型 上限);
char *追加字符串(char *目标位置, const char *来源位置);
char *限长追加字符串(char *目标位置, const char *来源位置, 大小类型 上限);
int 比较字符串(const char *左值, const char *右值);
int 限长比较字符串(const char *左值, const char *右值, 大小类型 上限);
int 按排序规则比较字符串(const char *左值, const char *右值);
大小类型 生成字符串排序键(char *目标位置, const char *来源位置, 大小类型 上限);
char *查找字符串首个值(const char *字符串, int 字符值);
char *查找字符串最后值(const char *字符串, int 字符值);
char *查找子字符串(const char *字符串, const char *来源位置);
大小类型 取得允许值前缀长度(const char *字符串, const char *分隔值集合);
大小类型 取得无排除值前缀长度(const char *字符串, const char *分隔值集合);
char *查找字符串中的集合值(const char *字符串, const char *分隔值集合);
char *分割字符串词段(char *字符串, const char *分隔值集合);
char *指定状态分割字符串词段(char *字符串, const char *分隔值集合, char **保存进度状态);
char *在新空间复制字符串(const char *字符串);
char *限长在新空间复制字符串(const char *字符串, 大小类型 上限);
#endif
