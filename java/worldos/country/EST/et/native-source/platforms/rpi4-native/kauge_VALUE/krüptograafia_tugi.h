#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *lisama_kauge(size_t);
void vabastama_kauge(void *);
void *원격재할당(void *, size_t);
int kauge_juhuslik(unsigned char *, unsigned);
void kauge_kokkuvõte(const void *, size_t, unsigned char [32]);
#endif
