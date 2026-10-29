#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *ଷ୍ଟ୍ରିଂ_ମୂଲ୍ୟ);
int strcmp(const char *앞, const char *ପଛ_ମୂଲ୍ୟ);
int memcmp(const void *앞, const void *ପଛ_ମୂଲ୍ୟ, size_t 바이트수);
void *memcpy(void *ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ, const void *원본, size_t 바이트수);
void *memset(void *ଲକ୍ଷସ୍ଥଳ_ମୂଲ୍ୟ, int ମୂଲ୍ୟ, size_t 바이트수);
#endif
