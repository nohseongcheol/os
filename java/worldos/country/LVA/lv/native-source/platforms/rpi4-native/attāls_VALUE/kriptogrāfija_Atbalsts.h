#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *piešķirt_attāls(size_t);
void izlaist_attāls(void *);
void *원격재할당(void *, size_t);
int attāls_nejaušs(unsigned char *, unsigned);
void attāls_kopsavilkums(const void *, size_t, unsigned char [32]);
#endif
