#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *caktoj_në_largësi(size_t);
void liroj_në_largësi(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void në_largësi_përmbledhje(const void *, size_t, unsigned char [32]);
#endif
