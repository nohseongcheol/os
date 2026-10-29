#ifndef nativní_síť_řetězec_Nadpis
#define nativní_síť_řetězec_Nadpis
#include <stddef.h>
void *memcpy(void *, const void *, size_t);
void *memset(void *, int, size_t);
void *memmove(void *, const void *, size_t);
int memcmp(const void *, const void *, size_t);
size_t strlen(const char *);
int strncmp(const char *, const char *, size_t);
#endif
