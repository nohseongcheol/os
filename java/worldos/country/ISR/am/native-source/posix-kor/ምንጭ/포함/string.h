#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ኅብረቁምፊ_እሴት);
int strcmp(const char *ፊት_እሴት, const char *ተመለስ_እሴት);
int memcmp(const void *ፊት_እሴት, const void *ተመለስ_እሴት, size_t 바이트수);
void *memcpy(void *መድረሻ_እሴት, const void *원본, size_t 바이트수);
void *memset(void *መድረሻ_እሴት, int እሴት, size_t 바이트수);
#endif
