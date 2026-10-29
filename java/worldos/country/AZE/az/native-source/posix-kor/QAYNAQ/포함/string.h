#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *sətir_VALUE);
int strcmp(const char *ön_VALUE, const char *GERİ_VALUE);
int memcmp(const void *ön_VALUE, const void *GERİ_VALUE, size_t bayt_COUNT);
void *memcpy(void *təyinat_VALUE_a0fbc067, const void *원본, size_t bayt_COUNT);
void *memset(void *təyinat_VALUE_a0fbc067, int VALUE, size_t bayt_COUNT);
#endif
