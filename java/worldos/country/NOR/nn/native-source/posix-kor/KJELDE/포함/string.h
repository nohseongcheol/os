#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *streng_VALUE);
int strcmp(const char *앞, const char *TILBAKE_VALUE);
int memcmp(const void *앞, const void *TILBAKE_VALUE, size_t byte_COUNT);
void *memcpy(void *mål_VALUE, const void *원본, size_t byte_COUNT);
void *memset(void *mål_VALUE, int VALUE, size_t byte_COUNT);
#endif
