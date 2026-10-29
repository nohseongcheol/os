#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *문자열);
int strcmp(const char *앞, const char *뒤);
int memcmp(const void *앞, const void *뒤, size_t 바이트수);
void *memcpy(void *목적, const void *원본, size_t 바이트수);
void *memset(void *목적, int 값, size_t 바이트수);
#endif
