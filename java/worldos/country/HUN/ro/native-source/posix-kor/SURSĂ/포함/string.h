#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *șir_VALUE);
int strcmp(const char *frontală_VALUE, const char *ÎNAPOI_VALUE);
int memcmp(const void *frontală_VALUE, const void *ÎNAPOI_VALUE, size_t byte_COUNT);
void *memcpy(void *destinație_VALUE, const void *원본, size_t byte_COUNT);
void *memset(void *destinație_VALUE, int VALUE, size_t byte_COUNT);
#endif
