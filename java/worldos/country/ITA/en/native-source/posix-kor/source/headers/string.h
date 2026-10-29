#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *stringValue);
int strcmp(const char *frontValue, const char *backValue);
int memcmp(const void *frontValue, const void *backValue, size_t byteCount);
void *memcpy(void *destinationValue, const void *original, size_t byteCount);
void *memset(void *destinationValue, int value, size_t byteCount);
#endif
