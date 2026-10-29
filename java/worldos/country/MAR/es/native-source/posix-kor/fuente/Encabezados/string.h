#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *Cadena);
int strcmp(const char *valorLadoDelantero, const char *valorLadoPosterior);
int memcmp(const void *valorLadoDelantero, const void *valorLadoPosterior, size_t númeroElementosByte);
void *memcpy(void *valorDestino, const void *original, size_t númeroElementosByte);
void *memset(void *valorDestino, int valor, size_t númeroElementosByte);
#endif
