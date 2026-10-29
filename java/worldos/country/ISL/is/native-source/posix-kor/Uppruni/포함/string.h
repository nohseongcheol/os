#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *strengur_VALUE);
int strcmp(const char *myndavél_að_framan_VALUE, const char *TIL_BAKA_VALUE);
int memcmp(const void *myndavél_að_framan_VALUE, const void *TIL_BAKA_VALUE, size_t bæti_COUNT);
void *memcpy(void *endastaður_VALUE, const void *원본, size_t bæti_COUNT);
void *memset(void *endastaður_VALUE, int VALUE, size_t bæti_COUNT);
#endif
