#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *cadeia_VALOR);
int strcmp(const char *câmera_frontal_VALOR, const char *BACK_VALOR);
int memcmp(const void *câmera_frontal_VALOR, const void *BACK_VALOR, size_t byte_CONT_NÚM);
void *memcpy(void *destino_VALOR, const void *원본, size_t byte_CONT_NÚM);
void *memset(void *destino_VALOR, int VALOR, size_t byte_CONT_NÚM);
#endif
