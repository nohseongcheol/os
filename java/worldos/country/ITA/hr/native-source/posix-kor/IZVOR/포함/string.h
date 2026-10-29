#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *niz_VALUE);
int strcmp(const char *prednja_VALUE, const char *TRAG_VALUE);
int memcmp(const void *prednja_VALUE, const void *TRAG_VALUE, size_t bajt_COUNT);
void *memcpy(void *odredište_VALUE, const void *원본, size_t bajt_COUNT);
void *memset(void *odredište_VALUE, int VALUE, size_t bajt_COUNT);
#endif
