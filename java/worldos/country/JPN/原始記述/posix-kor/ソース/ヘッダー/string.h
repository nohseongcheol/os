#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *文字列);
int strcmp(const char *前面値, const char *後端値);
int memcmp(const void *前面値, const void *後端値, size_t バイト個数);
void *memcpy(void *宛先値, const void *原本, size_t バイト個数);
void *memset(void *宛先値, int 値, size_t バイト個数);
#endif
