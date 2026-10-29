#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *rentetan_VALUE);
int strcmp(const char *hadapan_VALUE, const char *BACK_VALUE);
int memcmp(const void *hadapan_VALUE, const void *BACK_VALUE, size_t bait_COUNT);
void *memcpy(void *destinasi_VALUE, const void *원본, size_t bait_COUNT);
void *memset(void *destinasi_VALUE, int VALUE, size_t bait_COUNT);
#endif
