#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *sònraich_cian(size_t);
void sgaoileadh_cian(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void 원격요약(const void *, size_t, unsigned char [32]);
#endif
