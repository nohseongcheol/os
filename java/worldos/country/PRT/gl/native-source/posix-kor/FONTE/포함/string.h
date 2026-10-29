#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *cadea_VALOR);
int strcmp(const char *frontal_VALOR, const char *ATRÁS_VALOR);
int memcmp(const void *frontal_VALOR, const void *ATRÁS_VALOR, size_t byte_CONTAR);
void *memcpy(void *destino_VALOR, const void *원본, size_t byte_CONTAR);
void *memset(void *destino_VALOR, int VALOR, size_t byte_CONTAR);
#endif
