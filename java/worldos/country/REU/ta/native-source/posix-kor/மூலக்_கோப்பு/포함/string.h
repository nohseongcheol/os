#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *சரம்_மதிப்பு);
int strcmp(const char *முன்_மதிப்பு, const char *பின்_மதிப்பு);
int memcmp(const void *முன்_மதிப்பு, const void *பின்_மதிப்பு, size_t 바이트수);
void *memcpy(void *இலக்கு_மதிப்பு, const void *원본, size_t 바이트수);
void *memset(void *இலக்கு_மதிப்பு, int மதிப்பு, size_t 바이트수);
#endif
