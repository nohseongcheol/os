#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *tildele_fjern(size_t);
void frigi_fjern(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void fjern_samandrag(const void *, size_t, unsigned char [32]);
#endif
