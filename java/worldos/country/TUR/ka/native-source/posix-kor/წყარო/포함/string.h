#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *სტრიქონი_მნიშვნელობა);
int strcmp(const char *앞, const char *უკან_მნიშვნელობა);
int memcmp(const void *앞, const void *უკან_მნიშვნელობა, size_t 바이트수);
void *memcpy(void *მიმართულება_მნიშვნელობა, const void *원본, size_t 바이트수);
void *memset(void *მიმართულება_მნიშვნელობა, int მნიშვნელობა, size_t 바이트수);
#endif
