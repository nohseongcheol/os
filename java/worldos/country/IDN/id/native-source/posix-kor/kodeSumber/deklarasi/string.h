#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *string_VALUE);
int strcmp(const char *depan_VALUE, const char *BACK_VALUE);
int memcmp(const void *depan_VALUE, const void *BACK_VALUE, size_t byte_COUNT);
void *memcpy(void *tujuan_VALUE, const void *원본, size_t byte_COUNT);
void *memset(void *tujuan_VALUE, int VALUE, size_t byte_COUNT);
#endif
