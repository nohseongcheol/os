#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *স্ট্রিং_মান);
int strcmp(const char *সম্মুখ_মান, const char *ফিরে_যান_মান);
int memcmp(const void *সম্মুখ_মান, const void *ফিরে_যান_মান, size_t 바이트수);
void *memcpy(void *গন্তব্য_মান, const void *원본, size_t 바이트수);
void *memset(void *গন্তব্য_মান, int মান, size_t 바이트수);
#endif
