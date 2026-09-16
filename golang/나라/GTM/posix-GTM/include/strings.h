/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_STRINGS_H
#define _LIBC_STRINGS_H
#include <definiciones_básicas.h>
int strcasecmp(const char *left, const char *right);
int strncasecmp(const char *left, const char *right, size_t limit);
#endif
