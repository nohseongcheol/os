#ifndef _LIBC_STRINGS_H
#define _LIBC_STRINGS_H
#include <définitions_de_base.h>
int strcasecmp(const char *left, const char *right);
int strncasecmp(const char *left, const char *right, size_t limit);
#endif
