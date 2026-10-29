#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *string_VALUE);
int strcmp(const char *voor_VALUE, const char *TERUG_VALUE);
int memcmp(const void *voor_VALUE, const void *TERUG_VALUE, size_t greep_COUNT);
void *memcpy(void *bestemming_VALUE, const void *원본, size_t greep_COUNT);
void *memset(void *bestemming_VALUE, int VALUE, size_t greep_COUNT);
#endif
