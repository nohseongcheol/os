#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *συμβολοσειρά_τιμή);
int strcmp(const char *μπροστινή_τιμή, const char *Πίσω_τιμή);
int memcmp(const void *μπροστινή_τιμή, const void *Πίσω_τιμή, size_t 바이트수);
void *memcpy(void *προορισμός_τιμή, const void *원본, size_t 바이트수);
void *memset(void *προορισμός_τιμή, int τιμή, size_t 바이트수);
#endif
