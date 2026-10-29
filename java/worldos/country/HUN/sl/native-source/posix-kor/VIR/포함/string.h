#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *niz_VALUE);
int strcmp(const char *sprednja_VALUE, const char *ZAJ_VALUE);
int memcmp(const void *sprednja_VALUE, const void *ZAJ_VALUE, size_t bajt_COUNT);
void *memcpy(void *cilj_VALUE, const void *원본, size_t bajt_COUNT);
void *memset(void *cilj_VALUE, int VALUE, size_t bajt_COUNT);
#endif
