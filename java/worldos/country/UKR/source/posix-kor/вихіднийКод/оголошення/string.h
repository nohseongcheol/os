#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *рядок_значення);
int strcmp(const char *фронтальна_камера_значення, const char *НАЗАД_значення);
int memcmp(const void *фронтальна_камера_значення, const void *НАЗАД_значення, size_t 바이트수);
void *memcpy(void *місце_значення, const void *원본, size_t 바이트수);
void *memset(void *місце_значення, int значення, size_t 바이트수);
#endif
