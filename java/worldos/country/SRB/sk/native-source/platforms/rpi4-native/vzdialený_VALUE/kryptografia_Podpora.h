#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *vyhradiť_vzdialený(size_t);
void vydať_vzdialený(void *);
void *원격재할당(void *, size_t);
int vzdialený_náhodný(unsigned char *, unsigned);
void vzdialený_súhrn(const void *, size_t, unsigned char [32]);
#endif
