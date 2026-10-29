#ifndef 原生密碼學標頭
#define 原生密碼學標頭
#include <stddef.h>
#include <stdint.h>
void *分配遠程(size_t);
void 釋放遠程(void *);
void *重新分配遠程(void *, size_t);
int 遠程隨機(unsigned char *, unsigned);
void 遠程摘要(const void *, size_t, unsigned char [32]);
#endif
