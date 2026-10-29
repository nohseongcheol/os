#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *reťazec_VALUE);
int strcmp(const char *predný_VALUE, const char *BACK_VALUE);
int memcmp(const void *predný_VALUE, const void *BACK_VALUE, size_t Byte_COUNT);
void *memcpy(void *cieľ_VALUE, const void *원본, size_t Byte_COUNT);
void *memset(void *cieľ_VALUE, int VALUE, size_t Byte_COUNT);
#endif
