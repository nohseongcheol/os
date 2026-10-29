#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *cadena_VALOR);
int strcmp(const char *frontal_VALOR, const char *ENRERE_VALOR);
int memcmp(const void *frontal_VALOR, const void *ENRERE_VALOR, size_t byte_COMPT);
void *memcpy(void *destinació_VALOR, const void *원본, size_t byte_COMPT);
void *memset(void *destinació_VALOR, int VALOR, size_t byte_COMPT);
#endif
