#ifndef JKOROS_STRING_H
#define JKOROS_STRING_H
#include <stddef.h>
size_t strlen(const char *સ્ટ્રિંગ_મૂલ્ય);
int strcmp(const char *앞, const char *બેક_મૂલ્ય);
int memcmp(const void *앞, const void *બેક_મૂલ્ય, size_t 바이트수);
void *memcpy(void *ગંતવ્ય_મૂલ્ય, const void *원본, size_t 바이트수);
void *memset(void *ગંતવ્ય_મૂલ્ય, int મૂલ્ય, size_t 바이트수);
#endif
