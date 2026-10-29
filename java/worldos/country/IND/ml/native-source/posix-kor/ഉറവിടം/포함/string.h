#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *സ്ട്രിംഗ്_മൂല്യം);
int strcmp(const char *മുൻവശം_മൂല്യം, const char *പിന്നിലേക്ക്_മൂല്യം);
int memcmp(const void *മുൻവശം_മൂല്യം, const void *പിന്നിലേക്ക്_മൂല്യം, size_t 바이트수);
void *memcpy(void *ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം, const void *원본, size_t 바이트수);
void *memset(void *ഉദ്ദിഷ്ടസ്ഥാനം_മൂല്യം, int മൂല്യം, size_t 바이트수);
#endif
