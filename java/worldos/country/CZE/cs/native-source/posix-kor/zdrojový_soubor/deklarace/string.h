#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *řetězec_HODNOTA);
int strcmp(const char *přední_fotoaparát_HODNOTA, const char *BACK_HODNOTA);
int memcmp(const void *přední_fotoaparát_HODNOTA, const void *BACK_HODNOTA, size_t bajt_POČET);
void *memcpy(void *cíl_HODNOTA, const void *원본, size_t bajt_POČET);
void *memset(void *cíl_HODNOTA, int HODNOTA, size_t bajt_POČET);
#endif
