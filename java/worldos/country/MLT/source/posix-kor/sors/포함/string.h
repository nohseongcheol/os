#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *string_VALUE);
int strcmp(const char *앞, const char *Lura_VALUE);
int memcmp(const void *앞, const void *Lura_VALUE, size_t byte_COUNT);
void *memcpy(void *destinazzjoni_VALUE, const void *원본, size_t byte_COUNT);
void *memset(void *destinazzjoni_VALUE, int VALUE, size_t byte_COUNT);
#endif
