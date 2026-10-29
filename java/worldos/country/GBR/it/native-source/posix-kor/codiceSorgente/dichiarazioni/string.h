#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *stringa_VALORE);
int strcmp(const char *frontale_VALORE, const char *BACK_VALORE);
int memcmp(const void *frontale_VALORE, const void *BACK_VALORE, size_t byte_CONTA_NUMERI);
void *memcpy(void *meta_VALORE, const void *원본, size_t byte_CONTA_NUMERI);
void *memset(void *meta_VALORE, int VALORE, size_t byte_CONTA_NUMERI);
#endif
