#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *అక్షరసరం_మూల్యం);
int strcmp(const char *ముందు_మూల్యం, const char *వెనుకకు_మూల్యం);
int memcmp(const void *ముందు_మూల్యం, const void *వెనుకకు_మూల్యం, size_t 바이트수);
void *memcpy(void *గమ్యం_మూల్యం, const void *원본, size_t 바이트수);
void *memset(void *గమ్యం_మూల్యం, int మూల్యం, size_t 바이트수);
#endif
