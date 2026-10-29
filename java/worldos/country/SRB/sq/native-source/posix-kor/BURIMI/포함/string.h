#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *varg_VALUE);
int strcmp(const char *e_përparme_VALUE, const char *PAS_VALUE);
int memcmp(const void *e_përparme_VALUE, const void *PAS_VALUE, size_t bajt_COUNT);
void *memcpy(void *vendmbërritje_VALUE, const void *원본, size_t bajt_COUNT);
void *memset(void *vendmbërritje_VALUE, int VALUE, size_t bajt_COUNT);
#endif
