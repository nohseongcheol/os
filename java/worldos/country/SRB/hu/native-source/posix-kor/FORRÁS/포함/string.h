#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *sztring_ÉRTÉK);
int strcmp(const char *elülső_kamera_ÉRTÉK, const char *BACK_ÉRTÉK);
int memcmp(const void *elülső_kamera_ÉRTÉK, const void *BACK_ÉRTÉK, size_t bájt_DARAB);
void *memcpy(void *cél_ÉRTÉK, const void *원본, size_t bájt_DARAB);
void *memset(void *cél_ÉRTÉK, int ÉRTÉK, size_t bájt_DARAB);
#endif
