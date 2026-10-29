#ifndef 자체암호기반머리
#define 자체암호기반머리
#include <stddef.h>
#include <stdint.h>
void *атап_бирү_читтәге(size_t);
void Чыгарылыш_читтәге(void *);
void *원격재할당(void *, size_t);
int 원격난수(unsigned char *, unsigned);
void читтәге_Җыелма_нәтиҗә(const void *, size_t, unsigned char [32]);
#endif
