#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *bölüp_aýyr_uzakdan(size_t);
void goýbermek_uzakdan(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void uzakdan_gysgaça_mazmun(const void *, size_t, unsigned char [32]);
#endif
