#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *dodijeli_udaljeno(size_t);
void izdati_udaljeno(void *);
void *원격재할당(void *, size_t);
int udaljeno_slučajan(unsigned char *, unsigned);
void udaljeno_sažetak(const void *, size_t, unsigned char [32]);
#endif
