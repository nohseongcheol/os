#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *virkne_VALUE);
int strcmp(const char *priekšējā_VALUE, const char *ATPAKAĻ_VALUE);
int memcmp(const void *priekšējā_VALUE, const void *ATPAKAĻ_VALUE, size_t byte_COUNT);
void *memcpy(void *mērķis_VALUE, const void *원본, size_t byte_COUNT);
void *memset(void *mērķis_VALUE, int VALUE, size_t byte_COUNT);
#endif
