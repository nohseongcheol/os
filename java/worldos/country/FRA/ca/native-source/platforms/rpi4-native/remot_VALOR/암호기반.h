#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *assignar_remot(size_t);
void versió_remot(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void remot_resum(const void *, size_t, unsigned char [32]);
#endif
