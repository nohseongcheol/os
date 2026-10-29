#ifndef 原生密码学头部
#define 原生密码学头部
#include <stddef.h>
#include <stdint.h>
void *分配远程(size_t);
void 释放远程(void *);
void *重新分配远程(void *, size_t);
int 远程随机(unsigned char *, unsigned);
void 远程摘要(const void *, size_t, unsigned char [32]);
#endif
