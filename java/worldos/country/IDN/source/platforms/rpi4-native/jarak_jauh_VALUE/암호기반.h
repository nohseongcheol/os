#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *alokasi_jarak_jauh(size_t);
void lepas_jarak_jauh(void *);
void *원격재할당(void *, size_t);
int jarak_jauh_acak(unsigned char *, unsigned);
void jarak_jauh_ringkasan(const void *, size_t, unsigned char [32]);
#endif
