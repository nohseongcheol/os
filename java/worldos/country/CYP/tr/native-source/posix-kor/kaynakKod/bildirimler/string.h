#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *dize_değer);
int strcmp(const char *ön_kamera_değer, const char *BACK_değer);
int memcmp(const void *ön_kamera_değer, const void *BACK_değer, size_t bayt_BAĞ_DEĞ_SAY);
void *memcpy(void *hedef_değer, const void *원본, size_t bayt_BAĞ_DEĞ_SAY);
void *memset(void *hedef_değer, int değer, size_t bayt_BAĞ_DEĞ_SAY);
#endif
