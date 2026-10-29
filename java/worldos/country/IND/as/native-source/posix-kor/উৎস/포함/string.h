#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ষ্ট্ৰিং_মান);
int strcmp(const char *앞, const char *পাছলৈ_মান);
int memcmp(const void *앞, const void *পাছলৈ_মান, size_t 바이트수);
void *memcpy(void *গন্তব্য_স্থান_মান, const void *원본, size_t 바이트수);
void *memset(void *গন্তব্য_স্থান_মান, int মান, size_t 바이트수);
#endif
