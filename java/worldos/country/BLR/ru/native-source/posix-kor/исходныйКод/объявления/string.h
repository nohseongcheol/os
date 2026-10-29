#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *строка_ЗНАЧЕН);
int strcmp(const char *лицевая_камера_ЗНАЧЕН, const char *BACK_ЗНАЧЕН);
int memcmp(const void *лицевая_камера_ЗНАЧЕН, const void *BACK_ЗНАЧЕН, size_t байт_СЧЁТ);
void *memcpy(void *цель_ЗНАЧЕН, const void *원본, size_t байт_СЧЁТ);
void *memset(void *цель_ЗНАЧЕН, int ЗНАЧЕН, size_t байт_СЧЁТ);
#endif
