#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *string_VALUE);
int strcmp(const char *esikaamera_VALUE, const char *Tagasi_VALUE);
int memcmp(const void *esikaamera_VALUE, const void *Tagasi_VALUE, size_t bait_COUNT);
void *memcpy(void *sihtkoht_VALUE, const void *원본, size_t bait_COUNT);
void *memset(void *sihtkoht_VALUE, int VALUE, size_t bait_COUNT);
#endif
