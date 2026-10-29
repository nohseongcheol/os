#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *стринг_вриједност);
int strcmp(const char *앞, const char *Назад_вриједност);
int memcmp(const void *앞, const void *Назад_вриједност, size_t 바이트수);
void *memcpy(void *одредиште_вриједност, const void *원본, size_t 바이트수);
void *memset(void *одредиште_вриједност, int вриједност, size_t 바이트수);
#endif
