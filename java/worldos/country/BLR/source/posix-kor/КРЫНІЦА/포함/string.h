#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *радок_значэнне);
int strcmp(const char *пярэдняя_камера_значэнне, const char *Назад_значэнне);
int memcmp(const void *пярэдняя_камера_значэнне, const void *Назад_значэнне, size_t 바이트수);
void *memcpy(void *прызначэнне_значэнне_a0fbc067, const void *원본, size_t 바이트수);
void *memset(void *прызначэнне_значэнне_a0fbc067, int значэнне, size_t 바이트수);
#endif
