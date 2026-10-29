#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *رست_نرخ);
int strcmp(const char *앞, const char *دواوە_نرخ);
int memcmp(const void *앞, const void *دواوە_نرخ, size_t 바이트수);
void *memcpy(void *جێمەبەست_نرخ, const void *원본, size_t 바이트수);
void *memset(void *جێمەبەست_نرخ, int نرخ, size_t 바이트수);
#endif
