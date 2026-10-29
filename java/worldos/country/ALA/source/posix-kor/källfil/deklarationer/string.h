#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *sträng_värde);
int strcmp(const char *framåtvänd_värde, const char *BACK_värde);
int memcmp(const void *framåtvänd_värde, const void *BACK_värde, size_t byte_ANTAL);
void *memcpy(void *mål_värde, const void *원본, size_t byte_ANTAL);
void *memset(void *mål_värde, int värde, size_t byte_ANTAL);
#endif
