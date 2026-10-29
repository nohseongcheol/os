#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *priskirti_nuotolinis(size_t);
void išleisti_nuotolinis(void *);
void *원격재할당(void *, size_t);
int nuotolinis_atsitiktinis(unsigned char *, unsigned);
void nuotolinis_suvestinė(const void *, size_t, unsigned char [32]);
#endif
