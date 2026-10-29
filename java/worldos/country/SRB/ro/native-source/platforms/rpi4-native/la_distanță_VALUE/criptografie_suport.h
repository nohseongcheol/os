#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *aloca_la_distanță(size_t);
void lansa_la_distanță(void *);
void *원격재할당(void *, size_t);
int la_distanță_aleator(unsigned char *, unsigned);
void la_distanță_rezumat(const void *, size_t, unsigned char [32]);
#endif
