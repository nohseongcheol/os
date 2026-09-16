/*
	Copyright 2020. (노성철, nsch78@nate.com, nsch@naver.com) All right reserved
*/

#ifndef _LIBC_STDLIB_H
#define _LIBC_STDLIB_H
#include <basic_definitions.h>
typedef struct { int quot; int rem; } div_t;
typedef struct { long quot; long rem; } ldiv_t;
#define successful_exit 0
#define failed_exit 1
void *malloc(object_size_type digit_count);
void *calloc(object_size_type count, object_size_type element_size);
void *realloc(void *address, object_size_type digit_count);
void free(void *address);
long strtol(const char *text, char **end_pointer, int radix);
unsigned long strtoul(const char *text, char **end_pointer, int radix);
int atoi(const char *text);
long atol(const char *text);
int abs(int value);
long labs(long value);
div_t div(int left, int right);
ldiv_t ldiv(long left, long right);
void qsort(void *elements, object_size_type count, object_size_type element_size,
           int (*compare)(const void *, const void *));
void *bsearch(const void *source, const void *elements, object_size_type count,
              object_size_type element_size, int (*compare)(const void *, const void *));
char *getenv(const char *system_identity);
#endif
