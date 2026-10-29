#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *اسٽرنگ_قدر);
int strcmp(const char *앞, const char *واپس_قدر);
int memcmp(const void *앞, const void *واپس_قدر, size_t 바이트수);
void *memcpy(void *منزل_مقصود_قدر, const void *원본, size_t 바이트수);
void *memset(void *منزل_مقصود_قدر, int قدر, size_t 바이트수);
#endif
