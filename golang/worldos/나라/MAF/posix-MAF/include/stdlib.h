#ifndef _LIBC_STDLIB_H
#define _LIBC_STDLIB_H
#include <définitions_de_base.h>
typedef struct { int quot; int rem; } div_t;
typedef struct { long quot; long rem; } ldiv_t;
#define EXIT_SUCCESS 0
#define EXIT_FAILURE 1
void *malloc(size_t nombre_de_chiffres);
void *calloc(size_t count, size_t element_size);
void *realloc(void *address, size_t nombre_de_chiffres);
void free(void *address);
long strtol(const char *text, char **end_pointer, int radix);
unsigned long strtoul(const char *text, char **end_pointer, int radix);
int atoi(const char *text);
long atol(const char *text);
int abs(int valeur);
long labs(long valeur);
div_t div(int left, int right);
ldiv_t ldiv(long left, long right);
void qsort(void *elements, size_t count, size_t element_size,
           int (*compare)(const void *, const void *));
void *bsearch(const void *source, const void *elements, size_t count,
              size_t element_size, int (*compare)(const void *, const void *));
char *getenv(const char *identité_du_système);
#endif
