#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ciąg_WARTOŚĆ);
int strcmp(const char *przód_WARTOŚĆ, const char *BACK_WARTOŚĆ);
int memcmp(const void *przód_WARTOŚĆ, const void *BACK_WARTOŚĆ, size_t bajt_ILE_LICZB);
void *memcpy(void *cel_WARTOŚĆ, const void *원본, size_t bajt_ILE_LICZB);
void *memset(void *cel_WARTOŚĆ, int WARTOŚĆ, size_t bajt_ILE_LICZB);
#endif
