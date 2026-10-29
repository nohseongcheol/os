#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *сап_маани);
int strcmp(const char *앞, const char *Артка_маани);
int memcmp(const void *앞, const void *Артка_маани, size_t 바이트수);
void *memcpy(void *көздөө_жайы_маани, const void *원본, size_t 바이트수);
void *memset(void *көздөө_жайы_маани, int маани, size_t 바이트수);
#endif
