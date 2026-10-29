#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *tekenreeks_WAARDE);
int strcmp(const char *voorkant_WAARDE, const char *BACK_WAARDE);
int memcmp(const void *voorkant_WAARDE, const void *BACK_WAARDE, size_t byte_AANTAL);
void *memcpy(void *doel_WAARDE, const void *원본, size_t byte_AANTAL);
void *memset(void *doel_WAARDE, int WAARDE, size_t byte_AANTAL);
#endif
