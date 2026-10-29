#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *字符串);
int strcmp(const char *前端值, const char *後端值);
int memcmp(const void *前端值, const void *後端值, size_t 位元組個數);
void *memcpy(void *目的地址值, const void *原始, size_t 位元組個數);
void *memset(void *目的地址值, int 值, size_t 位元組個數);
#endif
