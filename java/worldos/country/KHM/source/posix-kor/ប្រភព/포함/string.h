#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *សំនុំអក្សរ_តំលៃ);
int strcmp(const char *ខាងមុខ_តំលៃ, const char *ការថយ_តំលៃ);
int memcmp(const void *ខាងមុខ_តំលៃ, const void *ការថយ_តំលៃ, size_t 바이트수);
void *memcpy(void *ទិសដៅ_តំលៃ, const void *원본, size_t 바이트수);
void *memset(void *ទិសដៅ_តំលៃ, int តំលៃ, size_t 바이트수);
#endif
