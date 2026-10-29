#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *स्ट्रिङ_मान);
int strcmp(const char *앞, const char *पछाडि_मान);
int memcmp(const void *앞, const void *पछाडि_मान, size_t 바이트수);
void *memcpy(void *गन्तव्य_मान, const void *원본, size_t 바이트수);
void *memset(void *गन्तव्य_मान, int मान, size_t 바이트수);
#endif
