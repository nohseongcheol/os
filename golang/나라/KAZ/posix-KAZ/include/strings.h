#ifndef _LIBC_STRINGS_H
#define _LIBC_STRINGS_H
#include <основные_определения.h>
int strcasecmp(const char *left, const char *right);
int strncasecmp(const char *left, const char *right, size_t limit);
#endif
