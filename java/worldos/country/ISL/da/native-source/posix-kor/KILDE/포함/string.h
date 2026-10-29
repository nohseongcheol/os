#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *streng_VÆRDI);
int strcmp(const char *frontvendt_VÆRDI, const char *BACK_VÆRDI);
int memcmp(const void *frontvendt_VÆRDI, const void *BACK_VÆRDI, size_t byte_TÆL);
void *memcpy(void *destination_VÆRDI, const void *원본, size_t byte_TÆL);
void *memset(void *destination_VÆRDI, int VÆRDI, size_t byte_TÆL);
#endif
