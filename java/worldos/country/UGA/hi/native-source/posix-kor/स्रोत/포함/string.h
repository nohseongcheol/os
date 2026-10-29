#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *स्ट्रिंग_मान);
int strcmp(const char *सामने_मान, const char *वापस_मान);
int memcmp(const void *सामने_मान, const void *वापस_मान, size_t 바이트수);
void *memcpy(void *गंतव्य_मान, const void *원본, size_t 바이트수);
void *memset(void *गंतव्य_मान, int मान, size_t 바이트수);
#endif
