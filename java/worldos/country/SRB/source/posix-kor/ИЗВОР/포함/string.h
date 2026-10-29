#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ниска_вриједност);
int strcmp(const char *앞, const char *НАЗАД_вриједност);
int memcmp(const void *앞, const void *НАЗАД_вриједност, size_t 바이트수);
void *memcpy(void *одредиште_вриједност, const void *원본, size_t 바이트수);
void *memset(void *одредиште_вриједност, int вриједност, size_t 바이트수);
#endif
