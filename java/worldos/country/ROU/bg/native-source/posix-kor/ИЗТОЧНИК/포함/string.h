#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *низ_стойност);
int strcmp(const char *предна_стойност, const char *НАЗАД_стойност);
int memcmp(const void *предна_стойност, const void *НАЗАД_стойност, size_t 바이트수);
void *memcpy(void *местоназначение_стойност, const void *원본, size_t 바이트수);
void *memset(void *местоназначение_стойност, int стойност, size_t 바이트수);
#endif
