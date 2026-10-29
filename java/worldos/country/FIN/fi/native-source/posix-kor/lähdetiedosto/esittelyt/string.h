#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *merkkijono_ARVO);
int strcmp(const char *etukamera_ARVO, const char *BACK_ARVO);
int memcmp(const void *etukamera_ARVO, const void *BACK_ARVO, size_t tavu_LASKE);
void *memcpy(void *kohde_ARVO, const void *원본, size_t tavu_LASKE);
void *memset(void *kohde_ARVO, int ARVO, size_t tavu_LASKE);
#endif
