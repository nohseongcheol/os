#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *eilutė_VALUE);
int strcmp(const char *priekinis_VALUE, const char *ATGAL_VALUE);
int memcmp(const void *priekinis_VALUE, const void *ATGAL_VALUE, size_t baitas_COUNT);
void *memcpy(void *vieta_VALUE, const void *원본, size_t baitas_COUNT);
void *memset(void *vieta_VALUE, int VALUE, size_t baitas_COUNT);
#endif
