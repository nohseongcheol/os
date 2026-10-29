#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ChuỗiKýTự);
int strcmp(const char *giáTrịPhíaTrước, const char *giáTrịLùi);
int memcmp(const void *giáTrịPhíaTrước, const void *giáTrịLùi, size_t sốLượngByte);
void *memcpy(void *giáTrịĐích, const void *nguyênBản, size_t sốLượngByte);
void *memset(void *giáTrịĐích, int giáTrị, size_t sốLượngByte);
#endif
